'''
Used to support hudson auto builds.
'''

import sys
import os

CWD = os.environ.get("WORKSPACE")
sys.path.append("%s/api-common-python/src/tests" % CWD)

import unittest
import test_exceptions
from d1common import xmlrunner

suite = unittest.TestSuite(
  [unittest.TestLoader().loadTestsFromTestCase(test_exceptions.TestExceptions), ]
)
testRunner = xmlrunner.XmlTestRunner(sys.stdout)
testRunner.run(suite)
