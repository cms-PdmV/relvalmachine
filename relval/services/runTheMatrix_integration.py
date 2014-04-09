from relval.database.dao import RequestsDao, StepsDao
from relval.database.models import StepType

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


class ConfigurationPreparationService(object):

    def __init__(self):
        self.requests_dao = RequestsDao()
        self.steps_dao = StepsDao()

    def prepare_configuration(self, request_id):
        """ Prepares configuration for run the matrix.
            Return python dictionary
        """

        request = self.requests_dao.get(request_id)
        configuration = dict()

        configuration["label"] = request.label
        steps = dict()

        for step in request.steps:
            conf_step = dict()

            if step.type == StepType.Default:
                parameters = dict()
                for param in step.parameters:
                    parameters[param.flag] = param.value

                conf_step["parameters"] = parameters
            else:
                info = dict()
                data_step = step.data_step
                info["data_set"] = data_step.data_set
                info["label"] = data_step.label
                info["run"] = data_step.run
                info["ib_block"] = data_step.ib_block
                info["ib_blacklist"] = data_step.ib_blacklist
                info["files"] = data_step.files
                info["data_set"] = data_step.data_set
                info["events"] = data_step.split
                info["data_set"] = data_step.location


                conf_step["INFO"] = info

            steps[step.title] = conf_step

        configuration["steps"] = steps

        return configuration

