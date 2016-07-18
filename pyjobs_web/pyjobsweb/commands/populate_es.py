# -*- coding: utf-8 -*-
import elasticsearch_dsl
import elasticsearch
import logging

import pyjobsweb.commands as commands
import pyjobsweb.model as model
import pyjobsweb.lib.geolocation as geolocation


class PopulateESCommand(commands.AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(PopulateESCommand, self).__init__(args, kwargs)
        self._geolocator = geolocation.Geolocator()

    @staticmethod
    def _error_logging(job_id, message, logging_level):
        err_msg = '[Job offer id: %s] %s.' % (job_id, message)
        logging.getLogger(__name__).log(logging_level, err_msg)

    def _handle_insertion_task(self, job_offer):
        es_job_offer = job_offer.to_elasticsearch_job_offer()

        # Compute lat, lng of the job offer
        try:
            location = self._geolocator.geocode(job_offer.address)

            es_job_offer.geolocation = [location.longitude, location.latitude]
            es_job_offer.geolocation_error = False
        except geolocation.BaseError as e:
            es_job_offer.geolocation = [0, 0]
            es_job_offer.geolocation_error = True
            self._error_logging(job_offer.id, e.message, logging.WARNING)

        # Perform the insertion in Elasticsearch
        try:
            es_job_offer.save()
        except elasticsearch.exceptions.RequestError as e:
            err_msg = 'Elasticsearch insertion error: %s, %s.' % (e, e.info)
            self._error_logging(job_offer.id, err_msg, logging.ERROR)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        # We first try to recompute the geolocation of job offers of which the
        # geolocation could not have been computed earlier. (Timeout...).
        failed_geolocs_query = model.ElasticsearchQuery(0, 10000)
        import pyjobsweb.lib.search_query as sq
        failed_geolocs_query.builder.add_elem(
            sq.BooleanFilter('geolocation_error', True)
        )
        failed_geolocs = failed_geolocs_query.execute_query()

        for f in failed_geolocs:
            try:
                location = self._geolocator.geocode(f.address)
                f.update(
                    location=[location.longitude, location.latitude],
                    geolocation_error=False
                )
            except geolocation.BaseError as e:
                self._error_logging(f.id, e, logging.WARNING)

        job_offers = model.JobOfferSQLAlchemy.\
            compute_elasticsearch_pending_insertion()

        for j in job_offers:
            self._handle_insertion_task(j)
            # Mark the task as handled so we don't retreat it next time
            model.JobOfferSQLAlchemy.\
                mark_as_inserted_in_elasticsearch(j.id)

        # Refresh indices to increase research speed
        elasticsearch_dsl.Index('jobs').refresh()

