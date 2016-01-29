# -*- coding: utf-8 -*-
import os

from pyjobs_crawlers.run import start_crawlers

from crawlers import PyJobsWebConnector
from pyjobsweb.commands import AppContextCommand


class CrawlCommand(AppContextCommand):

    def take_action(self, parsed_args):
        super(CrawlCommand, self).take_action(parsed_args)
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'pyjobs_crawlers.settings'
        start_crawlers(connector_class=PyJobsWebConnector, processes=1, debug=False)
