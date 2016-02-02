# -*- coding: utf-8 -*-
"""Template Helpers used in pyjobsweb."""
import json
import logging
from urllib import quote_plus

from markupsafe import Markup
from datetime import datetime
from slugify import slugify as base_slugify
from tg import config

log = logging.getLogger(__name__)


def current_year():
    now = datetime.now()
    return now.strftime('%Y')


def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)


def slugify(string):
    return base_slugify(string)


def to_json(data, **kwargs):
    return json.dumps(data, **kwargs)


def get_job_url(job_id, job_title=None, previous=None, absolute=False):
    job_url = "/job/%s" % job_id
    if job_title:
        job_url += "/%s" % slugify(job_title)
    if previous:
        job_url += "?previous=%s" % quote_plus(previous)
    if absolute:
        job_url = "%s%s" % (config.get('site.domain_base_url'), job_url)
    return job_url

# Import commonly used helpers from WebHelpers2 and TG
from tg.util.html import script_json_encode

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")
