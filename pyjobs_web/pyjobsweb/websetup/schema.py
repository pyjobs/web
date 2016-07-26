# -*- coding: utf-8 -*-
"""Setup the pyjobsweb application"""
from __future__ import print_function

import json
import elasticsearch_dsl.index
import elasticsearch.exceptions
from elasticsearch_dsl.connections import connections

from tg import config
import transaction

from pyjobsweb import model

from pyjobsweb.lib.helpers import elasticsearch_bulk_indexing


def setup_schema(command, conf, vars):
    """Place any commands to setup pyjobsweb here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from pyjobsweb import model
    # <websetup.websetup.schema.after.model.import>

    # <websetup.websetup.schema.before.metadata.create_all>
    print("Creating tables")
    model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
    print('Initializing Migrations')
    import alembic.config
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    import alembic.command
    alembic.command.stamp(alembic_cfg, "head")

    # Setup Elasticsearch's database schema
    print("Setting up Elasticsearch's model")

    connections.create_connection(hosts=[config.get('elasticsearch.host')],
                                  send_get_body_as='POST',
                                  timeout=20)

    # Setup the jobs index
    jobs_index = elasticsearch_dsl.Index('jobs')
    jobs_index.settings()
    jobs_index.doc_type(model.JobOfferElasticsearch)

    try:
        jobs_index.create()
    except elasticsearch.ElasticsearchException as e:
        print("Error while creating the 'jobs' index: %s." % e)

    # Setup the geocomplete index
    geocomplete_index = elasticsearch_dsl.Index('geocomplete')
    geocomplete_index.settings()
    geocomplete_index.doc_type(model.Geocomplete)

    try:
        geocomplete_index.create()

        # Populate the geocomplete index
        elasticsearch_conn = connections.get_connection()
        elasticsearch_bulk_indexing(elasticsearch_conn,
                                    geocompletion_documents())
    except elasticsearch.ElasticsearchException as e:
        print("Error while creating the 'geocomplete' index: %s." % e)


def geocompletion_documents():
    geolocation_data = open(config.get('fr.geolocation_data.path'))

    json_dict = json.loads(geolocation_data.read())

    for postal_code, places in json_dict.items():
        for place in places:
            yield model.Geocomplete(
                name=place['name'],
                postal_code=postal_code,
                geolocation=dict(
                    lat=float(place['lat']),
                    lon=float(place['lon'])
                ),
                weight=place['weight']
            )
