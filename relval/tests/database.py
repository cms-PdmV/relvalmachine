__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.dao_tests

    Unit tests for database layer
"""

from relval.tests import factory
from relval.tests.base import BaseTestsCase
from relval.database.dao import UsersDao, RequestsDao, RevisionsDao
from relval.database.models import Users, Requests, Revisions, Steps


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



