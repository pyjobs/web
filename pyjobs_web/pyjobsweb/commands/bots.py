# -*- coding: utf-8 -*-
from pyjobsweb.bot.github import GitHubBot
from pyjobsweb.commands import AppContextCommand


class BotsCommand(AppContextCommand):

    def take_action(self, parsed_args):
        super(BotsCommand, self).take_action(parsed_args)

        github_bot = GitHubBot()
        github_bot.run()
