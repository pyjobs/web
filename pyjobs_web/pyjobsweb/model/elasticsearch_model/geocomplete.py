# -*- coding: utf-8 -*-
import elasticsearch_dsl as es

from pyjobsweb.lib.elasticsearch_ import compute_index_name


class Geocomplete(es.DocType):
    class Meta:
        index = 'geocomplete'
        doc_type = 'geoloc-entry'

    french_elision = es.token_filter(
        'french_elision',
        type='elision',
        articles_case=True,
        articles=[
            'l', 'm', 't', 'qu', 'n', 's',
            'j', 'd', 'c', 'jusqu', 'quoiqu',
            'lorsqu', 'puisqu'
        ]
    )

    geocompletion_ngram_filter = es.token_filter(
        'geocompletion_ngram',
        type='edgeNGram',
        min_gram=1,
        max_gram=50,
        side='front'
    )

    town_filter = es.token_filter(
        'town_filter',
        type='pattern_replace',
        pattern=' ',
        replacement='-'
    )

    geocompletion_index_tokenizer = es.tokenizer(
        'geocompletion_index_tokenizer',
        type='pattern',
        pattern='@'
    )

    geocompletion_index_analyzer = es.analyzer(
        'geocompletion_index_analyzer',
        type='custom',
        tokenizer=geocompletion_index_tokenizer,
        filter=[
            'lowercase',
            'asciifolding',
            french_elision,
            town_filter,
            geocompletion_ngram_filter
        ]
    )

    geocompletion_search_analyzer = es.analyzer(
        'geocompletion_search_analyzer',
        type='custom',
        tokenizer=geocompletion_index_tokenizer,
        filter=[
            'lowercase',
            'asciifolding',
            town_filter,
            french_elision
        ]
    )

    name = es.String(
        index='analyzed',
        analyzer=geocompletion_index_analyzer,
        search_analyzer=geocompletion_search_analyzer,
        fields=dict(raw=es.String(index='not_analyzed'))
    )

    complement = es.String(index='not_analyzed')

    postal_code_ngram_filter = es.token_filter(
        'postal_code_ngram',
        type='edgeNGram',
        min_gram=1,
        max_gram=5,
        side='front'
    )

    postal_code_index_analyzer = es.analyzer(
        'postal_code_index_analyzer',
        type='custom',
        tokenizer='standard',
        filter=[
            postal_code_ngram_filter
        ]
    )

    postal_code_search_analyzer = es.analyzer(
        'postal_code_search_analyzer',
        type='custom',
        tokenizer='standard'
    )

    postal_code = es.String(
        index='analyzed',
        analyzer=postal_code_index_analyzer,
        search_analyzer=postal_code_search_analyzer
    )

    geolocation = es.GeoPoint()

    weight = es.Float()

    def __init__(self, meta=None, **kwargs):
        super(Geocomplete, self).__init__(meta, **kwargs)

        if self.index in compute_index_name(self.index):
            self._doc_type.index = compute_index_name(self.index)

    @property
    def index(self):
        return self._doc_type.index

    @property
    def doc_type(self):
        return self._doc_type.name
