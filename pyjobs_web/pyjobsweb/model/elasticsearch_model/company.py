# -*- coding: utf-8 -*-
import elasticsearch_dsl as es

from pyjobsweb.lib.elasticsearch_ import compute_index_name


class Company(es.DocType):
    class Meta:
        index = 'companies'
        doc_type = 'company'

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

    french_stopwords = es.token_filter('french_stopwords',
                                       type='stop', stopwords='_french_')

    # Do not include this filter if keywords is empty
    french_keywords = es.token_filter('french_keywords',
                                      type='keyword_maker', keywords=[])

    french_stemmer = es.token_filter('french_stemmer',
                                     type='stemmer', language='light_french')

    french_analyzer = es.analyzer(
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

    french_description_analyzer = es.analyzer(
        'french_description_analyzer',
        tokenizer='standard',
        filter=[
            'lowercase',
            french_elision,
            french_stopwords,
            # french_keywords,
            french_stemmer
        ],
        char_filter=['html_strip']
    )

    technologies_tokenizer = es.tokenizer('comma_tokenizer',
                                          type='pattern', pattern=',')
    technologies_analyzer = es.analyzer('technologies_analyzer',
                                        tokenizer=technologies_tokenizer)

    id = es.String(index='no')

    name = es.String(index='analyzed')
    logo_url = es.String(index='no')
    description = es.String(analyzer=french_description_analyzer)
    url = es.String(index='no')
    technologies = es.String(analyzer=technologies_analyzer)

    address = es.String(index='no')
    address_is_valid = es.Boolean()

    email = es.String(index='no')
    phone = es.String(index='no')

    geolocation = es.GeoPoint()
    geolocation_is_valid = es.Boolean()

    def __init__(self, meta=None, **kwargs):
        super(Company, self).__init__(meta, **kwargs)
        self._doc_type.index = compute_index_name(self.index)

    @property
    def index(self):
        return self._doc_type.index

    @property
    def doc_type(self):
        return self._doc_type.name
