# -*- coding: utf-8 -*-
import abc


class Filter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def translate(self, translator):
        pass

    @abc.abstractmethod
    def __str__(self):
        return str()


class KeywordFilter(Filter):
    _fields = None
    _keywords = None

    def __init__(self, fields, keywords):
        self.fields = fields
        self.keywords = keywords

    def translate(self, translator):
        translator.translate_keywordfilter(self)

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        if not isinstance(fields, list) \
                or not all(isinstance(f, basestring) for f in fields):
            raise TypeError('fields should should be a list of strings.')

        self._fields = fields

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        if not isinstance(keywords, list) \
                or not all(isinstance(kw, basestring) for kw in keywords):
            raise TypeError('keywords should should be a list of strings.')

        self._keywords = keywords

    def __str__(self):
        return 'KeywordFilter: [{}, {}]'.format(self._fields, self._keywords)


class GeolocationFilter(Filter):
    _center = None
    _radius = None
    _unit = None

    from enum import Enum

    class UnitsEnum(Enum):
        km = 'km'
        m = 'm'

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

    def __init__(self, center, radius, unit=UnitsEnum.km):
        self.center = center
        self.radius = radius
        self.unit = unit

    def translate(self, translator):
        translator.translate_geolocationfilter(self)

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
        return 'GeolocationFilter[Center: {}, Radius: {}]'\
            .format(self._center, self._radius)


class Query(list):
    def __init__(self):
        super(list, self).__init__()
        self._type = Filter

    def append(self, search_filter):
        if not isinstance(search_filter, Filter):
            raise TypeError('search_filter should be of type %s.' % self._type)

        super(Query, self).append(search_filter)

    def __str__(self):
        res = '['

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
            search_query.translate(self)

        return self.query_object

    @abc.abstractmethod
    def translate_keywordfilter(self, search_filter):
        pass

    @abc.abstractmethod
    def translate_geolocationfilter(self, search_filter):
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

    def add_filter(self, search_filter):
        self._query.append(search_filter)

    def build(self):
        return self._translator.translate(self._query)

    def __str__(self):
        return self._query.__str__()
