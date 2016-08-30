# -*- coding: utf-8 -*-
import logging

import pyjobsweb.lib.geolocation as geolocation
from pyjobsweb import model
from pyjobsweb.commands import AppContextCommand


class GeocodeCommand(AppContextCommand):
    def __init__(self, *args, **kwargs):
        super(GeocodeCommand, self).__init__(args, kwargs)
        self._geolocator = geolocation.Geolocator()
        self._logger = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GeocodeCommand, self).get_parser(prog_name)

        jobs_help_msg = 'geocode job offers stored in the jobs table'
        parser.add_argument('-j', '--jobs',
                            help=jobs_help_msg,
                            dest='geocode_jobs',
                            action='store_const', const=True)

        companies_help_msg = 'geocode the companies stored in the companies ' \
                             'table'
        parser.add_argument('-co', '--companies',
                            help=companies_help_msg,
                            dest='geocode_companies',
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

    def _geocode(self, cls_to_geocode, id_logger):
        to_geoloc = cls_to_geocode.get_pending_geolocations()

        log_msg = 'Computing required geolocations...'
        self._logging(logging.INFO, log_msg)

        for obj in to_geoloc:
            obj_id = obj.id
            obj_address = obj.address

            log_msg = 'Resolving address: %s.' % obj_address
            id_logger(obj_id, logging.INFO, log_msg)

            try:
                location = self._geolocator.geocode(obj_address)
            except geolocation.GeolocationFailure as e:
                cls_to_geocode.set_address_is_valid(obj_id, False)
                cls_to_geocode.set_geolocation_is_valid(obj_id, False)
                id_logger(obj_id, logging.ERROR, e)
            except geolocation.TemporaryError as e:
                cls_to_geocode.set_geolocation_is_valid(obj_id, False)
                id_logger(obj_id, logging.WARNING, e)
            except geolocation.GeolocationError as e:
                cls_to_geocode.set_geolocation_is_valid(obj_id, False)
                id_logger(obj_id, logging.ERROR, e)
            else:
                log_msg = 'Successful geocoding:  (lat: %s, lon: %s).' % (
                    location.latitude, location.longitude)
                id_logger(obj_id, logging.INFO, log_msg)

                cls_to_geocode.set_geolocation(
                    obj_id, location.latitude, location.longitude)

        log_msg = 'Geolocations computed.'
        self._logging(logging.INFO, log_msg)

    def _geocode_job_offers(self):
        self._geocode(model.JobAlchemy, self._job_id_logging)

    def _geocode_companies(self):
        self._geocode(model.CompanyAlchemy, self._company_id_logging)

    def take_action(self, parsed_args):
        super(GeocodeCommand, self).take_action(parsed_args)

        log_msg = 'Starting geocoding operations.'
        self._logging(logging.INFO, log_msg)

        if parsed_args.geocode_jobs:
            log_msg = 'Starting job offers geocoding operations...'
            self._logging(logging.INFO, log_msg)
            self._geocode_job_offers()

        if parsed_args.geocode_companies:
            log_msg = 'Starting companies geocoding operations...'
            self._logging(logging.INFO, log_msg)
            self._geocode_companies()

        log_msg = 'Geocoding operations done.'
        self._logging(logging.INFO, log_msg)
