__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.dao_tests

    Unit tests for database layer
"""

from relval.tests.base import BaseTestsCase
from relval.database.dao import UsersDao, RequestsDao
from relval.database.models import Users, Requests, Revisions, Steps


class UsersDaoTests(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.users_dao = UsersDao()

        self.test_user = Users(
            user_name="TestUsername",
            email="test@mail",
            role="user",
            notifications=True)

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
        self.test_request = Requests(
            status="NEW",
            test_status="NOT-TESTED",
            priority=1,
            type="TYPE",
            cmssw_release="7_0_0",
            description="test description",
            log_url="test-log-url",
            event=100,
            user=Users(
                user_name="TestUsername",
                email="test@mail",
                role="user",
                notifications=True),
            revisions=[
                Revisions(
                    revision_number=1,
                    run_the_matrix_conf="-wm=init",
                    steps=[
                        Steps(
                            name="step1"
                        ),
                        Steps(
                            name="step2"
                        ),
                    ]
                )
            ]

        )

    def test_request_insertion(self):
        self.assertModelEmpty(Requests)
        self.request_dao.insertRequestObject(self.test_request)
        self.assertModelCount(Requests, 1)



