# -*- coding: utf-8 -*-
import elasticsearch
import geopy.geocoders
import geopy.exc
import transaction
import logging

import pyjobsweb.commands
import pyjobsweb.model
import pyjobsweb.lib


class PopulateESCommand(pyjobsweb.commands.AppContextCommand):
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
            geolocator = geopy.geocoders.Nominatim(timeout=5)
            location = geolocator.geocode(job_offer.address, True)

            if not location:
                raise PopulateESCommand.FailedGeoloc

            es_job_offer.geolocation = [location.latitude, location.longitude]
            es_job_offer.geolocation_error = False
        except (geopy.exc.GeocoderQueryError, PopulateESCommand.FailedGeoloc):
            logging.getLogger(__name__).log(
                logging.WARNING,
                '{}{}{}{}'.format(
                    "Job offer id : ",
                    job_offer.id,
                    " Couldn't compute geolocation of the following address : ",
                    u''.join(job_offer.address).encode('utf-8').strip()
                )
            )
            es_job_offer.geolocation = [0, 0]
            es_job_offer.geolocation_error = True
        except (geopy.exc.GeocoderQuotaExceeded,
                geopy.exc.GeocoderAuthenticationFailure,
                geopy.exc.GeocoderUnavailable,
                geopy.exc.GeocoderNotFound) as e:
            logging.getLogger(__name__).log(
                logging.WARNING,
                '{}{}{}{}{}'.format(
                    "Job offer id : ",
                    job_offer.id,
                    " Error during geolocation : ",
                    e.message,
                    ". Aborting Elasticsearch insertions now..."
                )
            )
            raise PopulateESCommand.AbortException
        except geopy.exc.GeopyError as e:
            logging.getLogger(__name__).log(
                logging.WARNING,
                '{}{}{}{}'.format(
                    "Job offer id : ",
                    job_offer.id,
                    " Error during geolocation : ",
                    e.message
                )
            )

        try:
            # Perform the insertion
            es_job_offer.save()
        except elasticsearch.exceptions.RequestError as e:
            logging.getLogger(__name__).log(
                logging.ERROR,
                '{}{}{}{}{}{}'.format(
                    "Job offer id : ",
                    job_offer.id,
                    ", error during the Elasticsearch insertion : ",
                    e,
                    ".\nInfo : ",
                    e.info
                )
            )
            return

        # Mark the task as handled so we don't retreat it next time
        self.__mark_task_as_handled(job_offer)

    def take_action(self, parsed_args):
        super(PopulateESCommand, self).take_action(parsed_args)

        job_offers = self.__compute_pending_insertions()

        for j in job_offers:
            try:
                self.__handle_insertion_task(j)
            except PopulateESCommand.AbortException:
                return

    class FailedGeoloc(Exception):
        pass

    class AbortException(Exception):
        pass
