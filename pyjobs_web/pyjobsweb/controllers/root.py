# -*- coding: utf-8 -*-
"""Main Controller"""
import datetime
import collections
import webhelpers.feedgenerator as feedgenerator
from sqlalchemy.orm.exc import NoResultFound
from tg import expose, flash, require, lurl, config
from tg import predicates
from tg import request, redirect, tmpl_context
from tg.decorators import paginate
from tg.exceptions import HTTPFound
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.controller import AdminController
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig

from pyjobsweb import model
from pyjobsweb.controllers.error import ErrorController
from pyjobsweb.controllers.secure import SecureController
from pyjobsweb.lib.base import BaseController
from pyjobsweb.lib.helpers import slugify, get_job_url
from pyjobsweb.lib.stats import StatsQuestioner
from pyjobsweb.model import DBSession, Log
from pyjobsweb.model.data import JobOfferSQLAlchemy, SOURCES
from pyjobsweb.forms.ResearchForm import ResearchForm

__all__ = ['RootController']
existing_fields = (
    'title',
    'publication_datetime',
    'company',
    'company_url',
    'address',
    'description',
    'tags',
)


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
        tmpl_context.project_name = "Algoo"

    items_per_page = 20

    @expose('pyjobsweb.templates.jobs')
    @paginate('jobs', items_per_page=items_per_page)
    def index(self, query=None, radius=None, center=None, unit=None):
        if not query and not center and not radius:
            job_offers = JobOfferSQLAlchemy.get_all_job_offers()
        else:
            import pyjobsweb.lib.search_query as sq

            search_query = model.ElasticsearchQuery(0, self.items_per_page * 50)

            search_on = ['description', 'title']
            for q in query.split(','):
                search_query.builder.add_elem(sq.KeywordFilter(search_on, [q]))

            if center and radius:
                import geopy.exc
                try:
                    import geopy
                    geolocator = geopy.geocoders.Nominatim()
                    loc = geolocator.geocode(center)
                    center_point = sq.GeolocationFilter.Center(
                        loc.latitude, loc.longitude
                    )
                    radius = float(radius)
                    unit = sq.GeolocationFilter.UnitsEnum(unit)
                    search_query.builder.add_elem(
                        sq.GeolocationFilter(center_point, radius, unit)
                    )
                except AttributeError:
                    pass  # TODO : Mr proper, in case of impossible @ resolution
                except geopy.exc.GeopyError:
                    pass  # TODO : Mr proper
                except ValueError:
                    pass  # TODO : Mr proper

            ms = sq.Sort()
            ms.append(sq.DescSortStatement('publication_datetime'))
            search_query.builder.add_elem(ms)

            job_offers = search_query.execute_query()

        search_form = ResearchForm(action='/', method='POST').req()

        return dict(
            sources=SOURCES,
            jobs=job_offers,
            job_offer_search_form=search_form
        )

    @staticmethod
    def photon_query_builder(address):  # TODO: Export this in a package
        import urllib
        return u'http://photon.komoot.de/api/?q={}&lang=fr'\
            .format(urllib.quote(address.encode('utf-8')))

    @staticmethod
    def execute_query(url):
        import urllib2
        return urllib2.urlopen(url).read()

    @staticmethod
    def format_result(result):  # TODO: export this in a package
        import json
        return json.loads(result)  # TODO

    @expose('json')
    def geocomplete(self, *args, **kwargs):
        if 'address' not in kwargs:
            return []

        req_url = self.photon_query_builder(kwargs['address'])
        query_res = self.format_result(self.execute_query(req_url))

        results = list()
        for qr in query_res['features']:
            address_elem = ['name', 'housenumber', 'street', 'postcode', 'state', 'country']
            address = dict()
            for e in address_elem:
                if e not in qr['properties']:
                    continue

                address[e] = qr['properties'][e].encode('utf-8')

            results.append(address)

        return dict(results=results)

    @expose()
    def rss(self, limit=50, source=None):
        """
        RSS feed of jobs
        :param source: source name
        :param limit: number of displayed jobs
        :return: RSS feed content
        """
        site_url = config.get('site.domain_base_url')
        feed = feedgenerator.Rss201rev2Feed(
            title=u"pyjobs : le job qu'il vous faut en python",
            link=site_url,
            description=u"Agrégation de jobs python",
            language=u"fr",
            feed_url=u"http://www.pyjobs.fr/rss?limit=%s" % limit
        )

        jobs = DBSession.query(JobOfferSQLAlchemy) \
            .order_by(JobOfferSQLAlchemy.publication_datetime.desc()) \
            .limit(limit)

        if source is not None:
            jobs = jobs.filter(JobOfferSQLAlchemy.source == source)

        for job in jobs:
            job_slug = slugify(job.title)
            feed.add_item(
                    title=job.title,
                    link=get_job_url(job.id, job_title=job.title, absolute=True),
                    description=job.description,
                    pubdate=job.publication_datetime,
                    unique_id="%s/job/%d/%s" % (site_url, job.id, job_slug)
            )

        return feed.writeString('utf-8')

    @expose('pyjobsweb.templates.job')
    def job(self, job_id, job_title=None, previous=None):
        """
        Job detail page
        :param job_id: Job identifier
        :param job_title: Job title (optional) for pretty url
        :return: dict
        """
        try:
            job = DBSession.query(JobOfferSQLAlchemy).filter_by(id=job_id).one()
        except NoResultFound:
            pass  # TODO: TubroGears 404 ?
        return dict(
                job=job,
                sources=SOURCES
        )

    @expose('pyjobsweb.templates.sources')
    def sources(self):
        sources_last_crawl = {}
        sorted_sources = collections.OrderedDict(sorted(SOURCES.items(), key=lambda x: x[1].label))
        for source_name in sorted_sources:
            try:
                sources_last_crawl[source_name] = DBSession.query(Log.datetime) \
                    .filter(Log.source == source_name) \
                    .order_by(Log.datetime.desc()) \
                    .limit(1)\
                    .one()[0]
            except NoResultFound:
                sources_last_crawl[source_name] = None

        return dict(
                sources=sorted_sources,
                existing_fields=existing_fields,
                sources_last_crawl=sources_last_crawl
        )

    @expose('pyjobsweb.templates.stats')
    def stats(self, since_months=4):
        stats = StatsQuestioner
        stats_questioner = stats(DBSession)
        date_from, date_to = stats.get_month_period(int(since_months))

        by_months = stats_questioner.by_complete_period(
            period=stats.PERIOD_MONTH,
            date_from=date_from,
            date_to=date_to,
        ).all()
        months = stats.extract(by_months, stats.FIELD_DATE)
        stats_month = stats.extract_stats(query_result=by_months, sources=SOURCES.keys())
        flat_month = stats.flat_query_by_y(
            query_result=by_months,
            sources=SOURCES.keys(),
            date_value_callback=lambda date: date.strftime('%Y-%m')
        )

        by_weeks = stats_questioner.by_complete_period(
            stats.PERIOD_WEEK,
            date_from=date_from,
            date_to=date_to,
        ).all()
        weeks = stats.extract(by_weeks, stats.FIELD_DATE)
        stats_week = stats.extract_stats(query_result=by_weeks, sources=SOURCES.keys())
        flat_week = stats.flat_query_by_y(
            query_result=by_weeks,
            sources=SOURCES.keys(),
            date_value_callback=lambda date: date.strftime('%Y-%m-%d')
        )

        return dict(
            sources=SOURCES,
            stats_month=stats_month,
            flat_month=flat_month,
            stats_week=stats_week,
            flat_week=flat_week,
            months=months,
            weeks=weeks,
            flat_x_field=stats.FIELDS[stats.FLAT_X_FIELD],
            flat_y_fields=SOURCES.keys(),
            sources_labels=[SOURCES[source].label for source in SOURCES]
        )

    @expose('pyjobsweb.templates.logs')
    def logs(self, source=None, last_days=1):

        logs_query = DBSession.query(Log)\
            .order_by(Log.datetime.desc())\
            .filter(Log.datetime >= datetime.datetime.now() + datetime.timedelta(days=-int(last_days)))\
            .filter(Log.message.in_(('CRAWL_LIST_START',
                                    'CRAWL_LIST_FINISHED',
                                    'ERROR_UNEXPECTED_END',
                                    'ERROR_CRAWNLING')))

        if source is not None:
            logs_query = logs_query.filter(Log.source == source)

        return dict(
            sources=SOURCES,
            logs=logs_query.all(),
            last_days=last_days
        )

    @expose('pyjobsweb.templates.about')
    def about(self):
        return dict()

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
