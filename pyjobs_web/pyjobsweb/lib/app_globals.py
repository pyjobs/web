# -*- coding: utf-8 -*-

"""The application's Globals object"""

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Do nothing, by default."""
        from elasticsearch_dsl.connections import connections
        from tg import config

        connections.create_connection(hosts=[config.get('elasticsearch.host')],
                                      send_get_body_as="POST",
                                      timeout=20)
