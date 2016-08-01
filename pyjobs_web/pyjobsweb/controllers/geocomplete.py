# -*- coding: utf-8 -*-
import json
from tg.decorators import expose
from elasticsearch_dsl.aggs import A
from elasticsearch_dsl.query import Q
from elasticsearch_dsl.function import SF

from pyjobsweb import model
from pyjobsweb.lib.base import BaseController


class GeocompleteController(BaseController):
    @expose('json')
    def index(self, address=None):
        if not address:
            return dict(results=[])

        query_tokens = address.split(' ')

        postal_code = None
        address = None

        for token in query_tokens:
            try:
                int(token)

                if len(token) <= 5:
                    postal_code = postal_code if postal_code else token
                else:
                    return dict(results=[])
            except ValueError:
                address = u'%s %s' % (address, token) if address else token

        search = model.Geocomplete.search()

        address_query = Q()
        postal_code_query = Q()

        if address:
            address_query = Q('match', name=address)

        if postal_code:
            postal_code_query = Q('match', postal_code=postal_code)

        weight_scoring_function = \
            SF('field_value_factor', modifier='log1p', field='weight')

        search.query = Q('function_score',
                         query=address_query & postal_code_query,
                         functions=[weight_scoring_function])

        unique_agg = A('terms',
                       field='name.raw',
                       size=5,
                       order={'avg_doc_score': 'desc'})
        field_agg = A('top_hits', size=1)
        score_agg = A('max', script=dict(lang='expression', script='_score'))

        unique_agg.bucket('top_geo_matches', field_agg)
        unique_agg.bucket('avg_doc_score', score_agg)

        search.aggs.bucket('geo_matches', unique_agg)

        raw_res = search[0:0].execute()

        res = list()
        for bucket in raw_res.aggregations.geo_matches.buckets:
            for source_doc in bucket['top_geo_matches']['hits']['hits']:
                fields = source_doc['_source']
                geo_field = fields['geolocation']
                geoloc = dict(lat=geo_field['lat'], lon=geo_field['lon'])
                submit = json.dumps(geoloc)
                display = u'%s %s - %s, France' % (fields['name'].upper(),
                                                   fields['complement'].upper(),
                                                   fields['postal_code']) \
                    if fields['complement'] else \
                    u'%s - %s, France' % (fields['name'].upper(),
                                          fields['postal_code'])
                res.append(dict(to_submit=submit, to_display=display))

        return dict(results=res)
