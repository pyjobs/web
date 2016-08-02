# -*- coding: utf-8 -*-
from tg.decorators import expose, with_trailing_slash
from tgext.admin.controller import AdminController
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin import CrudRestControllerConfig
from tgext.crud import EasyCrudRestController
from sprox.widgets import TextField

from pyjobsweb import model
from pyjobsweb.model import DBSession


class InvalidAddressesController(EasyCrudRestController):
    __table_options__ = {
        '__omit_fields__': ['description', 'company', 'company_url', 'tags',
                            'publication_datetime',
                            'publication_datetime_is_fake', 'title',
                            'crawl_datetime', 'dirty', 'geolocation_is_valid',
                            'latitude', 'longitude'],
        '__field_order__': ['url', 'id', 'source', 'address',
                            'address_is_valid'],
        '__xml_fields__': ['url'],
        'url': lambda filler, row: '<a class="btn btn-default" '
                                   'target="_blank" href="%(url)s">'
                                   '<span class="glyphicon glyphicon-link">'
                                   '</span>'
                                   '</a>' % dict(url=row.url),
        '__actions__': lambda filler, row:
            InvalidAddressesController.__actions__(filler, row)
    }

    __form_options__ = {
        '__hide_fields__': ['description', 'company', 'company_url', 'tags',
                            'publication_datetime',
                            'title', 'publication_datetime_is_fake',
                            'crawl_datetime', 'dirty',
                            'url', 'id', 'source', 'address_is_valid',
                            'geolocation_is_valid', 'latitude', 'longitude'],
        '__field_widget_types__': {'address': TextField}
    }

    def __init__(self, session, menu_items=None):
        super(InvalidAddressesController, self).__init__(session, menu_items)

    @classmethod
    def __actions__(cls, filler, row):
        primary_fields = filler.__provider__.get_primary_fields(filler
                                                                .__entity__)
        pklist = '/'.join(map(lambda x: str(getattr(row, x)), primary_fields))
        value = '''
            <a href="%s/edit" class="btn btn-primary">
                <span class="glyphicon glyphicon-pencil"></span>
            </a>
            <div class="hidden-lg hidden-md">&nbsp;</div>
            <form method="POST" action="%s" style="display: inline">
            <input name="_method" value="DELETE" type="hidden">
                <button type="submit" class="btn btn-danger"
                    onclick="return confirm('Are you sure?')">
                    <span class="glyphicon glyphicon-trash"></span>
                </button>
            </form>
        ''' % (pklist, pklist)
        return value

    @expose(inherit=True)
    def get_all(self, *args, **kw):
        # Since this controller is only meant to fix invalid addresses, we only
        # request job offers with invalid addresses.
        kw['address_is_valid'] = False
        return super(InvalidAddressesController, self).get_all(*args, **kw)

    @expose(inherit=True)
    def post(self, *args, **kw):
        return EasyCrudRestController.post(self, *args, **kw)

    @expose(inherit=True)
    def put(self, *args, **kw):
        # TODO: Could this test be removed if 'publication_datetime_is_fake'
        # TODO: was False by default and un-nullable
        if not kw['publication_datetime_is_fake']:
            kw['publication_datetime_is_fake'] = False

        # The address has been modified, therefore this row is now dirty, and
        # should be resynchronized with Elasticsearch. Also, the geolocation
        # should be recomputed too, so we mark the address as valid, so that
        # the geolocation program will try and recompute it later on.
        kw['dirty'] = True
        kw['address_is_valid'] = True
        # TODO: Implement kw['geolocation_is_valid'] = False
        return EasyCrudRestController.put(self, *args, **kw)


class InvalidAddressesAdminConfig(TGAdminConfig):
    def __init__(self, models, translations=None):
        super(InvalidAddressesAdminConfig, self).__init__(models, translations)

    class job(CrudRestControllerConfig):
        defaultCrudRestController = InvalidAddressesController


class AdminAddressesController(AdminController):
    def __init__(self):
        super(AdminAddressesController, self).__init__(
            [model.JobAlchemy],
            DBSession,
            config_type=InvalidAddressesAdminConfig
        )


class JobsController(EasyCrudRestController):
    __table_options__ = {
        '__omit_fields__': [],
        '__field_order__': ['url', 'id', 'source', 'address',
                            'address_is_valid'],
        '__xml_fields__': ['url'],
        'url': lambda filler, row: '<a class="btn btn-default" '
                                   'target="_blank" href="%(url)s">'
                                   '<span class="glyphicon glyphicon-link">'
                                   '</span>'
                                   '</a>' % dict(url=row.url)
    }

    def __init__(self, session, menu_items=None):
        super(JobsController, self).__init__(session, menu_items)

    @expose(inherit=True)
    def put(self, *args, **kw):
        # TODO: Could this test be removed if 'publication_datetime_is_fake'
        # TODO: was False by default and un-nullable
        if not kw['publication_datetime_is_fake']:
            kw['publication_datetime_is_fake'] = False

        # The row has been modified, therefore this row is now dirty, and
        # should be resynchronized with Elasticsearch. Also, the geolocation
        # should be recomputed too, so we mark the address as valid, so that
        # the geolocation program will try and recompute it later on.
        kw['dirty'] = True
        return EasyCrudRestController.put(self, *args, **kw)


class PyJobsAdminConfig(TGAdminConfig):
    def __init__(self, models, translations=None):
        super(PyJobsAdminConfig, self).__init__(models, translations)

    class job(CrudRestControllerConfig):
        defaultCrudRestController = JobsController


class PyJobsAdminController(AdminController):
    def __init__(self):
        super(PyJobsAdminController, self).__init__(model, DBSession,
                                                    config_type=TGAdminConfig)

        self.addresses = AdminAddressesController()

    @with_trailing_slash
    @expose()
    def index(self):
        res = super(PyJobsAdminController, self).index()
        res['models'].append('Addresse')
        return res
