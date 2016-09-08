# -*- coding: utf-8 -*-
import json

from elasticsearch_dsl.aggs import A
from elasticsearch_dsl.function import SF
from elasticsearch_dsl.query import Q
from tg.decorators import expose

from pyjobsweb import model
from pyjobsweb.lib.base import BaseController


class GeocompleteController(BaseController):
    @staticmethod
    def geocomplete_town_input_parser(address_input):
        query_tokens = address_input.split(' ')

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

        return address, postal_code

    @expose('json')
    def index(self, address=None, *args, **kwargs):
        if not address:
            return dict(results=[])

        search = model.Geocomplete().search()

        address_query = Q()
        postal_code_query = Q()

        (address, postal_code) = self.geocomplete_town_input_parser(address)

        if address:
            address_query = Q('match', name=address)

        if postal_code:
            postal_code_query = Q('match', postal_code=postal_code)

        weight_scoring_function = SF(
            'field_value_factor',
            factor=1,
            modifier='none',
            field='weight'
        )

        search.query = Q(
            'function_score',
            query=address_query & postal_code_query,
            functions=[weight_scoring_function]
        )

        dedup_docs = A(
            'top_hits',
            size=1
        )

        dedup = A(
            'terms',
            field='name.raw',
            size=5,
            order={'score_sort': 'desc'}
        )

        score_sort = A(
            'max',
            script=dict(lang='expression', script='_score')
        )

        dedup.bucket('dedup_docs', dedup_docs)
        dedup.bucket('score_sort', score_sort)
        search.aggs.bucket('dedup', dedup)

        # Do not compute the results, we are only interested by the aggregations
        raw_res = search[0:0].execute()

        res = list()
        for bucket in raw_res.aggregations.dedup.buckets:
            for source_doc in bucket['dedup_docs']['hits']['hits']:
                fields = source_doc['_source']
                geo_field = fields['geolocation']
                geoloc = dict(lat=geo_field['lat'], lon=geo_field['lon'])

                display = u'%s %s - %s, France' % (fields['name'].upper(),
                                                   fields['complement'].upper(),
                                                   fields['postal_code']) \
                    if fields['complement'] else \
                    u'%s - %s, France' % (fields['name'].upper(),
                                          fields['postal_code'])
                res.append(dict(to_submit=geoloc, to_display=display))

        return dict(results=res)
