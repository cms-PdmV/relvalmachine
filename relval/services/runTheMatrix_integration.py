__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval.database.dao import RequestsDao, StepsDao
from relval.database.models import StepType


class DictWithoutNone(dict):
    def __setitem__(self, key, value):
        if value is not None:
            dict.__setitem__(self, key, value)


class ConfigurationPreparationService(object):

    def __init__(self):
        self.requests_dao = RequestsDao()
        self.steps_dao = StepsDao()

    def prepare_configuration(self, request_id):
        """ Prepares configuration for run the matrix.
            Return python dictionary
        """

        request = self.requests_dao.get(request_id)
        if not request:
            raise Exception("No request exists with given id={0}".format(request_id))
        configuration = dict()

        configuration["label"] = request.label
        steps = dict()

        print [(assoc.sequence_number, assoc.step.title) for assoc in self.requests_dao.get_steps_sorted(request)]

        for step_assoc in self.requests_dao.get_steps_sorted(request):
            step = step_assoc.step
            conf_step = dict()
            conf_step["name"] = step.name
            conf_step["sequence_number"] = step_assoc.sequence_number

            if step.type == StepType.Default:
                conf_step["parameters"] = self.construct_parameters(step)
            elif step.type == StepType.FirstData:
                conf_step["inputInfo"] = self.construct_data_step(step)
            else:
                # first mc step can have parameters or data_step

                ## if has any steps of blobs
                blobs = step.predefined_blobs
                if (step.parameters and len(step.parameters) > 0) or \
                        (blobs and blobs.parameters and len(blobs.parameters) > 0):

                    conf_step["parameters"] = self.construct_parameters(step)
                else:  # otherwise
                    conf_step["inputInfo"] = self.construct_data_step(step)

            steps[step.title] = conf_step

        configuration["steps"] = steps

        return configuration

    def construct_parameters(self, step):
        parameters = dict()
        for param in step.parameters:
            parameters[param.flag] = param.value
        for blob in step.predefined_blobs:
            for param in blob.parameters:
                parameters[param.flag] = param.value
        return parameters

    def construct_data_step(self, step):
        info = DictWithoutNone()
        data_step = step.data_step
        info["dataSet"] = data_step.data_set
        info["label"] = data_step.label
        info["files"] = data_step.files
        info["events"] = data_step.events
        info["split"] = data_step.split
        info["location"] = data_step.location
        info["ib_blacklist"] = data_step.ib_blacklist
        info["ib_block"] = data_step.ib_block

        info["run"] = "1234,53432,6534 ,   6534, 524"
        # info["run"] = data_step.run  # should be numbers separated by comma
        return info



