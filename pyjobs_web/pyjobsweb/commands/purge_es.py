# -*- coding: utf-8 -*-
import logging

import elasticsearch.exceptions
import elasticsearch_dsl

from pyjobsweb import model
from pyjobsweb.commands import AppContextCommand


class PurgeESCommand(AppContextCommand):
    def get_parser(self, prog_name):
        parser = super(PurgeESCommand, self).get_parser(prog_name)

        jobs_help_msg = 'purges the jobs index of the elasticsearch database'
        parser.add_argument('-j', '--jobs',
                            help=jobs_help_msg,
                            dest='purge_jobs_index',
                            action='store_const', const=True)

        geocomplete_help_msg = \
            'purges the geocomplete index of the elasticsearch database'
        parser.add_argument('-g', '--geocomplete',
                            help=geocomplete_help_msg,
                            dest='purge_geocomplete_index',
                            action='store_const', const=True)

        return parser

    @staticmethod
    def _purge_index(index_name, index_settings, doc_type_class):
        log_msg = 'Dropping %s index.' % index_name
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        index = elasticsearch_dsl.Index(index_name)
        index.settings(**index_settings)
        index.doc_type(doc_type_class)

        try:
            index.delete()
            index.create()
        except elasticsearch.exceptions.ElasticsearchException as e:
            log_msg = 'Error while dropping %s index: %s.' % (index_name, e)
            logging.getLogger(__name__).log(logging.ERROR, log_msg)
            return

        log_msg = 'Index %s has been dropped successfully.' % index_name
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def purge_jobs_index(self):
        self._purge_index('jobs', dict(), model.JobElastic)

        # Update the Postgresql database
        log_msg = 'Resetting jobs table dirty flags in Postgresql.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        model.JobAlchemy.reset_dirty_flags()

        log_msg = 'Postgresql jobs table dirty flags have been reset.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def purge_geocomplete_index(self):
        self._purge_index('geocomplete', dict(), model.Geocomplete)

    def take_action(self, parsed_args):
        super(PurgeESCommand, self).take_action(parsed_args)

        if parsed_args.purge_jobs_index:
            self.purge_jobs_index()

        if parsed_args.purge_geocomplete_index:
            self.purge_geocomplete_index()
