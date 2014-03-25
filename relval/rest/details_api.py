from flask import jsonify
from flask.ext.restful import Resource
from relval.database.dao import PredefinedBlobsDao

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