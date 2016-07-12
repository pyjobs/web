# -*- coding: utf-8 -*-
import json
import urllib
import urllib2


class PhotonQuery(object):
    _query = None

    def __init__(self, query):
        if not isinstance(query, basestring):
            raise TypeError('query should be of type: %s.' % basestring)

        self.query = query

    def execute_query(self):
        return self._format_result(urllib2.urlopen(self.query).read())

    @staticmethod
    def _format_result(photon_res):
        results_dict = json.loads(photon_res)

        results = list()

        if 'features' not in results_dict:
            return dict()

        features = results_dict['features']

        address_elem = [
            'name',
            'housenumber',
            'street',
            'city',
            'postcode',
            'state',
            'country'
        ]

        for qr in features:
            properties = qr['properties']

            res = dict()

            for k in address_elem:
                try:
                    res[k] = properties[k]
                except KeyError:
                    pass

            if properties['osm_key'] == 'boundary' \
                    and properties['osm_value'] == 'administrative':
                res.pop('name')
                res['county'] = properties['name']

            if properties['osm_key'] == 'place' \
                    and properties['osm_value'] in ['village', 'town', 'city']:
                res.pop('name')
                res['city'] = properties['name']

            if res not in results:
                results.append(res)

        return results

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = u'http://photon.komoot.de/api/?q={}&lang=fr&lat=46.2&lon=2.2'\
            .format(urllib.quote(query.encode('utf-8')))
