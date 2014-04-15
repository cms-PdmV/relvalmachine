__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from relval.database.dao import RequestsDao, StepsDao
from relval.database.models import RequestStatus
from relval.services.log_manager import LogsManager
from relval.services.ssh_service import SshService
from runTheMatrix_integration import ConfigurationPreparationService
from relval import app
import os
import json


class CommandsService(object):
    """ Service handles operations related to commands execution or creation
    """

    def __init__(self):
        self.env = Environment(loader=PackageLoader("relval", "/templates/bash"))
        self.request_dao = RequestsDao()
        self.ssh_service = SshService()
        self.log_manager = LogsManager()
        self.config_preparation = ConfigurationPreparationService()

    def get_test_command(self, request_id):
        request = self.request_dao.get(request_id)
        return self.__render_test_command(request)

    def submit_for_testing(self, request_id):
        request = self.request_dao.get(request_id)
        command = self.__render_test_command(request)

        json_data_dir = os.path.join(self.__get_testing_directory(request), "json_data")
        json_file = "{0}.json".format(request_id)

        try:
            self.ssh_service.connect_to_server()
            data_to_upload = json.dumps(self.config_preparation.prepare_configuration(request.id))
            self.ssh_service.upload_file_to_server(json_data_dir, json_file, data_to_upload)

            logs, errors = self.ssh_service.execute(command)
        except:
            app.logger.error("Request id={0} testing failed with technical error".format(request_id))
            self.request_dao.update_status(request_id, RequestStatus.TestFailed)
            raise

        if len(errors) > 0:
            app.logger.error("Request id={0} testing failed".format(request_id))
            self.request_dao.update_status(request_id, RequestStatus.TestFailed)
            self.log_manager.save_testing_log(request.label, errors, logs, self.__get_subdir(request))
            raise Exception("Testing failed. More info in log files.")
        else:
            self.log_manager.save_testing_log(request.label, None, logs, self.__get_subdir(request))
            app.logger.info("Request id={0} testing passed".format(request_id))
            self.request_dao.update_status(request_id, RequestStatus.TestPassed)

        return True

    def get_logs(self, request_id):
        request = self.request_dao.get(request_id)
        return self.log_manager.get_logs(request.label, self.__get_subdir(request))

    def __render_test_command(self, request):
        template = self.env.get_template('test_request.sh')
        directory = self.__get_testing_directory(request)

        params = dict(
            cmssw_release=request.cmssw_release,
            directory=directory)

        if request.run_the_matrix_conf:
            params["run_the_matrix_conf"] = request.run_the_matrix_conf
        # TODO: just temporary. Remove this
        else:
            params["run_the_matrix_conf"] = "--what machine -n -e"

        return template.render(params)

    def __get_testing_directory(self, request):
        return os.path.join(app.config["TESTS_DIR"], self.__get_subdir(request))

    def __get_subdir(self, request):
        return "{0}_{1}".format(request.cmssw_release, request.id)




