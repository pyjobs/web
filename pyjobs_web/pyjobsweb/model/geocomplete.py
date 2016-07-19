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
    french_stopwords = elasticsearch_dsl.token_filter(
        'french_stopwords', type='stop', stopwords='_french_'
    )
    # Do not include this filter if keywords is empty
    french_keywords = elasticsearch_dsl.token_filter(
        'french_keywords', type='keyword_maker', keywords=[]
    )
    french_stemmer = elasticsearch_dsl.token_filter(
        'french_stemmer', type='stemmer', language='light_french'
    )

    french_analyzer = elasticsearch_dsl.analyzer(
        'french_analyzer',
        tokenizer='standard',
        filter=[
            'lowercase',
            french_elision,
            french_stopwords,
            # french_keywords,
            french_stemmer
        ]
    )

    name = elasticsearch_dsl.String(index='analyzed')

    name_suggest = elasticsearch_dsl.Completion(
        analyzer=french_analyzer,
        search_analyzer=french_analyzer,
        payloads=True
    )
