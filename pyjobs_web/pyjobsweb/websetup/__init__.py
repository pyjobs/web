# -*- coding: utf-8 -*-
"""Setup the pyjobsweb application"""

import logging

from pyjobsweb.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)

from .schema import setup_schema
from .bootstrap import bootstrap
from .mapping import setup_mapping


def setup_app(command, conf, vars):
    """Place any commands to setup pyjobsweb here"""
    load_environment(conf.global_conf, conf.local_conf)
    setup_schema(command, conf, vars)
    setup_mapping(command, conf, vars)
    bootstrap(command, conf, vars)
