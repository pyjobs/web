# -*- coding: utf-8 -*-
"""Main Controller"""
from pyjobsweb.model.data import Source, Job, SOURCES
from sqlalchemy.orm.exc import NoResultFound

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.decorators import paginate
from tg.exceptions import HTTPFound
from tg import predicates

from pyjobsweb import model
from pyjobsweb.controllers.secure import SecureController
from pyjobsweb.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from pyjobsweb.lib.base import BaseController
from pyjobsweb.controllers.error import ErrorController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the pyjobsweb application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "pyjobsweb"

    @expose('pyjobsweb.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('pyjobsweb.templates.jobs')
    @paginate('jobs', items_per_page=20)
    def jobs(self):
        #
        # sources = {
        #     'afpy': {'logo_url': 'http://www.afpy.org/logo.png',
        #              'label': 'AFPY'},
        #     'remixjobs': {'logo_url': 'https://remixjobs.com/images/press/logos/logo2-450-140.png',
        #              'label': 'RemixJobs'},
        #     'lolix': {'logo_url': 'http://fr.lolix.org/img/lolix/offer.png',
        #          'label': 'Lolix'},
        #
        #     'linuxjobs': {'logo_url': 'https://pbs.twimg.com/profile_images/649599776573403140/vaMrmib1_400x400.png',
        #          'label': 'LinuxJobs'}
        #
        #
        # }

        jobs = DBSession.query(Job) \
            .order_by(Job.publication_datetime.desc())

        return dict(
            sources=SOURCES,
            jobs=jobs
        )

    @expose('pyjobsweb.templates.job')
    def job(self, job_id, job_title=None):
        """
        Job detail page
        :param job_id: Job identifier
        :param job_title: Job title (optional) for pretty url
        :return: dict
        """
        try:
            job = DBSession.query(Job).filter_by(id=job_id).one()
        except NoResultFound:
            pass  # TODO: TubroGears 404 ?
        return dict(
                job=job,
                sources=SOURCES,
        )

    @expose('pyjobsweb.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('pyjobsweb.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('pyjobsweb.templates.data')
    @expose('json')
    def data(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='data', params=kw)

    @expose('pyjobsweb.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('pyjobsweb.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('pyjobsweb.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
