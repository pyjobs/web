# -*- coding: utf-8 -*-
import json

from elasticsearch_dsl.function import SF
from elasticsearch_dsl.query import Q
from tg import redirect
from tg.decorators import expose, paginate

from pyjobsweb import model
from pyjobsweb.forms.research_form import ResearchForm
from pyjobsweb.lib.base import BaseController
from pyjobsweb.model.data import SOURCES


class SearchController(BaseController):
    items_per_page = 20

    @expose('pyjobsweb.templates.jobs')
    @paginate('jobs', items_per_page=items_per_page)
    def jobs(self, query=None, radius=None, center=None, *args, **kwargs):
        if not query and not radius and not center:
            redirect('/')

        search_query = model.JobElastic.search()

        search_on = ['description', 'title^10', 'company^20']

        keyword_query = Q()

        if query:
            query = query.replace(',', ' ')

            keyword_query = Q('multi_match',
                              type='cross_fields',
                              query=query,
                              fields=search_on,
                              minimum_should_match='2<50%')

        decay_function = SF('gauss',
                            publication_datetime=dict(origin='now',
                                                      scale='120d',
                                                      offset='7d',
                                                      decay='0.1'))
        search_query.query = Q('function_score',
                               query=keyword_query,
                               functions=[decay_function])

        try:
            geoloc_query = json.loads(center)
            lat, lon = (geoloc_query['lat'], geoloc_query['lon'])

            search_query = \
                search_query.filter('geo_distance',
                                    geolocation=[lon, lat],
                                    distance='%skm' % float(radius))

            search_query = \
                search_query.filter('term', geolocation_is_valid=True)
        except (ValueError, TypeError):
            # One of the following case has occurred:
            #     - Center wasn't a valid json string
            #     - Radius couldn't be converted to float
            # Since both these information are required to set a geolocation
            # filter are required, we ignore it.
            pass

        # TODO: result pagination
        job_offers = search_query[0:self.items_per_page * 50].execute()

        search_form = ResearchForm(action='/', method='POST').req()

        return dict(sources=SOURCES, jobs=job_offers,
                    job_offer_search_form=search_form)
