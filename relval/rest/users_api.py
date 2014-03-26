__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval.services.users_service import UsersManagementService
from flask.ext.restful import Resource
from flask.globals import request
from flask import jsonify


class UsersResource(Resource):

    def __init__(self):
        self.users_service = UsersManagementService()

    def get(self, field):
        headers = request.headers
        if field == "username":
            result = self.users_service.get_username(headers)
        elif field == "email":
            result = self.users_service.get_email(headers)
        return jsonify(
            result=result
        )