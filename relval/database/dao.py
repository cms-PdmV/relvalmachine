from __builtin__ import object

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.dao

    Data Access Objects

    Used for accessing database models.
"""

from relval import db
from relval.database.models import Users, Requests, PredefinedBlob, Parameters

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


class PredefinedBlobsDao(object):

    def add(self, title, parameters=[]):
        predefinedBlob = PredefinedBlob(
            title=title,
            creation_date=datetime.utcnow())
        predefinedBlob.parameters = [
            Parameters(flag=param['flag'], value=param['value']) for param in parameters
        ]
        db.session.add(predefinedBlob)
        db.session.commit()