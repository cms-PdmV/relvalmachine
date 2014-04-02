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


class BaseValidationDao(object):

    def __init__(self, entity):
        self.entity = entity

    def validate_distinct_value(self, value_to_validate, column):
        if not value_to_validate:
            raise Exception("Validation failed")
        if not self.entity.query.filter(column == value_to_validate).count() == 0:
            raise Exception("Validation failed")

    def validate_distinct_title(self, title_to_validate):
        self.validate_distinct_value(title_to_validate, self.entity.title)

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


class RequestsDao(BaseValidationDao):
    def __init__(self):
        BaseValidationDao.__init__(self, Requests)
        self.steps_dao = StepsDao()

    def add(self, label="", description="", immutable=False, type=None, cmssw_release=None,
            run_the_matrix_conf=None, events=None, priority=1, ancestor_request=None, steps=[]):
        self.validate_distinct_label(label)
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
            status=RequestStatus.New,
            ancestor_request=ancestor_request
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
        if label != request.label:
            self.validate_distinct_label(label)
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

    def get_details(self, id):
        request = self.get(id)

        steps = []
        for i, step in enumerate(request.steps):
            text = "[{0}] {1}".format(i, self.steps_dao.get_details(step.id)["text"])
            steps.append(dict(
                title=step.title,
                id=step.id,
                text=text
            ))

        return {
            "steps": steps,
            "cmssw_release": request.cmssw_release,
            "run_the_matrix": request.run_the_matrix_conf,
            "description": request.description,

        }

    def validate_distinct_label(self, label_to_validate):
        self.validate_distinct_value(label_to_validate, Requests.label)

    def search_all(self, query, page_num, items_per_page):
        return Requests.query \
            .filter(Requests.label.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)

    def delete(self, id):
        request = Requests.query.get(id)
        db.session.delete(request)
        db.session.commit()

    def get_ancestor(self, request):
        ancestor = request
        while ancestor.ancestor_request is not None:
            ancestor = ancestor.ancestor_request
        return ancestor

    def clone(self, req, new_label, customization):
        run_the_matrix = customization.run_the_matrix if customization.run_the_matrix else req.run_the_matrix_conf
        cmssw_release = customization.cmssw_release if customization.cmssw_release else req.cmssw_release
        priority_to_set = customization.priority if customization.priority else req.priority
        steps = [
            {"id": step.id} for step in req.steps
        ]

        ancestor = self.get_ancestor(req)
        return self.add(label=new_label, description=req.description, immutable=False,
                        type=req.type, cmssw_release=cmssw_release, run_the_matrix_conf=run_the_matrix,
                        events=req.events, priority=priority_to_set, ancestor_request=ancestor, steps=steps)


class Customization():

    def __init__(self, run_the_matrix, cmssw_release, priority):
        self.run_the_matrix = run_the_matrix
        self.cmssw_release = cmssw_release
        self.priority = priority

    def is_any_defined(self):
        return self.run_the_matrix or self.priority or self.cmssw_release

    def is_customization_changed(self, batch):
        return batch.run_the_matrix_conf != self.run_the_matrix or \
            batch.priority != self.priority or \
            batch.cmssw_release != self.cmssw_release


class BatchesDao(BaseValidationDao):

    def __init__(self):
        BaseValidationDao.__init__(self, Batches)
        self.requests_dao = RequestsDao()

    def add(self, **kwargs):
        return self.insert_batch(is_cloning=False, **kwargs)

    def clone(self, **kwargs):
        return self.insert_batch(is_cloning=True, **kwargs)

    def insert_batch(self, title="", description="", immutable=False, run_the_matrix_conf=None,
                     priority=None, cmssw_release=None, requests=[], is_cloning=False):
        self.validate_distinct_title(title)
        batch = Batches(
            title=title,
            description=description,
            immutable=immutable,
            run_the_matrix_conf=run_the_matrix_conf,
            priority=priority,
            cmssw_release=cmssw_release
        )
        customization = Customization(run_the_matrix_conf, cmssw_release, priority)
        # if request is cloning or run the matrix conf or priority
        # or cmssw release are defined then we clone all requests
        if is_cloning or customization.is_any_defined():
            batch.requests = self.__clone_requests(requests, title, customization)
        else:
            batch.requests = [
                self.requests_dao.get(request["id"]) for request in requests
            ]

        db.session.add(batch)
        db.session.commit()
        return batch

    def update(self, id, title="", description="", immutable=False, run_the_matrix_conf=None,
               priority=None, cmssw_release=None, requests=[]):
        batch = self.get(id)
        if title != batch.title:
            self.validate_distinct_title(title)
        batch.title = title
        batch.description = description
        batch.immutable = immutable
        cust = Customization(run_the_matrix_conf, cmssw_release, priority)

        if cust.is_customization_changed(batch):
            new_requests = []
            for req in requests:
                req_object = self.requests_dao.get(req["id"])

                # if request is frozen then clone it
                if req_object.immutable:
                    new_requests.append(self.__clone_request(req_object, title, cust))

                # if request is not frozen and don't belong to other batches then no cloning - just update request
                elif len(req_object.batches) == 0 or \
                        (len(req_object.batches) == 1 and req_object.batches[0].id == batch.id):
                    req_object.run_the_matrix_conf = cust.run_the_matrix
                    req_object.priority = cust.priority
                    req_object.cmssw_release = cust.cmssw_release
                    new_requests.append(req_object)
                else:
                    new_requests.append(self.__clone_request(req_object, title, cust))

            batch.requests = new_requests

            batch.run_the_matrix_conf = cust.run_the_matrix
            batch.priority = cust.priority
            batch.cmssw_release = cust.cmssw_release
        else:
            new_requests = []
            for request in requests:
                req = self.requests_dao.get(request["id"])

                # check if run the matrix config or priority need to be overwritten for request
                if self.__is_customizations_differs(batch, req):
                    new_requests.append(self.__clone_request(req, title, cust))
                else:
                    new_requests.append(req)
            batch.requests = new_requests
        db.session.commit()

    def __is_customizations_differs(self, batch, request):
        return (batch.run_the_matrix_conf is not None and request.run_the_matrix_conf != batch.run_the_matrix_conf) or \
               (batch.cmssw_release is not None and request.cmssw_release != batch.cmssw_release) or \
               (batch.priority is not None and request.priority != batch.priority)

    def get_paginated(self, page_num=1, items_per_page=10):
        return Batches.query \
            .paginate(page_num, items_per_page, False)

    def get(self, id):
        return Batches.query.get(id)

    def get_details(self, id):
        batch = self.get(id)

        requests = []
        for req in batch.requests:
            steps = self.requests_dao.get_details(req.id)["steps"]
            requests.append(dict(
                steps=steps,
                id=req.id,
                label=req.label
            ))
        return dict(
            requests=requests
        )



    def search_all(self, query, page_num, items_per_page):
        return Batches.query \
            .filter(Batches.title.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)

    def __clone_requests(self, requests, title, customization):
        cloned = []
        for request in requests:
            req = self.requests_dao.get(request["id"])
            cloned_req = self.__clone_request(req, title, customization)
            cloned.append(cloned_req)
        return cloned

    def __clone_request(self, request, title, customization):
        new_label = self.__resolve_request_label(request, title)
        cloned_req = self.requests_dao.clone(request, new_label, customization)
        return cloned_req

    def __resolve_request_label(self, old_request, batch_title):
        """ Method cloned request label
        """
        ancestor = self.requests_dao.get_ancestor(old_request)
        return "%s_%s_%s" % (
            ancestor.label, batch_title, datetime.now().strftime("%d-%m-%Y_%H:%M")
        )


class StepsDao(BaseValidationDao):
    def __init__(self):
        BaseValidationDao.__init__(self, Steps)
        self.blobs_dao = PredefinedBlobsDao()

    def add(self, title="", immutable=False, type=StepType.Default, name="",
            parameters=[], blobs=[], data_step={}):
        self.validate_distinct_title(title)
        step = Steps(
            title=title,
            immutable=immutable,
            type=type,
            name=name
        )
        if type == StepType.Default or type == StepType.FirstMc:
            step.parameters = [
                Parameters(flag=param['flag'], value=param['value']) for param in parameters
            ]
            step.predefined_blobs = [
                self.blobs_dao.get(blob['id']) for blob in blobs
            ]
        if type == StepType.FirstData or type == StepType.FirstMc:
            step.data_step = self.construct_data_step(data_step)

        db.session.add(step)
        db.session.commit()

    def update(self, id, title=None, immutable=False, type=StepType.Default, name=None,
               parameters=[], blobs=[], data_step={}):
        step = self.get(id)
        if step.immutable:
            raise Exception("Cannot edit entity that is immutable.")
        if title != step.title:
            self.validate_distinct_title(title)
        if title is not None:
            step.title = title
        if name is not None:
            step.name = name
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
        if type == StepType.FirstData or type == StepType.FirstMc:
            if step.data_step is not None:
                db.session.delete(step.data_step)
            step.data_step = self.construct_data_step(data_step)

        db.session.commit()

    def get_paginated(self, page_num=1, items_per_page=10):
        return Steps.query \
            .paginate(page_num, items_per_page, False)

    def get(self, id):
        return Steps.query.get(id)

    def get_details(self, id):
        step = self.get(id)
        text = "cmsDriver.py {0} ".format(step.name or "")
        blobs = []
        if step.type == StepType.FirstMc:
            text += step.data_step.data_set + " "
        if step.type == StepType.Default or step.type == StepType.FirstMc:
            for p in step.parameters:
                text += " ".join([p.flag or "", p.value or ""]) + " "  # null safe
            for blob in step.predefined_blobs:
                text += " " + self.blobs_dao.get_details(blob.id)["text"]
                blobs.append(dict(title=blob.title, id=blob.id))

        if step.type == StepType.FirstData:
            data_step = step.data_step
            if data_step.ib_block:
                text = "input from: {0} with run {1}#{2}".format(
                    data_step.data_set, data_step.ib_block, data_step.run)
            else:
                text = "input from: {0} with run {1}".format(data_step.data_set, data_step.run)

        return dict(
            text=text,
            blobs=blobs
        )

    def search_all(self, query, page_num, items_per_page):
        return Steps.query \
            .filter(Steps.title.ilike("%{0}%".format(query))) \
            .paginate(page_num, items_per_page, False)

    def delete(self, id):
        step = Steps.query.get(id)
        db.session.delete(step)
        db.session.commit()

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


class PredefinedBlobsDao(BaseValidationDao):

    def __init__(self):
        BaseValidationDao.__init__(self, PredefinedBlob)

    def add(self, title, creation_date=None, immutable=False, parameters=[]):
        self.validate_distinct_title(title)
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

    def get_details(self, id):
        blob = self.get(id)
        details = ""
        for p in blob.parameters:
            details += " ".join([p.flag or "", p.value or ""]) + " "

        return dict(
            text=details
        )

    def validate(self, entity):
        if not self.validate_distinct_title(entity.title):
            raise Exception("Title must be unique")

    def update(self, id, title=None, immutable=False, parameters=[]):
        blob = self.get(id)
        if blob.immutable:
            raise Exception("Cannot edit entity that is immutable.")
        if title != blob.title:
            self.validate_distinct_title(title)
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