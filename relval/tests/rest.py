__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"


""" relval.tests.rest

    Unit tests for relval machine rest methods
"""

from relval.tests.base import BaseTestsCase
from relval.tests import factory
from relval.database.dao import PredefinedBlobsDao, StepsDao, RequestsDao
from relval.database.models import StepType

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

            self.assertEqual(len(data['items']), 3)
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

            self.assertEqual(len(data['items']), 2)
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
            self.assertEqual(len(data['items']), 1)
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
            self.assertEqual(len(data['items']), 3)
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
                immutable=False,
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
                immutable=True,
                parameters=request["parameters"])


class StepsRestTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)

    def test_new_step_creation(self):
        with patch.object(StepsDao, "add") as mock_method:
            request = factory.JSONRequests.new_step()
            response = self.app.post(
                "/api/steps",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                title=request["title"],
                immutable=True,
                parameters=request["parameters"],
                blobs=request["blobs"],
                type=StepType.Default,
                data_set="test-data-set")

    def test_step_fetch_paginating(self):
        steps = []
        for _ in range(2):
            steps.append(factory.step())
        page = Pagination(None, None, None, 3, steps)

        with patch.object(StepsDao, "get_paginated") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/steps?page_num=1&items_per_page=2")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)

            self.assertEqual(len(data['items']), 2)
            self.assertEqual(data['total'], "3")
            mock_method.assert_called_once_with(page_num=1, items_per_page=2)

    def test_step_search(self):
        step = [factory.step(3)]
        page = Pagination(None, None, None, 1, step)

        with patch.object(StepsDao, "search_all") as mock_method:
            mock_method.return_value = page
            response = self.app.get("/api/steps?search=query&pagu_num=1&items_per_page=10")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data['items']), 1)
            self.assertEqual(data['total'], "1")
            mock_method.assert_called_once_with(query="query", page_num=1, items_per_page=10)

    def test_single_step_fetch(self):
        step = factory.step()
        step.id = 1
        with patch.object(StepsDao, "get") as mock_method:
            mock_method.return_value = step
            response = self.app.get("/api/steps/1")

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)

            self.assertEqual(data['title'], step.title)
            mock_method.assert_called_once_with(1)

    def test_step_update(self):
        with patch.object(StepsDao, "update") as mock_method:
            request = factory.JSONRequests.update_step()
            response = self.app.put(
                "/api/steps/3",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                3,
                title=request["title"],
                immutable=request["immutable"],
                parameters=request["parameters"],
                blobs=request["blobs"],
                data_set=request["data_set"],
                type=request["type"])

class RequestRestTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)

    def test_new_step_creation(self):
        with patch.object(RequestsDao, "add") as mock_method:
            request = factory.JSONRequests.new_request()
            response = self.app.post(
                "/api/requests",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                label=request["label"],
                immutable=True,
                steps=request["steps"],
                description=request["description"],
                type=request["type"],
                cmssw_release=request["cmssw_release"],
                run_the_matrix_conf=request["run_the_matrix_conf"],
                events=request["events"],
                priority=request["priority"])

    def test_request_update(self):
        with patch.object(RequestsDao, "update") as mock_method:
            request = factory.JSONRequests.new_request()
            response = self.app.put(
                "/api/requests/3",
                data=json.dumps(request),
                content_type='application/json')

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(
                3,
                label=request["label"],
                immutable=True,
                steps=request["steps"],
                description=request["description"],
                type=request["type"],
                cmssw_release=request["cmssw_release"],
                run_the_matrix_conf=request["run_the_matrix_conf"],
                events=request["events"],
                priority=request["priority"])

    def test_request_delete(self):
        with patch.object(RequestsDao, "delete") as mock_method:
            response = self.app.delete("/api/requests/1")

            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(1)


class DetailsApiTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)

    def test_blob_details_fetch(self):
        with patch.object(PredefinedBlobsDao, "get_details") as mock_method:
            mock_method.return_value = "--flag value"
            response = self.app.get("/api/predefined_blob/2/details")
            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(2)
            data = json.loads(response.data)
            self.assertEqual(data["details"], "--flag value")

    def test_step_details_fetch(self):
        with patch.object(StepsDao, "get_details") as mock_method:
            mock_method.return_value = "--flag value"
            response = self.app.get("/api/steps/5/details")
            self.assertEqual(response.status_code, 200)
            mock_method.assert_called_once_with(5)
            data = json.loads(response.data)
            self.assertEqual(data["details"], "--flag value")
