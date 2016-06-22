# -*- coding: utf-8 -*-
"""Setup the pyjobsweb application"""
from __future__ import print_function

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
    import elasticsearch_dsl.connections
    import elasticsearch_dsl.index
    from pyjobsweb import model

    print("Setting up Elasticsearch's model")

    elasticsearch_dsl.connections.connections.create_connection(
        hosts=[config.get('elasticsearch.host')],
        send_get_body_as='POST',
        timeout=20
    )

    # Setup the jobs index
    jobs_index = elasticsearch_dsl.Index('jobs')
    # Empty at the moment
    jobs_index.settings()
    # Register a JobOffer doc_type in the jobs index
    jobs_index.doc_type(model.JobOfferElasticsearch)
    # Create the index
    # TODO : should we drop the index if it already exists ?
    jobs_index.create(ignore=400)

    # Create the mapping for the JobOffer documents
    model.JobOfferElasticsearch.init()
