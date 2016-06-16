# -*- coding: utf-8 -*-
import datetime

import sqlalchemy
import transaction
import elasticsearch
from pyjobs_crawlers.run import Connector
from sqlalchemy.orm.exc import NoResultFound
from tg import config

from pyjobsweb import model
from pyjobsweb.model import DBSession, Log
from pyjobsweb.model.data import Job

__all__ = ('helpers', 'app_globals')


class PyJobsWebConnector(Connector):
    # Elasticsearch connection setup
    elastic_search = elasticsearch.Elasticsearch()

    def __init__(self):
        # Postgresql connection setup
        engine = sqlalchemy.engine.create_engine(config.get('sqlalchemy.url'))
        engine.connect()
        model.init_model(engine)

    def add_job(self, job_item):
        """

        Add job to PyJobsWeb database

        :param job_item: Scrapy pyjobs_crawlers item object
        :return:
        """
        job_public_id = job_item['url']

        if self.job_exist(job_public_id):
            print 'Skip existing item'
            return

        # Instantiate two different kind of objects which will store job offers
        # in different formats :
        #     - The first  one will store job offers in a suitable format
        #       to store them in the Postgresql database (a.k.a: sqlalchemy)
        #     - The second one will store job offers in a suitable format
        #       to store them in the ElasticSearch database (a.k.a: json)
        job = Job()
        json_job_offer = {}

        # Populate attributes which do not require special treatments before
        # population
        attributes = ['title', 'description', 'company', 'address', 'company_url',
                      'publication_datetime', 'publication_datetime_is_fake']

        # Populate job attributes if item contain it
        for attribute in attributes:
            if attribute in job_item:
                setattr(job, attribute, job_item[attribute])
                json_job_offer[attribute] = job_item[attribute]

        job.url = job_item['url']
        job.source = job_item['source']
        job.crawl_datetime = job_item['initial_crawl_datetime']

        json_job_offer['url'] = job_item['url']
        json_job_offer['source'] = job_item['source']
        json_job_offer['crawl_datetime'] = job_item['initial_crawl_datetime']

        # Populate attributes which require special treatments before population
        if 'tags' in job_item:
            import json
            tags = [{'tag': t.tag, 'weight': t.weight} for t in job_item['tags']]
            job.tags = json.dumps(tags)
            json_job_offer['tags'] = tags

        # Insert the job offer in the Postgresql database
        DBSession.add(job)
        transaction.commit()

        # Insert the job offer in the ElasticSearch database too, in order to
        # ease both the keyword specific, and the geolocation lookups of job
        # offers
        self.elastic_search.index(
                index="jobs", doc_type="job-offer", body=json_job_offer
        )

    def job_exist(self, job_url):
        """

        Return count of jobs having this url

        :param job_url: External identifier of job (url)
        :return:
        """
        return model.DBSession \
            .query(model.data.Job) \
            .filter(model.data.Job.url == job_url) \
            .count()

    def log(self, source, action, more=None):
        if more is not None:
            message = '%s (%s)' % (action, more)
        else:
            message = action

        log = Log()
        log.source = source
        log.message = message
        log.datetime = datetime.datetime.now()

        DBSession.add(log)
        transaction.commit()

    def get_most_recent_job_date(self, source):
        try:
            return model.DBSession.query(model.data.Job.publication_datetime)\
                .filter(model.data.Job.source == source)\
                .order_by(model.data.Job.publication_datetime.desc())\
                .limit(1)\
                .one()[0]  # First element is publication_datetime datetime value
        except NoResultFound:
            return datetime.datetime(1970, 1, 1, 0, 0, 0)
