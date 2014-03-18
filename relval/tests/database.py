__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.tests.dao_tests

    Unit tests for database layer
"""

from relval.tests import factory
from relval.tests import utils
from relval.tests.base import BaseTestsCase
from relval.database.dao import UsersDao, RequestsDao, PredefinedBlobsDao, StepsDao, BatchesDao
from relval.database.models import Users, Requests, Parameters, PredefinedBlob, Steps, StepType, DataStep, Batches


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

    def test_request_insertion(self):
        self.assertModelEmpty(Requests)
        self.assertModelEmpty(Steps)

        utils.prepare_step()
        utils.prepare_step()
        steps = [{"id": step.id} for step in Steps.query.all()]

        self.request_dao.add(label="test-title", description="desc", immutable=False, cmssw_release="7_0_0",
                             run_the_matrix_conf="-l -i", events=20, priority=3, steps=steps)
        self.assertModelCount(Steps, 2)
        self.assertModelCount(Requests, 1)

        request = Requests.query.one()

        self.assertEqual(request.label, "test-title")
        self.assertEqual(request.immutable, False)
        self.assertEqual(request.description, "desc")
        self.assertEqual(request.cmssw_release, "7_0_0")
        self.assertEqual(request.events, 20)
        self.assertEqual(request.priority, 3)
        self.assertEqual(request.run_the_matrix_conf, "-l -i")
        self.assertEqual(len(request.steps), 2)

    def test_request_update(self):
        utils.prepare_request(label="label", description="desc", steps_count=2)
        id = Requests.query.one().id

        utils.prepare_step()
        steps = [{"id": step.id} for step in Steps.query.all()]

        new_label = "new-req-label"
        new_desc = "new-description"

        self.request_dao.update(id=id, label=new_label, description=new_desc, steps=steps)

        self.assertModelCount(Requests, 1)
        self.assertModelCount(Steps, 3)

        new_request = Requests.query.one()
        self.assertEqual(new_request.label, new_label)
        self.assertEqual(new_request.description, new_desc)
        self.assertEqual(len(new_request.steps), 3)

    def test_request_search(self):
        utils.prepare_request(label="label")
        utils.prepare_request(label="search-label")

        result = self.request_dao.search_all("search", 1, 10)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].label, "search-label")

    def test_request_paginated_fetch(self):
        for i in range(3):
            utils.prepare_request(label="title%d" % i)

        result = self.request_dao.get_paginated(1, 1)

        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.total, 3)
        self.assertEqual(result.items[0].label, "title0")
        self.assertModelCount(Requests, 3)

    def test_request_delete(self):
        utils.prepare_request(steps_count=2)

        self.assertModelCount(Requests, 1)
        self.assertModelCount(Steps, 2)
        id = Requests.query.one().id

        self.request_dao.delete(id)

        self.assertModelEmpty(Requests)
        self.assertModelCount(Steps, 2)

    def test_request_clone(self):
        req = utils.prepare_request(steps_count=2)
        self.assertModelCount(Requests, 1)

        new_req = self.request_dao.clone(req, "new-lbl", run_the_matrix_conf="new-conf", priority=1)

        self.assertModelCount(Requests, 2)
        self.assertEqual(new_req.label, "new-lbl")
        self.assertEqual(new_req.run_the_matrix_conf, "new-conf")
        self.assertEqual(new_req.priority, 1)
        self.assertEqual(new_req.description, req.description)
        self.assertEqual(new_req.cmssw_release, req.cmssw_release)
        self.assertEqual(len(new_req.steps), len(req.steps))


class BatchesDaoTest(BaseTestsCase):

    def setUp(self):
        BaseTestsCase.setUp(self)
        self.dao = BatchesDao()

    def test_simple_batch_insert(self):
        self.insert_batch()
        self.assertModelCount(Requests, 2)
        self.assertModelCount(Batches, 1)

        batch = Batches.query.one()

        self.assertEqual(batch.title, "test-title")
        self.assertEqual(batch.immutable, False)
        self.assertEqual(batch.description, "desc")
        self.assertEqual(len(batch.requests), 2)

    def test_batch_insert_with_request_clone(self):
        run_the_matrix_conf = "-i -all"
        self.insert_batch(run_the_matrix=run_the_matrix_conf)

        self.assertModelCount(Requests, 4)
        self.assertModelCount(Batches, 1)

        batch = Batches.query.one()
        self.assertEqual(batch.run_the_matrix_conf, run_the_matrix_conf)
        self.assertEqual(len(batch.requests), 2)
        for req in batch.requests:
            self.assertEqual(req.run_the_matrix_conf, run_the_matrix_conf)

    def insert_batch(self, run_the_matrix=None):
        self.assertModelEmpty(Batches)
        self.assertModelEmpty(Requests)

        utils.prepare_request()
        utils.prepare_request()
        requests = [{"id": req.id} for req in Requests.query.all()]

        self.dao.add(title="test-title", description="desc", immutable=False,
                     run_the_matrix_conf=run_the_matrix, requests=requests)

    def test_blob_update(self):
        utils.prepare_batch(requests_count=2)
        id = Batches.query.one().id

        new_title = "new-blob-title"
        utils.prepare_request()
        requests = [{"id": req.id} for req in Requests.query.all()]

        self.dao.update(id=id, title=new_title, requests=requests)

        self.assertModelCount(Batches, 1)
        self.assertModelCount(Requests, 3)

        new_batch = Batches.query.one()
        self.assertEqual(new_batch.title, new_title)
        self.assertEqual(len(new_batch.requests), 3)

    def test_blob_update_with_request_clone(self):
        utils.prepare_batch(requests_count=2)
        id = Batches.query.one().id

        new_run_the_matrix = "--test"
        requests = [{"id": req.id} for req in Requests.query.all()]

        self.dao.update(id=id, title="new-title", run_the_matrix_conf=new_run_the_matrix,
                        requests=requests)

        self.assertModelCount(Batches, 1)
        self.assertModelCount(Requests, 4)  # 2 old and two cloned
        new_batch = Batches.query.one()
        self.assertEqual(len(new_batch.requests), 2)
        for req in new_batch.requests:
            self.assertEqual(req.run_the_matrix_conf, "--test")
            self.assertEqual(req.priority, None)



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

    def test_step_step1_data_insertion(self):
        data_step = factory.data_step(data_set="test-data_set", files="100")
        self.steps_dao.add(title="step",
                           immutable=False,
                           type=StepType.FirstData,
                           data_step=data_step)

        self.assertModelCount(Steps, 1)
        self.assertModelCount(DataStep, 1)

        step = Steps.query.one()
        self.assertEqual(step.title, "step")
        self.assertEqual(step.type, StepType.FirstData)
        self.assertEqual(type(step.data_step), DataStep)
        self.assertEqual(step.data_step.data_set, "test-data_set")
        self.assertEqual(step.data_step.events, 1)
        self.assertEqual(step.data_step.files, 100)

    def test_step_step1_data_insertion_default_values_are_correct(self):
        data_step = factory.data_step(events="", files=None, split="any")
        self.steps_dao.add(title="step",
                           immutable=False,
                           type=StepType.FirstData,
                           data_step=data_step)

        self.assertModelCount(Steps, 1)
        self.assertModelCount(DataStep, 1)

        step = Steps.query.one()
        self.assertEqual(step.type, StepType.FirstData)
        self.assertEqual(step.data_step.events, 2000000)
        self.assertEqual(step.data_step.files, 1000)
        self.assertEqual(step.data_step.split, 10)


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

    def test_step_1_data_step_update(self):
        data_step = factory.data_step(data_set="test-data_set", files="100")
        utils.prepare_step(title="step-title", parameters_count=3, type=StepType.Default)
        id = Steps.query.one().id

        new_title = "new-step-title"
        self.steps_dao.update(id=id, title=new_title, type=StepType.FirstData, data_step=data_step)

        self.assertModelCount(Steps, 1)
        self.assertModelCount(Parameters, 0)
        self.assertModelCount(DataStep, 1)

        new_step = Steps.query.one()
        self.assertEqual(new_step.title, new_title)
        self.assertEqual(new_step.type, StepType.FirstData)
        self.assertEqual(new_step.data_step.data_set, "test-data_set")
        self.assertEqual(new_step.data_step.files, 100)