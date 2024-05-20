Setting up Solr for Plant Cell Wall KnowledgeBase
=====

Step 1: Installation of Java 11
------------

The first step is to install Java 11

```bash
conda create -n java11
conda activate java11
conda install -c conda-forge openjdk=11
```

Step 2: Installation and Activation of Solr
------------

Here we are using version 9.4.0 of Solr, so we will do the entire process with it.

```bash
curl -LO https://www.apache.org/dyn/closer.lua/solr/solr/9.4.0/solr-9.5.0.tgz?action=download
tar -xzf solr-9.5.0.tgz
./solr-9.5.0/bin/solr start -h 0.0.0.0 -Dsolr.jetty.host=0.0.0.0
```

Step 3: Building a Core
------------

```bash
./solr-9.5.0/bin/solr create -c tester -n basic_config
```

Step 4: Building a Schema
------------

A schema in Solr is a fundamental component that defines the structure and behavior of your search index. It's essential for maintaining data quality, enabling effective searching, and improving search relevance. Creating and managing a well-designed wschema is crucial for getting the most out of Solr's search capabilities. 
    Here, we build the schema:

```bash
./manage.py build_solr_schema --configure-directory=<path_to_tester_core_managed-schema.xml_file>
```
Instead of "path to tester core config folder" you should have something like: pcwkb/solr-9.4.0/server/solr/tester/conf/managed-schema.xml

Step 5: Rebuild Index
-------------

Use the Django `manage.py` command to rebuild the index:

```bash
./manage.py rebuild_index
```

Type this command in order to build your index, based on the fields given to Solr and
    the .txt index files that are placed under `templates/`.

   Whenever you wish to update the index, type:

```bash
./manage.py update_index
```