__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.dao_tests

    Unit tests for database layer
"""

from relval.tests import factory
from relval.tests import utils
from relval.tests.base import BaseTestsCase
from relval.database.dao import UsersDao, RequestsDao, RevisionsDao, PredefinedBlobsDao, StepsDao
from relval.database.models import Users, Requests, Parameters, PredefinedBlob, Steps, StepType


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
        utils.prepare_blob(parameters_count=2)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 2)
        id = PredefinedBlob.query.one().id

        self.blobs_dao.delete(id)

        self.assertModelEmpty(PredefinedBlob)
        self.assertModelEmpty(Parameters)

    def test_blob_search_single_result(self):
        utils.prepare_blob()
        utils.prepare_blob("aa-search-this")

        result = self.blobs_dao.search_all("search", 1, 10)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].title, "aa-search-this")

    def test_blob_search_multiple_result(self):
        utils.prepare_blob()
        utils.prepare_blob("search-aa-smt")
        utils.prepare_blob("aa-search")

        result = self.blobs_dao.search_all("search", 1, 10)

        result.items.sort(key=lambda blob: blob.title)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0].title, "aa-search")
        self.assertEqual(result.items[1].title, "search-aa-smt")

    def test_blob_paginated_fetch_single(self):
        for i in range(3):
            utils.prepare_blob("title%d" % i)

        result = self.blobs_dao.get_paginated(1, 1)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.total, 3)
        self.assertEqual(result.items[0].title, "title0")
        # assert that we not changed model
        self.assertModelCount(PredefinedBlob, 3)

    def test_blob_paginated_fetch_multiple(self):
        for i in range(10):
            utils.prepare_blob("title%d" % i)

        result = self.blobs_dao.get_paginated(2, 3)

        self.assertEqual(len(result.items), 3)
        for i in range(3):
            # "title3", "title4", "title5"
            self.assertEqual(result.items[i].title, "title%d" % (i+3))

    def test_blob_paginated_fetch_last_incomplete(self):
        for i in range(10):
            utils.prepare_blob("title%d" % i)

        result = self.blobs_dao.get_paginated(4, 3)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].title, "title9")

    def test_blob_update(self):
        utils.prepare_blob(parameters_count=2)
        id = PredefinedBlob.query.one().id

        new_title = "new-blob-title"
        new_parameters = factory.parameters(3)

        self.blobs_dao.update(id=id, title=new_title, parameters=new_parameters)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 3)

        new_blob = PredefinedBlob.query.one()
        self.assertEqual(new_blob.title, new_title)

    def test_immutable_blob_update(self):
        utils.prepare_blob(parameters_count=2, immutable=True)
        id = PredefinedBlob.query.one().id

        self.assertRaises(Exception, self.blobs_dao.update, id=id)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, 2)

    def blob_insertion_test(self, params_num):
        self.assertModelEmpty(PredefinedBlob)
        blob = utils.prepare_blob(parameters_count=params_num)

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Parameters, params_num)

        actual_blob = PredefinedBlob.query.one()
        self.assertBlobs(blob, actual_blob)

    def assertBlobs(self, expected, actual):

        self.assertEqual(expected.title, actual.title)
        self.assertEqual(len(expected.parameters), len(actual.parameters))

        for expected_param, actual_param in zip(expected.parameters, actual.parameters):
            self.assertEqual(expected_param.flag, actual_param.flag)
            self.assertEqual(expected_param.value, actual_param.value)


class StepsDaoTest(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.steps_dao = StepsDao()

    def test_step_insertion_without_blobs(self):
        self.assertModelEmpty(PredefinedBlob)
        self.assertModelEmpty(Steps)

        self.steps_dao.add(title="step", immutable=False, type=StepType.Default,
                           parameters=factory.parameters(2))

        self.assertModelCount(PredefinedBlob, 0)
        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 2)

        step = Steps.query.one()

        self.assertEqual(step.title, "step")
        self.assertEqual(step.immutable, False)
        self.assertEqual(step.type, StepType.Default)
        self.assertEqual(step.predefined_blobs, [])

    def test_step_montecarlo_step_insertion(self):
        self.steps_dao.add(title="step",
                           immutable=False,
                           type=StepType.Default,
                           parameters=factory.parameters(2),
                           data_set="data_set")

        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 2)

        step = Steps.query.one()
        self.assertEqual(step.title, "step")
        self.assertEqual(step.type, StepType.Default)
        self.assertEqual(len(step.parameters), 2)
        # should not insert those fields because is_monte_carlo = true
        self.assertEqual(step.data_set, None)

    def test_step_step1_mc_insertion(self):
        utils.prepare_blob()
        blob = PredefinedBlob.query.one()
        self.steps_dao.add(title="step",
                           immutable=False,
                           type=StepType.FirstMc,
                           parameters=factory.parameters(2),
                           blobs=[{"id": blob.id}],
                           data_set="data_set")

        self.assertModelCount(Steps, 1)

        step = Steps.query.one()
        self.assertEqual(step.title, "step")
        self.assertEqual(step.type, StepType.FirstMc)
        self.assertEqual(len(step.parameters), 2)
        self.assertEqual(len(step.predefined_blobs), 1)
        # should not insert those fields because is_monte_carlo = true
        self.assertEqual(step.data_set, "data_set")

    def test_step_insertion_without_parameters(self):
        utils.prepare_blob()
        id = PredefinedBlob.query.one().id

        self.steps_dao.add(title="step", immutable=False, type=StepType.Default, blobs=[{"id": id}])

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 1) # blob creates parameters

        step = Steps.query.one()
        self.assertEqual(step.parameters, [])

    def test_step_paginated_fetch_single(self):
        for i in range(3):
            utils.prepare_step(title="title%d" % i)

        result = self.steps_dao.get_paginated(1, 1)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.total, 3)
        self.assertEqual(result.items[0].title, "title0")
        # assert that we not changed model
        self.assertModelCount(Steps, 3)

    def test_steps_paginated_fetch_multiple(self):
        for i in range(10):
            utils.prepare_step(title="title%d" % i)

        result = self.steps_dao.get_paginated(2, 3)

        self.assertEqual(len(result.items), 3)
        for i in range(3):
            # "title3", "title4", "title5"
            self.assertEqual(result.items[i].title, "title%d" % (i+3))

    def test_step_search_single_result(self):
        utils.prepare_step(title="aa-search")
        utils.prepare_blob(title="title")

        result = self.steps_dao.search_all("search", 1, 10)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].title, "aa-search")

    def test_search_search_multiple_result(self):
        utils.prepare_step()
        utils.prepare_step(title="search-aa-smt")
        utils.prepare_step(title="aa-search")

        result = self.steps_dao.search_all("search", 1, 10)

        result.items.sort(key=lambda step: step.title)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0].title, "aa-search")
        self.assertEqual(result.items[1].title, "search-aa-smt")

    def test_monte_carlo_step_update(self):
        utils.prepare_step(title="step-title", parameters_count=3, type=StepType.FirstMc,
                           data_set="data_set")
        utils.prepare_blob()
        blob_id = PredefinedBlob.query.one().id
        id = Steps.query.one().id

        new_title = "new-step-title"
        new_parameters = factory.parameters(5)

        self.steps_dao.update(id=id, title=new_title, parameters=new_parameters,
                              type=StepType.Default, blobs=[{"id": blob_id}])

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 6)  # 5 from updated step and 1 from blob

        new_step = Steps.query.one()
        self.assertEqual(new_step.title, new_title)
        self.assertEqual(new_step.type, StepType.Default)
        self.assertEqual(len(new_step.predefined_blobs), 1)
        self.assertEqual(len(new_step.parameters), 5)

    def test_step_1_mc_step_update(self):
        utils.prepare_step(title="step-title", parameters_count=3, type=StepType.Default)
        utils.prepare_blob()
        blob_id = PredefinedBlob.query.one().id
        id = Steps.query.one().id

        new_title = "new-step-title"
        new_parameters = factory.parameters(4)

        self.steps_dao.update(id=id, title=new_title, data_set="data_set", parameters=new_parameters,
                              type=StepType.FirstMc, blobs=[{"id": blob_id}])

        self.assertModelCount(PredefinedBlob, 1)
        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 5)  # 4 from updated step and 1 from blob

        new_step = Steps.query.one()
        self.assertEqual(new_step.title, new_title)
        self.assertEqual(new_step.data_set, "data_set")
        self.assertEqual(new_step.type, StepType.FirstMc)
        self.assertEqual(len(new_step.predefined_blobs), 1)
        self.assertEqual(len(new_step.parameters), 4)