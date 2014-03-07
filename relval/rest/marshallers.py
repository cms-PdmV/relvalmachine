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
    'blobs': fields.Nested(blobs_marshaller)
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

steps_marshaller = {
    'id': fields.String,
    'title': fields.String,
    'immutable': fields.Boolean,
    'is_monte_carlo': fields.Boolean
}

steps_marshaller_paginated = {
    'total': fields.String,
    'steps': fields.Nested(steps_marshaller)
}
