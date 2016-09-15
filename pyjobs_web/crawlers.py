# -*- coding: utf-8 -*-
import datetime
import json

import transaction
from pyjobs_crawlers.run import Connector
from sqlalchemy.orm.exc import NoResultFound

from pyjobsweb import model
from pyjobsweb.model import DBSession, Log

__all__ = ('helpers', 'app_globals')


class PyJobsWebConnector(Connector):
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

        job = model.JobAlchemy()

        # Populate attributes which do not require special treatments before
        # population
        attributes = ['title', 'description', 'company', 'address',
                      'company_url', 'publication_datetime',
                      'publication_datetime_is_fake']

        # Populate job attributes if item contain it
        for attribute in attributes:
            if attribute in job_item:
                setattr(job, attribute, job_item[attribute])

        job.url = job_item['url']
        job.source = job_item['source']
        job.crawl_datetime = job_item['initial_crawl_datetime']

        # Populate attributes which require special treatments before population
        if 'tags' in job_item:
            tags = [{'tag': t.tag, 'weight': t.weight}
                    for t in job_item['tags']]
            job.tags = json.dumps(tags)

        # Insert the job offer in the Postgresql database
        DBSession.add(job)
        transaction.commit()

    def job_exist(self, job_url):
        """

        Return count of jobs having this url

        :param job_url: External identifier of job (url)
        :return:
        """
        return model.JobAlchemy.job_offer_exists(job_url)

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
            return \
                model.DBSession.query(model.JobAlchemy.publication_datetime)\
                .filter(model.JobAlchemy.source == source)\
                .order_by(model.JobAlchemy.publication_datetime.desc())\
                .limit(1)\
                .one()[0]  # First element is publication_datetime value
        except NoResultFound:
            return datetime.datetime(1970, 1, 1, 0, 0, 0)
