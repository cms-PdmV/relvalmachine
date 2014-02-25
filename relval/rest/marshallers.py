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
    'creation_date': fields.String
}