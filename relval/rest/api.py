__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.rest.api

    Relval Machine rest api
"""

from flask.ext.restful import Resource, marshal_with, reqparse
from flask import request
import collections

from relval import app
from relval.database.models import Users
from relval.database.dao import UsersDao, PredefinedBlobsDao
from relval.rest import marshallers

BLOBS_PER_PAGE = app.config['BLOBS_PER_PAGE']


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

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page_num', type=int)
        self.parser.add_argument('items_per_page', type=int)
        self.parser.add_argument('search', type=str)

    @marshal_with(marshallers.blobs_marshaller_paginated)
    def get(self):
        """ Returns all existing predefined blobs
        """
        args = self.parser.parse_args()

        if args['search']:
            blobs, total = self.__search(args['search'])
        elif args['page_num'] and args['items_per_page']:
            blobs, total = self.__get_page(args['page_num'], args['items_per_page'])
        else:
            blobs, total = self.__get_page()

        resp = {
            'blobs': blobs,
            'total': total
        }
        return resp

    def post(self):
        """ Creates new predefined blob
        """
        data = convert_keys_to_string(request.json)
        self.blobs_dao.add(**data)

    def __search(self, query):
        blobs = self.blobs_dao.search_all(query)
        total = len(blobs)
        return blobs, total

    def __get_page(self, page_num=1, items_per_page=BLOBS_PER_PAGE):
        result = self.blobs_dao.get_paginated(page_num, items_per_page)
        blobs = result.items
        total = result.total
        return blobs, total


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

