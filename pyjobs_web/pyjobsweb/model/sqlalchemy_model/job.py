# -*- coding: utf-8 -*-
from datetime import datetime

import elasticsearch_dsl as es
import sqlalchemy as sa
import transaction
from babel.dates import format_date, format_timedelta
from pyjobs_crawlers.tools import condition_tags

from pyjobsweb.model import DeclarativeBase, DBSession
from pyjobsweb.model.data import Tag2
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
    address_is_valid = sa.Column(sa.Boolean, nullable=False, default=True)

    tags = sa.Column(sa.Text(), nullable=False, default='')  # JSON

    publication_datetime = sa.Column(sa.DateTime)
    publication_datetime_is_fake = sa.Column(sa.Boolean,
                                             nullable=False, default=False)

    crawl_datetime = sa.Column(sa.DateTime)

    latitude = sa.Column(sa.Float, nullable=False, default=0.0)
    longitude = sa.Column(sa.Float, nullable=False, default=0.0)
    geolocation_is_valid = sa.Column(sa.Boolean, nullable=False, default=False)

    dirty = sa.Column(sa.Boolean, nullable=False, default=True)

    pushed_on_twitter = sa.Column(sa.Boolean, nullable=False, default=False)

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

    def to_elasticsearch_document(self):
        deserialize = es.serializer.serializer.loads
        job_tags = deserialize(self.tags)
        tags = []

        for tag in job_tags:
            tags.append(tag)

        return JobElastic(
            meta={'id': self.id},
            id=self.id,
            url=self.url,
            source=self.source,
            title=self.title,
            description=self.description,
            company=self.company,
            company_url=self.company_url,
            address=self.address,
            address_is_valid=self.address_is_valid,
            tags=tags,
            publication_datetime=self.publication_datetime,
            publication_datetime_is_fake=self.publication_datetime_is_fake,
            crawl_datetime=self.publication_datetime,
            geolocation=dict(lat=self.latitude, lon=self.longitude),
            geolocation_is_valid=self.geolocation_is_valid
        )

    @classmethod
    def job_offer_exists(cls, url):
        return DBSession.query(cls).filter(cls.url == url).count()

    @classmethod
    def set_dirty(cls, offer_id, dirty):
        transaction.begin()
        DBSession.query(cls).filter(cls.id == offer_id).update({'dirty': dirty})
        transaction.commit()

    @classmethod
    def reset_dirty_flags(cls):
        transaction.begin()
        DBSession.query(cls).update({'dirty': True})
        transaction.commit()

    @classmethod
    def get_dirty_rows(cls):
        return DBSession.query(cls).filter(cls.dirty).order_by(cls.id.asc())

    @classmethod
    def get_all_job_offers(cls):
        return DBSession.query(cls).order_by(cls.publication_datetime.desc())

    @classmethod
    def set_address_is_valid(cls, offer_id, is_valid):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'address_is_valid': is_valid})
        transaction.commit()

    @classmethod
    def get_invalid_addresses(cls):
        return DBSession.query(cls).filter_by(address_is_valid=False)

    @classmethod
    def get_pending_geolocations(cls):
        return DBSession.query(cls) \
            .filter_by(address_is_valid=True) \
            .filter_by(geolocation_is_valid=False) \
            .order_by(cls.id.asc())

    @classmethod
    def set_geolocation(cls, offer_id, lat, lon):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'latitude': lat,
                     'longitude': lon,
                     'geolocation_is_valid': True,
                     'dirty': True})
        transaction.commit()

    @classmethod
    def set_geolocation_is_valid(cls, offer_id, is_valid):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'geolocation_is_valid': is_valid, 'dirty': True})
        transaction.commit()

    @classmethod
    def get_not_pushed_on_twitter(cls, limit=None):
        if limit:
            return DBSession.query(cls) \
                .filter_by(pushed_on_twitter=False) \
                .order_by(cls.id.asc()) \
                .limit(limit)
        else:
            return DBSession.query(cls) \
                .filter_by(pushed_on_twitter=False) \
                .order_by(cls.id.asc())

    @classmethod
    def set_pushed_on_twitter(cls, offer_id, pushed_on_twitter):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == offer_id) \
            .update({'pushed_on_twitter': pushed_on_twitter})
        transaction.commit()
