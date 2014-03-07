__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.utils

    utils for unit tests
"""

from relval.tests import factory
from relval.database.dao import PredefinedBlobsDao

blobs_dao = PredefinedBlobsDao()


def prepare_blob(title=None, parameters_count=1, immutable=False):
    blob = factory.predefined_blob(parameters_count)
    if title:
        blob.title = title
    parameters = factory.parameters(parameters_count)

    blobs_dao.add(blob.title, creation_date=blob.creation_date, immutable=immutable, parameters=parameters)
    return blob