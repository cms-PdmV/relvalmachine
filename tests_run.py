#!/usr/bin/python2.6

__author__ = "Zygimantas Gatelis"
__email__ = "zygimantas.gatelis@cern.ch"

import sys
import unittest

from relval.tests import RelValMachineTestSuite


def run_tests():
    suite = RelValMachineTestSuite()
    runner = unittest.TextTestRunner()
    result = runner.run(suite.suite())
    exit_code = 0 if result.wasSuccessful() else -1
    sys.exit(exit_code)

if __name__ == '__main__':
    run_tests()
