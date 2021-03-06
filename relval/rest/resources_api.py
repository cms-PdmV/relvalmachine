
__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.rest.api

    Relval Machine rest api
"""

from flask.ext.restful import Resource, marshal_with, reqparse
from flask import request, jsonify

from relval import app
from relval.database.models import Users
from relval.database.dao import UsersDao, PredefinedBlobsDao, StepsDao, RequestsDao, BatchesDao
from relval.rest.utils import convert_keys_to_string
from relval.rest import marshallers
from relval.services.runTheMatrix_integration import ConfigurationPreparationService


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


class ListApi(object):
    """ Base class for Resources that return paginated results
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page_num', type=int)
        self.parser.add_argument('items_per_page', type=int)
        self.parser.add_argument('search', type=str)

    def get_result(self):
        args = self.parser.parse_args()

        if args['search']:
            page_num = args['page_num'] if args['page_num'] else 1
            items_per_page = args['items_per_page'] if args['items_per_page'] else None
            items, total = self.__search(args['search'], page_num, items_per_page)
        elif args['page_num'] and args['items_per_page']:
            items, total = self.__get_page(args['page_num'], args['items_per_page'])
        else:
            items, total = self.__get_page()

        resp = {
            'items': items,
            'total': total
        }
        return resp

    def __search(self, query, page_num=1, items_per_page=None):
        return self.__paginated_result(
            self.dao.search_all,
            page_num=page_num,
            items_per_page=items_per_page,
            query=query)

    def __get_page(self, page_num=1, items_per_page=None):
        return self.__paginated_result(
            self.dao.get_paginated,
            page_num,
            items_per_page
        )

    def __paginated_result(self, dao_func, page_num=1, items_per_page=None, **kwargs):
        if not items_per_page:
            items_per_page = self.default_items_per_page
        result = dao_func(page_num=page_num, items_per_page=items_per_page, **kwargs)
        blobs = result.items
        total = result.total
        return blobs, total


class PredefinedBlobsApi(Resource, ListApi):
    """ Predefined blobs resource
    """

    def __init__(self):
        ListApi.__init__(self)
        self.dao = PredefinedBlobsDao()
        self.default_items_per_page = app.config['BLOBS_PER_PAGE']

    @marshal_with(marshallers.blobs_marshaller_paginated)
    def get(self):
        """ Returns all existing predefined blobs
        """
        return self.get_result()

    def post(self):
        """ Creates new predefined blob
        """
        data = convert_keys_to_string(request.json)
        self.dao.add(**data)


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


class StepsApi(Resource, ListApi):
    """ Steps resource
    """

    def __init__(self):
        ListApi.__init__(self)
        self.dao = StepsDao()
        self.default_items_per_page = app.config['STEPS_PER_PAGE']

    def post(self):
        """ Creates new step
        """
        data = convert_keys_to_string(request.json)
        self.dao.add(**data)

    @marshal_with(marshallers.steps_marshaller_paginated)
    def get(self):
        """ Returns all existing steps
        """
        return self.get_result()


class StepApi(Resource):
    """ Step resource to work with single step
    """

    def __init__(self):
        self.steps_dao = StepsDao()

    @marshal_with(marshallers.step_marshaller)
    def get(self, step_id):
        """ Retrieves step with id=step_id
        """
        step = self.steps_dao.get(step_id)
        step.parameters  # load all parameters from blob
        step.predefined_blobs  # load all blobs
        for blob in step.predefined_blobs:
            blob.parameters
        step.data_step  # load data_step data
        return step

    def put(self, step_id):
        """ Updates step with id=step_id
        """
        data = convert_keys_to_string(request.json)
        self.steps_dao.update(step_id, **data)

    def delete(self, step_id):
        """ Deletes step with id=step_id
        """
        self.steps_dao.delete(step_id)


class RequestsApi(Resource, ListApi):
    """ Requests resource
    """

    def __init__(self):
        ListApi.__init__(self)
        self.dao = RequestsDao()
        self.default_items_per_page = app.config['REQUESTS_PER_PAGE']

    def post(self):
        """ Creates new step
        """
        data = convert_keys_to_string(request.json)
        self.dao.add(**data)

    @marshal_with(marshallers.requests_marshaller_paginated)
    def get(self):
        """ Returns all existing steps
        """
        return self.get_result()


class RequestApi(Resource):
    """ Request resource to work with single request
    """
    def __init__(self):
        self.dao = RequestsDao()

    @marshal_with(marshallers.request_marshaller)
    def get(self, request_id):
        """ Retrieves request with id=request_id
        """
        req = self.dao.get(request_id)
        req.steps_assoc
        return req

    def put(self, request_id):
        """ Updates request with id=request_id
        """
        data = convert_keys_to_string(request.json)
        self.dao.update(request_id, **data)

    def delete(self, request_id):
        """ Deletes request with id=request_id
        """
        self.dao.delete(request_id)


class BatchesApi(Resource, ListApi):
    """ Batches resource
    """
    def __init__(self):
        ListApi.__init__(self)
        self.dao = BatchesDao()
        self.default_items_per_page = app.config['BATCHES_PER_PAGE']
        self.parser.add_argument('clone', type=bool)

    @marshal_with(marshallers.batches_marshaller_paginated)
    def get(self):
        return self.get_result()

    def post(self):
        """ Creates new batch
        """
        args = self.parser.parse_args()
        data = convert_keys_to_string(request.json)
        if args["clone"]:
            self.dao.clone(**data)
        else:
            self.dao.add(**data)


class BatchApi(Resource):
    """ Batch resource to work with single resource
    """
    def __init__(self):
        self.dao = BatchesDao()

    @marshal_with(marshallers.batch_marshaller)
    def get(self, batch_id):
        batch = self.dao.get(batch_id)
        batch.requests
        return batch

    def put(self, batch_id):
        data = convert_keys_to_string(request.json)
        self.dao.update(batch_id, **data)

