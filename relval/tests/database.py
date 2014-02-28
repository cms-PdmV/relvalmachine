__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.dao_tests

    Unit tests for database layer
"""

from relval.tests import factory
from relval.tests.base import BaseTestsCase
from relval.database.dao import UsersDao, RequestsDao, RevisionsDao, PredefinedBlobsDao
from relval.database.models import Users, Requests, Parameters, PredefinedBlob


class UsersDaoTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.users_dao = UsersDao()
        self.test_user = factory.user()

    def test_single_user_insert(self):
        user = self.test_user
        self.assertModelEmpty(Users)
        self.users_dao.insertUser(user.user_name, user.email, user.role, user.notifications)
        self.assertModelCount(Users, 1)

        inserted_user = Users.query.one()
        self.assertUsers(user, inserted_user)

    def test_user_object_insert(self):
        self.assertModelEmpty(Users)
        self.users_dao.insertUserObject(self.test_user)
        self.assertModelCount(Users, 1)

    def test_get_user_by_id(self):
        self.users_dao.insertUserObject(self.test_user)
        # first element always has id=1
        retrieved_user = self.users_dao.get(1)
        self.assertUsers(self.test_user, retrieved_user)

    def assertUsers(self, expected, actual):
        self.assertEqual(expected.user_name, actual.user_name)
        self.assertEqual(expected.email, actual.email)
        self.assertEqual(expected.role, actual.role)
        self.assertEqual(expected.notifications, actual.notifications)


class RequestsDaoTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.request_dao = RequestsDao()
        self.test_request = factory.request()

    def test_request_insertion(self):
        self.assertModelEmpty(Requests)
        self.request_dao.insertRequestObject(self.test_request)
        self.assertModelCount(Requests, 1)


class RevisionsDaoTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.revision_dao = RevisionsDao()
        self.request_dao = RequestsDao()
        self.test_request = factory.request()

    def test_revision_append_to_request(self):
        self.request_dao.insertRequestObject(self.test_request)
        revision_to_append = factory.create_revision(rev_num=2)

        self.revision_dao.addRevisionToRequest(self.test_request.id, revision_to_append)

        self.assertModelCount(Requests, 1)
        revisions = Requests.query.one().revisions

        self.assertEqual(len(revisions), 2)
        self.assertEqual(revisions[0].revision_number, 1)
        self.assertEqual(revisions[1].revision_number, 2)


class PredefinedBlobsDaoTest(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.blobs_dao = PredefinedBlobsDao()

    def test_blob_insertion_with_multiple_params(self):
        self.blob_insertion_test(3)

    def test_blob_insertion_with_single_params(self):
        self.blob_insertion_test(1)

    def test_blob_deletion(self):
        self.prepare_blob(parameters_count=2)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 2)
        id = PredefinedBlob.query.one().id

        self.blobs_dao.delete(id)

        self.assertModelEmpty(PredefinedBlob)
        self.assertModelEmpty(Parameters)

    def test_blob_search_single_result(self):
        self.prepare_blob()
        self.prepare_blob("aa-search-this")

        result = self.blobs_dao.search_all("search")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "aa-search-this")

    def test_blob_search_multiple_result(self):
        self.prepare_blob()
        self.prepare_blob("search-aa-smt")
        self.prepare_blob("aa-search")

        result = self.blobs_dao.search_all("search")

        result.sort(key=lambda blob: blob.title)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "aa-search")
        self.assertEqual(result[1].title, "search-aa-smt")

    def blob_update_test(self):
        self.prepare_blob(parameters_count=2)
        id = PredefinedBlob.query.one().id

        new_title = "new-blob-title"
        new_parameters = factory.predefined_blob_paramters(3)

        self.blobs_dao.update(id=id, title=new_title, parameters=new_parameters)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 3)

        new_blob = PredefinedBlob.query.one()
        self.assertEqual(new_blob.title, new_title)

    def blob_insertion_test(self, params_num):
        self.assertModelEmpty(PredefinedBlob)
        blob = self.prepare_blob(parameters_count=params_num)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, params_num)

        actual_blob = PredefinedBlob.query.one()
        self.assertBlobs(blob, actual_blob)

    def prepare_blob(self, title=None, parameters_count=1):
        blob = factory.predefined_blob(parameters_count)
        if title:
            blob.title = title
        parameters = factory.predefined_blob_paramters(parameters_count)

        self.blobs_dao.add(blob.title, creation_date=blob.creation_date, parameters=parameters)
        return blob

    def assertBlobs(self, expected, actual):

        self.assertEqual(expected.title, actual.title)
        self.assertEqual(len(expected.parameters), len(actual.parameters))

        for expected_param, actual_param in zip(expected.parameters, actual.parameters):
            self.assertEqual(expected_param.flag, actual_param.flag)
            self.assertEqual(expected_param.value, actual_param.value)
