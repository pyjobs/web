# -*- coding: utf-8 -*-
import tg
import json
import logging
import transaction
from slugify import slugify

from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate, validate
from elasticsearch_dsl import Q

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.model import CompanyElastic
from pyjobsweb.model import DBSession
from pyjobsweb.lib.base import BaseController
from pyjobsweb.forms.new_form import NewCompanyForm
from pyjobsweb.forms.research_form import ResearchForm


class AddCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.new')
    def index(self, *args, **kwargs):
        errors = tg.request.validation['errors']

        error_msg = u''

        for _, err in errors.iteritems():
            if err:
                error_msg = u'Il a eu des erreurs lors de la saisie du ' \
                            u'formulaire. Merci de bien vouloir les corriger.'
                break

        if error_msg:
            tg.flash(error_msg, 'error')

        return dict(new_company_form=NewCompanyForm)

    @expose()
    @validate(NewCompanyForm, error_handler=index)
    def submit(self, *args, **kwargs):
        company = CompanyAlchemy()

        company.id = slugify(kwargs['company_name'])
        company.name = kwargs['company_name']
        company.logo_url = kwargs['company_logo']
        company.url = kwargs['company_url']
        company.description = kwargs['company_description']
        company.technologies = kwargs['company_technologies']
        company.address = kwargs['company_address']
        company.address_is_valid = True
        company.email = kwargs['company_email']
        company.phone = kwargs['company_phone']

        redirect_to = '/company/list'
        redirect_msg = u"Votre demande d'ajout d'entreprise a bien été " \
                       u"soumise à modération. L'entreprise sera ajoutée à " \
                       u"cette liste sous peu si elle satisfait les critères " \
                       u"attendus."
        redirect_status = 'ok'

        transaction.begin()
        DBSession.add(company)
        transaction.commit()

        tg.flash(redirect_msg, redirect_status)
        redirect(redirect_to)


class SearchCompanyController(BaseController):
    items_per_page = 20

    @expose('pyjobsweb.templates.companies.list')
    @paginate('companies')
    def index(self, query=None, radius=None, center=None, *args, **kwargs):
        if not query and not radius and not center:
            redirect('/company')

        search_query = CompanyElastic.search()

        search_on = ['description', 'technologies^20', 'name^20']

        keyword_query = Q()

        if query:
            query = query.replace(',', ' ')

            keyword_query = Q('multi_match',
                              type='cross_fields',
                              query=query,
                              fields=search_on,
                              minimum_should_match='2<50%')

        search_query.query = keyword_query

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
        companies = search_query[0:self.items_per_page * 50].execute()

        return dict(companies=companies, company_search_form=ResearchForm)


class CompanyController(BaseController):
    new = AddCompanyController()
    search = SearchCompanyController()

    @expose()
    def index(self, *args, **kwargs):
        redirect('/company/list')

    @expose('pyjobsweb.templates.companies.list')
    @paginate('companies')
    def list(self, *args, **kwargs):
        try:
            companies = CompanyAlchemy.get_validated_companies()
        except NoResultFound:
            companies = None

        return dict(companies=companies, company_search_form=ResearchForm)

    @expose('pyjobsweb.templates.companies.details')
    def details(self, company_id, *args, **kwargs):
        try:
            company = CompanyAlchemy.get_company(company_id=company_id)
        except NoResultFound:
            redirect('/company/details')
        except Exception as exc:
            logging.getLogger(__name__).log(logging.ERROR, exc)
            redirect('/company/details')
        else:
            return dict(company=company)
