#!/usr/bin/env python3
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.api.__init__ import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def init_db():
    os.system('createdb pickanddrop_db')
    os.system('createdb pdptesting_db')
    print('Databases created')


@manager.command
def drop_db():
    os.system(
        'psql -c "DROP DATABASE IF EXISTS pdptesting_db"')
    os.system(
        'psql -c "DROP DATABASE IF EXISTS pickanddrop_db"')
    print('Databases dropped')


if __name__ == '__main__':
    manager.run()
