# -*- coding: utf-8 -*-
import json
import logging
from elasticsearch_dsl import Q, SF

from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate
from tg.exceptions import HTTPNotFound

from pyjobsweb.model import JobAlchemy
from pyjobsweb.model import JobElastic
from pyjobsweb.model.data import SOURCES
from pyjobsweb.lib.base import BaseController
from pyjobsweb.lib.elasticsearch_ import PaginatedSearch
from pyjobsweb.forms.research_forms import JobsResearchForm


class SearchJobsController(BaseController):
    items_per_page = 10

    def __init__(self, items_per_page=10):
        self.items_per_page = items_per_page

    @staticmethod
    def _compute_keyword_queries(terms, search_on):
        queries = list()
        queries.append(Q())

        for elem in terms:
            keyword_query = Q(
                'multi_match',
                type='cross_fields',
                query=elem,
                fields=search_on,
                analyzer='french_description_analyzer'
            )
            queries.append(keyword_query)

        keyword_queries = Q(
            'bool',
            must=[],
            should=queries,
            minimum_should_match='1<50% 3<66% 4<75%'
        )

        return keyword_queries

    @staticmethod
    def _compute_decay_functions():
        decay_function = SF(
            'gauss',
            publication_datetime=dict(
                origin='now',
                scale='15d',
                offset='7d',
                decay='0.5'
            )
        )

        return [decay_function]

    @staticmethod
    def _apply_geolocation_filters(query, (lat, lon), radius):
        query = query.filter(
            'geo_distance',
            geolocation=[lon, lat],
            distance='%skm' % float(radius)
        )

        query = query.filter(
            'term',
            geolocation_is_valid=True
        )

        return query

    @staticmethod
    def _apply_date_sort(query):
        query = query.sort(
            '-publication_datetime',
            '-_score'
        )

        return query

    @expose('pyjobsweb.templates.jobs.list')
    @paginate('jobs', items_per_page=items_per_page)
    def index(self, query=None, radius=None, center=None, sort_by=None,
              *args, **kwargs):
        if not query and not radius and not center:
            redirect('/jobs')

        search_query = JobElastic().search()

        search_on = ['description', 'title^50', 'company^100']

        terms = query.split(',')
        keyword_queries = self._compute_keyword_queries(terms, search_on)
        decay_functions = self._compute_decay_functions()

        search_query.query = Q(
            'function_score',
            query=keyword_queries,
            functions=decay_functions
        )

        try:
            geoloc_query = json.loads(center)
            lat, lon = (geoloc_query['lat'], geoloc_query['lon'])
        except (ValueError, TypeError):
            # One of the following case has occurred:
            #     - Center wasn't a valid json string
            #     - Radius couldn't be converted to float
            # Since both these information are required to set a geolocation
            # filter are required, we ignore it.
            pass
        else:
            search_query = self._apply_geolocation_filters(
                search_query, (lat, lon), radius if radius else 5.0)

        if sort_by == 'dates':
            search_query = self._apply_date_sort(search_query)

        return dict(sources=SOURCES, jobs=PaginatedSearch(search_query),
                    job_offer_search_form=JobsResearchForm)


class JobsController(BaseController):
    items_per_page = 10
    search = SearchJobsController(items_per_page)

    @expose('pyjobsweb.templates.jobs.list')
    @paginate('jobs', items_per_page=items_per_page)
    def index(self, *args, **kwargs):
        try:
            job_offers = JobAlchemy.get_all_job_offers()
        except NoResultFound:
            job_offers = None

        return dict(sources=SOURCES, jobs=job_offers,
                    job_offer_search_form=JobsResearchForm)

    @expose('pyjobsweb.templates.jobs.details')
    def details(self, offer_id, *args, **kwargs):
        try:
            job = JobAlchemy.get_job_offer(offer_id)
        except NoResultFound:
            raise HTTPNotFound()
        except Exception as exc:
            logging.getLogger(__name__).log(logging.ERROR, exc)
            raise HTTPNotFound()
        else:
            return dict(
                job=job,
                sources=SOURCES
            )

