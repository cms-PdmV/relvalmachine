__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import unittest

from relval import app, db


class BaseTestsCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['BLOBS_PER_PAGE'] = 3
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def assertModelEmpty(self, model):
        self.assertModelCount(model, 0)

    def assertModelCount(self, model, count):
        self.assertEqual(count, model.query.count())