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
