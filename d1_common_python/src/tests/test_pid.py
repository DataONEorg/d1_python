#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Module d1_common.tests.test_pid
===============================

Unit tests for serializaton and de-serialization of the PID type.

:Created: 2011-03-03
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest

from d1_common import xmlrunner
from d1_common.types import pid_serialization

EG_PID_GMN = (
  """<?xml version="1.0" ?>
  <ns1:identifier xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">
  testpid
  </ns1:identifier>""",
  'testpid',
)

# TODO.
EG_PID_KNB = ("""""", '', )

EG_BAD_PID_1 = (
  """<?xml version="1.0" ?>
  <ns1:identifier xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">
  testpid
  </ns1:identifier>""",
  'testpid',
)

EG_BAD_PID_2 = (
  """<?xml version="1.0" ?>
  <ns1:identifier xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">
  testpid
  </ns1:identifier>""",
  'testpid',
)


class TestPID(unittest.TestCase):
  def test_serialization(self):
    loader = pid_serialization.Identifier('testpid')

    def doctest(doc, shouldfail=False):
      try:
        pid = loader.deserialize(doc[0], content_type="text/xml")
      except:
        if shouldfail:
          pass
        else:
          raise
      else:
        self.assertEqual(pid.value().strip(), doc[1].strip())

    doctest(EG_PID_GMN)
    # TODO.
    #doctest(EG_PID_KNB)
    doctest(EG_BAD_PID_1, shouldfail=True)
    doctest(EG_BAD_PID_2, shouldfail=True)

#===============================================================================
if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
