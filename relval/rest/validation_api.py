from relval.database.dao import StepsDao
from relval.rest.utils import convert_keys_to_string

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


from flask.ext.restful import Resource, marshal_with, reqparse
from flask import request, jsonify


class BaseValidationApi(object):

    def __init__(self):
        pass


class StepsValidationApi(Resource):

    def __init__(self):
        self.dao = StepsDao()

    def post(self, field):
        data = convert_keys_to_string(request.json)

        if not data or "value" not in data:
            return {"error": "Bad request"}, 400

        result = False

        if field == "title":
            result = self.dao.validate_distinct_title(data["value"])

        return jsonify(
            valid=result
        )