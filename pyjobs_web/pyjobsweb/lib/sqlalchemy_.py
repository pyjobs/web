# -*- coding: utf-8 -*-
from tzlocal import get_localzone
from datetime import datetime
from sqlalchemy import func

from pyjobsweb.model import DBSession
from pyjobsweb.model import JobAlchemy, CompanyAlchemy


def _find_type(sqlalchemy_table_class, column_name):
    if hasattr(sqlalchemy_table_class, '__table__') \
            and column_name in sqlalchemy_table_class.__table__.c:
        return sqlalchemy_table_class.__table__.c[column_name].type
    for base in sqlalchemy_table_class.__bases__:
        return _find_type(base, column_name)
    raise NameError(column_name)


def is_dirty(old_model, new_model):
    for column in old_model.__table__.columns:
        column = column.name
        if getattr(old_model, column, None) != getattr(new_model, column, None):
            return True

    return False


def kw_to_sqlalchemy(sqlalchemy_table_cls, kw):
    sqlalchemy_table = sqlalchemy_table_cls()

    for column, value in kw.iteritems():
        try:
            column_type = _find_type(sqlalchemy_table_cls, column)
            python_type = column_type.python_type
        except NameError:
            continue

        try:
            if not issubclass(type(value), python_type):
                if issubclass(python_type, bool):
                    column_value = True if value.lower() == 'true' else False
                else:
                    column_value = python_type(value)
            else:
                column_value = value
        except UnicodeEncodeError:
            column_value = unicode(value)
        finally:
            if issubclass(python_type, datetime):
                if column_type.timezone:
                    # Convert to local time
                    tz = get_localzone()
                    column_value = tz.localize(column_value, is_dst=None)
            setattr(sqlalchemy_table, column, column_value)

    return sqlalchemy_table


def sqlalchemy_to_kw(sqlalchemy_obj):
    res = {}
    for column in sqlalchemy_obj.__table__.columns:
        res[column.name] = getattr(sqlalchemy_obj, column.name)

    return res


def prepare_job_for_address_update(job_offer):
    assert isinstance(job_offer, JobAlchemy)

    # The address has been modified, therefore the geolocation should be
    # recomputed, so we mark the address as valid, so that the geolocation
    # program will try and recompute it later on.
    job_offer.address_is_valid = True

    # We reset the geolocation related fields to their default values too.
    # This bit isn't necessary, because the controller can only alter the
    # content of rows with invalid addresses, and therefore rows which
    # geolocation isn't valid by definition. But it doesn't hurt to put this
    # additional code here. It just makes the manipulation of the Companies
    # table consistent across the geocoding issues controller and the
    # general crud controller.
    job_offer.latitude = 0.0
    job_offer.longitude = 0.0
    job_offer.geolocation_is_valid = False


def prepare_company_for_address_update(company):
    assert isinstance(company, CompanyAlchemy)

    # The address has been modified, therefore the geolocation should be
    # recomputed, so we mark the address as valid, so that the geolocation
    # program will try and recompute it later on.
    company.address_is_valid = True

    # We reset the geolocation related fields to their default values too.
    # This bit isn't necessary, because the controller can only alter the
    # content of rows with invalid addresses, and therefore rows which
    # geolocation isn't valid by definition. But it doesn't hurt to put this
    # additional code here. It just makes the manipulation of the Companies
    # table consistent across the geocoding issues controller and the
    # general crud controller.
    company.latitude = 0.0
    company.longitude = 0.0
    company.geolocation_is_valid = False


def prepare_company_for_validation(company):
    assert isinstance(company, CompanyAlchemy)

    # Someone just validated this company. Therefore, mark it as such.
    company.validated = True


def current_server_timestamp():
    return DBSession.execute(func.current_timestamp()).scalar()
