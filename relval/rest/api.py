__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.rest.api

    Relval Machine rest api
"""

from flask.ext.restful import Resource, Api, fields, marshal_with
from flask import request
import collections

from relval.database.models import PredefinedBlob, Users
from relval.database.dao import UsersDao, PredefinedBlobsDao
from relval.rest.marshallers import users_marshaller, blobs_marshaller

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

    @marshal_with(users_marshaller)
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

    @marshal_with(blobs_marshaller)
    def get(self):
        """ Returns all existing predefined blobs
        """

        blobs = self.blobs_dao.all()
        return blobs

    def post(self):
        """ Creates new predefined blob
        """
        data = convert_keys_to_string(request.json)
        self.blobs_dao.add(**data)