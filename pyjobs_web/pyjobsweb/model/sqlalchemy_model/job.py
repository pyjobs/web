# -*- coding: utf-8 -*-
import sqlalchemy as sa
import elasticsearch_dsl as es
import transaction
from datetime import datetime
from babel.dates import format_date, format_timedelta

from pyjobs_crawlers.tools import condition_tags
from pyjobsweb.model.data import Tag2
from pyjobsweb.model import DeclarativeBase, DBSession
from pyjobsweb.model.elasticsearch_model.job import Job as JobElastic


class Job(DeclarativeBase):
    __tablename__ = 'jobs'

    id = sa.Column(sa.Integer, primary_key=True)

    url = sa.Column(sa.String(1024))
    source = sa.Column(sa.String(64))

    title = sa.Column(sa.String(1024), nullable=False, default='')
    description = sa.Column(sa.Text(), nullable=False, default='')
    company = sa.Column(sa.String(1024), nullable=False, default='')
    company_url = sa.Column(sa.String(1024), nullable=True, default='')

    address = sa.Column(sa.String(2048), nullable=False, default='')
    is_valid_address = sa.Column(sa.Boolean, nullable=False, default=True)

    tags = sa.Column(sa.Text(), nullable=False, default='')  # JSON

    publication_datetime = sa.Column(sa.DateTime)
    publication_datetime_is_fake = sa.Column(sa.Boolean)

    crawl_datetime = sa.Column(sa.DateTime)

    indexed_in_elasticsearch = sa.Column(sa.Boolean,
                                         nullable=False, default=False)

    def __init__(self):
        pass

    def __repr__(self):
        return "<Job: id='%d'>" % self.id

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
                    tag = Tag2(tag['tag'],
                               tag['weight'], Tag2.get_css(tag['tag']))
                    tags.append(tag)
        return tags

    def to_elasticsearch_job_offer(self):
        deserialize = es.serializer.serializer.loads
        job_tags = deserialize(self.tags)
        tags = []

        for tag in job_tags:
            tags.append(tag)

        return JobElastic(
            id=self.id,
            url=self.url,
            source=self.source,
            title=self.title,
            description=self.description,
            company=self.company,
            company_url=self.company_url,
            address=self.address,
            is_valid_address=self.is_valid_address,
            tags=tags,
            publication_datetime=self.publication_datetime,
            publication_datetime_is_fake=self.publication_datetime_is_fake,
            crawl_datetime=self.publication_datetime
        )

    @classmethod
    def job_offer_exists(cls, url):
        return DBSession.query(cls).filter(cls.url == url).count()

    @classmethod
    def set_indexed_in_elasticsearch(cls, offer_id, inserted):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'indexed_in_elasticsearch': inserted})
        transaction.commit()

    @classmethod
    def reset_indexed_in_elasticsearch(cls):
        transaction.begin()
        DBSession.query(cls).update({'indexed_in_elasticsearch': False})
        transaction.commit()

    @classmethod
    def get_offers_to_index(cls):
        return DBSession.query(cls).filter_by(indexed_in_elasticsearch=False)

    @classmethod
    def get_all_job_offers(cls):
        return DBSession.query(cls).order_by(cls.publication_datetime.desc())

    @classmethod
    def set_is_valid_address(cls, offer_id, is_valid):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'is_valid_address': is_valid})
        transaction.commit()

    @classmethod
    def get_invalid_addresses(cls):
        return DBSession.query(cls).filter_by(is_valid_address=False)
