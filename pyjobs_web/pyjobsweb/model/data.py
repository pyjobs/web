# -*- coding: utf-8 -*-
from pyjobs_crawlers.tools import get_sources, condition_tags
from sqlalchemy import Column, Text, String, Integer, DateTime, Boolean

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
            u'télé-travail': 'job-remote',
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
    publication_datetime_is_fake = Column(Boolean)

    crawl_datetime = Column(DateTime)

    already_in_elasticsearch = Column(Boolean, default=False)

    def __init__(self):
        pass

    def __repr__(self):
        return "<Job: id='%d'>" % (self.id)

    def to_dict(self):
        import json

        return {
            'id': self.id,
            'url': self.url,
            'source': self.source,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'company_url': self.company_url,
            'address': self.address,
            'tags': json.loads(self.tags),
            'publication_datetime': self.publication_datetime,
            'publication_datetime_is_fake': self.publication_datetime_is_fake
        }

    @property
    def published(self):
        return format_date(self.publication_datetime, locale='FR_fr')

    @property
    def published_in_days(self):
        delta = datetime.now() - self.publication_datetime
        return format_timedelta(delta, granularity='day', locale='en_US')

    @property
    def alltags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] not in condition_tags:
                    tags.append(Tag2(tag['tag'], tag['weight']))
        return tags

    @property
    def condition_tags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] in condition_tags:
                    tag = Tag2(tag['tag'], tag['weight'], Tag2.get_css(tag['tag']))
                    tags.append(tag)
        return tags
