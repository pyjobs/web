# -*- coding: utf-8 -*-
"""Setup the pyjobsweb application"""
from __future__ import print_function

import elasticsearch.exceptions
import elasticsearch_dsl.index
import transaction
from elasticsearch_dsl.connections import connections
from tg import config


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
    jobs_index.doc_type(model.JobElastic)

    try:
        jobs_index.create()
    except elasticsearch.ElasticsearchException as e:
        print("Exception while creating index 'jobs': %s." % e)

    # Setup the geocomplete index
    geocomplete_index = elasticsearch_dsl.Index('geocomplete')
    geocomplete_index.settings()
    geocomplete_index.doc_type(model.Geocomplete)

    try:
        geocomplete_index.create()
    except elasticsearch.ElasticsearchException as e:
        print("Exception while creating index 'geocomplete': %s." % e)
