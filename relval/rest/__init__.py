__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


from relval import app
from relval.rest.api import \
    UsersListApi,\
    PredefinedBlobsApi,\
    PredefinedBlobApi,\
    StepsApi,\
    StepApi

from flask.ext.restful import Api


restful_api = Api(app)
restful_api.add_resource(UsersListApi, "/api/users")
restful_api.add_resource(PredefinedBlobsApi, "/api/predefined_blob")
restful_api.add_resource(PredefinedBlobApi, "/api/predefined_blob/<int:blob_id>")
restful_api.add_resource(StepsApi, "/api/steps")
restful_api.add_resource(StepApi, "/api/steps/<int:blob_id>")



