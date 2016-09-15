# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, DateTime

from pyjobsweb.model import DeclarativeBase


class Log(DeclarativeBase):

    __tablename__ = 'crawl_log'

    id = Column(Integer, primary_key=True)
    source = Column(String(64))
    message = Column(String(1024), nullable=False)
    datetime = Column(DateTime)
