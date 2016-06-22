# -*- coding: utf-8 -*-
import sqlalchemy
import elasticsearch_dsl.connections
import elasticsearch_dsl.exceptions
import tg
import transaction
import logging

import pyjobsweb.commands
import pyjobsweb.model
import pyjobsweb.lib


class PopulateESCommand(pyjobsweb.commands.AppContextCommand):
    __elastic_search = \
        elasticsearch_dsl.connections.connections.create_connection(
            hosts=["localhost"], send_get_body_as="POST", timeout=20
        )

    @staticmethod
    def __compute_pending_insertions():
        pending_insertions = pyjobsweb.model.DBSession\
            .query(pyjobsweb.model.data.JobOfferSQLAlchemy)\
            .filter_by(
                already_in_elasticsearch=False
            )
        return pending_insertions

    @staticmethod
    def __mark_task_as_handled(job_offer):
        transaction.begin()
        pyjobsweb.model.DBSession\
            .query(pyjobsweb.model.data.JobOfferSQLAlchemy)\
            .filter(pyjobsweb.model.data.JobOfferSQLAlchemy.id == job_offer.id)\
            .update({'already_in_elasticsearch': True})
        transaction.commit()

    def __handle_insertion_task(self, job_offer):
        es_job_offer = job_offer.to_elasticsearch_job_offer()

        # Perform the insertion in Elasticsearch
        try:
            # Compute lat, lng of the job offer
            geolocator = pyjobsweb.lib.geolocation.Geolocator(job_offer.address)
            es_job_offer.geolocation = geolocator.compute_geoloc()
            es_job_offer.geolocation_error = False
        except pyjobsweb.lib.geolocation.GeolocationError:
            logging.getLogger(__name__).log(
                logging.WARNING,
                '{}{}'.format(
                    "Couldn't compute geolocation of the following address : ",
                    job_offer.address
                )
            )
            es_job_offer.geolocation = [0, 0]
            es_job_offer.geolocation_error = True

        try:
            # Perform the insertion
            es_job_offer.save()
        except elasticsearch_dsl.exceptions.ElasticsearchDslException:
            logging.getLogger(__name__).log(
                logging.ERROR,
                '{}{}{}'.format(
                    "Error during insertion in Elasticsearch : ",
                    job_offer.id,
                    " Aborting now..."
                )
            )
            return

        # Mark the task as handled so we don't retreat it next time
        self.__mark_task_as_handled(job_offer)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        job_offers = self.__compute_pending_insertions()

        for j in job_offers:
            self.__handle_insertion_task(j)
