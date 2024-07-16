# Adding test data to PCW KB

Now that the databases are established, we have to populate it with some data.

Inside pcwkb/pcwkb/pcwkbcore/tests are some files to populate the site with a minimum data for the pages to work. But, for those there, is a need to insert the data in the correct order so the foreign keys that link each model/table works properly.

The command that will be used is manage.py loaddata that based on a json file, it populates the database.

```
python manage.py loaddata pcwkb_core/tests/data/taxonomy/species.json
python manage.py loaddata pcwkb_core/tests/data/molecular_components/genes.json
```