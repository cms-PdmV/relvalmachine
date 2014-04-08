__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import logging
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="relval/templates")
app.config.from_object('relval.config')
db = SQLAlchemy(app)

###############################################################
# Logging configuration
###############################################################

if not os.path.exists("logs"):
    os.makedirs("logs")

# root logger
logging.root.setLevel(logging.INFO)


# sql alchemy logger setup
db_log_handler = logging.FileHandler("logs/database.log")
db_log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
sql_alchemy_logger = logging.getLogger('sqlalchemy.engine')
sql_alchemy_logger.setLevel(logging.INFO)
sql_alchemy_logger.addHandler(db_log_handler)


# relval custom logging (works only on production)
service_log_handler = logging.FileHandler("logs/service.log")
service_log_handler.setLevel(logging.DEBUG)
service_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(service_log_handler)


scheduler_logger = logging.getLogger("apscheduler")
scheduler_logger.addHandler(service_log_handler)

paramiko_logger = logging.getLogger("paramiko")
paramiko_logger.addHandler(service_log_handler)



import relval.views
import relval.rest
import relval.services
import relval.database.models

