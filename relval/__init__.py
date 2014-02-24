__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="relval/templates")
app.config.from_object('relval.config')
db = SQLAlchemy(app)

import relval.views
import relval.rest
import relval.database.models
