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
from flask_sqlalchemy import Pagination
from mock import patch


class PredefinedBlobsRestTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.blobs_dao = PredefinedBlobsDao()

    def test_blob_fetch(self):
        blobs = []
        for _ in range(3):
            blobs.append(factory.predefined_blob(3))
        page = Pagination(None, None, None, 3, blobs)

        with patch.object(PredefinedBlobsDao, "get_paginated") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/predefined_blob")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)

            self.assertEqual(len(data['blobs']), 3)
            self.assertEqual(data['total'], "3")
            mock_method.assert_called_once_with(page_num=1, items_per_page=3)  # default items per page

    def test_blob_fetch_paginating(self):
        blobs = []
        for _ in range(2):
            blobs.append(factory.predefined_blob(3))
        page = Pagination(None, None, None, 2, blobs)

        with patch.object(PredefinedBlobsDao, "get_paginated") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/predefined_blob?page_num=1&items_per_page=2")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)

            self.assertEqual(len(data['blobs']), 2)
            self.assertEqual(data['total'], "2")
            mock_method.assert_called_once_with(page_num=1, items_per_page=2)

    def test_blob_search(self):
        blobs = [factory.predefined_blob(3)]
        page = Pagination(None, None, None, 1, blobs)

        with patch.object(PredefinedBlobsDao, "search_all") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/predefined_blob?search=query")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data['blobs']), 1)
            self.assertEqual(data['total'], "1")
            mock_method.assert_called_once_with(query="query", page_num=1, items_per_page=3)

    def test_blob_search_with_pagination_params(self):
        blobs = []
        for _ in range(3):
            blobs.append(factory.predefined_blob(3))
        page = Pagination(None, None, None, 6, blobs)

        with patch.object(PredefinedBlobsDao, "search_all") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/predefined_blob?search=query&page_num=2&items_per_page=3")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data['blobs']), 3)
            self.assertEqual(data['total'], "6")
            mock_method.assert_called_once_with(query="query", page_num=2, items_per_page=3)

    def test_new_blob_creation(self):
        with patch.object(PredefinedBlobsDao, "add") as mock_method:
            request = factory.JSONRequests.new_blob()
            response = self.app.post(
                "/api/predefined_blob",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                title=request["title"],
                parameters=request["parameters"])

    def test_blob_deletion(self):
        with patch.object(PredefinedBlobsDao, "delete") as mock_method:
            response = self.app.delete("/api/predefined_blob/1")

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(1)

    def test_blob_update(self):
        with patch.object(PredefinedBlobsDao, "update") as mock_method:
            request = factory.JSONRequests.update_blob()
            response = self.app.put(
                "/api/predefined_blob/3",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                id=3,
                title=request["title"],
                parameters=request["parameters"])


