# -*- coding: utf-8 -*-
import elasticsearch_dsl


class Geocomplete(elasticsearch_dsl.DocType):
    class Meta:
        index = 'geocomplete'
        doc_type = 'geoloc-entry'

    geocompletion_ngram_filter = elasticsearch_dsl.token_filter(
        'geocompletion_ngram',
        type='edgeNGram',
        min_gram=1,
        max_gram=10,
        side='front'
    )

    geocompletion_index_analyzer = elasticsearch_dsl.analyzer(
        'geocompletion_index_analyzer',
        tokenizer='standard',
        filter=[
            'lowercase',
            'asciifolding',
            'word_delimiter',
            geocompletion_ngram_filter
        ]
    )

    geocompletion_search_analyzer = elasticsearch_dsl.analyzer(
        'geocompletion_search_analyzer',
        tokenizer='standard',
        filter=[
            'standard',
            'lowercase',
            'asciifolding'
        ]
    )

    postal_code_ngram_filter = elasticsearch_dsl.token_filter(
        'postal_code_ngram',
        type='edgeNGram',
        min_gram=1,
        max_gram=5,
        side='front'
    )

    postal_code_index_analyzer = elasticsearch_dsl.analyzer(
        'postal_code_index_analyzer',
        tokenizer='standard',
        filter=[
            'lowercase',
            'asciifolding',
            postal_code_ngram_filter
        ]
    )

    postal_code_search_analyzer = elasticsearch_dsl.analyzer(
        'postal_code_search_analyzer',
        tokenizer='standard',
        filter=[
            'standard'
        ]
    )

    name = elasticsearch_dsl.String(
        index='analyzed',
        analyzer=geocompletion_index_analyzer,
        search_analyzer=geocompletion_search_analyzer
    )

    postal_code = elasticsearch_dsl.String(
        index='analyzed',
        analyzer=postal_code_index_analyzer,
        search_analyzer=postal_code_search_analyzer
    )

    geolocation = elasticsearch_dsl.GeoPoint()
