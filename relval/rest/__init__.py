__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

# Set up rest service for sqlalchemy
from flask.ext.restless import APIManager
from datetime import datetime

from relval import app, db
from relval.database.models import PredefinedBlob


restless_manager = APIManager(app, flask_sqlalchemy_db=db)


#TODO: move to another module
def post_predefined_blob(data=None):
    if isinstance(data, dict):
        data['creation_date'] = datetime.now().isoformat()


# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
restless_manager.create_api(
    PredefinedBlob,
    methods=['GET', 'POST', 'DELETE'],
    preprocessors={
        'POST': [post_predefined_blob]
    })