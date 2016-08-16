# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.lib.base import BaseController


class AddCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.new')
    def index(self):
        raise NotImplementedError('TODO')

    @expose()
    def submit(self):
        raise NotImplementedError('TODO')


class SearchCompanyController(BaseController):
    @expose('pyjobsweb.templates.companies.search')
    def index(self):
        raise NotImplementedError('TODO')

    @expose()
    def submit(self):
        raise NotImplementedError('TODO')


class CompanyController(BaseController):
    new = AddCompanyController()
    search = SearchCompanyController()

    @expose()
    def index(self):
        redirect('/company/list')

    @expose('pyjobsweb.templates.companies.list')
    @paginate('companies')
    def list(self):
        companies = CompanyAlchemy.get_validated_companies()
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
