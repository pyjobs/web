# -*- coding: utf-8 -*-
import elasticsearch_dsl
import elasticsearch_dsl.serializer
import sqlalchemy
import transaction
from pyjobs_crawlers.tools import get_sources, condition_tags


import pyjobsweb.lib.search_query as search_query
import pyjobsweb.model
from pyjobsweb.model import DeclarativeBase

from datetime import datetime
from babel.dates import format_date, format_timedelta


class Status(object):
    INITIAL_CRAWL_OK = 'initial-crawl-ok'
    PUBLISHED = 'published'


class Source(object):
    AFPY_JOBS = 'afpy-jobs'
    REMIXJOBS_PYTHON = 'remixjobs-python'


SOURCES = get_sources()


class Tag2(object):
    def __init__(self, tag, weight=1, css=''):
        self.tag = tag
        self.weight = weight
        self.css = css

    @classmethod
    def get_css(cls, tagname):
        css = {
            u'cdd': 'job-cdd',
            u'cdi': 'job-cdi',
            u'freelance': 'job-freelance',
            u'stage': 'job-stage',
            u'télétravail': 'job-remote',
            u'télé-travail': 'job-remote',
        }
        return css[tagname]


class Tags(elasticsearch_dsl.InnerObjectWrapper):
    pass


class Tag(elasticsearch_dsl.InnerObjectWrapper):
    pass


class JobOfferElasticsearch(elasticsearch_dsl.DocType):
    class Meta:
        index = 'jobs'
        doc_type = 'job-offer'

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
    french_description_analyzer = elasticsearch_dsl.analyzer(
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

    id = elasticsearch_dsl.Integer()

    url = elasticsearch_dsl.String()

    source = elasticsearch_dsl.String()

    title = elasticsearch_dsl.String(
            analyzer=french_analyzer
    )

    description = elasticsearch_dsl.String(
            analyzer=french_description_analyzer
    )

    company = elasticsearch_dsl.String()

    company_url = elasticsearch_dsl.String()

    address = elasticsearch_dsl.String()

    tags = elasticsearch_dsl.Nested(
            doc_class=Tag,
            properties={
                'tag': elasticsearch_dsl.String(),
                'weight': elasticsearch_dsl.Integer()
            }
    )

    publication_datetime = elasticsearch_dsl.Date()
    publication_datetime_is_fake = elasticsearch_dsl.Boolean()
    crawl_datetime = elasticsearch_dsl.Date()
    geolocation_error = elasticsearch_dsl.Boolean()
    geolocation = elasticsearch_dsl.GeoPoint()

    @property
    def published(self):
        return format_date(self.publication_datetime, locale='FR_fr')

    @property
    def published_in_days(self):
        delta = datetime.now() - self.publication_datetime
        return format_timedelta(delta, granularity='day', locale='en_US')

    @property
    def alltags(self):
        tags = []
        if self.tags:
            for tag in self.tags:
                if tag['tag'] not in condition_tags:
                    tags.append(Tag2(tag['tag'], tag['weight']))
        return tags

    @property
    def condition_tags(self):
        tags = []
        if self.tags:
            for tag in self.tags:
                if tag['tag'] in condition_tags:
                    tag = Tag2(
                            tag['tag'], tag['weight'],
                            Tag2.get_css(tag['tag'])
                    )
                    tags.append(tag)
        return tags


class ElasticsearchTranslator(search_query.QueryTranslator):
    def __init__(self, query_object):
        super(ElasticsearchTranslator, self).__init__(query_object)

    def translate_multisort(self, multi_sort):
        return self.query_object.sort(*[s.translate(self) for s in multi_sort])

    def translate_ascsort(self, asc_sort):
        return '{}'.format(asc_sort.to_sort)

    def translate_descsort(self, desc_sort):
        return '-{}'.format(desc_sort.to_sort)

    def translate_keywordfilter(self, search_filter):
        return self.query_object.query(
                'multi_match',
                fields=search_filter.fields,
                query=search_filter.keywords
        )

    def translate_geolocationfilter(self, search_filter):
        return self.query_object.filter(
                'geo_distance',
                geolocation=[
                    search_filter.center.longitude,
                    search_filter.center.latitude
                ],
                distance='{}{}'.format(search_filter.radius, search_filter.unit)
        )


class ElasticsearchQuery(search_query.GenericSearchQuery):
    def __init__(self):
        search_obj = JobOfferElasticsearch.search()
        search_obj = search_obj.params(size=1000)
        translator = ElasticsearchTranslator(search_obj)
        query_builder = search_query.QueryBuilder(translator)

        super(ElasticsearchQuery, self).__init__(query_builder)

    def execute_query(self):
        return self.builder.build().execute().hits


class JobOfferSQLAlchemy(DeclarativeBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    url = sqlalchemy.Column(sqlalchemy.String(1024))
    source = sqlalchemy.Column(sqlalchemy.String(64))

    title = sqlalchemy.Column(
            sqlalchemy.String(1024), nullable=False, default=''
    )
    description = sqlalchemy.Column(
            sqlalchemy.Text(), nullable=False, default=''
    )
    company = sqlalchemy.Column(
            sqlalchemy.String(1024), nullable=False, default=''
    )
    company_url = sqlalchemy.Column(
            sqlalchemy.String(1024), nullable=True, default=''
    )

    address = sqlalchemy.Column(
            sqlalchemy.String(2048), nullable=False, default=''
    )
    tags = sqlalchemy.Column(
            sqlalchemy.Text(), nullable=False, default=''
    )  # JSON

    publication_datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    publication_datetime_is_fake = sqlalchemy.Column(sqlalchemy.Boolean)

    crawl_datetime = sqlalchemy.Column(sqlalchemy.DateTime)

    already_in_elasticsearch = sqlalchemy.Column(
            sqlalchemy.Boolean, nullable=False, default=False
    )

    def __init__(self):
        pass

    def __repr__(self):
        return "<Job: id='%d'>" % self.id

    @property
    def published(self):
        return format_date(self.publication_datetime, locale='FR_fr')

    @property
    def published_in_days(self):
        delta = datetime.now() - self.publication_datetime
        return format_timedelta(delta, granularity='day', locale='en_US')

    @property
    def alltags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] not in condition_tags:
                    tags.append(Tag2(tag['tag'], tag['weight']))
        return tags

    @property
    def condition_tags(self):
        import json
        tags = []
        if self.tags:
            for tag in json.loads(self.tags):
                if tag['tag'] in condition_tags:
                    tag = Tag2(
                            tag['tag'], tag['weight'],
                            Tag2.get_css(tag['tag'])
                    )
                    tags.append(tag)
        return tags

    def to_elasticsearch_job_offer(self):
        deserialize = elasticsearch_dsl.serializer.serializer.loads
        job_tags = deserialize(self.tags)
        tags = []

        for tag in job_tags:
            tags.append(tag)

        return JobOfferElasticsearch(
                id=self.id,
                url=self.url,
                source=self.source,
                title=self.title,
                description=self.description,
                company=self.company,
                company_url=self.company_url,
                address=self.address,
                tags=tags,
                publication_datetime=self.publication_datetime,
                publication_datetime_is_fake=self.publication_datetime_is_fake,
                crawl_datetime=self.publication_datetime
        )

    @classmethod
    def job_offer_exists(cls, url):
        return pyjobsweb.model.DBSession \
            .query(JobOfferSQLAlchemy) \
            .filter(JobOfferSQLAlchemy.url == url) \
            .count()

    @classmethod
    def mark_as_inserted_in_elasticsearch(cls, offer_id):
        transaction.begin()
        pyjobsweb.model.DBSession \
            .query(JobOfferSQLAlchemy) \
            .filter(JobOfferSQLAlchemy.id == offer_id) \
            .update({'already_in_elasticsearch': True})
        transaction.commit()

    @classmethod
    def compute_elasticsearch_pending_insertion(cls):
        return pyjobsweb.model.DBSession \
            .query(JobOfferSQLAlchemy) \
            .filter_by(already_in_elasticsearch=False)

    @classmethod
    def get_all_job_offers(cls):
        return pyjobsweb.model.DBSession \
            .query(JobOfferSQLAlchemy) \
            .order_by(JobOfferSQLAlchemy.publication_datetime.desc())
