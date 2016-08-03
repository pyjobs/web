# -*- coding: utf-8 -*-
import logging

import pyjobsweb.lib.geolocation as geolocation
from pyjobsweb import model
from pyjobsweb.commands import AppContextCommand


class GeocodeCommand(AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(GeocodeCommand, self).__init__(args, kwargs)
        self._geolocator = geolocation.Geolocator()

    def get_parser(self, prog_name):
        parser = super(GeocodeCommand, self).get_parser(prog_name)
        return parser

    @staticmethod
    def _logging(message, logging_level):
        logging.getLogger(__name__).log(logging_level, message)

    def _job_id_logging(self, job_id, message, logging_level):
        log_msg = u'[Job offer id: %s] %s' % (job_id, message)
        self._logging(log_msg, logging_level)

    def _geocode_job_offers(self):
        to_geoloc = model.JobAlchemy.get_pending_geolocations()

        log_msg = 'Computing required geolocations of job offers.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

        for job in to_geoloc:
            job_id = job.id
            job_address = job.address

            try:
                log_msg = 'Resolving address: %s.' % job_address
                self._job_id_logging(job_id, log_msg, logging.INFO)

                location = self._geolocator.geocode(job.address)

                log_msg = 'Successful resolution: (lat: %s, lon: %s).' \
                          % (location.latitude, location.longitude)
                self._job_id_logging(job_id, log_msg, logging.INFO)

                model.JobAlchemy.set_geolocation(job_id,
                                                 location.latitude,
                                                 location.longitude)
            except geolocation.GeolocationFailure as e:
                model.JobAlchemy.set_address_is_valid(job_id, False)
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.ERROR)
            except geolocation.TemporaryError as e:
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.WARNING)
            except geolocation.GeolocationError as e:
                model.JobAlchemy.set_geolocation_is_valid(job_id, False)
                self._job_id_logging(job_id, e, logging.ERROR)

        log_msg = 'Geolocations computed.'
        logging.getLogger(__name__).log(logging.INFO, log_msg)

    def take_action(self, parsed_args):
        super(GeocodeCommand, self).take_action(parsed_args)

        self._geocode_job_offers()
