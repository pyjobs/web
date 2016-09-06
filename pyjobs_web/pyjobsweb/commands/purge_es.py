# -*- coding: utf-8 -*-
import logging

import elasticsearch.exceptions
import elasticsearch_dsl

from pyjobsweb import model
from pyjobsweb.commands import AppContextCommand


class PurgeESCommand(AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(PurgeESCommand, self).__init__(args, kwargs)
        self._logger = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PurgeESCommand, self).get_parser(prog_name)

        jobs_help_msg = 'purges the jobs index of the elasticsearch database'
        parser.add_argument('-j', '--jobs',
                            help=jobs_help_msg,
                            dest='purge_jobs_index',
                            action='store_const', const=True)

        companies_help_msg = 'purges the companies index of the elasticsearch' \
                             'database'
        parser.add_argument('-co', '--companies',
                            help=companies_help_msg,
                            dest='purge_companies_index',
                            action='store_const', const=True)

        geocomplete_help_msg = \
            'purges the geocomplete index of the elasticsearch database'
        parser.add_argument('-g', '--geocomplete',
                            help=geocomplete_help_msg,
                            dest='purge_geocomplete_index',
                            action='store_const', const=True)

        return parser

    def _logging(self, logging_level, message):
        self._logger.log(logging_level, message)

    def _purge_index(self, index_name, index_settings, doc_type_class):
        log_msg = 'Dropping %s index.' % index_name
        self._logging(logging.INFO, log_msg)

        index = elasticsearch_dsl.Index(index_name)
        index.settings(**index_settings)
        index.doc_type(doc_type_class)

        try:
            index.delete()
            index.create()
        except elasticsearch.exceptions.ElasticsearchException as e:
            log_msg = 'Error while dropping %s index: %s.' % (index_name, e)
            self._logging(logging.ERROR, log_msg)
            return

        log_msg = 'Index %s has been dropped successfully.' % index_name
        self._logging(logging.INFO, log_msg)

    def _reset_sync(self, sqlalchemy_table_class):
        # Update the Postgresql database
        table_name = model.JobAlchemy.__tablename__
        log_msg = 'Resetting %s table sync data in Postgresql.' % table_name
        self._logging(logging.INFO, log_msg)

        sqlalchemy_table_class.reset_last_sync()

        log_msg = 'Postgresql %s table sync data have been reset.' % table_name
        self._logging(logging.INFO, log_msg)

    def purge_jobs_index(self):
        index_name = model.JobElastic().index
        self._purge_index(index_name, dict(), model.JobElastic)
        self._reset_sync(model.JobAlchemy)

    def purge_companies_index(self):
        index_name = model.CompanyElastic().index
        self._purge_index(index_name, dict(), model.CompanyElastic)
        self._reset_sync(model.CompanyAlchemy)

    def purge_geocomplete_index(self):
        index_name = model.Geocomplete().index
        self._purge_index(index_name, dict(), model.Geocomplete)

    def take_action(self, parsed_args):
        super(PurgeESCommand, self).take_action(parsed_args)

        if parsed_args.purge_jobs_index:
            self.purge_jobs_index()

        if parsed_args.purge_companies_index:
            self.purge_companies_index()

        if parsed_args.purge_geocomplete_index:
            self.purge_geocomplete_index()
