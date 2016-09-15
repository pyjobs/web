# -*- coding: utf-8 -*-

#  Quickstarted Options:
#
#  sqlalchemy: True
#  auth:       sqlalchemy
#  mako:       True
#
#

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'gearbox'
]

install_requires = [
    "TurboGears2 >= 2.3.7",
    "Beaker",
    "Genshi",
    "Mako",
    "zope.sqlalchemy >= 0.4",
    "sqlalchemy",
    "alembic",
    "repoze.who",
    "tw2.forms",
    "tgext.admin >= 0.6.1",
    "WebHelpers2",
    "GitPython==1.0.1"
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")

setup(
    name='pyjobsweb',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'pyjobsweb': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'pyjobsweb': [
        ('**.py', 'python', None),
        ('templates/**.mak', 'mako', None),
        ('templates/**.html', 'genshi', None),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = pyjobsweb.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ],
        'gearbox.commands': [
            'crawl-job-boards = pyjobsweb.commands.crawl:CrawlCommand',
            'run-publication-bots = pyjobsweb.commands.bots:BotsCommand',
            'populate-elasticsearch = pyjobsweb.commands.populate_es:PopulateESCommand',
            'purge-elasticsearch = pyjobsweb.commands.purge_es:PurgeESCommand',
            'geotag-jobs-and-companies = pyjobsweb.commands.geocode:GeocodeCommand'
        ]
    },
    zip_safe=False,
    requires=['gearbox', 'paste', 'webtest', 'webtest']
)
