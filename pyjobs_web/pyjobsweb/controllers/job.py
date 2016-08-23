# -*- coding: utf-8 -*-
import json
import logging
from elasticsearch_dsl import Q, SF

from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate

from pyjobsweb.model import JobAlchemy
from pyjobsweb.model import JobElastic
from pyjobsweb.model.data import SOURCES
from pyjobsweb.lib.base import BaseController
from pyjobsweb.forms.research_form import ResearchForm


class SearchJobController(BaseController):
    items_per_page = 20

    @expose('pyjobsweb.templates.jobs.list')
    @paginate('jobs')
    def index(self, query=None, radius=None, center=None, *args, **kwargs):
        if not query and not radius and not center:
            redirect('/job')

        search_query = JobElastic.search()

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

        return dict(sources=SOURCES, jobs=job_offers,
                    job_offer_search_form=ResearchForm)


class JobController(BaseController):
    search = SearchJobController()

    @expose()
    def index(self, *args, **kwargs):
        redirect('/job/list')

    @expose('pyjobsweb.templates.jobs.list')
    @paginate('jobs')
    def list(self, *args, **kwargs):
        try:
            job_offers = JobAlchemy.get_all_job_offers()
        except NoResultFound:
            job_offers = None

        return dict(sources=SOURCES, jobs=job_offers,
                    job_offer_search_form=ResearchForm)

    @expose('pyjobsweb.templates.jobs.details')
    def details(self, offer_id, *args, **kwargs):
        try:
            job = JobAlchemy.get_job_offer(offer_id)
        except NoResultFound:
            # Causes a 404 error
            redirect('/job/details')
        except Exception as exc:
            logging.getLogger(__name__).log(logging.ERROR, exc)
            redirect('/job/details')
        else:
            return dict(
                job=job,
                sources=SOURCES
            )

