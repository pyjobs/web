# -*- coding: utf-8 -*-
import sqlalchemy
from pyjobsweb import model
from pyjobs_crawlers import Connector
from pyjobsweb.model.data import Job
from pyjobsweb.model import DBSession
import transaction

__all__ = ('helpers', 'app_globals')


class PyJobsWebConnector(Connector):
    def __init__(self):
        # TODO - B.S. - 20160114: Centraliser la config postgres
        engine = sqlalchemy.engine.create_engine('postgres://pyjobs:pyjobs@localhost/pyjobs')
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

        job = Job()
        attributes = ['title', 'description', 'company', 'address', 'company_url',
                      'publication_datetime']

        # Populate job attributes if item contain it
        for attribute in attributes:
            if attribute in job_item:
                setattr(job, attribute, job_item[attribute])

        job.url = job_item['url']
        job.source = job_item['source']
        job.crawl_datetime = job_item['initial_crawl_datetime']

        if 'tags' in job_item:
            import json
            tags = [{'tag': t.tag, 'weight': t.weight} for t in job_item['tags']]
            job.tags = json.dumps(tags)

        DBSession.add(job)
        transaction.commit()

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
