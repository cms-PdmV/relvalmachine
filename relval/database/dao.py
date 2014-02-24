from __builtin__ import object

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.database.dao

    Data Access Objects

    Used for accessing database models.
"""

from relval import db
from relval.database.models import Users, Requests, PredefinedBlob


class UsersDao(object):

    def get(self, id):
        user = Users.query.get(id)
        if not user:
            raise Exception("Cannot find user with id=%s" % id)
        return user

    def insertUser(self, username, email, role, notifications):
        user = Users(user_name=username, email=email, role=role, notifications=notifications)
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
