# -*- coding: utf-8 -*-
from gearbox.command import Command
# from pyjobs_crawlers.run import start_crawlers
# import os
# from crawlers import PyJobsWebConnector
from tg import config


class CrawlCommand(Command):
    def take_action(self, parsed_args):
        print(config.get('sqlalchemy.url'))


        # os.environ['SCRAPY_SETTINGS_MODULE'] = 'pyjobs_crawlers.settings'
        # start_crawlers(connector_class=PyJobsWebConnector, processes=1, debug=True)
