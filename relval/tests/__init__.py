__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import unittest
from relval.tests import \
    database
    # add more


class RelValMachineTestSuite(unittest.TestSuite):
    """ Test suite for relval machine application
    """

    def add_module(self, test_module):
        tests = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        self.addTest(tests)

    def add_case(self, test_case):
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_case)
        self.addTest(tests)

    def suite(self):
        self.add_module(database)
        # add more modules here

        return self
