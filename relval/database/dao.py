from __builtin__ import object

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.dao

    Data Access Objects

    Used for accessing database models.
"""

from relval import db
from relval.database.models import Users, Requests, PredefinedBlob, Parameters, \
    Steps, StepType, DataStep, RequestStatus, Batches

from datetime import datetime


class UsersDao(object):

    def get(self, id):
        user = Users.query.get(id)
        if not user:
            raise Exception("Cannot find user with id=%s" % id)
        return user

    def insertUser(self, user_name, email=None, role=None, notifications=None):
        user = Users(user_name=user_name, email=email, role=role, notifications=notifications)
        self.insertUserObject(user)

    def insertUserObject(self, user):
        db.session.add(user)
        db.session.commit()


class RequestsDao(object):

    def __init__(self):
        self.steps_dao = StepsDao()

    def add(self, label="", description="", immutable=False, type=None, cmssw_release=None,
            run_the_matrix_conf=None, events=None, priority=1, steps=[]):
        request = Requests(
            label=label,
            description=description,
            immutable=immutable,
            type=type,
            cmssw_release=cmssw_release,
            run_the_matrix_conf=run_the_matrix_conf,
            events=events,
            priority=priority,  # TODO check if user has rights to set priority
            updated=datetime.now(),
            status=RequestStatus.New
        )
        request.steps = [
            self.steps_dao.get(step["id"]) for step in steps
        ]

        #TODO: set status, test_status
        db.session.add(request)
        db.session.commit()
        return request

    def update(self, id, label="", description="", immutable=False, type=None, cmssw_release=None,
               run_the_matrix_conf=None, events=None, priority=1, steps=[]):
        request = self.get(id)
        if label:
            request.label = label
        request.description = description
        request.immutable = immutable
        request.type = type
        request.cmssw_release = cmssw_release
        request.run_the_matrix_conf = run_the_matrix_conf
        request.events = events
        request.priority = priority
        request.steps = [
            self.steps_dao.get(step["id"]) for step in steps
        ]
        db.session.commit()

    def get_paginated(self, page_num=1, items_per_page=10):
        return Requests.query \
            .paginate(page_num, items_per_page, False)

    def get(self, id):
        return Requests.query.get(id)

    def search_all(self, query, page_num, items_per_page):
        return Requests.query \
            .filter(Requests.label.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)

    def delete(self, id):
        request = Requests.query.get(id)
        db.session.delete(request)
        db.session.commit()

    def clone(self, req, new_label, run_the_matrix_conf, priority):
        run_the_matrix = run_the_matrix_conf if run_the_matrix_conf else req.run_the_matrix_conf
        priority_to_set = priority if priority else req.priority
        steps = [
            {"id": step.id} for step in req.steps
        ]
        return self.add(label=new_label, description=req.description, immutable=req.immutable,
                        type=req.type, cmssw_release=req.cmssw_release, run_the_matrix_conf=run_the_matrix,
                        events=req.events, priority=priority_to_set, steps=steps)


class BatchesDao(object):

    def __init__(self):
        self.requests_dao = RequestsDao()

    def add(self, title="", description="", immutable=False, run_the_matrix_conf=None,
            priority=None, requests=[]):
        batch = Batches(
            title=title,
            description=description,
            immutable=immutable,
            run_the_matrix_conf=run_the_matrix_conf,
            priority=priority
        )

        # if run the matrix conf or priority are defined then we clone all requests
        if run_the_matrix_conf or priority:
            print "should clone all requests"
            batch.requests = []
            for request in requests:
                req = self.requests_dao.get(request["id"])
                new_label = "%s_%s_%s" % (
                    req.label, title, datetime.now().strftime("%d-%m-%Y_%H:%M")
                )
                cloned_req = self.requests_dao.clone(req, new_label, run_the_matrix_conf, priority)
                batch.requests.append(cloned_req)
        else:
            batch.requests = [
                self.requests_dao.get(request["id"]) for request in requests
            ]
        db.session.commit()


class StepsDao(object):

    def __init__(self):
        self.blobs_dao = PredefinedBlobsDao()

    def add(self, title="", immutable=False, data_set="",
            type=StepType.Default, parameters=[], blobs=[], data_step={}):
        step = Steps(
            title=title,
            immutable=immutable,
            type=type,
        )
        if type == StepType.Default or type == StepType.FirstMc:
            step.parameters = [
                Parameters(flag=param['flag'], value=param['value']) for param in parameters
            ]
            step.predefined_blobs = [
                self.blobs_dao.get(blob['id']) for blob in blobs
            ]
        if type == StepType.FirstMc:
            step.data_set = data_set
        if type == StepType.FirstData:
            step.data_step = self.construct_data_step(data_step)

        db.session.add(step)
        db.session.commit()

    def update(self, id, title=None, immutable=False, data_set=None,
               type=StepType.Default, parameters=[], blobs=[], data_step={}):
        step = self.get(id)
        if step.immutable:
            raise Exception("Cannot edit entity that is immutable.")
        if title is not None:
            step.title = title
        step.immutable = immutable
        for parameter in step.parameters:
            db.session.delete(parameter)
        step.type = type
        if type == StepType.Default or type == StepType.FirstMc:
            step.parameters = [
                Parameters(flag=param['flag'], value=param['value']) for param in parameters
            ]
            step.predefined_blobs = [
                self.blobs_dao.get(blob['id']) for blob in blobs
            ]
        if type == StepType.FirstMc:
            step.data_set = data_set
        if type == StepType.FirstData:
            if step.data_step is not None:
                db.session.delete(step.data_step)
            step.data_step = self.construct_data_step(data_step)

        db.session.commit()

    def get_paginated(self, page_num=1, items_per_page=10):
        return Steps.query \
            .paginate(page_num, items_per_page, False)

    def get(self, id):
        return Steps.query.get(id)

    def search_all(self, query, page_num, items_per_page):
        return Steps.query \
            .filter(Steps.title.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)

    def construct_data_step(self, data_step):
        return DataStep(
            data_set=data_step.get("data_set", None),
            label=data_step.get("label", None),
            run=data_step.get("run", None),
            ib_block=data_step.get("ib_block", None),
            ib_blacklist=data_step.get("ib_blacklist", None),
            location=data_step.get("location", None),
            files=self.to_int(data_step.get("files", None)),
            events=self.to_int(data_step.get("events", None)),
            split=self.to_int(data_step.get("split", None))
        )

    def to_int(self, item):
        if item:
            if isinstance(item, (int, long)):
                return item
            elif item.isdigit():
                return int(item)
        return None


class PredefinedBlobsDao(object):

    def add(self, title, creation_date=None, immutable=False, parameters=[]):
        if not creation_date:
            creation_date = datetime.now()
        predefined_blob = PredefinedBlob(
            title=title,
            creation_date=creation_date,
            immutable=immutable)
        predefined_blob.parameters = [
            Parameters(flag=param['flag'], value=param['value']) for param in parameters
        ]
        db.session.add(predefined_blob)
        db.session.commit()

    def all(self):
        return PredefinedBlob.query.all()

    def get_paginated(self, page_num=1, items_per_page=10):
        return PredefinedBlob.query \
            .order_by(PredefinedBlob.creation_date.asc()) \
            .paginate(page_num, items_per_page, False)

    def search_all(self, query, page_num, items_per_page):
        return PredefinedBlob.query \
            .filter(PredefinedBlob.title.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)


    def get(self, id):
        return PredefinedBlob.query.get(id)

    def update(self, id, title=None, immutable=False, parameters=[]):
        blob = self.get(id)
        if blob.immutable:
            raise Exception("Cannot edit entity that is immutable.")
        if title is not None:
            blob.title = title
        for parameter in blob.parameters:
            db.session.delete(parameter)
        blob.immutable = immutable
        blob.parameters = [
            Parameters(flag=param['flag'], value=param['value']) for param in parameters
        ]
        db.session.commit()

    def delete(self, id):
        blob = PredefinedBlob.query.get(id)
        db.session.delete(blob)
        db.session.commit()