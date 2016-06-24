# -*- coding: utf-8 -*-
import elasticsearch_dsl
import transaction

import pyjobsweb.commands
import pyjobsweb.model


class PurgeESCommand(pyjobsweb.commands.AppContextCommand):
    def take_action(self, parsed_args):
        super(PurgeESCommand, self).take_action(parsed_args)
        # Drop the index and create a new one
        jobs_index = elasticsearch_dsl.Index('jobs')
        # Empty at the moment
        jobs_index.settings()
        # Register a JobOffer doc_type in the jobs index
        jobs_index.doc_type(pyjobsweb.model.JobOfferElasticsearch)
        # Create the index
        jobs_index.delete(ignore=404)
        jobs_index.create(ignore=400)

        # Update the Postgresql database
        transaction.begin()
        pyjobsweb.model.DBSession\
            .query(pyjobsweb.model.data.JobOfferSQLAlchemy)\
            .update({'already_in_elasticsearch': False})
        transaction.commit()
