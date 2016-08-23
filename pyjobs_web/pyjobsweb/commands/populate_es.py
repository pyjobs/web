# -*- coding: utf-8 -*-
import json
import logging

import elasticsearch_dsl
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl.connections import connections
from tg import config

from pyjobsweb import model
from pyjobsweb.commands import AppContextCommand


class PopulateESCommand(AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(PopulateESCommand, self).__init__(args, kwargs)
        self._logger = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PopulateESCommand, self).get_parser(prog_name)

        jobs_help_msg = 'synchronizes the jobs index from the Elasticsearch ' \
                        'database with the jobs table from the Postgresql ' \
                        'database'
        parser.add_argument('-j', '--jobs',
                            help=jobs_help_msg,
                            dest='synchronize_jobs_index',
                            action='store_const', const=True)

        companies_help_msg = 'synchronizes the companies index from the ' \
                             'Elasticsearch database with the companies ' \
                             'table from the Postgresql database'
        parser.add_argument('-co', '--companies',
                            help=companies_help_msg,
                            dest='synchronize_companies_index',
                            action='store_const', const=True)

        geocomplete_help_msg = \
            'populates the geocomplete index of the elasticsearch database'
        parser.add_argument('-g', '--geocomplete',
                            help=geocomplete_help_msg,
                            dest='populate_geocomplete_index',
                            action='store_const', const=True)

        return parser

    def _logging(self, logging_level, message):
        self._logger.log(logging_level, message)

    def _job_id_logging(self, job_id, logging_level, message):
        log_msg = u'[Job offer id: %s] %s' % (job_id, message)
        self._logging(logging_level, log_msg)

    def _company_id_logging(self, company_id, logging_level, message):
        log_msg = u'[Company: %s] %s' % (company_id, message)
        self._logging(logging_level, log_msg)

    @staticmethod
    def _compute_dirty_documents(sql_table_cls):
        dirty_rows = sql_table_cls.get_dirty_rows()

        for row in dirty_rows:
            yield row.to_elasticsearch_document()

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
    def _synchronisation_op(elasticsearch_doctype, pending_insertions):
        for p in pending_insertions:
            doc_dict = p.to_dict(True)

            try:
                elasticsearch_doctype.get(p.id)
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

    def _synchronise_index(self, sql_table_cls, es_doc_cls, id_logger):
        es_doc = es_doc_cls()

        log_msg = 'Synchronizing %s index.' % es_doc.index
        self._logging(logging.INFO, log_msg)

        elasticsearch_conn = connections.get_connection()

        self._logging(logging.INFO,
                      'Computing out of sync %s documents.'
                      % es_doc.doc_type)

        pending_insertions = self._compute_dirty_documents(sql_table_cls)

        self._logging(logging.INFO,
                      'Computing required operations to synchronize documents.')

        bulk_op = self._synchronisation_op(es_doc, pending_insertions)

        self._logging(logging.INFO, 'Performing synchronisation.')

        for ok, info in parallel_bulk(elasticsearch_conn, bulk_op):
            obj_id = info['index']['_id'] \
                if 'index' in info else info['update']['_id']

            if ok:
                # Mark the task as handled so we don't retreat it next time
                self._logging(logging.INFO,
                              'Document %s has been synced successfully.'
                              % obj_id)
                sql_table_cls.set_dirty(obj_id, False)
            else:
                id_logger(obj_id, logging.ERROR,
                          'Error while syncing document %s index.' % obj_id)

        # Refresh indices to increase research speed
        elasticsearch_dsl.Index(es_doc.index).refresh()

        self._logging(logging.INFO,
                      'Index %s is now synchronized.' % es_doc.index)

    def _synchronise_jobs_index(self):
        self._synchronise_index(model.JobAlchemy,
                                model.JobElastic, self._job_id_logging)

    def _synchronise_companies_index(self):
        self._synchronise_index(model.CompanyAlchemy,
                                model.CompanyElastic, self._company_id_logging)

    def _populate_geocomplete_index(self):
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
            self._populate_geocomplete_index()

        if parsed_args.synchronize_jobs_index:
            self._synchronise_jobs_index()

        if parsed_args.synchronize_companies_index:
            self._synchronise_companies_index()
