# -*- coding: utf-8 -*-
from __future__ import absolute_import

import twitter
import logging

from pyjobsweb.model import JobAlchemy
from pyjobsweb.lib.helpers import get_job_url
from pyjobsweb.lib.lock import acquire_inter_process_lock


class TwitterBot(object):
    MAX_TWEET_LENGTH = 140
    MAX_URL_LENGTH = 23
    MAX_TWEETS_TO_PUSH = 250

    def __init__(self, credentials):
        err_msg = ''
        exception = None

        self._logger = logging.getLogger(__name__)

        try:
            self._twitter_api = twitter.Api(
                consumer_key=credentials['consumer_key'],
                consumer_secret=credentials['consumer_secret'],
                access_token_key=credentials['access_token_key'],
                access_token_secret=credentials['access_token_secret']
            )
        except twitter.TwitterError as exc:
            err_msg = 'The following error: %s, occurred while connecting ' \
                      'to the twitter API.' % exc.message
            exception = exc
        except KeyError as exc:
            err_msg = 'Malformed credentials dictionary: %s.' % exc.message
            exception = exc
        except Exception as exc:
            err_msg = 'An unhandled error: %s, occurred while connecting ' \
                      'to the twitter API.' % exc
            exception = exc

        if err_msg:
            logging.getLogger(__name__).log(logging.ERROR, err_msg)
            raise exception

    def _logging(self, logging_level, message):
        self._logger.log(logging_level, message)

    def _format_tweet(self, job_id, job_title):
        self._logging(logging.INFO, 'Formatting tweet.')
        # The Twitter API automatically shrinks URLs to 23 characters
        url = get_job_url(job_id, job_title, absolute=True)

        # Tweet format string
        tweet_format = u'%s. %s'

        # The number of punctuation characters in the tweet string format
        punctuation = len(tweet_format.replace(u'%s', u''))

        total_length = len(job_title) + self.MAX_URL_LENGTH + punctuation

        # Make sure our tweet doesn't exceed max_length
        if total_length > self.MAX_TWEET_LENGTH:
            diff = total_length - self.MAX_TWEET_LENGTH
            job_title = job_title[:-diff]

        # Return the formatted tweet
        return tweet_format % (job_title, url)

    def _push_job_offers_to_twitter(self, num_tweets_to_push):
        # Do not push every job offer at once. The Twitter API won't allow it.
        # We thus push them num_offers_to_push at a time.
        if num_tweets_to_push > self.MAX_TWEETS_TO_PUSH:
            err_msg = 'Cannot push %s tweets at once, pushing %s tweets ' \
                      'instead.' % (num_tweets_to_push, self.MAX_TWEETS_TO_PUSH)
            self._logging(logging.WARNING, err_msg)

            num_tweets_to_push = self.MAX_TWEETS_TO_PUSH

        self._logging(logging.INFO, 'Acquiring unpublished job offers.')
        to_push = JobAlchemy.get_not_pushed_on_twitter(num_tweets_to_push)

        for job_offer in to_push:
            tweet = self._format_tweet(job_offer.id, job_offer.title)

            try:
                self._logging(logging.INFO, 'Publishing to Twitter.')
                self._twitter_api.PostUpdate(tweet)
            except twitter.TwitterError as exc:
                err_msg = '[Job offer id: %s] The following error: %s, ' \
                          'occurred while pushing the following tweet: %s.' \
                          % (job_offer.id, exc.message, tweet)
                self._logging(logging.WARNING, err_msg)
            except Exception as exc:
                err_msg = '[Job offer id: %s] An unhandled error: %s, ' \
                          'occurred while pushing the following tweet: %s.' \
                          % (job_offer.id, exc, tweet)
                self._logging(logging.ERROR, err_msg)
            else:
                # The tweet has been pushed successfully. Mark the job offer as
                # pushed on Twitter in the Postgresql database, so we don't push
                # it again on Twitter later on.
                self._logging(logging.INFO, 'Marking as published on Twitter.')
                JobAlchemy.set_pushed_on_twitter(job_offer.id, True)

    def run(self, num_tweets_to_push):
        self._logging(logging.INFO, 'Starting the Twitter bot.')

        with acquire_inter_process_lock('twitter_bot') as acquired:
            if not acquired:
                err_msg = 'Another instance of the Twitter bot is already ' \
                          'running, aborting now.'
                self._logging(logging.WARNING, err_msg)
            else:
                self._push_job_offers_to_twitter(num_tweets_to_push)
