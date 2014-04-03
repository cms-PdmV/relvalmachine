from flask.wrappers import Response
from relval.services.commands_service import CommandsService

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from flask.ext.restful import Resource
from functools import wraps


def returns_plain_text(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/plain')
    return decorated_function


def handle_exception(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
            return r
        except Exception as ex:
            return {"error": str(ex)}, 500
    return decorated_function


class RequestCommandApi(Resource):
    def __init__(self):
        self.service = CommandsService()

    @returns_plain_text
    def get(self, request_id):
        return self.service.get_test_command(request_id)

    @handle_exception
    def post(self, request_id):
        self.service.submit_for_testing(request_id)