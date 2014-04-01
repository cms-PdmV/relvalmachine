from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader, PackageLoader

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

from relval.database.dao import RequestsDao
from flask import render_template


class CommandsService(object):

    def __init__(self):
        self.env = Environment(loader=PackageLoader("relval", "/templates/bash"))
        self.request_dao = RequestsDao()

    def get_test_command(self, request_id):
        template = self.env.get_template('test_request.sh')
        request = self.request_dao.get(request_id)

        return template.render(dict(
            cmssw_release=request.cmssw_release)
        )



