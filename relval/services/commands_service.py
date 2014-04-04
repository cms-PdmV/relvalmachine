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

    def get_test_command(self, request_id):
        request = self.request_dao.get(request_id)
        return self.__render_command(request)

    def submit_for_testing(self, request_id):
        request = self.request_dao.get(request_id)
        command = self.__render_command(request)

        logs, errors = self.ssh_service.execute(command)

        if len(errors) > 0:
            raise Exception("Testing failed. More info in log files.")

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




