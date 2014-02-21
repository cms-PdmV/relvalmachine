__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.drop

    Script for dropping database.
    cd into app root folder and run
    `python relval/database/drop.py`
"""

from relval import db

db.drop_all()