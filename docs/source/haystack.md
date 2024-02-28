Setting up Haystack for Plant Cell Wall KnowledgeBase
=====

   To install Django-Haystack, use the `requirements.py`, which already has the correct version of Haystack used for the project (which is version 3.2.1)

Step 1: Configuration
------------

As with most Django applications, you should add Haystack to the `INSTALLED_APPS` within your settings file (usually `settings.py`). As an example:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # Added.
    'haystack',

    # Then your usual apps...
    'blog',
]
```

Within your `settings.py`, you’ll need to add a setting to indicate where your site configuration file will live and which backend to use, as well as other settings for that backend.

`HAYSTACK_CONNECTIONS` is a required setting and this is what we used for Solr X.9:

```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://0.0.0.0:8983/solr/tester',                 # Assuming you created a core named 'tester' as described in installing search engines.
        'ADMIN_URL': 'http://0.0.0.0:8983/solr/admin/cores'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
```


Step 2: Creating SearchIndexes
------------

To build a `SearchIndex`, all that’s necessary is to subclass both indexes. `SearchIndex` & `indexes.Indexable`, define the fields you want to store data with and define a `get_model method`. 
Additionally, we’re providing `use_template=True` on the text field. This allows us to use a data template (rather than error-prone concatenation) to build the document the search engine will index. You’ll need to create a new template inside your template directory called `search/indexes/myapp/note_text.txt` and place an object inside it for each field of your models class, as follows in this example:

```python
{{ object.title }}
{{ object.user.get_full_name }}
{{ object.body }}
```

Step 3: Reindex
------------

You should run `./manage.py build_solr_schema` first, drop the XML output in your Solr’s schema.xml file and restart your Solr server:

```bash
./manage.py build_solr_schema --configure-directory=/home/bianca/project/pcwkb/pcwkb/solr-9.4.0/server/solr/tester/conf
python manage.py rebuild_index
```

