# -*- coding: utf-8 -*-
import elasticsearch_dsl
import logging
import json
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import parallel_bulk

from tg import config

import pyjobsweb.model as model
import pyjobsweb.lib.geolocation as geolocation
from pyjobsweb.commands import AppContextCommand


class PopulateESCommand(AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(PopulateESCommand, self).__init__(args, kwargs)
        self._geolocator = geolocation.Geolocator()

    def get_parser(self, prog_name):
        parser = super(PopulateESCommand, self).get_parser(prog_name)

        jobs_help_msg = 'populates the jobs index of the elasticsearch database'
        parser.add_argument('-j', '--jobs',
                            help=jobs_help_msg,
                            dest='populate_jobs_index',
                            action='store_const', const=True)

        geocomplete_help_msg = \
            'populates the geocomplete index of the elasticsearch database'
        parser.add_argument('-g', '--geocomplete',
                            help=geocomplete_help_msg,
                            dest='populate_geocomplete_index',
                            action='store_const', const=True)

        return parser

    @staticmethod
    def _jobs_error_logging(job_id, message, logging_level):
        err_msg = u'[Job offer id: %s] %s.' % (job_id, message)
        logging.getLogger(__name__).log(logging_level, err_msg)

    def _compute_geoloc(self):
        # We first try to recompute the geolocation of job offers whose
        # geolocation could not be computed earlier. (Timeout...).
        log_msg = 'Computing document requiring their geolocation ' \
                  'to be computed.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        to_geoloc_query = \
            model.ElasticsearchQuery(model.JobOfferElasticsearch, 0, 10000)
        import pyjobsweb.lib.search_query as sq
        to_geoloc_query. \
            add_elem(sq.BooleanFilter('geolocation_is_valid', False))
        to_geoloc_query. \
            add_elem(sq.BooleanFilter('address_is_valid', True))
        to_geoloc = to_geoloc_query.execute_query()

        log_msg = 'Computing geolocations for documents requiring it.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for document in to_geoloc:
            try:
                location = self._geolocator.geocode(document.address)
                document.update(geolocation=dict(lat=location.latitude,
                                                 lon=location.longitude),
                                geolocation_is_valid=True)
            except geolocation.BaseError as e:
                self._jobs_error_logging(document.id, e, logging.WARNING)

    @staticmethod
    def _compute_job_offers_elasticsearch_documents():
        pending_insertion_job_offers = \
            model.JobOfferSQLAlchemy.compute_elasticsearch_pending_insertions()

        res = list()

        for job_offer in pending_insertion_job_offers:
            es_job_offer = job_offer.to_elasticsearch_job_offer()
            es_job_offer.geolocation = dict(lat=0.0, lon=0.0)
            es_job_offer.geolocation_is_valid = False

            res.append(es_job_offer)

        return res

    @staticmethod
    def _geocompletion_documents():
        geolocation_data = open(config.get('fr.geolocation_data.path'))

        json_dict = json.loads(geolocation_data.read())

        for postal_code, places in json_dict.items():
            for place in places:
                yield model.Geocomplete(name=place['name'],
                                        complement=place['complement'],
                                        postal_code=postal_code,
                                        geolocation=dict(
                                            lat=float(place['lat']),
                                            lon=float(place['lon'])
                                        ),
                                        weight=place['weight'])

    def populate_jobs_index(self):
        log_msg = "Populating 'jobs' index."
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        elasticsearch_conn = connections.get_connection()

        log_msg = "Computing required 'job-offer' documents."
        logging.getLogger(__name__).log(logging.INFO, log_msg)
        pending_insertions = self._compute_job_offers_elasticsearch_documents()

        to_index = (d.to_dict(True) for d in pending_insertions)

        bulk_results = enumerate(parallel_bulk(elasticsearch_conn, to_index))

        log_msg = 'Indexing documents in elasticsearch.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for i, (ok, info) in bulk_results:
            if i == 0:
                log_msg = 'Marking indexed documents as ' \
                          'indexed_in_elasticsearch in the Postgresql database.'
                logging.getLogger(__name__).log(logging.INFO, log_msg)

            job_id = pending_insertions[i].id

            if ok:
                # Mark the task as handled so we don't retreat it next time
                model.JobOfferSQLAlchemy. \
                    mark_as_inserted_in_elasticsearch(job_id)
            else:
                doc_id = info['create']['_id']
                doc_type = info['create']['_type']
                doc_index = info['create']['_index']

                err_msg = "Couldn't index document: '%s', of type: %s, " \
                          "under index: %s." % (doc_id, doc_type, doc_index)
                self._jobs_error_logging(job_id, err_msg, logging.ERROR)

        # Refresh indices to increase research speed
        elasticsearch_dsl.Index('jobs').refresh()

        log_msg = "'jobs' index populated and refreshed."
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def populate_geocomplete_index(self):
        log_msg = "Populating 'geocomplete' index."
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        elasticsearch_conn = connections.get_connection()

        log_msg = "Computing required 'geoloc-entry' documents."
        logging.getLogger(__name__).log(logging.INFO, log_msg)
        to_index = (d.to_dict(True) for d in self._geocompletion_documents())

        log_msg = 'Indexing documents.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for ok, info in parallel_bulk(elasticsearch_conn, to_index):
            if not ok:
                doc_id = info['create']['_id']
                doc_type = info['create']['_type']
                doc_index = info['create']['_index']

                logging_level = logging.ERROR
                err_msg = "Couldn't index document: '%s', of type: %s, " \
                          "under index: %s." % (doc_id, doc_type, doc_index)

                logging.getLogger(__name__).log(logging_level, err_msg)

        elasticsearch_dsl.Index('geocomplete').refresh()

        log_msg = "'gecomplete' index populated and refreshed."
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        if parsed_args.populate_geocomplete_index:
            self.populate_geocomplete_index()

        if parsed_args.populate_jobs_index:
            self.populate_jobs_index()
            self._compute_geoloc()
