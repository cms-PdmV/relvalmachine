from flask import jsonify
from flask.ext.restful import Resource
from relval.database.dao import PredefinedBlobsDao, StepsDao, RequestsDao, BatchesDao

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


class BaseDetailsApi(Resource):
    def __init__(self, dao):
        self.dao = dao

    def get(self, item_id):
        details = self.dao.get_details(item_id)
        return jsonify(
            details=details
        )


class BlobDetailsApi(BaseDetailsApi):
    def __init__(self):
        BaseDetailsApi.__init__(self, PredefinedBlobsDao())


class StepDetailsApi(BaseDetailsApi):
    def __init__(self):
        BaseDetailsApi.__init__(self, StepsDao())


class RequestDetailsApi(BaseDetailsApi):
    def __init__(self):
        BaseDetailsApi.__init__(self, RequestsDao())


class BatchDetailsApi(BaseDetailsApi):
    def __init__(self):
        BaseDetailsApi.__init__(self, BatchesDao())