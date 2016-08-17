# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate, validate

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.lib.base import BaseController
from pyjobsweb.forms.new_form import NewCompanyForm


class AddCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.new')
    def index(self, *args, **kwargs):
        new_form = NewCompanyForm(action='/company/new/submit',
                                  method='POST').req()
        return dict(new_company_form=new_form)

    @expose()
    @validate(NewCompanyForm, error_handler=index)
    def submit(self, *args, **kwargs):
        raise NotImplementedError('TODO')


class SearchCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.search')
    def index(self, *args, **kwargs):
        raise NotImplementedError('TODO')

    @expose()
    def submit(self, *args, **kwargs):
        raise NotImplementedError('TODO')


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

        return dict(companies=companies)

    @expose('pyjobsweb.templates.companies.details')
    def details(self, siren, *args, **kwargs):
        try:
            company = CompanyAlchemy.get_company(siren=siren)
        except NoResultFound:
            redirect('/company/details')
        except Exception as exc:
            logging.getLogger(__name__).log(logging.ERROR, exc)
            redirect('/company/details')
        else:
            return dict(company=company)
