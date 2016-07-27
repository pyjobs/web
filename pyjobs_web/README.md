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

## Populate the Elasticsearch database with populate-es

Run ``gearbox populate-es [-j|--jobs] [-g|--geocomplete]`` command. This command allows you to index the job offers present in the Postgresql database (through the
``-j`` or ``--jobs`` argument) under the ``jobs`` index. These documents are required if you want the research form to work. It also allows you to index the required
geocomplete documents present in the ``static/geolocations/fr_locations.json`` file, under the ``geocomplete`` index (through the ``-g`` or ``--geocomplete`` argument).
These documents are required for the geocompletion in the research form to work.

## Purge the Elasticsearch database with purge-es

Run ``gearbox purge-es [-j|--jobs] [-g|--geocomplete]`` command. The command will delete both the ``jobs`` and/or ``geocomplete`` Elasticsearch indices depending on
the specified arguments. After deleting them it will recreate them along with their mappings. Also, after purging the ``jobs`` index, the command will also set back
the ``indexed_in_elasticsearch`` column to ``False`` for every entry in the Postgresql ``jobs`` table.
