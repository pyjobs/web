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
    def _compute_keyword_queries(terms):
        queries = list()

        search_on = ['description', 'title', 'company']

        description_query = Q(
            'multi_match',
            query=terms,
            fields=[search_on[0]],
            fuzziness='AUTO',
            operator='or',
            minimum_should_match='1<2 2<3 3<3 4<4 5<4 6<5 7<5 8<5 9<5',
            boost=len(terms)
        )
        queries.append(description_query)

        title_query = Q(
            'multi_match',
            query=terms,
            fields=[search_on[1]],
            fuzziness='AUTO',
            operator='or',
            minimum_should_match='1<1',
            boost=10 - len(terms) + 1
        )
        queries.append(title_query)

        company_name_query = Q(
            'multi_match',
            query=terms,
            fields=[search_on[2]],
            fuzziness='AUTO',
            operator='or',
            minimum_should_match='1<1',
            boost=50
        )
        queries.append(company_name_query)

        minimum_should_match = '66%'

        keyword_queries = Q(
            'bool',
            should=queries,
            minimum_should_match=minimum_should_match
        )
        return keyword_queries

    @staticmethod
    def _compute_decay_functions():
        decay_function = SF(
            'gauss',
            publication_datetime=dict(
                origin='now',
                scale='30d',
                offset='7d',
                decay='0.1'
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

        if query:
            keyword_queries = self._compute_keyword_queries(query)
            decay_functions = self._compute_decay_functions()

            search_query.query = Q(
                'function_score',
                query=keyword_queries,
                functions=decay_functions
            )

        try:
            geoloc_query = json.loads(center)
            coordinates = geoloc_query['coordinates']
            lat, lon = (coordinates['lat'], coordinates['lon'])
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

