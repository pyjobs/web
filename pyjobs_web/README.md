## Installation and setup

### Dependencies

Pyjobs_web require some OS dependencies (to build project python libs), for a debian-like you can install them with ``apt-get``:

```
# apt-get install python python-dev python-pip git libpq-dev libxml2-dev libxslt1-dev libffi-dev
```

Pyjobs_web also requires an Elasticsearch database to be installed on the server. On a debian-like server you can do the following:

```
# wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -
# echo "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main" | tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
```

```
# apt-get update && apt-get install elasticsearch
```

```
# /bin/systemctl daemon-reload
# /bin/systemctl enable elasticsearch.service
```
For other systems (and if you need more details for the installation on debian), you can refer to the official documentation:
https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-repositories.html

If you are not interested in setting up replication on different nodes for Elasticsearch, you might want to consider adding the following line at the end of your ``/etc/elasticsearch/elasticsearch.yml`` file for your pyjobs cluster:

 ```
 index.number_of_replicas: 0
 ```

This will prevent your cluster's health to turn to yellow due to impossible to perform replication on another node (since there are no other node).

### Pyjobs Web

**Note**: For production environment, create ``production.ini`` configuration file from copying ``development.ini.template`` and replace ``development.ini`` by ``production.ini`` in following instructions.

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
* ``elasticsearch.host``: Elasticsearch's address and port (default is localhost:9200)
* ``elasticsearch.project_name``: The name of the project (default is pyjobs)
* ``elasticsearch.instance_name``: The instance of the project (default is dev)
* ``processes.project_name``: The name of the project (default is pyjobs)
* ``processes.instance_name``: The instance of the project (default is dev)

``elasticsearch.project_name`` and ``elasticsearch.instance_name`` will be used as prefix (in the form ``elasticsearch.project_name``_``elasticsearch.instance_name``) for indexes defined in pyjobs. This every indexes for this instance will have the following names: ``elasticsearch.project_name``_``elasticsearch.project_name``_pyjobs_index_name, making it possible for you to run several instances of pyjobs on the same instance of Elasticsearch.

The same applies for ``processes.project_name`` and ``processes.instance_name`` though these are used by interprocesses locks used by pyjobs' background processes.

Create the project PostgreSQL database for any model classes defined, as well as Elasticsearch indexes:

    $ gearbox setup-app -c development.ini

At this point the PostgreSQL database is up and running and Elasticsearch too. Though you will first need to populate the geocompletion index of Elasticsearch for you pyjobs' instance. This is done using the following command:

    $ gearbox populate-elasticsearch -g

At this point the geocompletion data is indexed and ready for search in Elasticsearch. IICIICICICI

### Run PyJobs Web

Start the paste http server::

    $ gearbox serve -c development.ini

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve -c development.ini --reload --debug

Then you are ready to go.

## Update job database with crawls

Run ``gearbox crawl-job-boards`` command. It will be run [PyJobs Crawlers](https://github.com/pyjobs/crawlers) and feed PyJobs Web database.

## Geotagging job offers and companies

You may want to geotag job offers and companies so that they can be filter through geolocation filters (that is if you want the research form to be completely operational).
Pyjobs comes with a command to do just this: ``geotag-jobs-and-companies [-j|--jobs] [-co|--companies]``. This command will perform geotagging operations for job offers or companies depending on the specified parameters. Though you might want to do just one at a time (to not flood the nominatim API, be respectful please :). If some addresses couldn't be geotagged (which might happen for various reasons), you will have to solve theses problems by hand through the admin interface of pyjobs.

## Populate the Elasticsearch database with populate-elasticsearch

Now that we have some data stored in the PostgreSQL database, it is time to index it in Elasticsearch, to make it searchable. To do so, run ``gearbox populate-elasticsearch [-j|--jobs] [-co|--companies] [-g|--geocomplete]`` command. This command, depending on the specified arguments will perform synchronization between the PostgreSQL database and Elasticsearch, or it might have a different behavior when using the -g option. Indeed, when specifying -j or -co, it will perform a synchronization of the job offers stored in PostgreSQL and their corresponding documents in Elasticsearch (the same goes for the companies with -co). But when you specify the -g (or --geocomplete), it will build geocompletion documents based from the static data present in the ``static/geolocations/fr_locations.json`` file, and then index these documents under the geocompletion index. If you run the command:

    $ gearbox populate-elasticsearch -g

several times, it will create duplicates in the Elasticsearch database (which won't happen with -j or -co, which perform synchronization operations!).

This leads us to the next command.

## Purge the Elasticsearch database with purge-elasticsearch

Run ``gearbox purge-elasticsearch [-j|--jobs] [-co|--companies] [-g|--geocomplete]`` command. This command will drop the corresponding index in Elasticsearch (the job, company or geocomplete index based on the argument) and will then re-create it.
This is useful while developing, since it allows you to change the mapping for an index, and then re-index documents corresponding to the with the new mapping with the ``gearbox populate-elasticsearch`` command. It will also reset every synchronization data (stored in PostgreSQL), so that running ``gearbox populate-elasticsearch`` still works after purging an index.

## Publication bots

Pyjobs comes with two different publication bots right now. One of them is customizable, while the other isn't. The command which you can use to start these bots is the following: ``gearbox run-publication-bots [twitter [-n NUMBER] -cf credentials_file.json] [github]``. As stated earlier the Github bot isn't customizable and is likely not to work for you (unless you have the authorization to push on the official https://github.com/pyjobs/annonces.git repository) right now. On the other hand, the Twitter bot will work if you provide it with a .json file, containing your Twitter credentials keys in the following format:

{
    "consumer_key":"consumer_key_value_here",
	"consumer_secret":"consumer_secret_value_here",
	"access_token_key":"access_token_key_value_here",
	"access_token_secret":"access_token_secret_value_here"
}
