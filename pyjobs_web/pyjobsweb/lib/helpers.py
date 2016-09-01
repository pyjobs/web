# -*- coding: utf-8 -*-
"""Template Helpers used in pyjobsweb."""
import json
import logging
from datetime import datetime
from urllib import quote_plus

from markupsafe import Markup
from slugify import slugify as base_slugify
from tg import config

log = logging.getLogger(__name__)
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
mois = ["Janvier", u"Février", "Mars", "Avril", "Mai", "Juin", "Juillet", u"Août", "Septembtre", "Octobre"]


def current_year():
    now = datetime.now()
    return now.strftime('%Y')


def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)


def slugify(string):
    return base_slugify(string)


def to_json(data, **kwargs):
    return json.dumps(data, **kwargs)


def french_day(day_number):
    return jours[day_number-1]


def french_month(month_number):
    return mois[month_number-1]


def head_js():
    return config.get('site.head_js')


def get_job_url(job_id, job_title=None, previous=None, absolute=False):
    job_url = "/jobs/details/%s" % job_id
    if job_title:
        job_url += "/%s" % slugify(job_title)
    if previous:
        job_url += "?previous=%s" % quote_plus(previous)
    if absolute:
        job_url = "%s%s" % (config.get('site.domain_base_url'), job_url)
    return job_url


def get_company_url(company_id, previous=None, absolute=False):
    company_url = '/societes-qui-recrutent/details/%s' % company_id

    if previous:
        company_url = '%s?previous=%s' % (company_url, quote_plus(previous))
    if absolute:
        company_url = '%s%s' % (config.get('site.domain_base_url'), company_url)

    return company_url

# Import commonly used helpers from WebHelpers2 and TG

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")

