[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/pyjobs/web/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/pyjobs/web/?branch=master)

## Installation and setup

### Dependencies

Pyjobs_web require some OS dependencies (to build project python libs), for a debian-like you can install them with ``apt-get``:

```
apt-get install python python-dev python-pip git libpq-dev libxml2-dev libxslt1-dev libffi-dev python-pip virtualenv
```

### Pyjobs Web

**Note**: For production environment, create ``production.ini`` configuration file from copying ``development.ini`` and replace ``development.ini`` by ``production.ini`` in following instructions.

Clone the project:

```
git clone https://github.com/pyjobs/web.git
```

Move to ``web/pyjobs_web`` directory:

```
cd pyjobs_web/pyjobs_web
```

Install python dependencies:

```
pip install -r requirements.txt
```

Install ``pyjobsweb`` using the setup.py script:

```
python setup.py develop
```

Update config according to your database in ``pyjobs_web/pyjobs_web/development.ini``. Import lines to update are:

* ``debug``: Think to switch at ``False`` if you are in production environment.
* ``session.secret``
* ``session.validate_key``
* ``sqlalchemy.url``: Update it according to your database (MySQL, PostgreSQL, SQLite, [etc](http://docs.sqlalchemy.org/en/latest/core/engines.html).).

Create the project database for any model classes defined::

    $ gearbox setup-app -c development.ini

### Run PyJobs Web

Start the paste http server::

    $ gearbox serve -c development.ini

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve -c development.ini --reload --debug

Then you are ready to go.

## Update job database with crawls

Run ``gearbox crawl`` command. It will be run [PyJobs Crawlers](https://github.com/pyjobs/crawlers) and feed PyJobs Web database.
