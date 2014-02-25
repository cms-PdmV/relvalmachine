__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


""" relval.tests.rest

    Unit tests for relval machine rest methods
"""

from relval.tests.base import BaseTestsCase
from relval.tests import factory
from relval.database.dao import PredefinedBlobsDao
from relval.database.models import PredefinedBlob, Parameters

import json


class PredefinedBlobsRestTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.blobs_dao = PredefinedBlobsDao()

    def test_blob_fetch(self):
        for _ in range(3):
            blob = factory.predefined_blob(3)
            self.blobs_dao.add(title=blob.title,
                               parameters=factory.predefined_blob_paramters(3))
        response = self.app.get("/api/predefined_blob")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertModelCount(PredefinedBlob, 3)
        self.assertEqual(len(data), 3)

    def test_new_blob_creation(self):
        self.assertModelEmpty(PredefinedBlob)

        response = self.app.post(
            "/api/predefined_blob",
            data=json.dumps(factory.JSONRequests.new_blob()),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 2)