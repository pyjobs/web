# -*- coding: utf-8 -*-


def is_dirty(old_model, new_model):
    for column in old_model.__table__.columns:
        column = column.name
        if getattr(old_model, column, None) != getattr(new_model, column, None):
            return True

    return False


def find_type(sqlalchemy_table_class, column_name):
    if hasattr(sqlalchemy_table_class, '__table__') \
            and column_name in sqlalchemy_table_class.__table__.c:
        return sqlalchemy_table_class.__table__.c[column_name].type
    for base in sqlalchemy_table_class.__bases__:
        return find_type(base, column_name)
    raise NameError(column_name)


def kw_to_sqlalchemy(sqlalchemy_table_cls, kw):
    sqlalchemy_table = sqlalchemy_table_cls()

    for column, value in kw.iteritems():
        try:
            column_type = find_type(sqlalchemy_table_cls, column).python_type
        except NameError:
            continue

        try:
            if not issubclass(type(value), column_type):
                if issubclass(column_type, bool):
                    column_value = True if value.lower() == 'true' else False
                else:
                    column_value = column_type(value)
            else:
                column_value = value
        except UnicodeEncodeError:
            column_value = unicode(value)
        finally:
            setattr(sqlalchemy_table, column, column_value)

    return sqlalchemy_table


def prepare_kw_for_address_update(kw):
    required_fields = ['address_is_valid', 'latitude', 'longitude',
                       'geolocation_is_valid']

    for field in required_fields:
        assert field in kw

    # The address has been modified, therefore this row is now dirty, and
    # should be resynchronized with Elasticsearch. Also, the geolocation
    # should be recomputed too, so we mark the address as valid, so that
    # the geolocation program will try and recompute it later on.
    mark_kw_as_dirty(kw)
    kw['address_is_valid'] = True

    # We reset the geolocation related fields to their default values too.
    # This bit isn't necessary, because the controller can only alter the
    # content of rows with invalid addresses, and therefore rows which
    # geolocation isn't valid by definition. But it doesn't hurt to put this
    # additional code here. It just makes the manipulation of the Companies
    # table consistent across the geocoding issues controller and the
    # general crud controller.
    kw['latitude'] = 0.0
    kw['longitude'] = 0.0
    kw['geolocation_is_valid'] = False

    return kw


def prepare_kw_for_validation(kw):
    required_fields = ['validated']

    for field in required_fields:
        assert field in kw

    # Someone just validated this company. Therefore, mark it as such.
    kw['validated'] = True


def mark_kw_as_dirty(kw):
    required_fields = ['dirty']

    for field in required_fields:
        assert field in kw

    kw['dirty'] = True
