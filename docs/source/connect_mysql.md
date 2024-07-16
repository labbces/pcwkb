# Setting up MySQL/MariaDB for Plant Cell Wall KnowledgeBase

First create a MySQL/MariaDB user with root:

```sql
CREATE USER pcwkb_db_admin@localhost IDENTIFIED BY 'password1';
```


Create Databases in this case there will be a database that will be used in the site directly and a other to receive submissions:

```sql
CREATE DATABASE pcwkb_db;
CREATE DATABASE pcwkb_db_temp_data;
```

Give permissions to that user to access the database:

```sql
GRANT INDEX, CREATE, DROP, SELECT, UPDATE, DELETE, ALTER, EXECUTE, INSERT on pcwkb_db.* TO pcwkb_db_admin@localhost;
GRANT FILE on *.* TO pcwkb_db_admin@localhost;
```

You can edit `settings.py` to add the database connection information as follows:

```python
DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'pcwkb_db',
         'USER': 'pcwkb_db_admin',
         'PASSWORD': 'password1',
         'HOST': '127.0.0.1',
         'PORT': '',
      },
      "temporary_data":{
        'ENGINE': 'django.db.backends.mysql',
         'NAME': 'pcwkb_db_temp_data',
         'USER': 'pcwkb_db_admin',
         'PASSWORD': 'password1',
         'HOST': '127.0.0.1',
         'PORT': '',
      }
   }
```

Note that the databases, user and password should match those in settings.py "DATABASES section".

Once the database is created we can create the migration using:

```bash
python manage.py makemigrations
python manage.py makemigrations pcwkb_core
python manage.py check
python manage.py migrate
./manage.py migrate --database=pcwkb_db_temp_data
```

By default, management command operates on the default database, the --database option is for to synchronizing a different database.