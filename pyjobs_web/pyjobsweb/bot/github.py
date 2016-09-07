# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import re
import codecs
import os
from os.path import expanduser

import sqlalchemy
from git import Repo, Actor
from mako.template import Template
from tg import config

from pyjobsweb import model
from pyjobsweb.lib.helpers import get_job_url
from pyjobsweb.lib.lock import acquire_inter_process_lock

home = expanduser("~")


class GitHubBot(object):

    # TODO - B.S. - 20160118: from config
    #REPOSITORY_ADDRESS = 'git@github.com:pyjobs/annonces.git'
    #REPOSITORY_ADDRESS = 'git@github.com:algoo/annonces.git'
    REPOSITORY_ADDRESS = 'git@github.com:BenoitEchernier/annonces.git'

    # TODO - B.S. - 20160118: from config ... tout ça
    _repository_path = home + '/.pyjobs_web/bot/github'
    _jobs_template_file_path = os.path.dirname(os.path.realpath(__file__)) + '/github_jobs.mak'
    _jobs_message_file_path = os.path.dirname(os.path.realpath(__file__)) + '/github_commit_message.mak'
    _jobs_file_path = _repository_path + '/README.md'
    _last_jobs_count = 50
    _deployment_key_file_path = home + '.ssh/id_rsa.pub'
    
    def __init__(self):
        engine = sqlalchemy.engine.create_engine(config.get('sqlalchemy.url'))
        engine.connect()
        model.init_model(engine)

        self._repo = None

    def _check_repository_directory(self):
        """
        Create repository directory if not exist
        :return:
        """
        if not os.path.exists(self._repository_path):
            os.makedirs(self._repository_path)

    def _check_repository(self):
        """
        Check if repository exist and clone it if not.
        Then fill _repo instance attribute et make a pull.
        :return:
        """
        if not os.path.exists("%s/.git" % self._repository_path):
            Repo.clone_from(self.REPOSITORY_ADDRESS, self._repository_path)

        self._repo = Repo(self._repository_path)
        self._pull()

    def _prepare_local_repo(self):
        self._check_repository_directory()
        self._check_repository()

    def _compute_new_job_offers(self):
        last_jobs = self._get_lasts_jobs()
        return self._get_new_jobs(last_jobs)

    def _commit_new_job_offers(self, new_job_offers):
        new_job_offers.reverse()

        for new_job_offer in new_job_offers:
            old_jobs = self._get_old_jobs()[:-1]
            self._write_jobs(new_job_offer, old_jobs)
            message = self._get_commit_message(new_job_offer)
            self._commit(message)

    def _push_new_job_offers_to_github(self):
        self._prepare_local_repo()

        new_job_offers = self._compute_new_job_offers()

        if not new_job_offers:
            return

        self._commit_new_job_offers(new_job_offers)
        self._push()

    def run(self):
        """
        Update job file if new jobs. Then make a push.
        :return:
        """
        with acquire_inter_process_lock('github_bot') as acquired:
            if not acquired:
                err_msg = 'Another instance of the Github bot is already ' \
                          'running, aborting now.'
                logging.getLogger(__name__).log(logging.WARNING, err_msg)
            else:
                self._push_new_job_offers_to_github()

    def _get_lasts_jobs(self):
        """
        :return: x last jobs, where x is _last_jobs_count class attribute
        :rtype: list
        """
        lasts_jobs = model.DBSession \
            .query(model.JobAlchemy) \
            .order_by(model.JobAlchemy.publication_datetime.desc()) \
            .limit(self._last_jobs_count) \
            .all()
        return lasts_jobs

    def _get_new_jobs(self, jobs):
        """
        :param jobs: job to parse
        :return: jobs not listed in jobs file
        """
        cleaned_jobs = []
        with codecs.open(self._jobs_file_path, 'r', 'utf-8') as jobs_file:
            jobs_file_read = jobs_file.read()
            for job in jobs:
                pyjobs_url = get_job_url(job.id, job.title, absolute=True)
                if pyjobs_url not in jobs_file_read:
                    cleaned_jobs.append(job)
        return cleaned_jobs

    def _get_old_jobs(self):
        old_jobs = []

        with codecs.open(self._jobs_file_path, 'r', 'utf-8') as jobs_file:
            job_offer_re = u'^\*'
            pattern = re.compile(job_offer_re, re.UNICODE)
            for line in jobs_file.readlines():
                if re.search(pattern, line):
                    old_jobs.append(line[:-1])

        return old_jobs

    def _write_jobs(self, new_job, old_jobs):
        """
        Append a new job offer at the beginning of an old job list
        :param new_job: the new jobs offer to append at the beginning of the
        old list
        :param old_jobs: the old job offer list
        :return:
        """
        template = Template(filename=self._jobs_template_file_path)
        with codecs.open(self._jobs_file_path, 'w', 'utf-8') as jobs_file:
            print(template.render(new_job=new_job,
                                  get_job_url=get_job_url,
                                  old_jobs=old_jobs),
                  file=jobs_file)
    
    def _get_commit_message(self, job):
        """
        :param job:
        :return: Message rendered from message template, where template file is
        specified in _jobs_message_file_path class attribute
        """
        template = Template(filename=self._jobs_message_file_path)
        return template.render(job=job)
    
    def _commit(self, message):
        """
        Make the commit
        :param message: commit message
        :return:
        """
        repo_index = self._repo.index
        repo_index.add([self._jobs_file_path])
        # TODO - B.S. - 20160118: From config
        author = Actor("pyjobs", "contact@pyjobs.fr")
        repo_index.commit(message, author=author, committer=author)

    def _pull(self):
        origin = self._get_origin()
        with self._get_remote_environment():
            origin.pull()

    def _push(self):
        origin = self._get_origin()
        with self._get_remote_environment():
            origin.push()

    def _get_remote_environment(self):
        """
        :return: Return an environment who specify to use class attribute
        _deployment_key_file_path key
        """
        ssh_cmd = 'ssh -i %s' % self._deployment_key_file_path
        return self._repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd)

    def _get_origin(self):
        return self._repo.remotes.origin
