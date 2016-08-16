# -*- coding: utf-8 -*-
import sqlalchemy as sa

from pyjobsweb.model import DeclarativeBase, DBSession
from pyjobsweb.model.elasticsearch_model.company import Company \
    as CompanyElastic


class Company(DeclarativeBase):
    __tablename__ = 'companies'

    siren = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String(1024), nullable=False, default='')
    logo_url = sa.Column(sa.String(1024), nullable=False, default='')
    description = sa.Column(sa.Text(), nullable=False, default='')
    url = sa.Column(sa.String(1024), nullable=False, default='')
    # Coma separated technologies. We only store a textual representation of
    # the technologies used by the company to make it easier to duplicate the
    # model into Elasticsearch to allow searching on this field (Elasticsearch
    # is really good at string research).
    technologies = sa.Column(sa.Text(), nullable=False, default='')
    address = sa.Column(sa.String(1024), nullable=False, default='')
    email = sa.Column(sa.String(1024), nullable=False, default='')
    phone = sa.Column(sa.String(1024), nullable=False, default='')

    latitude = sa.Column(sa.Float, nullable=False, default=0.0)
    longitude = sa.Column(sa.Float, nullable=False, default=0.0)
    geolocation_is_valid = sa.Column(sa.Boolean, nullable=False, default=False)

    validated = sa.Column(sa.Boolean, nullable=False, default=False)

    dirty = sa.Column(sa.Boolean, nullable=False, default=True)

    def to_elasticsearch_company(self):
        result = CompanyElastic(
            meta={'id': self.siren},
            siren=self.siren,
            name=self.name,
            logo_url=self.logo_url,
            description=self.description,
            url=self.url,
            technologies=self.technologies,
            address=self.address,
            email=self.email,
            phone=self.phone,
            geolocation=dict(lat=self.latitude, lon=self.longitude),
            geolocation_is_valid=self.geolocation_is_valid
        )

        return result

    @classmethod
    def get_validated_companies(cls):
        return DBSession.query(cls) \
            .filter_by(validated=True) \
            .order_by(cls.name.asc())

    @classmethod
    def get_company(cls, siren):
        return DBSession.query(cls).filter(cls.siren == siren).one()
