# -*- coding: utf-8 -*-
from pyjobs_crawlers import get_sources
from sqlalchemy import Column, Text, String, Integer, DateTime

from pyjobsweb.model import DeclarativeBase
from datetime import datetime
from babel.dates import format_date, format_timedelta


class Status(object):
    INITIAL_CRAWL_OK = 'initial-crawl-ok'
    PUBLISHED = 'published'


class Source(object):
    AFPY_JOBS = 'afpy-jobs'
    REMIXJOBS_PYTHON = 'remixjobs-python'


SOURCES = get_sources()


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
        }
        return css[tagname]


class Job(DeclarativeBase):

    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)

    url = Column(String(1024))
    source = Column(String(64))

    title = Column(String(1024), nullable=False, default='')
    description = Column(Text(), nullable=False, default='')
    company = Column(String(1024), nullable=False, default='')
    company_url = Column(String(1024), nullable=True, default='')

    address = Column(String(2048), nullable=False, default='')
    tags = Column(Text(), nullable=False, default='')  # JSON

    publication_datetime = Column(DateTime)

    crawl_datetime = Column(DateTime)

    def __init__(self):
        pass

    def __repr__(self):
        return "<Job: id='%d'>" % (self.id)

    @property
    def published(self):
        return format_date(self.publication_datetime, locale='FR_fr')

    @property
    def published_in_days(self):
        delta = datetime.now() - self.publication_datetime
        return format_timedelta(delta, granularity='day', locale='en_US')

    job_condition_tags = (u'cdd', u'cdi', u'freelance', u'stage', u'télétravail')

    @property
    def alltags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] not in self.job_condition_tags:
                    tags.append(Tag2(tag['tag'], tag['weight']))
        return tags

    @property
    def condition_tags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] in self.job_condition_tags:
                    tag = Tag2(tag['tag'], tag['weight'], Tag2.get_css(tag['tag']))
                    tags.append(tag)
        return tags
