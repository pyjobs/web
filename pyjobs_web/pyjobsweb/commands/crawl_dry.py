# -*- coding: utf-8 -*-
import pyjobs_crawlers.run

import crawlers
import pyjobsweb.commands


class DryRunCrawlCommand(pyjobsweb.commands.AppContextCommand):
    def get_parser(self, prog_name):

        parser = super(DryRunCrawlCommand, self).get_parser(prog_name)

        parser.add_argument(
                "-s", "--spider",
                help='Spider name.',
                dest='spider_name'
        )

        parser.add_argument(
                "-t", "--type",
                help='Mandatory value : (list|offer).',
                dest='page_type'
        )

        parser.add_argument(
                "-u", "--url",
                help='Page url.',
                dest='url'
        )

        return parser

    def take_action(self, parsed_args):
        super(DryRunCrawlCommand, self).take_action(parsed_args)
        pyjobs_crawlers.run.start_crawler(
                connector_class=crawlers.PyJobsWebDryRunCrawlConnector(),
                spider_name=parsed_args.spider_name
                #type=parsed_args.type,
                #url=parsed_args.url
        )
