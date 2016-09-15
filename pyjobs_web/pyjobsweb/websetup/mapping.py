# -*- coding: utf-8 -*-
from __future__ import print_function

import elasticsearch.exceptions
import elasticsearch_dsl.index
from elasticsearch_dsl.connections import connections

from tg import config

from pyjobsweb import model


def _setup_index(elasticsearch_doc_cls, **index_settings):
    index_name = elasticsearch_doc_cls().index

    index = elasticsearch_dsl.Index(index_name)
    index.settings(**index_settings)
    index.doc_type(elasticsearch_doc_cls)

    try:
        index.create()
    except elasticsearch.ElasticsearchException as e:
        print("Exception while creating index '%s': %s." % (index_name, e))


def setup_mapping(command, conf, vars):
    # Setup Elasticsearch's database mapping
    print("Setting up Elasticsearch's model")

    connections.create_connection(
        hosts=[config.get('elasticsearch.host')], send_get_body_as='POST')

    # Setup the jobs index
    _setup_index(model.JobElastic)
    # Setup the company index
    _setup_index(model.CompanyElastic)
    # Setup the geocomplete index
    _setup_index(model.Geocomplete)
