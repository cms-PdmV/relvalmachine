__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


from relval.services.runTheMatrix_integration import ConfigurationPreparationService
from relval.services.concurrent_executor import SubmitForTestingTask
from relval.services import tasks_executor
from relval import app
from relval.services.commands_service import CommandsService
from flask.ext.restful import Resource
from flask.wrappers import Response
from flask import jsonify
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
            app.logger.error("Error occurred: " + str(ex))
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
        task = SubmitForTestingTask(request_id)
        tasks_executor.add_task(task)


class RequestLogsCommandApi(Resource):

    def __init__(self):
        self.service = CommandsService()

    @returns_plain_text
    def get(self, request_id):
        return self.service.get_logs(request_id)


class RunTheMatrixConfigurationApi(Resource):
    """ Endpoint to fetch json configuration for runTheMatrix
    """

    def __init__(self):
        self.service = ConfigurationPreparationService()

    def get(self, request_id):
        return jsonify(
            self.service.prepare_configuration(request_id)
        )