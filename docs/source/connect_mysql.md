# Setting up MySQL/MariaDB for Plant Cell Wall KnowledgeBase

First create a MySQL/MariaDB user with root:

```sql
CREATE USER pcwkb_db_admin@localhost IDENTIFIED BY 'password1';
```

The character set and collate are important as sqlalchemy-migrate doesn't work with utf8mb4 (the default).

```sql
CREATE DATABASE pcwkb_db CHARACTER SET latin1 COLLATE latin1_general_ci;
```
    
Give permissions to that user to access the database:

```sql
GRANT INDEX, CREATE, DROP, SELECT, UPDATE, DELETE, ALTER, EXECUTE, INSERT on pcwkb_db.* TO pcwkb_db_admin@localhost;
GRANT FILE on *.* TO pcwkb_db_admin@localhost;
```

Creating the database:

```SQL
CREATE DATABASE pcwkb_db;
```

Edit `settings.py` to add the database connection information as follows:

```python
DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'pcwkb_db',
         'USER': 'pcwkb_db_admin',
         'PASSWORD': 'password1',
         'HOST': '127.0.0.1',
         'PORT': '',
      }
   }
```

Once the database is created we can create the migration using:

```bash
python manage.py makemigrations
python manage.py check
python manage.py migrate
```