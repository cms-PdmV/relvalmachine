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

        result = func(*args, **kwargs)
        return jsonify(
            valid=result
        )

    return validation_boilerplate


class StepsValidationApi(Resource):

    def __init__(self):
        self.dao = StepsDao()

    @validation
    def post(self, field):
        result = False
        if field == "title":
            result = self.dao.validate_distinct_title(request.json["value"])
        return result


class RequestsValidationApi(Resource):

    def __init__(self):
        self.dao = RequestsDao()

    @validation
    def post(self, field):
        result = False
        if field == "label":
            result = self.dao.validate_distinct_label(request.json["value"])

        return result


class BlobsValidationApi(Resource):

    def __init__(self):
        self.dao = PredefinedBlobsDao()

    @validation
    def post(self, field):
        result = False
        if field == "title":
            result = self.dao.validate_distinct_title(request.json["value"])

        return result

class BatchesValidationApi(Resource):

    def __init__(self):
        self.dao = BatchesDao()

    @validation
    def post(self, field):
        result = False
        if field == "title":
            result = self.dao.validate_distinct_title(request.json["value"])

        return result