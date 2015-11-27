# omega
DB Management System

# deploy
## Install flask and gunicorn

Install the following software package:

```
pip install MySQL-python flask requests Flask-SQLAlchemy WTForms flask-login gunicorn
```

## Create database and user
To deply the omega, you should create database `omega` in a database like mysql:

```
mysql> create database omega character set utf8 collate utf8_general_ci;
mysql> create user 'omega'@'%' identified by 'omega_test';
mysql> grant all on omega.* to 'omega'@'%' identified by 'omega_test';
mysql> flush privileges;
```

## Modify config.py

Change the database name, user and password is right in the config.py
 
## Create omega tables

Runnig the command as follows:
```
# python
Python 2.7.10 (default, Nov 19 2015, 19:06:05)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from apps import db
>>> db.create_all()
```



