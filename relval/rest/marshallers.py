__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

""" relval.rest.marshallers

    Marshallers rest api to construct json files
"""

from flask.ext.restful import fields


users_marshaller = {
    'id': fields.String,
    'user_name': fields.String,
    'email': fields.String,
    'role': fields.String,
    'notifications': fields.Boolean
}

blobs_marshaller = {
    'id': fields.String,
    'title': fields.String,
    'creation_date': fields.String,
    'immutable': fields.Boolean
}

blobs_marshaller_paginated = {
    'total': fields.String,
    'items': fields.Nested(blobs_marshaller)
}

parameter_marshaller = {
    "flag": fields.String,
    "value": fields.String
}

blob_marshaller = {
    'id': fields.String,
    'title': fields.String,
    'creation_date': fields.String,
    'immutable': fields.Boolean,
    'parameters': fields.Nested(parameter_marshaller)
}

blob_tight_marshaller = {
    'id': fields.String,
    'title': fields.String
}

steps_marshaller = {
    'id': fields.String,
    'title': fields.String,
    'immutable': fields.Boolean,
    'type': fields.String
}

steps_marshaller_paginated = {
    'total': fields.String,
    'items': fields.Nested(steps_marshaller)
}

data_step_marshaller = {
    "data_set": fields.String,
    "label": fields.String,
    "run": fields.String,
    "ib_block": fields.String,
    "ib_blacklist": fields.String,
    "location": fields.String,
    "files": fields.Integer,
    "events": fields.Integer,
    "split": fields.Integer
}

step_marshaller = {
    'id': fields.String,
    'title': fields.String,
    'immutable': fields.Boolean,
    'type': fields.String,
    'parameters': fields.Nested(parameter_marshaller),
    'data_set': fields.String,
    'data_step': fields.Nested(data_step_marshaller),
    'blobs': fields.Nested(blob_tight_marshaller, attribute="predefined_blobs")
}
