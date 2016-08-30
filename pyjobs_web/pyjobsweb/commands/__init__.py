# -*- coding: utf-8 -*-
import os
import sys

from gearbox.command import Command
from paste.deploy import loadapp
from webtest import TestApp


class BaseCommand(Command):
    pass


class AppContextCommand(BaseCommand):
    """
    Command who initialize app context at beginning of take_action method.
    """
    def __init__(self, *args, **kwargs):
        super(AppContextCommand, self).__init__(*args, **kwargs)
        self._wsgi_app = None
        self._test_app = None

    @staticmethod
    def _get_initialized_app_context(parsed_args):
        """
        :param parsed_args: parsed args (eg. from take_action)
        :return: (wsgi_app, test_app)
        """
        config_file = parsed_args.config_file
        config_name = 'config:%s' % config_file
        here_dir = os.getcwd()

        # Load locals and populate with objects for use in shell
        sys.path.insert(0, here_dir)

        # Load the wsgi app first so that everything is initialized right
        wsgi_app = loadapp(config_name, relative_to=here_dir)
        test_app = TestApp(wsgi_app)

        # Make available the tg.request and other global variables
        tresponse = test_app.get('/_test_vars')

        return wsgi_app, test_app

    def take_action(self, parsed_args):
        wsgi_app, test_app = self._get_initialized_app_context(parsed_args)
        self._wsgi_app = wsgi_app
        self._test_app = test_app

    def get_parser(self, prog_name):
        parser = super(AppContextCommand, self).get_parser(prog_name)

        parser.add_argument("-c", "--config",
                            help='application config file to read (default: development.ini)',
                            dest='config_file', default="development.ini")
        return parser
