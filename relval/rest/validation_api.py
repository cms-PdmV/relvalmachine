from functools import wraps
from relval.database.dao import StepsDao, RequestsDao, PredefinedBlobsDao, BatchesDao
from relval.rest.utils import convert_keys_to_string

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


from flask.ext.restful import Resource
from flask import request, jsonify


def validation(func):
    @wraps(func)
    def validation_boilerplate(*args, **kwargs):
        data = convert_keys_to_string(request.json)
        if not data or "value" not in data:
            return {"error": "Bad request"}, 400
        try:
            func(*args, **kwargs)
        except Exception, e:
            return jsonify(
                valid=False,
                msg=e.message
            )

        return jsonify(
            valid=True
        )

    return validation_boilerplate


class StepsValidationApi(Resource):

    def __init__(self):
        self.dao = StepsDao()

    @validation
    def post(self, field):
        if field == "title":
            self.dao.validate_distinct_title(request.json["value"])


class RequestsValidationApi(Resource):

    def __init__(self):
        self.dao = RequestsDao()

    @validation
    def post(self, field):
        if field == "label":
            self.dao.validate_distinct_label(request.json["value"])


class BlobsValidationApi(Resource):

    def __init__(self):
        self.dao = PredefinedBlobsDao()

    @validation
    def post(self, field):
        if field == "title":
            self.dao.validate_distinct_title(request.json["value"])

class BatchesValidationApi(Resource):

    def __init__(self):
        self.dao = BatchesDao()

    @validation
    def post(self, field):
        if field == "title":
            self.dao.validate_distinct_title(request.json["value"])