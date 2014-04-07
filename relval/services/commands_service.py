from relval.database.models import RequestStatus
from relval.services.log_manager import LogsManager

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from relval.services.ssh_service import SshService
from relval.database.dao import RequestsDao, StepsDao


class CommandsService(object):
    """ Service handles operations related to commands execution or creation
    """

    def __init__(self):
        self.env = Environment(loader=PackageLoader("relval", "/templates/bash"))
        self.request_dao = RequestsDao()
        self.steps_dao = StepsDao()
        self.ssh_service = SshService()
        self.log_manager = LogsManager()

    def get_test_command(self, request_id):
        request = self.request_dao.get(request_id)
        return self.__render_command(request)

    def submit_for_testing(self, request_id):
        request = self.request_dao.get(request_id)
        command = self.__render_command(request)

        try:
            logs, errors = self.ssh_service.execute(command)
        except:
            self.request_dao.update_status(request_id, RequestStatus.TestFailed)
            raise

        if len(errors) > 0:
            self.request_dao.update_status(request_id, RequestStatus.TestFailed)
            self.log_manager.save_testing_log(request.label, errors)
            raise Exception("Testing failed. More info in log files.")
        else:
            self.request_dao.update_status(request_id, RequestStatus.TestPassed)

        return True

    def __render_command(self, request):
        template = self.env.get_template('test_request.sh')

        steps = []
        for step in request.steps:
            step_details = self.steps_dao.get_details(step.id)
            step_details["events_num"] = 2
            steps.append(step_details)

        return template.render(dict(
            cmssw_release=request.cmssw_release,
            steps=steps))




