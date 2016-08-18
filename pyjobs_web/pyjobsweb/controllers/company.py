# -*- coding: utf-8 -*-
import tg
import logging
from sqlalchemy.orm.exc import NoResultFound
from tg.decorators import expose, redirect, paginate, validate

from pyjobsweb.model import CompanyAlchemy
from pyjobsweb.model import DBSession
from pyjobsweb.lib.base import BaseController
from pyjobsweb.forms.new_form import NewCompanyForm


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

        # TODO: Export all of this code into setters ?
        company.siren = kwargs['company_siren']
        company.siren = company.siren.replace('-', ' ')
        company.name = kwargs['company_name']
        company.logo_url = kwargs['company_logo']
        company.url = kwargs['company_url']
        company.description = kwargs['company_description']
        company.technologies = kwargs['company_technologies']
        company.technologies = company.technologies.replace(', ', ',')
        company.technologies = company.technologies.replace(' ', ',')
        company.address = kwargs['company_address']
        company.email = kwargs['company_email']
        company.phone = kwargs['company_phone']
        company.phone = company.phone.replace('-', '.')
        company.phone = company.phone.replace(' ', '.')

        redirect_to = '/company/list'
        redirect_msg = u"Votre demande d'ajout d'entreprise a bien été " \
                       u"soumis à modération. L'entreprise sera ajoutée à " \
                       u"cette liste sous peu si elle satisfait les critères " \
                       u"attendus."
        redirect_status = 'ok'

        DBSession.add(company)
        DBSession.commit()

        tg.flash(redirect_msg, redirect_status)
        redirect(redirect_to)


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
