# -*- coding: utf-8 -*-
import re
import tg
import json
import logging
import transaction
from slugify import slugify
from elasticsearch_dsl import Q

from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate, validate
from tg.exceptions import HTTPNotFound

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.model import CompanyElastic
from pyjobsweb.model import DBSession
from pyjobsweb.lib.base import BaseController
from pyjobsweb.lib.elasticsearch_ import PaginatedSearch
from pyjobsweb.forms.new_form import NewCompanyForm
from pyjobsweb.forms.research_forms import CompaniesResearchForm


class NewCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.new')
    def index(self, *args, **kwargs):
        errors = tg.request.validation['errors']

        error_msg = u''

        for _, err in errors.iteritems():
            if err:
                error_msg = u'Il y a eu des erreurs lors de la saisie du ' \
                            u'formulaire. Merci de bien vouloir les corriger.'
                break

        if error_msg:
            tg.flash(error_msg, 'error')

        return dict(new_company_form=NewCompanyForm)

    @staticmethod
    def _parse_technologies(technologies):
        technologies = re.sub(',+', ' ', technologies)
        technologies = re.sub('(\s|\t)+', ' ', technologies)
        technologies = technologies.strip()
        technologies = technologies.replace(' ', ', ')

        return technologies

    def _build_company_obj(self, **kwargs):
        company = CompanyAlchemy()

        company.id = slugify(kwargs['company_name'])
        company.name = kwargs['company_name']
        company.logo_url = kwargs['company_logo']
        company.url = kwargs['company_url']
        company.description = kwargs['company_description']

        company.technologies = self._parse_technologies(
            kwargs['company_technologies'])

        company.address = kwargs['company_address']
        company.address_is_valid = True
        company.email = kwargs['company_email']
        company.phone = kwargs['company_phone']

        return company

    @staticmethod
    def _redirect():
        redirect_to = '/societes-qui-recrutent'
        redirect_msg = u"Votre demande d'ajout d'entreprise a bien été " \
                       u"soumise à modération. L'entreprise sera ajoutée à " \
                       u"cette liste sous peu si elle satisfait les critères " \
                       u"attendus."
        redirect_status = 'ok'

        tg.flash(redirect_msg, redirect_status)
        redirect(redirect_to)

    @expose()
    @validate(NewCompanyForm, error_handler=index)
    def submit(self, *args, **kwargs):
        company = self._build_company_obj(**kwargs)

        transaction.begin()
        DBSession.add(company)
        transaction.commit()

        self._redirect()


class SearchCompaniesController(BaseController):
    items_per_page = 10

    def __init__(self, items_per_page=10):
        self.items_per_page = items_per_page

    @staticmethod
    def _compute_keyword_queries(terms, search_on):
        queries = list()

        for elem in terms.split(','):
            keyword_query = Q(
                'multi_match',
                type='best_fields',
                query=elem,
                fields=search_on,
                fuzziness='AUTO',
                operator='or',
                tie_breaker=0.3
            )
            queries.append(keyword_query)

        # We could have used a cross_fields query to narrow the results given,
        # by the previous queries, but it doesn't support fuzzy yet (and will
        # probably never: https://github.com/elastic/elasticsearch/issues/6866).
        # keyword_query = Q(
        #     'multi_match',
        #     type='cross_fields',
        #     query=terms,
        #     fields=search_on,
        #     analyzer='french_description_analyzer',
        #     minimum_should_match='1<2 2<3 3<3 4<3 5<4 6<4 7<4 8<4 9<5'
        # )
        # queries.append(keyword_query)

        # Use another best_fields query with a minimum_should_match config. This
        # will help us narrow the global keyword search query.
        keyword_query = Q(
            'multi_match',
            type='best_fields',
            query=terms,
            fields=search_on,
            fuzziness='AUTO',
            operator='or',
            tie_breaker=0.3,
            minimum_should_match='1<2 2<3 3<3 4<3 5<4 6<4 7<4 8<4 9<5'
        )
        queries.append(keyword_query)

        keyword_queries = Q(
            'bool',
            should=queries,
            minimum_should_match='1<2 2<3 3<4 4<4 5<5 6<5 7<5 8<5 9<6'
        )

        return keyword_queries

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

    @expose('pyjobsweb.templates.companies.list')
    @paginate('companies', items_per_page=items_per_page)
    def index(self, query=None, radius=None, center=None, *args, **kwargs):
        if not query and not radius and not center:
            redirect('/societes-qui-recrutent')

        search_query = CompanyElastic().search()

        search_on = ['description', 'technologies^50', 'name^100']

        terms = query
        if terms:
            search_query.query = self._compute_keyword_queries(terms, search_on)

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

        return dict(companies=PaginatedSearch(search_query),
                    company_search_form=CompaniesResearchForm)


class CompaniesController(BaseController):
    items_per_page = 10

    new = NewCompanyController()
    search = SearchCompaniesController(items_per_page)

    @expose('pyjobsweb.templates.companies.list')
    @paginate('companies', items_per_page=items_per_page)
    def index(self, *args, **kwargs):
        try:
            companies = CompanyAlchemy.get_validated_companies()
        except NoResultFound:
            companies = None

        return dict(companies=companies,
                    company_search_form=CompaniesResearchForm)

    @expose('pyjobsweb.templates.companies.details')
    def details(self, company_id, *args, **kwargs):
        try:
            company = CompanyAlchemy.get_validated_company(company_id)
        except NoResultFound:
            raise HTTPNotFound()
        except Exception as exc:
            logging.getLogger(__name__).log(logging.ERROR, exc)
            raise HTTPNotFound()
        else:
            return dict(company=company)
