# -*- coding: utf-8 -*-
import geopy.geocoders as geocoders
import geopy.exc as exc


class BaseError(Exception):
    pass


class GeolocationFailure(BaseError):
    pass


class GeolocationError(BaseError):
    pass


class TemporaryError(BaseError):
    pass


class Geolocator(object):
    def __init__(self):
        self._geocoder = geocoders.Nominatim(timeout=5, country_bias='fr')

    def geocode(self, address):
        if not isinstance(address, basestring) \
                and not isinstance(address, dict):
            err_msg = u"address should either be of type: %s, or of type %s." \
                      % (basestring, dict)
            raise TypeError(err_msg)

        try:
            geolocation = self._geocoder.geocode(address)

            if not geolocation:
                err_msg = u"Couldn't resolve following address: '%s'" % address
                raise GeolocationFailure(err_msg)
        except (exc.GeocoderQuotaExceeded,
                exc.GeocoderUnavailable,
                exc.GeocoderTimedOut) as e:
            raise TemporaryError(u'Geolocation error: %s' % e)
        except exc.GeocoderServiceError as e:
            raise GeolocationError(u'Geolocation error: %s' % e)

        return geolocation
