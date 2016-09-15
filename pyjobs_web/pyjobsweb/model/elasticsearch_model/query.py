# -*- coding: utf-8 -*-
import pyjobsweb.lib.search_query as search_query


class ElasticsearchTranslator(search_query.QueryTranslator):
    def __init__(self, query_object):
        super(ElasticsearchTranslator, self).__init__(query_object)

    def translate_sort(self, multi_sort):
        return self.query_object.sort(*[s.translate(self) for s in multi_sort])

    def translate_asc_sort_statement(self, asc_sort):
        return '{}'.format(asc_sort.to_sort)

    def translate_desc_sort_statement(self, desc_sort):
        return '-{}'.format(desc_sort.to_sort)

    def translate_boolean_filter(self, search_filter):
        return self.query_object.filter(
            'terms',
            **{search_filter.field: [search_filter.value]}
        )

    def translate_keyword_filter(self, search_filter):
        return self.query_object.query(
            'multi_match',
            fields=search_filter.fields,
            query=search_filter.keywords
        )

    def translate_geolocation_filter(self, search_filter):
        return self.query_object.filter(
            'geo_distance',
            geolocation=[
                search_filter.center.longitude,
                search_filter.center.latitude
            ],
            distance='{}{}'.format(search_filter.radius, search_filter.unit)
        )


class ElasticsearchQuery(search_query.BaseSearchQuery):
    def __init__(self, class_name, page_num, page_size):
        search_obj = class_name.search()
        search_obj = search_obj.params()
        translator = ElasticsearchTranslator(search_obj)
        query_builder = search_query.QueryBuilder(translator)

        self._from = page_num * page_size
        self._to = self._from + page_size

        super(ElasticsearchQuery, self).__init__(query_builder)

    def execute_query(self):
        return (self.builder.build()[self._from:self._to]).execute().hits


