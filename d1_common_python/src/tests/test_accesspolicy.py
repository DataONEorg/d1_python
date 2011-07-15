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
Module d1_common.tests.test_accesspolicy
=======================================

Unit tests for serializaton and de-serialization of the AccessPolicy type.

:Created: 2011-03-03
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest
import datetime

from d1_common import xmlrunner
from d1_common.types import accesspolicy_serialization

EG_ACCESSPOLICY_GMN = \
u"""<?xml version="1.0" encoding="UTF-8"?>
    <ns1:accessPolicy xmlns:ns1="http://ns.dataone.org/service/types/0.6.2">
        <allow>
            <subject>subject0</subject>
            <subject>subject1</subject>
            <permission>read</permission>
            <permission>read</permission>
            <resource>resource0</resource>
            <resource>resource1</resource>
        </allow>
        <allow>
            <subject>subject2</subject>
            <subject>subject3</subject>
            <permission>read</permission>
            <permission>read</permission>
            <resource>resource2</resource>
            <resource>resource3</resource>
        </allow>
    </ns1:accessPolicy>
"""


class TestAccessPolicy(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    deserializer = accesspolicy_serialization.AccessPolicy()
    try:
      access_policy = deserializer.deserialize(doc, content_type="text/xml")
    except:
      if shouldfail:
        return
      else:
        raise

  def test_serialization(self):
    self.deserialize_and_check(EG_ACCESSPOLICY_GMN)

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
