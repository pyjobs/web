# -*- coding: utf-8 -*-
"""Setup the pyjobsweb application"""
from __future__ import print_function

import json
import logging

from tg import config
import transaction


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
    from elasticsearch_dsl.connections import connections
    import elasticsearch_dsl.index
    from pyjobsweb import model

    print("Setting up Elasticsearch's model")

    connections.create_connection(
        hosts=[config.get('elasticsearch.host')],
        send_get_body_as='POST',
        timeout=20
    )

    # Setup the jobs index
    jobs_index = elasticsearch_dsl.Index('jobs')
    jobs_index.settings()
    jobs_index.doc_type(model.JobOfferElasticsearch)
    # jobs_index.delete(ignore=404)
    jobs_index.create(ignore=400)

    # Setup the geocompletion index
    geocomplete_index = elasticsearch_dsl.Index('geocomplete')
    geocomplete_index.settings()
    geocomplete_index.doc_type(model.Geocomplete)
    geocomplete_index.delete(ignore=404)
    geocomplete_index.create(ignore=400)

    # Population the geocompletion index
    geolocation_data = open(config.get('fr.geolocation_data.path'))

    json_dict = json.loads(geolocation_data.read())

    to_index = list()

    for postal_code, places in json_dict.items():
        for place in places:
            entry = model.Geocomplete(
                name=place['name'],
                postal_code=postal_code,
                geolocation=dict(
                    lat=float(place['lat']),
                    lon=float(place['lon'])
                )
            )

            to_index.append(entry)

    from elasticsearch.helpers import streaming_bulk

    conn = connections.get_connection()
    for ok, info in streaming_bulk(conn, (d.to_dict(True) for d in to_index)):
        if not ok:
            logging_level = logging.ERROR
            err_msg = u'Failed to index document: %s.' % info['create']['_id']
            logging.getLogger(__name__).log(logging_level, err_msg)
