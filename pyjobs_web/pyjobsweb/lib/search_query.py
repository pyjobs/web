# -*- coding: utf-8 -*-
import abc


class Translatable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def translate(self, translator):
        pass

    @abc.abstractmethod
    def __str__(self):
        return str()


class QueryStatement(Translatable):
    __metaclass__ = abc.ABCMeta


class SortStatement(Translatable):
    __metaclass__ = abc.ABCMeta

    _to_sort = None

    def __init__(self, to_sort):
        self.to_sort = to_sort

    @property
    def to_sort(self):
        return self._to_sort

    @to_sort.setter
    def to_sort(self, to_sort):
        self._to_sort = to_sort


class Filter(QueryStatement):
    __metaclass__ = abc.ABCMeta


class Sort(list, QueryStatement):
    def __init__(self):
        super(list, self).__init__()
        self._type = SortStatement

    def append(self, sort):
        if not isinstance(sort, SortStatement):
            raise TypeError('sort should be of type %s.' % self._type)

        super(Sort, self).append(sort)

    def translate(self, translator):
        return translator.translate_sort(self)

    def __str__(self):
        res = 'Sort['

        for i, e in enumerate(self):
            if i > 0:
                res = '{}, '.format(res)

            res = '{}{}'.format(res, e)

        return '{}]'.format(res)


class AscSortStatement(SortStatement):
    def translate(self, translator):
        return translator.translate_asc_sort_statement(self)

    def __str__(self):
        return 'AscSortStatement[to_sort: {}]'.format(self.to_sort)


class DescSortStatement(SortStatement):
    def translate(self, translator):
        return translator.translate_desc_sort_statement(self)

    def __str__(self):
        return 'DescSortStatement[to_sort: {}]'.format(self.to_sort)


class BooleanFilter(Filter):
    _field = None
    _value = None

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def translate(self, translator):
        return translator.translate_boolean_filter(self)

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        if not isinstance(field, basestring):
            raise TypeError('field should be of type: %s.' % basestring)

        self._field = field

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise TypeError('value should be of type: %s.' % bool)

        self._value = value

    def __str__(self):
        return 'BooleanFilter: [{} == {}]'.format(self.field, self.value)


class KeywordFilter(Filter):
    _fields = None
    _keywords = None

    def __init__(self, fields, keywords):
        self.fields = fields
        self.keywords = keywords

    def translate(self, translator):
        return translator.translate_keyword_filter(self)

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        if not isinstance(fields, list) \
                or not all(isinstance(f, basestring) for f in fields):
            raise TypeError('fields should be a list of strings.')

        self._fields = fields

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        if not isinstance(keywords, list) \
                or not all(isinstance(kw, basestring) for kw in keywords):
            raise TypeError('keywords should be a list of strings.')

        self._keywords = keywords

    def __str__(self):
        return 'KeywordFilter: [{}, {}]'.format(self._fields, self._keywords)


class GeolocationFilter(Filter):
    _center = None
    _radius = None
    _unit = None

    from enum import Enum

    class UnitsEnum(Enum):
        KM = 'km'
        M = 'm'

    class Center(object):
        _latitude = None
        _longitude = None

        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

        @property
        def latitude(self):
            return self._latitude

        @latitude.setter
        def latitude(self, latitude):
            if not isinstance(latitude, float):
                raise TypeError('latitude should be of type %s.' % float)

            self._latitude = latitude

        @property
        def longitude(self):
            return self._longitude

        @longitude.setter
        def longitude(self, longitude):
            if not isinstance(longitude, float):
                raise TypeError('longitude should be of type %s.' % float)

            self._longitude = longitude

        def __str__(self):
            return '[{}, {}]'.format(self.latitude, self.longitude)

    def __init__(self, center, radius, unit=UnitsEnum.KM):
        self.center = center
        self.radius = radius
        self.unit = unit

    def translate(self, translator):
        return translator.translate_geolocation_filter(self)

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, center):
        center_type = GeolocationFilter.Center
        if not isinstance(center, center_type):
            raise TypeError('center should be of type %s.', center_type)

        self._center = center

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if not isinstance(radius, float):
            raise TypeError('radius should be of type %s.' % float)

        self._radius = radius

    @property
    def unit(self):
        return self._unit.value

    @unit.setter
    def unit(self, unit):
        unit_enum = GeolocationFilter.UnitsEnum
        if unit not in unit_enum:
            raise TypeError('unit should be of type %s.' % unit_enum)

        self._unit = unit

    def __str__(self):
        return 'GeolocationFilter[Center: {}, Radius: {}, Unit: {}]'\
            .format(self._center, self._radius, self._unit)


class Query(list):
    def __init__(self):
        super(list, self).__init__()
        self._type = QueryStatement

    def append(self, query_elem):
        if not isinstance(query_elem, QueryStatement):
            raise TypeError('search_filter should be of type %s.' % self._type)

        super(Query, self).append(query_elem)

    def __str__(self):
        res = 'Query['

        for i, e in enumerate(self):
            if i > 0:
                res = '{}, '.format(res)

            res = '{}{}'.format(res, e)

        return '{}]'.format(res)


class QueryTranslator(object):
    __metaclass__ = abc.ABCMeta

    _query_object = None

    @abc.abstractmethod
    def __init__(self, query_object):
        self.query_object = query_object

    @property
    def query_object(self):
        return self._query_object

    @query_object.setter
    def query_object(self, query_object):
        if not query_object:
            raise ValueError('query_object should not be null.')

        self._query_object = query_object

    def translate(self, query):
        if not isinstance(query, Query):
            raise TypeError('query should be of type %s.' % Query)

        for search_query in query:
            self.query_object = search_query.translate(self)

        return self.query_object

    @abc.abstractmethod
    def translate_sort(self, multi_sort):
        pass

    @abc.abstractmethod
    def translate_asc_sort_statement(self, asc_sort):
        pass

    @abc.abstractmethod
    def translate_desc_sort_statement(self, desc_sort):
        pass

    @abc.abstractmethod
    def translate_boolean_filter(self, search_filter):
        pass

    @abc.abstractmethod
    def translate_keyword_filter(self, search_filter):
        pass

    @abc.abstractmethod
    def translate_geolocation_filter(self, search_filter):
        pass


class QueryBuilder(object):
    _translator = None

    def __init__(self, translator):
        self.translator = translator
        self._query = Query()

    @property
    def translator(self):
        return self._translator

    @translator.setter
    def translator(self, translator):
        qt_type = QueryTranslator
        if not isinstance(translator, qt_type):
            raise TypeError('translator should be of type %s.' % qt_type)

        self._translator = translator

    def add_elem(self, elem):
        self._query.append(elem)

    def build(self):
        return self.translator.translate(self._query)

    def __str__(self):
        return self._query.__str__()


class BaseSearchQuery(object):
    __metaclass__ = abc.ABCMeta

    _query_builder = None

    @abc.abstractmethod
    def __init__(self, query_builder):
        self.builder = query_builder

    @property
    def builder(self):
        return self._query_builder

    @builder.setter
    def builder(self, builder):
        build_type = QueryBuilder
        if not isinstance(builder, build_type):
            raise TypeError('query_builder should be of type %s.' % build_type)

        self._query_builder = builder

    def add_elem(self, elem):
        self.builder.add_elem(elem)

    @abc.abstractmethod
    def execute_query(self):
        pass

    def __str__(self):
        return self.builder.__str__()
