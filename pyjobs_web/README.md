## Installation and setup

### Dependencies

Pyjobs_web require some OS dependencies (to build project python libs), for a debian-like you can install them with ``apt-get``:

```
apt-get install python python-dev python-pip git libpq-dev libxml2-dev libxslt1-dev libffi-dev
```

### Pyjobs Web

**Note**: For production environment, create ``production.ini`` configuration file from copying ``development.ini`` and replace ``development.ini`` by ``production.ini`` in following instructions.

Clone the project:

```
git clone http://gitlab.algoo.fr:10080/algoo/pyjobs_web.git pyjobs_web
```

Move to ``pyjobs_web/pyjobs_web`` directory:

```
mv pyjobs_web/pyjobs_web
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

## Populate the Elasticsearch database with populateES

Run ``gearbox populateES`` command. It will fetch every entry in the Postgresl database which haven't been inserted into Elasticsearch yet and perform both the geolocation and the insertion of the job offers in Elasticsearch, so that the search engine of the pyjobs can find it.