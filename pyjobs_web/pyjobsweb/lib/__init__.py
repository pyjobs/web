# -*- coding: utf-8 -*-
from . import helpers
from . import app_globals

__all__ = ('helpers', 'app_globals')

from pyjobsweb.model.data import Job
# from pyjobs import db

from pyjobsweb.model import DBSession
import transaction

def save_item_as_job(item):
    # def uid(item):
    #     return '{}--{}'.format(item['source'], item['source_local_uid'])
    #
    existing = DBSession.query(Job).filter(Job.url==item['url']).count()
    if existing:
        print 'Skip existing item'
        return

    job = Job()
    attributes = ['title', 'description', 'company', 'address', 'company_url',
                  'publication_datetime']

    # Populate job attributes if item contain it
    for attribute in attributes:
        if attribute in item:
            setattr(job, attribute, item[attribute])

    job.url = item['url']
    job.crawl_datetime = item['initial_crawl_datetime']

    if 'tags' in item:
        import json
        tags = [{'tag': t.tag, 'weight': t.weight} for t in item['tags']]
        job.tags = json.dumps(tags)

    DBSession.add(job)
    transaction.commit()
