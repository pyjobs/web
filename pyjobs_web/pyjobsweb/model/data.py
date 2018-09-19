# -*- coding: utf-8 -*-
from pyjobs_crawlers.tools import get_sources


class Status(object):
    INITIAL_CRAWL_OK = 'initial-crawl-ok'
    PUBLISHED = 'published'


class Source(object):
    AFPY_JOBS = 'afpy-jobs'
    REMIXJOBS_PYTHON = 'remixjobs-python'

class FakeSource(object):
    def __init__(self, slug, url, logo_url, label):
        self.name = slug
        self.url = url
        self.logo_url = logo_url
        self.label = label

SOURCES = get_sources()
SOURCES['pyjobs'] = FakeSource('pyjobs', 'http://pyjobs.fr/', 'http://pyjobs.fr/img/pyjobs_logo_square.png', 'pyjobs')

class Tag2(object):
    def __init__(self, tag, weight=1, css=''):
        self.tag = tag
        self.weight = weight
        self.css = css

    @classmethod
    def get_css(cls, tagname):
        css = {
            u'cdd': 'job-cdd',
            u'cdi': 'job-cdi',
            u'freelance': 'job-freelance',
            u'stage': 'job-stage',
            u'télétravail': 'job-remote',
            u'télé-travail': 'job-remote',
        }
        return css[tagname]
