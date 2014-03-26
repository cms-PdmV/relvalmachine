from flask import jsonify
from flask.ext.restful import Resource
from relval.database.dao import PredefinedBlobsDao, StepsDao, RequestsDao

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


class BlobDetailsApi(Resource):

    def __init__(self):
        self.dao = PredefinedBlobsDao()

    def get(self, blob_id):
        details = self.dao.get_details(blob_id)
        return jsonify(
            details=details
        )


class StepDetailsApi(Resource):

    def __init__(self):
        self.dao = StepsDao()

    def get(self, step_id):
        details = self.dao.get_details(step_id)
        return jsonify(
            details=details
        )


class RequestDetailsApi(Resource):

    def __init__(self):
        self.dao = RequestsDao()

    def get(self, request_id):
        details = self.dao.get_details(request_id)
        return jsonify(
            details=details
        )