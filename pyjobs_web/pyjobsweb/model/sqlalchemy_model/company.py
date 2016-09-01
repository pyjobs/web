# -*- coding: utf-8 -*-
import transaction
from datetime import datetime

import sqlalchemy as sa

from pyjobsweb.model import DeclarativeBase, DBSession
from pyjobsweb.model.elasticsearch_model.company import Company \
    as CompanyElastic


class Company(DeclarativeBase):
    __tablename__ = 'companies'

    # The id column stores the company name column slug
    id = sa.Column(sa.String(1024), primary_key=True)

    name = sa.Column(sa.String(1024), nullable=False, default='')
    logo_url = sa.Column(sa.String(1024), nullable=False, default='')
    description = sa.Column(sa.Text(), nullable=False, default='')
    url = sa.Column(sa.String(1024), nullable=False, default='')
    # Comma separated technologies. We only store a textual representation of
    # the technologies used by the company to make it easier to duplicate the
    # model into Elasticsearch to allow searching on this field (Elasticsearch
    # is really good at string research).
    technologies = sa.Column(sa.Text(), nullable=False, default='')

    address = sa.Column(sa.String(1024), nullable=False, default='')
    address_is_valid = sa.Column(sa.Boolean, nullable=False, default=True)

    email = sa.Column(sa.String(1024), nullable=False, default='')
    phone = sa.Column(sa.String(1024), nullable=False, default='')

    latitude = sa.Column(sa.Float, nullable=False, default=0.0)
    longitude = sa.Column(sa.Float, nullable=False, default=0.0)
    geolocation_is_valid = sa.Column(sa.Boolean, nullable=False, default=False)

    validated = sa.Column(sa.Boolean, nullable=False, default=False)

    last_modified = sa.Column(sa.DateTime(timezone=True), nullable=False,
                              server_default=sa.func.now(),
                              onupdate=sa.func.current_timestamp())

    last_sync = sa.Column(sa.DateTime(timezone=True),
                          nullable=False, default=datetime.min)

    def to_elasticsearch_document(self):
        result = CompanyElastic(
            meta={'id': self.id},
            id=self.id,
            name=self.name,
            logo_url=self.logo_url,
            description=self.description,
            url=self.url,
            technologies=self.technologies,
            address=self.address,
            address_is_valid=self.address_is_valid,
            email=self.email,
            phone=self.phone,
            geolocation=dict(lat=self.latitude, lon=self.longitude),
            geolocation_is_valid=self.geolocation_is_valid
        )

        return result

    def __repr__(self):
        return "<Company: id='%d'>" % self.id

    @classmethod
    def get_validated_companies(cls):
        return DBSession.query(cls) \
            .filter_by(validated=True) \
            .order_by(cls.name.asc())

    @classmethod
    def get_validated_company(cls, company_id):
        return DBSession.query(cls) \
            .filter(cls.id == company_id) \
            .filter_by(validated=True) \
            .one()

    @classmethod
    def get_company(cls, company_id):
        return DBSession.query(cls).filter(cls.id == company_id).one()

    @classmethod
    def get_pending_geolocations(cls):
        return DBSession.query(cls) \
            .filter_by(address_is_valid=True) \
            .filter_by(geolocation_is_valid=False) \
            .filter_by(validated=True) \
            .order_by(cls.id.asc())

    @classmethod
    def set_geolocation(cls, company_id, lat, lon):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == company_id) \
            .update({'latitude': lat,
                     'longitude': lon,
                     'geolocation_is_valid': True})
        transaction.commit()

    @classmethod
    def set_geolocation_is_valid(cls, company_id, is_valid):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == company_id) \
            .update({'geolocation_is_valid': is_valid})
        transaction.commit()

    @classmethod
    def set_address_is_valid(cls, company_id, is_valid):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == company_id) \
            .update({'address_is_valid': is_valid})
        transaction.commit()

    @classmethod
    def get_dirty_rows(cls):
        return DBSession.query(cls) \
            .filter(cls.validated) \
            .filter(cls.last_modified > cls.last_sync) \
            .order_by(cls.id.asc())

    @classmethod
    def update_last_sync(cls, job_id, timestamp):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.id == job_id) \
            .update({'last_sync': timestamp,
                     'last_modified': cls.last_modified})
        DBSession.query(cls) \
            .filter(cls.id == job_id) \
            .filter(cls.last_modified < timestamp) \
            .update({'last_modified': timestamp})
        transaction.commit()

    @classmethod
    def reset_last_sync(cls):
        transaction.begin()
        DBSession.query(cls) \
            .filter(cls.validated) \
            .update({'last_sync': datetime.min})
        transaction.commit()
