from __builtin__ import object

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.dao

    Data Access Objects

    Used for accessing database models.
"""

from relval import db
from relval.database.models import Users, Requests, PredefinedBlob, Parameters, Steps

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

    def insertRequestObject(self, request):
        db.session.add(request)
        db.session.commit()


class RevisionsDao(object):

    def addRevisionToRequest(self, request_id, revision):
        request = Requests.query.get(request_id)
        last_revision = max([rev.revision_number for rev in request.revisions])
        revision.revision_number = last_revision + 1
        request.revisions.append(revision)


class StepsDao(object):

    def __init__(self):
        self.blobs_dao = PredefinedBlobsDao()

    def add(self, title="", immutable=False, data_set="", run_lumi="", is_monte_carlo=True, parameters=[], blobs=[]):
        step = Steps(
            title=title,
            immutable=immutable,
            is_monte_carlo=is_monte_carlo,
        )
        if is_monte_carlo:
            step.parameters = [
                Parameters(flag=param['flag'], value=param['value']) for param in parameters
            ]
            step.predefined_blobs = [
                self.blobs_dao.get(blob['id']) for blob in blobs
            ]
        else:
            step.data_set = data_set
            step.run_lumi = run_lumi
        db.session.add(step)
        db.session.commit()

    def update(self, id, title=None, immutable=False, data_set=None,
               run_lumi=None, is_monte_carlo=True, parameters=[], blobs=[]):
        step = self.get(id)
        if step.immutable:
            raise Exception("Cannot edit entity that is immutable.")
        if title is not None:
            step.title = title
        step.immutable = immutable
        for parameter in step.parameters:
            db.session.delete(parameter)
        step.is_monte_carlo = is_monte_carlo
        if is_monte_carlo:
            # make sure data values setted to none
            step.data_set = None
            step.run_lumi = None

            step.parameters = [
                Parameters(flag=param['flag'], value=param['value']) for param in parameters
            ]
            step.predefined_blobs = [
                self.blobs_dao.get(blob['id']) for blob in blobs
            ]
        else:
            step.data_set = data_set
            step.run_lumi = run_lumi

            step.parameters = []
            step.blobs = []
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


class PredefinedBlobsDao(object):

    def add(self, title, creation_date=None, immutable=False, parameters=[]):
        if not creation_date:
            creation_date = datetime.utcnow();
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