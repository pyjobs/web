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

        for qr in features:
            properties = qr['properties']
            address = dict(to_submit=u'', to_display=u'')

            if 'country' not in properties:
                continue

            if properties['country'] != 'France':
                continue

            if 'name' in properties:
                address['to_display'] = u'{}, '.format(properties['name'])

            if 'housenumber' in properties:
                address['to_submit'] = u'{}{} '.format(
                    address['to_submit'], properties['housenumber']
                )
                address['to_display'] = u'{}{} '.format(
                    address['to_display'], properties['housenumber']
                )

            if 'street' in properties:
                address['to_submit'] = u'{}{} '.format(
                    address['to_submit'], properties['street']
                )
                address['to_display'] = u'{}{} '.format(
                    address['to_display'], properties['street']
                )

            if 'postcode' in properties:
                address['to_submit'] = u'{}{} '.format(
                    address['to_submit'], properties['postcode']
                )
                address['to_display'] = u'{}{}, '.format(
                    address['to_display'], properties['postcode']
                )

            if 'state' in properties:
                address['to_display'] = u'{}{}, '.format(
                    address['to_display'], properties['state']
                )

            address['to_submit'] = u'{}{}'.format(
                address['to_submit'], properties['country']
            )
            address['to_display'] = u'{}{}'.format(
                address['to_display'], properties['country']
            )

            if address not in results:
                results.append(address)

        return results

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = u'http://photon.komoot.de/api/?q={}&lang=fr'\
            .format(urllib.quote(query.encode('utf-8')))
