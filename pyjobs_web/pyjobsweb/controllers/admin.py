# -*- coding: utf-8 -*-
import tg
from sprox.widgets import TextField, TextArea
from tg.decorators import expose, with_trailing_slash
from tg.exceptions import HTTPNotFound
from tgext.admin import CrudRestControllerConfig
from tgext.admin.controller import AdminController
from tgext.admin.tgadminconfig import TGAdminConfig, BootstrapTGAdminConfig
from tgext.admin.widgets import SubmitButton
from tgext.admin.layouts import BootstrapAdminLayout
from tgext.crud import EasyCrudRestController

from pyjobsweb import model
from pyjobsweb.model import DBSession
from pyjobsweb.lib.sqlalchemy_ import kw_to_sqlalchemy, sqlalchemy_to_kw, \
    prepare_job_for_address_update, prepare_company_for_address_update, \
    prepare_company_for_validation


class JobGeocodingController(EasyCrudRestController):
    __table_options__ = {
        '__limit_fields__': ['url', 'id', 'source', 'address',
                             'address_is_valid'],
        '__field_order__': ['url', 'id', 'source', 'address',
                            'address_is_valid'],
        '__xml_fields__': ['url'],
        'url': lambda filler, row: '<a class="btn btn-default" '
                                   'target="_blank" href="%(url)s">'
                                   '<span class="glyphicon glyphicon-link">'
                                   '</span>'
                                   '</a>' % dict(url=row.url),
        '__actions__': lambda filler, row:
            JobGeocodingController.__actions__(filler, row)
    }

    __form_options__ = {
        '__hide_fields__': ['id', 'address_is_valid'],
        '__omit_fields__': [
            'description', 'company', 'company_url', 'tags',
            'publication_datetime', 'title', 'publication_datetime_is_fake',
            'crawl_datetime', 'last_modified', 'last_sync', 'url', 'source',
            'geolocation_is_valid', 'latitude', 'longitude', 'pushed_on_twitter'
        ],
        '__field_widget_types__': {
            'address': TextField
        }
    }

    def __init__(self, session, menu_items=None):
        super(JobGeocodingController, self).__init__(session, menu_items)

    @classmethod
    def __actions__(cls, filler, row):
        primary_fields = filler.__provider__.get_primary_fields(filler
                                                                .__entity__)

        pklist = '/'.join(map(lambda x: str(getattr(row, x)), primary_fields))

        value = '''
            <a href="%s/edit" class="btn btn-primary">
                <span class="glyphicon glyphicon-pencil"></span>
            </a>
        ''' % pklist

        return value

    @expose(inherit=True)
    def get_all(self, *args, **kw):
        # Since this controller is only meant to fix invalid addresses, we only
        # request job offers with invalid addresses.
        kw['address_is_valid'] = False
        return super(JobGeocodingController, self).get_all(*args, **kw)

    @expose(inherit=True)
    def post_delete(self, *args, **kw):
        raise HTTPNotFound()

    @expose(inherit=True)
    def post(self, *args, **kw):
        raise HTTPNotFound()

    @expose(inherit=True)
    def new(self, *args, **kwargs):
        raise HTTPNotFound()

    @expose(inherit=True)
    def put(self, *args, **kw):
        new_model = kw_to_sqlalchemy(model.JobAlchemy, kw)

        prepare_job_for_address_update(new_model)
        kw = sqlalchemy_to_kw(new_model)

        return EasyCrudRestController.put(self, *args, **kw)


class CompanyGeocodingController(EasyCrudRestController):
    __table_options__ = {
        '__limit_fields__': ['url', 'id', 'name', 'address',
                             'address_is_valid'],
        '__field_order__': ['url', 'id', 'name', 'address',
                            'address_is_valid'],
        '__xml_fields__': ['url'],
        'url': lambda filler, row: '<a class="btn btn-default" '
                                   'target="_blank" href="%(url)s">'
                                   '<span class="glyphicon glyphicon-link">'
                                   '</span>'
                                   '</a>' % dict(url=row.url),
        '__actions__': lambda filler, row:
            CompanyGeocodingController.__actions__(filler, row)
    }

    __form_options__ = {
        '__hide_fields__': ['id', 'address_is_valid'],
        '__omit_fields__': [
            'last_modified', 'last_sync', 'name', 'logo_url', 'description',
            'url', 'technologies', 'email', 'phone', 'latitude', 'longitude',
            'geolocation_is_valid', 'validated'
        ],
        '__field_widget_types__': {'address': TextField}
    }

    def __init__(self, session, menu_items=None):
        super(CompanyGeocodingController, self).__init__(session,
                                                         menu_items)

    @classmethod
    def __actions__(cls, filler, row):
        primary_fields = filler.__provider__.get_primary_fields(filler
                                                                .__entity__)

        pklist = '/'.join(map(lambda x: str(getattr(row, x)), primary_fields))

        value = '''
            <a href="%s/edit" class="btn btn-primary">
                <span class="glyphicon glyphicon-pencil"></span>
            </a>
        ''' % pklist

        return value

    @expose(inherit=True)
    def get_all(self, *args, **kw):
        # Since this controller is only meant to fix invalid addresses, we only
        # request job offers with invalid addresses.
        kw['address_is_valid'] = False
        return super(CompanyGeocodingController, self).get_all(*args, **kw)

    @expose(inherit=True)
    def post_delete(self, *args, **kw):
        raise HTTPNotFound()

    @expose(inherit=True)
    def post(self, *args, **kw):
        raise HTTPNotFound()

    @expose(inherit=True)
    def new(self, *args, **kwargs):
        raise HTTPNotFound()

    @expose(inherit=True)
    def put(self, *args, **kw):
        new_model = kw_to_sqlalchemy(model.CompanyAlchemy, kw)

        prepare_company_for_address_update(new_model)
        kw = sqlalchemy_to_kw(new_model)

        return EasyCrudRestController.put(self, *args, **kw)


class CompanyModerationController(EasyCrudRestController):
    __table_options__ = {
        '__limit_fields__': ['url', 'id', 'name', 'address'],
        '__field_order__': ['url', 'id', 'name', 'address']
    }

    __form_options__ = {
        '__hide_fields__': [
            'address_is_valid', 'latitude', 'longitude',
            'geolocation_is_valid', 'validated'
        ],
        '__omit_fields__': ['last_modified', 'last_sync'],
        '__field_widget_types__': {
            'id': TextField,
            'name': TextField,
            'logo_url': TextField,
            'description': TextArea,
            'url': TextField,
            'Technologies': TextArea,
            'address': TextField,
            'email': TextField,
            'phone': TextField
        }
    }

    def __init__(self, session, menu_items=None):
        super(CompanyModerationController, self).__init__(session, menu_items)

        self.edit_form.__base_widget_args__['submit'] = SubmitButton(
            id='submit',
            value='Valider',
            css_class='btn btn-primary'
        )

    @expose(inherit=True)
    def get_all(self, *args, **kw):
        # Since this controller is only meant to moderate unvalidated company
        # submissions, we only query for companies that aren't yet validated.
        kw['validated'] = False
        return super(CompanyModerationController, self).get_all(*args, **kw)

    @expose(inherit=True)
    def post(self, *args, **kw):
        raise HTTPNotFound()

    @expose(inherit=True)
    def new(self, *args, **kwargs):
        raise HTTPNotFound()

    @expose(inherit=True)
    def edit(self, *args, **kw):
        # This is a somewhat ugly solution. There might be a better way to add
        # a delete button at the end of the edit form, but I haven't found one
        # so far.
        res = EasyCrudRestController.edit(self, *args, **kw)
        res['delete_url'] = '/%s' % tg.request.controller_url
        return res

    @expose(inherit=True)
    def put(self, *args, **kw):
        new_model = kw_to_sqlalchemy(model.CompanyAlchemy, kw)

        prepare_company_for_validation(new_model)
        kw = sqlalchemy_to_kw(new_model)

        return EasyCrudRestController.put(self, *args, **kw)


class GeocodingAdminLayout(BootstrapAdminLayout):
    """
    Pyjobs' custom admin geocoding issues resolution interface layout. Redefines
    template_index and crud_templates from the ones used in the
    BootstrapAdminLayout, to match the needs of the moderation interfaces.
    """
    template_index = 'pyjobsweb.templates.admin.geocoding.index'
    crud_templates = {
        'get_all': [
            'mako:pyjobsweb.templates.admin.geocoding.get_all'
        ],
        'edit': [
            'mako:pyjobsweb.templates.admin.geocoding.edit'
        ]
        # Notice how there is no 'new' crud template? It's because the
        # geocoding controller isn't meant to add new rows to the database,
        # it's just supposed to modify existing rows. The default crud
        # controller of PyJobs' admin already handles new row creations.
    }


class GeocodingAdminConfig(BootstrapTGAdminConfig):
    """
    PyJobs' geocoding related issues admin controller configuration. Every
    tables in the model that's prone to having geocoding issues which require
    a custom CrustRestController to solve, should be configured in this class.
    See Turbogears 2's documentation for more details:
    http://turbogears.readthedocs.io/en/latest/turbogears/wikier/admin.html?highlight=crud
    """
    layout = GeocodingAdminLayout

    def __init__(self, models, translations=None):
        super(GeocodingAdminConfig, self).__init__(models, translations)

    class job(CrudRestControllerConfig):
        defaultCrudRestController = JobGeocodingController

    class company(CrudRestControllerConfig):
        defaultCrudRestController = CompanyGeocodingController


class ModerationAdminLayout(BootstrapAdminLayout):
    """
    Pyjobs' custom admin moderation interface layout. Redefines template_index
    and crud_templates from the ones used in the BootstrapAdminLayout, to match
    the needs of the moderation interfaces.
    """
    template_index = 'pyjobsweb.templates.admin.moderation.index'
    crud_templates = {
        'get_all': [
            'mako:pyjobsweb.templates.admin.moderation.get_all'
        ],
        'edit': [
            'mako:pyjobsweb.templates.admin.moderation.edit'
        ]
        # Notice how there is no 'new' crud template? It's because the
        # moderation controller isn't meant to add new rows to the database,
        # it's just supposed to modify existing rows. The default crud
        # controller of PyJobs' admin already handles new row creations.
    }


class ModerationAdminConfig(BootstrapTGAdminConfig):
    """
    PyJobs' moderation related issues admin controller configuration. Every
    tables in the model that's prone to moderation which require a custom
    CrustRestController should be configured in this class. See Turbogears 2's
    documentation for more details:
    http://turbogears.readthedocs.io/en/latest/turbogears/wikier/admin.html?highlight=crud
    """
    layout = ModerationAdminLayout

    def __init__(self, models, translations=None):
        super(ModerationAdminConfig, self).__init__(models, translations)

    class company(CrudRestControllerConfig):
        defaultCrudRestController = CompanyModerationController


class AdminGeocodingController(AdminController):
    """
    PyJobs' admin sub-controller in charge of managing geolocation issues
    related routing in the admin. Every table in the model that might have
    geocoding issues should be added to the 'to_fix' list.
    """

    """
    A list containing every tables in the Postgresql database that might have
    geocoding issues that should be handled by this controller.
    """
    to_fix = [model.JobAlchemy, model.CompanyAlchemy]

    def __init__(self):
        super(AdminGeocodingController, self).__init__(
            self.to_fix, DBSession, config_type=GeocodingAdminConfig)

    @property
    def geocoding_list(self):
        models = [table.__name__ for table in self.config.models.values()]
        models.sort()

        geocoding_list = list()
        for m in models:
            geocoding_list.append(dict(link='%ss' % m.lower(), display=m))

        return geocoding_list

    @with_trailing_slash
    @expose()
    def index(self):
        # We use a custom index template, therefore, we have to change the dict
        # that's returned by the super.index() method, so that our template gets
        # the values it needs to operate correctly.
        super_res = super(AdminGeocodingController, self).index()

        res = dict(config=super_res['config'],
                   model_config=super_res['model_config'],
                   geocoding_list=self.geocoding_list)

        return res


class AdminModerationController(AdminController):
    """
    PyJobs' admin sub-controller in charge of managing moderation related
    routing in the admin. Every table in the model that requires moderation
    should be added to the 'to_moderate' list.
    """

    """
    A list containing every tables in the Postgresql database that should be
    handled by this controller.
    """
    to_moderate = [model.CompanyAlchemy]

    def __init__(self):
        super(AdminModerationController, self).__init__(
            self.to_moderate, DBSession, config_type=ModerationAdminConfig)

    @property
    def moderation_list(self):
        models = [table.__name__ for table in self.config.models.values()]
        models.sort()

        moderation_list = list()
        for m in models:
            moderation_list.append(dict(link='%ss' % m.lower(), display=m))

        return moderation_list

    @with_trailing_slash
    @expose()
    def index(self):
        # We use a custom index template, therefore, we have to change the dict
        # that's returned by the super.index() method, so that our template gets
        # the values it needs to operate correctly.
        super_res = super(AdminModerationController, self).index()

        res = dict(config=super_res['config'],
                   model_config=super_res['model_config'],
                   moderation_list=self.moderation_list)

        return res


class PyJobsAdminLayout(BootstrapAdminLayout):
    """
    Pyjobs' custom admin interface layout. Redefines template_index and
    crud_templates from the ones used in the BootstrapAdminLayout.
    """
    template_index = 'pyjobsweb.templates.admin.default.index'
    crud_templates = {
        'get_all': [
            'mako:pyjobsweb.templates.admin.default.get_all'
        ],
        'edit': [
            'mako:pyjobsweb.templates.admin.default.edit'
        ],
        'new': [
            'mako:pyjobsweb.templates.admin.default.new'
        ]
    }


class JobCrudRestController(EasyCrudRestController):
    """
    Not a whole lot of changes in this custom EasyCrudRestController. It just
    adds some database synchronization code (to keep both Postgresql and
    Elasticsearch databases in sync.
    """
    __form_options__ = {
        '__omit_fields__': ['last_modified', 'last_sync']
    }

    def __init__(self, session, menu_items=None):
        super(JobCrudRestController, self).__init__(session, menu_items)

    @expose(inherit=True)
    def put(self, *args, **kw):
        # TODO: Could this test be removed if 'publication_datetime_is_fake'
        # TODO: was False by default and un-nullable
        if not kw['publication_datetime_is_fake']:
            kw['publication_datetime_is_fake'] = False

        old_model = model.JobAlchemy.get_job_offer(kw['id'])
        new_model = kw_to_sqlalchemy(model.JobAlchemy, kw)

        # Check if the address has been modified. If it's the case, then
        # prepare the kw dict before insertion.
        if old_model.address != new_model.address:
            prepare_job_for_address_update(new_model)

        kw = sqlalchemy_to_kw(new_model)

        return EasyCrudRestController.put(self, *args, **kw)


class CompanyCrudRestController(EasyCrudRestController):
    """
    Not a whole lot of changes in this custom EasyCrudRestController. It just
    adds some database synchronization code (to keep both Postgresql and
    Elasticsearch databases in sync.
    """
    __form_options__ = {
        '__omit_fields__': ['last_modified', 'last_sync']
    }

    def __init__(self, session, menu_items=None):
        super(CompanyCrudRestController, self).__init__(session, menu_items)

    @expose(inherit=True)
    def put(self, *args, **kw):
        old_model = model.CompanyAlchemy.get_company(kw['id'])
        new_model = kw_to_sqlalchemy(model.CompanyAlchemy, kw)

        # Check if the address has been modified. If it's the case, then
        # prepare the kw dict before insertion.
        if old_model.address != new_model.address:
            prepare_company_for_address_update(new_model)

        kw = sqlalchemy_to_kw(new_model)

        return EasyCrudRestController.put(self, *args, **kw)


class PyJobsAdminConfig(TGAdminConfig):
    """
    The configuration of the PyJobs admin interface. As you can see, this config
    uses a custom AdminLayout (which redefines some templates used by the
    admin - like the index for instance).
    We also tell Turbogears admin to use our custom CrudRestControllers when
    it comes to editing the jobs and the companies tables
    """
    layout = PyJobsAdminLayout

    class job(CrudRestControllerConfig):
        defaultCrudRestController = JobCrudRestController

    class company(CrudRestControllerConfig):
        defaultCrudRestController = CompanyCrudRestController


class PyJobsAdminController(AdminController):
    """
    This controller handles the whole admin interface of PyJobs
    It consists of multiple CrudRestControllers that allows one to manipulate
    the database.
    The index of this controller points to the default CrudRest AdminController,
    with a few modifications to ensure some model integrity issues.
    """

    """
    This sub-controller is used to solve any geocoding related issues that
    might have occured during the geocoding operation performed by the
    gearbox geocode command.
    """
    geocoding = AdminGeocodingController()

    """
    This controller is used to moderate (edit, delete, accept) company
    submissions that have been submitted, but haven't yet been moderated.
    """
    moderation = AdminModerationController()

    # The clunky 's' after the table names are enforced by the way the
    # framework generates the admin controllers. So, even though the plural
    # form in english is a tad more complicated than just appending a 's' at
    # the end of the words, this is how it is in TG2 and this explains why there
    # are these 's' at the end of the link parameters.
    # TODO: find a way to remove the clunky 's'
    geocoding_list = [
        {'link': 'geocoding/jobs', 'display': 'Jobs'},
        {'link': 'geocoding/companys', 'display': 'Companies'}
    ]

    moderation_list = [
        {'link': 'moderation/companys', 'display': 'Companies'}
    ]

    def __init__(self):
        super(PyJobsAdminController, self).__init__(
            model, DBSession, config_type=PyJobsAdminConfig)

    @property
    def model_list(self):
        models = [table.__name__ for table in self.config.models.values()]
        models.sort()

        model_list = list()
        for m in models:
            model_list.append(dict(link='%ss' % m.lower(), display=m))

        return model_list

    @with_trailing_slash
    @expose()
    def index(self):
        # We use a custom index template, therefore, we have to change the dict
        # that's returned by the super.index() method, so that our template gets
        # the values it needs to operate correctly.
        super_res = super(PyJobsAdminController, self).index()

        res = dict(config=super_res['config'],
                   model_config=super_res['model_config'],
                   model_list=self.model_list,
                   geocoding_list=self.geocoding_list,
                   moderation_list=self.moderation_list)

        return res
