__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


from relval import app
from relval.rest.api import \
    UsersListApi, PredefinedBlobsApi, PredefinedBlobApi,\
    StepsApi, StepApi, RequestsApi, \
    RequestApi, BatchesApi, BatchApi
from relval.rest.validation_api import \
    StepsValidationApi, RequestsValidationApi
from flask.ext.restful import Api


restful_api = Api(app)
restful_api.add_resource(UsersListApi, "/api/users")
restful_api.add_resource(PredefinedBlobsApi, "/api/predefined_blob")
restful_api.add_resource(PredefinedBlobApi, "/api/predefined_blob/<int:blob_id>")
restful_api.add_resource(StepsApi, "/api/steps")
restful_api.add_resource(StepApi, "/api/steps/<int:step_id>")
restful_api.add_resource(RequestsApi, "/api/requests")
restful_api.add_resource(RequestApi, "/api/requests/<int:request_id>")
restful_api.add_resource(BatchesApi, "/api/batches")
restful_api.add_resource(BatchApi, "/api/batches/<int:batch_id>")

# validation
restful_api.add_resource(StepsValidationApi, "/api/validate/step/<field>")
restful_api.add_resource(RequestsValidationApi, "/api/validate/request/<field>")



