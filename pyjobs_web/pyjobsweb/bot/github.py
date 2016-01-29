# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sqlalchemy
from git import Repo, Actor
from os.path import expanduser
from pyjobsweb import model
from mako.template import Template
import codecs
from tg import config

home = expanduser("~")


class GitHubBot(object):

    # TODO - B.S. - 20160118: from config
    #REPOSITORY_ADDRESS = 'git@github.com:pyjobs/annonces.git'
    REPOSITORY_ADDRESS = 'git@github.com:algoo/annonces.git'

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
        self._check_repository_directory()
        self._check_repository()

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

    def run(self):
        """
        Update job file if new jobs. Then make a push.
        :return:
        """
        lasts_jobs = self._get_lasts_jobs()
        new_jobs = self._get_new_jobs(lasts_jobs)

        if new_jobs:
            self._write_jobs(lasts_jobs)
            message = self._get_commit_message(new_jobs)
            self._commit(message)
            self._push()
    
    def _get_lasts_jobs(self):
        """
        :return: x last jobs, where x is _last_jobs_count class attribute
        :rtype: list
        """
        lasts_jobs = model.DBSession \
            .query(model.data.Job) \
            .order_by(model.data.Job.publication_datetime.desc()) \
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
                if job.title not in jobs_file_read:
                    cleaned_jobs.append(job)
        return cleaned_jobs

    def _write_jobs(self, jobs):
        """
        Write jobs in jpobs file
        :param jobs: list of jobs
        :return:
        """
        template = Template(filename=self._jobs_template_file_path)
        with codecs.open(self._jobs_file_path, 'w', 'utf-8') as jobs_file:
            print(template.render(jobs=jobs), file=jobs_file)
    
    def _get_commit_message(self, jobs):
        """
        :param jobs:
        :return: Message rended from message template, where template file is specified in
         _jobs_message_file_path class attribute
        """
        template = Template(filename=self._jobs_message_file_path)
        return template.render(jobs=jobs)
    
    def _commit(self, message):
        """
        Make the commit
        :param message: commit message
        :return:
        """
        repo_index = self._repo.index
        repo_index.add([self._jobs_file_path])
        # TODO - B.S. - 20160118: Le mail est ok ?
        author = Actor("PyJobs GitHub bot", "pyjobs-github-bot@algoo.fr")
        repo_index.commit(message, author=author, committer=author)

    def _pull(self):
        origin = self._get_origin()
        with self._get_remote_environnement():
            origin.pull()

    def _push(self):
        origin = self._get_origin()
        with self._get_remote_environnement():
            origin.push()

    def _get_remote_environnement(self):
        """
        :return: Return an environment who specify to use class attribute _deployment_key_file_path key
        """
        ssh_cmd = 'ssh -i %s' % self._deployment_key_file_path
        return self._repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd)

    def _get_origin(self):
        return self._repo.remotes.origin
