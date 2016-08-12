# -*- coding: utf-8 -*-
import sqlalchemy as sa

from pyjobsweb.model import DeclarativeBase


class Company(DeclarativeBase):
    __tablename__ = 'companies'

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String(1024), nullable=False, default='')
    logo_url = sa.Column(sa.String(1024), nullable=False, default='')
    description = sa.Column(sa.Text(), nullable=False, default='')
    url = sa.Column(sa.String(1024), nullable=False, default='')
    technologies = sa.Column(sa.Text(), nullable=False, default='')  # JSON
    address = sa.Column(sa.String(1024), nullable=False, default='')
    email = sa.Column(sa.String(1024), nullable=False, default='')
    phone = sa.Column(sa.String(1024), nullable=False, default='')
