__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.create

    Script for creating database from scratch.
    cd into app root folder and run
    `python relval/database/create.py`
"""

from relval import db

db.create_all()

