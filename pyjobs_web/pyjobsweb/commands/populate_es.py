# -*- coding: utf-8 -*-
import json
import logging

import elasticsearch_dsl
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl.connections import connections
from tg import config

from pyjobsweb import model
from pyjobsweb.lib.sqlalchemy_ import current_server_timestamp
from pyjobsweb.lib.lock import acquire_inter_process_lock
from pyjobsweb.commands import AppContextCommand


class PopulateESCommand(AppContextCommand):
    """
    Populate (or synchronize) Elasticsearch indixes
    """
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

    def _compute_dirty_documents(self, sql_table_cls, doc_type):
        self._logging(logging.INFO,
                      'Computing out of sync %s documents.' % doc_type)

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

    def _synchronisation_op(self, elasticsearch_doctype, pending_insertions):
        self._logging(logging.INFO,
                      'Computing required operations to synchronize documents.')

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

    def _perform_index_sync(self, sql_table_cls, es_doc_cls, id_logger):
        es_doc = es_doc_cls()

        elasticsearch_conn = connections.get_connection()

        sync_timestamp = current_server_timestamp()

        pending_insertions = self._compute_dirty_documents(
            sql_table_cls, es_doc.doc_type)

        bulk_op = self._synchronisation_op(es_doc, pending_insertions)

        self._logging(logging.INFO, 'Performing synchronization.')

        for ok, info in parallel_bulk(elasticsearch_conn, bulk_op):
            obj_id = info['index']['_id'] \
                if 'index' in info else info['update']['_id']

            if ok:
                # Mark the task as handled so we don't retreat it next time
                self._logging(logging.INFO,
                              'Document %s has been synced successfully.'
                              % obj_id)

                sql_table_cls.update_last_sync(obj_id, sync_timestamp)
            else:
                id_logger(obj_id, logging.ERROR,
                          'Error while syncing document %s index.' % obj_id)

        # Refresh indices to increase research speed
        elasticsearch_dsl.Index(es_doc.index).refresh()

    def _synchronise_index(self, sql_table_cls, es_doc_cls, id_logger):
        es_doc = es_doc_cls()

        self._logging(logging.INFO,
                      'Synchronizing %s index.' % es_doc.index)

        with acquire_inter_process_lock('sync_%s' % es_doc.index) as acquired:
            if not acquired:
                es_doc = es_doc_cls()
                err_msg = 'Another process is already synchronizing the %s ' \
                          'index, aborting now.' % es_doc.index
                self._logging(logging.WARNING, err_msg)
            else:
                self._perform_index_sync(sql_table_cls, es_doc_cls, id_logger)

                self._logging(logging.INFO,
                              'Index %s is now synchronized.' % es_doc.index)

    def _synchronise_jobs_index(self):
        self._synchronise_index(model.JobAlchemy,
                                model.JobElastic, self._job_id_logging)

    def _synchronise_companies_index(self):
        self._synchronise_index(model.CompanyAlchemy,
                                model.CompanyElastic, self._company_id_logging)

    def _geocomplete_index_batch(self, elasticsearch_conn, to_index):
        log_msg = 'Indexing documents.'
        self._logging(logging.INFO, log_msg)

        for ok, info in parallel_bulk(elasticsearch_conn, to_index):
            if not ok:
                doc_id = info['create']['_id']
                doc_type = info['create']['_type']
                doc_index = info['create']['_index']

                logging_level = logging.ERROR
                err_msg = "Couldn't index document: '%s', of type: %s, " \
                          "under index: %s." % (doc_id, doc_type, doc_index)

                self._logging(logging_level, err_msg)

    def _perform_geocomplete_index_population(self, max_doc):
        elasticsearch_conn = connections.get_connection()

        to_index = list()

        for i, document in enumerate(self._geocompletion_documents()):
            if i % max_doc == 0:
                log_msg = 'Computing required geoloc-entry documents.'
                self._logging(logging.INFO, log_msg)

            to_index.append(document.to_dict(True))

            if len(to_index) < max_doc:
                continue

            self._geocomplete_index_batch(elasticsearch_conn, to_index)

            to_index = list()

        if len(to_index) != 0:
            self._geocomplete_index_batch(elasticsearch_conn, to_index)

        elasticsearch_dsl.Index('geocomplete').refresh()

    def _populate_geocomplete_index(self, max_doc=1000):
        log_msg = 'Populating geocomplete index.'
        self._logging(logging.INFO, log_msg)

        with acquire_inter_process_lock('populate_geocomplete') as acquired:
            if not acquired:
                err_msg = 'Another process is already populating the ' \
                          'geocomplete index, aborting now.'
                self._logging(logging.WARNING, err_msg)
            else:
                self._perform_geocomplete_index_population(max_doc)

                log_msg = 'gecomplete index populated and refreshed.'
                self._logging(logging.INFO, log_msg)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        if parsed_args.populate_geocomplete_index:
            self._populate_geocomplete_index()

        if parsed_args.synchronize_jobs_index:
            self._synchronise_jobs_index()

        if parsed_args.synchronize_companies_index:
            self._synchronise_companies_index()
