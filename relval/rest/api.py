__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.rest.api

    Relval Machine rest api
"""

from flask.ext.restful import Resource, marshal_with
from flask import request
import collections

from relval.database.models import Users
from relval.database.dao import UsersDao, PredefinedBlobsDao
from relval.rest import marshallers


def convert_keys_to_string(dictionary):
    """ Recursively converts dictionary keys to strings.
        Utility to help deal with unicode keys in dictionaries created from json requests.
        In order to pass dict to function as **kwarg we should transform key/value to str.
    """
    if isinstance(dictionary, basestring):
        return str(dictionary)
    elif isinstance(dictionary, collections.Mapping):
        return dict(map(convert_keys_to_string, dictionary.iteritems()))
    elif isinstance(dictionary, collections.Iterable):
        return type(dictionary)(map(convert_keys_to_string, dictionary))
    else:
        return dictionary


class UsersListApi(Resource):
    """ Users resource.
    """

    def __init__(self):
        self.users_dao = UsersDao()

    @marshal_with(marshallers.users_marshaller)
    def get(self):
        """ Returns list of all available users id db.
        """

        users = Users.query.all()
        return users

    def post(self):
        """ Creates new user in db.
        """

        data = convert_keys_to_string(request.json)
        self.users_dao.insertUser(**data)


class PredefinedBlobsApi(Resource):
    """ Predefined blobs resource
    """

    def __init__(self):
        self.blobs_dao = PredefinedBlobsDao()

    @marshal_with(marshallers.blobs_marshaller)
    def get(self):
        """ Returns all existing predefined blobs
        """
        search = request.args.get("search")
        if search:
            blobs = self.blobs_dao.search_all(search)
        else:
            blobs = self.blobs_dao.all()
        return blobs

    def post(self):
        """ Creates new predefined blob
        """
        data = convert_keys_to_string(request.json)
        self.blobs_dao.add(**data)


class PredefinedBlobApi(Resource):
    """ Predefined blobs resource to work with single entity
    """

    def __init__(self):
        self.blobs_dao = PredefinedBlobsDao()

    def delete(self, blob_id):
        """ Deletes predefined blob with id=blob_id
        """
        self.blobs_dao.delete(blob_id)

    @marshal_with(marshallers.blob_marshaller)
    def get(self, blob_id):
        """ Retrieves predefined blob with id=blob_id
        """
        blob = self.blobs_dao.get(blob_id)
        blob.parameters  # load all parameters from blob
        return blob

    def put(self, blob_id):
        """ Updates blob
        """
        data = convert_keys_to_string(request.json)
        self.blobs_dao.update(id=blob_id, **data)

