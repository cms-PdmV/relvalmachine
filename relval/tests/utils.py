__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.utils

    utils for unit tests
"""

from relval.tests import factory
from relval.database.dao import PredefinedBlobsDao, StepsDao, RequestsDao, BatchesDao
from relval.database.models import StepType, Steps

blobs_dao = PredefinedBlobsDao()
steps_dao = StepsDao()
requests_dao = RequestsDao()
batches_dao = BatchesDao()


def prepare_blob(title=None, parameters_count=1, immutable=False):
    blob = factory.predefined_blob(parameters_count)
    if title:
        blob.title = title
    parameters = factory.parameters(parameters_count)

    blobs_dao.add(blob.title, creation_date=blob.creation_date, immutable=immutable, parameters=parameters)
    return blob

def prepare_step(title=None, parameters_count=1, blobs_count=1,
                 immutable=False, type=StepType.Default, data_set=""):

    step = factory.step(title=title, parameters_count=parameters_count, blobs_count=blobs_count,
                        immutable=immutable, type=type, data_set=data_set)

    parameters = factory.parameters(parameters_count)

    steps_dao.add(title=step.title,
                  immutable=immutable,
                  type=type,
                  data_set=data_set,
                  parameters=parameters)
    return step


def prepare_request(label="test-label", description="desc", immutable=False,
                    cmssw_release="7_0_0", run_the_matrix_conf="-i -all",
                    events=20, priority=3, type="mc", steps_count=1, step_title="title"):

    for i in range(steps_count):
        prepare_step(title="%s-%d" % (step_title, i))
    steps = [{"id": step.id} for step in Steps.query.all()]

    req = requests_dao.add(label=label, description=description, immutable=immutable,
                           cmssw_release=cmssw_release, run_the_matrix_conf=run_the_matrix_conf,
                           events=events, priority=priority, type=type, steps=steps)

    return req


def prepare_batch(title="test-title", description="desc", immutable=False,
                  run_the_matrix_conf=None, priority=None, requests_count=1):

    for i in range(requests_count):
        prepare_request(label="label-%d" % i, run_the_matrix_conf=run_the_matrix_conf, priority=priority, step_title="step-%d" % i)
    requests = [{"id": request.id} for request in Steps.query.all()]

    batch = batches_dao.add(title=title, description=description, immutable=immutable,
                            run_the_matrix_conf=run_the_matrix_conf, priority=priority, requests=requests)
    return batch