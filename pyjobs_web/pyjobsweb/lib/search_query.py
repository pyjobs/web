# -*- coding: utf-8 -*-
import abc


class Filter(object):
    abc.__metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def translate(self, translator):
        pass


class KeywordFilter(Filter):
    def __init__(self, fields, keywords):
        self._fields = fields
        self._keywords = keywords

    def translate(self, translator):
        translator.translate_keywordfilter(self)


class GeolocationFilter(Filter):
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius

    def translate(self, translator):
        translator.translate_geolocationfilter(self)


class Query(list):
    def __init__(self):
        super(list, self).__init__()
        self._type = Filter

    def append(self, search_filter):
        if not isinstance(search_filter, Filter):
            raise TypeError('search_filter should be of type %s.' % self._type)

        super(Query, self).append(search_filter)


class QueryTranslator(object):
    abc.__metaclass__ = abc.ABCMeta

    def __init__(self):
        self._type = Query

    def translate(self, query):
        if not isinstance(query, Query):
            raise TypeError('query should be of type %s.' % self._type)

        for search_query in query:
            search_query.translate(self)

    @staticmethod
    @abc.abstractmethod
    def translate_keywordfilter(search_filter):
        pass

    @staticmethod
    @abc.abstractmethod
    def translate_geolocationfilter(search_filter):
        pass


class QueryBuilder(object):
    def __init__(self, translator):
        self._type = QueryTranslator

        if not isinstance(translator, QueryTranslator):
            raise TypeError('translator should be of type %s.' % self._type)

        self._translator = translator
        self._query = Query()

    def add_filter(self, search_filter):
        self._query.append(search_filter)

    def build(self):
        return self._translator.translate(self._query)
