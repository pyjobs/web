# -*- coding: utf-8 -*-
import elasticsearch_dsl


class Geocomplete(elasticsearch_dsl.DocType):
    class Meta:
        index = 'geocomplete'
        doc_type = 'geoloc-entry'

    french_elision = elasticsearch_dsl.token_filter(
        'french_elision',
        type='elision',
        articles_case=True,
        articles=[
            'l', 'm', 't', 'qu', 'n', 's',
            'j', 'd', 'c', 'jusqu', 'quoiqu',
            'lorsqu', 'puisqu'
        ]
    )

    geocompletion_ngram_filter = elasticsearch_dsl.token_filter(
        'geocompletion_ngram',
        type='edgeNGram',
        min_gram=1,
        max_gram=50,
        side='front'
    )

    geocompletion_index_analyzer = elasticsearch_dsl.analyzer(
        'geocompletion_index_analyzer',
        type='custom',
        tokenizer='standard',
        filter=[
            'lowercase',
            'asciifolding',
            'word_delimiter',
            french_elision,
            geocompletion_ngram_filter
        ]
    )

    geocompletion_search_analyzer = elasticsearch_dsl.analyzer(
        'geocompletion_search_analyzer',
        type='custom',
        tokenizer='standard',
        filter=[
            'lowercase',
            'asciifolding'
        ]
    )

    name = elasticsearch_dsl.String(
        index='analyzed',
        analyzer=geocompletion_index_analyzer,
        search_analyzer=geocompletion_search_analyzer,
        fields=dict(raw=elasticsearch_dsl.String(index='not_analyzed'))
    )

    postal_code = elasticsearch_dsl.String(
        index='not_analyzed'
    )

    geolocation = elasticsearch_dsl.GeoPoint()

    weight = elasticsearch_dsl.Float()
