# -*- coding: utf-8 -*-
import json
import logging

from pyjobsweb.bot.github import GitHubBot
from pyjobsweb.bot.twitter import TwitterBot
from pyjobsweb.commands import AppContextCommand


class BotsCommand(AppContextCommand):

    def get_parser(self, prog_name):
        parser = super(BotsCommand, self).get_parser(prog_name)

        bot_parser = parser.add_subparsers(
            title='Choose your bot',
            description='Use one of these commands to setup and start the '
                        'corresponding bot.',
            help='You must choose between one of these subcommands.',
            dest='bot_command'
        )

        twitter_parser = bot_parser.add_parser(
            'twitter',
            description='Starts the Twitter bot.',
            help="Use this command to start and customize the Twitter bot."
                 "For this command to work, you have to specify the path to "
                 "the file containing your Twitter API credentials using the "
                 "-c (or --credentials-file) argument. For more details about "
                 "the Twitter API credentials file format, please refer to the "
                 "following command: 'gearbox bots twitter -h'."
        )
        twitter_parser.add_argument(
            '-n', '--number-of-tweets', type=int,
            dest='number_of_tweets', default=TwitterBot.MAX_TWEETS_TO_PUSH,
            help='Sets a custom number of tweets to push on twitter, instead '
                 'of default: %s. Beware though, your value cannot be bigger '
                 'than the default one, only smaller.'
                 % TwitterBot.MAX_TWEETS_TO_PUSH
        )
        twitter_parser.add_argument(
            '-c', '--credentials-file', type=str,
            dest='twitter_credentials_file', required=True,
            help="This file must contain the your Twitter API "
                 "credentials in the following json format: "
                 "{"
                 "'consumer_key':'YOUR_CONSUMER_KEY', "
                 "'consumer_secret':'YOUR_CONSUMER_SECRET', "
                 "'access_token_key':'YOUR_ACCESS_TOKEN_KEY', "
                 "'access_token_secret':'YOUR_ACCESS_TOKEN_SECRET'"
                 "} "
                 "Each element of this file must be on a separate line, and "
                 "each line must end with an \\n character."
        )

        # TODO: Fix broken help display (gearbox bots twitter -h displays the
        # TODO: same help message as gearbox bots, which shouldn't be the case)

        bot_parser.add_parser('github',
                              description='Starts the Github bot.',
                              help='Starts the Github bot.')

        return parser

    @staticmethod
    def _get_twitter_credentials(credentials_path):
        err_msg = ''
        exception = None

        credentials = None

        try:
            with open(credentials_path) as credentials_file:
                credentials_json = credentials_file.read()
                credentials = json.loads(credentials_json)
        except ValueError as exc:
            err_msg = 'Malformed credentials file: %s.' % exc
            exception = exc
        except Exception as exc:
            err_msg = 'An error occurred while parsing credentials: %s.' % exc
            exception = exc

        if err_msg:
            logging.getLogger(__name__).log(logging.ERROR, err_msg)
            raise exception

        return credentials

    def take_action(self, parsed_args):
        super(BotsCommand, self).take_action(parsed_args)

        if parsed_args.bot_command == 'twitter':
            num_tweets = parsed_args.number_of_tweets

            try:
                credentials_path = parsed_args.twitter_credentials_file
                credentials = self._get_twitter_credentials(credentials_path)
                twitter_bot = TwitterBot(credentials)
                twitter_bot.run(num_tweets)
            except Exception:
                err_msg = 'A critical error occurred while ' \
                          'configuring/running the Twitter bot. Aborting now.'
                logging.getLogger(__name__).log(logging.ERROR, err_msg)
                exit(-1)

        if parsed_args.bot_command == 'github':
            github_bot = GitHubBot()
            github_bot.run()
