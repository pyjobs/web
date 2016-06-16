# -*- coding: utf-8 -*-
import sqlalchemy
import elasticsearch
import tg
import geocoder
import transaction

import pyjobsweb.commands
import pyjobsweb.model


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
    def __compute_geolocation(address):
        geoloc = geocoder.osm(address)

        lat, lng = None, None

        if len(geoloc.latlng) == 2:
            lat, lng = geoloc.latlng

        # TODO : How should we react in case of a failed conversion ?

        return lat, lng

    @staticmethod
    def __format_job_offer_to_json(job_offer, lat, lng):
        json_job_offer = job_offer.to_dict()
        json_job_offer['lat'] = lat
        json_job_offer['lng'] = lng
        return json_job_offer

    def __perform_insertion(self, json_job_offer):
        self.__elastic_search.index(
                index="jobs", doc_type="job-offer", body=json_job_offer
        )

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
        lat, lng = self.__compute_geolocation(job_offer.address)
        # Convert the job_offer object to a json format
        json_job_offer = self.__format_job_offer_to_json(job_offer, lat, lng)
        # Perform the insertion in Elasticsearch
        self.__perform_insertion(json_job_offer)
        # TODO : Check if the job offer insertion succeeded/failed
        # Mark the task as handled so we don't retreat it next time
        self.__mark_task_as_handled(job_offer)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        self.__database_connection()

        job_offers = self.__compute_pending_insertions()

        for j in job_offers:
            self.__handle_insertion_task(j)
