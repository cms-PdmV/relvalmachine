__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from flask.ext.script import Manager, prompt_bool
from relval import app, db


manager = Manager(app)

@manager.command
def dropdb():
    "Drops all database tables. All data will be lost."
    if prompt_bool("Are you sure you want to drop tables and loose all Your data"):
        db.drop_all()

@manager.command
def createdb():
    "Creates all database tables"
    db.create_all()

if __name__ == "__main__":
    manager.run()