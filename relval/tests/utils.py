__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.utils

    utils for unit tests
"""

from relval.tests import factory
from relval.database.dao import PredefinedBlobsDao, StepsDao

blobs_dao = PredefinedBlobsDao()
steps_dao = StepsDao()


def prepare_blob(title=None, parameters_count=1, immutable=False):
    blob = factory.predefined_blob(parameters_count)
    if title:
        blob.title = title
    parameters = factory.parameters(parameters_count)

    blobs_dao.add(blob.title, creation_date=blob.creation_date, immutable=immutable, parameters=parameters)
    return blob

def prepare_step(title=None, parameters_count=1, blobs_count=1,
                 immutable=False, is_monte_carlo=True, data_set="", run_lumi=""):

    step = factory.step(title=title, parameters_count=parameters_count, blobs_count=blobs_count,
                        immutable=immutable, is_monte_carlo=is_monte_carlo, data_set=data_set,
                        run_lumi=run_lumi)

    parameters = factory.parameters(parameters_count)

    steps_dao.add(title=step.title,
                  immutable=immutable,
                  is_monte_carlo=is_monte_carlo,
                  data_set=data_set,
                  run_lumi=run_lumi,
                  parameters=parameters)
    return step