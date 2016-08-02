# -*- coding: utf-8 -*-
import elasticsearch_dsl
import logging
import json
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import parallel_bulk
from elasticsearch.exceptions import NotFoundError

from tg import config

import pyjobsweb.lib.geolocation as geolocation
from pyjobsweb import model
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
    def _logging(message, logging_level):
        logging.getLogger(__name__).log(logging_level, message)

    def _job_id_logging(self, job_id, message, logging_level):
        log_msg = u'[Job offer id: %s] %s.' % (job_id, message)
        self._logging(log_msg, logging_level)

    def _compute_geoloc(self):
        to_geoloc = model.JobAlchemy.get_pending_geolocations()

        log_msg = 'Computing required geolocations.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for job in to_geoloc:
            job_id = job.id
            job_address = job.address

            try:
                log_msg = 'Resolving address: %s.' % job_address
                self._job_id_logging(job_id, log_msg, logging.INFO)

                location = self._geolocator.geocode(job.address)

                log_msg = 'Successful address resolution: (lat: %s, lon: %s).' \
                          % (location.latitude, location.longitude)
                self._job_id_logging(job_id, log_msg, logging.INFO)

                model.JobAlchemy.set_geolocation(job_id,
                                                 location.latitude,
                                                 location.longitude)
                model.JobAlchemy.set_dirty(job_id, True)
            except geolocation.GeolocationFailure as e:
                model.JobAlchemy.set_address_is_valid(job_id, False)
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.ERROR)
            except geolocation.TemporaryError as e:
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.WARNING)
            except geolocation.GeolocationError as e:
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.ERROR)

        log_msg = 'Geolocations computed.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    @staticmethod
    def _compute_job_offers_elasticsearch_documents():
        offers_to_index = model.JobAlchemy.get_dirty_offers()

        for job_offer in offers_to_index:
            yield job_offer.to_elasticsearch_job_offer()

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

    @staticmethod
    def _synchronisation_op(pending_insertions):
        for p in pending_insertions:
            doc_dict = p.to_dict(True)

            try:
                model.JobElastic.get(p.id)
                update_op = doc_dict
                update_op['_op_type'] = 'update'
                update_op['doc'] = doc_dict['_source']
                del update_op['_source']
                sync_op = update_op
            except NotFoundError:
                add_op = doc_dict
                add_op['_op_type'] = 'index'
                sync_op = add_op

            yield sync_op

    def _synchronise_jobs_index(self):
        log_msg = 'Synchronizing index jobs.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        elasticsearch_conn = connections.get_connection()

        log_msg = 'Computing out of sync job-offer documents.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)
        pending_insertions = self._compute_job_offers_elasticsearch_documents()

        log_msg = 'Computing required operations to sync job-offer documents.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        bulk_op = self._synchronisation_op(pending_insertions)

        log_msg = 'Performing synchronisation.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for ok, info in parallel_bulk(elasticsearch_conn, bulk_op):
            job_id = info['index']['_id'] \
                if 'index' in info else info['update']['_id']

            if ok:
                # Mark the task as handled so we don't retreat it next time
                log_msg = 'Document %s has been synced successfully.' % job_id
                logging.getLogger(__name__).log(logging.INFO, log_msg)
                model.JobAlchemy.set_dirty(job_id, False)
            else:
                err_msg = 'Error while syncing document %s index.' % job_id
                self._job_id_logging(job_id, err_msg, logging.ERROR)

        # Refresh indices to increase research speed
        elasticsearch_dsl.Index('jobs').refresh()

        log_msg = 'Index jobs is now synchronized.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def populate_geocomplete_index(self):
        log_msg = 'Populating geocomplete index.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        elasticsearch_conn = connections.get_connection()

        log_msg = 'Computing required geoloc-entry documents.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)
        to_index = [d.to_dict(True) for d in self._geocompletion_documents()]

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

        log_msg = 'gecomplete index populated and refreshed.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        if parsed_args.populate_geocomplete_index:
            self.populate_geocomplete_index()

        if parsed_args.populate_jobs_index:
            self._synchronise_jobs_index()
            self._compute_geoloc()
            self._synchronise_jobs_index()
