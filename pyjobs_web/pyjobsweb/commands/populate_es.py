# -*- coding: utf-8 -*-
import sqlalchemy
import elasticsearch
import tg
import transaction

import pyjobsweb.commands
import pyjobsweb.model
import pyjobsweb.lib


class PopulateESCommand(pyjobsweb.commands.AppContextCommand):
    __elastic_search = elasticsearch.Elasticsearch()

    @staticmethod
    def __database_connection():
        engine = sqlalchemy.engine.create_engine(
                tg.config.get('sqlalchemy.url')
        )

        engine.connect()
        pyjobsweb.model.init_model(engine)

    @staticmethod
    def __compute_pending_insertions():
        pending_insertions = pyjobsweb.model.DBSession\
            .query(pyjobsweb.model.data.Job)\
            .filter(
                pyjobsweb.model.data.Job.already_in_elasticsearch is not True
            )
        return pending_insertions

    @staticmethod
    def __format_job_offer_to_json(job_offer, lat, lng):
        json_job_offer = job_offer.to_dict()
        json_job_offer['lat'] = lat
        json_job_offer['lng'] = lng
        return json_job_offer

    @staticmethod
    def __mark_task_as_handled(job_offer):
        transaction.begin()
        # TODO : Check if there isn't a better way to handle the update
        pyjobsweb.model.DBSession\
            .query(pyjobsweb.model.data.Job)\
            .filter(pyjobsweb.model.data.Job.id == job_offer.id)\
            .update({'already_in_elasticsearch': True})
        transaction.commit()

    def __handle_insertion_task(self, job_offer):
        # Compute lat, lng of the job offer
        try:
            geolocator = pyjobsweb.lib.geolocation.Geolocator(job_offer.address)
            lat, lng = geolocator.compute_geoloc()
        except pyjobsweb.lib.geolocation.GeolocationError:
            return

        # Convert the job_offer object to a json format
        json_job_offer = self.__format_job_offer_to_json(job_offer, lat, lng)

        # Perform the insertion in Elasticsearch
        try:
            self.__elastic_search.index("jobs", "job-offer", json_job_offer)
        except elasticsearch.RequestError:
            return

        # Mark the task as handled so we don't retreat it next time
        self.__mark_task_as_handled(job_offer)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        self.__database_connection()

        job_offers = self.__compute_pending_insertions()

        for j in job_offers:
            self.__handle_insertion_task(j)
