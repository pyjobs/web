# -*- coding: utf-8 -*-
import geocoder


# TODO : Add details about what failed during geocoding
class GeolocationError(Exception):
    pass


class Geolocator(object):
    def __init__(self, address):
        self.__address = address

    def compute_geoloc(self):
        geoloc = geocoder.osm(self.__address)

        if len(geoloc.latlng) != 2:
            raise GeolocationError

        lat, lng = geoloc.latlng

        return lat, lng
