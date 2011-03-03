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
Module d1_common.tests.test_objectlocationlist
==============================================

Unit tests for serializaton and de-serialization of the ObjectLocationList type.

:Author: Vieglais, Dahl

..autoclass:: TestObjectLocationList
  :members:
'''

import logging
import sys
import unittest

from d1_common import xmlrunner
from d1_common.types import objectlocationlist_serialization

EG_OBJECTLOCATIONLIST_GMN = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<identifier>testobj</identifier>
<objectLocation><nodeIdentifier>test1</nodeIdentifier><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""

# TODO.
EG_OBJECTLOCATIONLIST_KNB = """"""

EG_BAD_OBJECTLOCATIONLIST_1 = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<identifier>hdl:10255/dryad.1073/mets.xml</identifier>
<objectLocation><nodeIdentifier>test1</nodeIdentifier><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""

EG_BAD_OBJECTLOCATIONLIST_2 = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://dataone.org/service/types/0.5.1">
<identifier>hdl:10255/dryad.1073/mets.xml</identifier>
<objectLocation><nodeIdentifier>test1</nodeIdentifier><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""


class TestObjectLocationList(unittest.TestCase):
  def test_serialization(self):
    loader = objectlocationlist_serialization.ObjectLocationList()

    def doctest(doc, shouldfail=False):
      try:
        checksum = loader.deserialize(doc, content_type="text/xml")
      except:
        if shouldfail:
          pass
        else:
          raise

    doctest(EG_OBJECTLOCATIONLIST_GMN)
    #doctest(EG_OBJECTLOCATIONLIST_KNB)
    doctest(EG_BAD_OBJECTLOCATIONLIST_1, shouldfail=True)
    doctest(EG_BAD_OBJECTLOCATIONLIST_2, shouldfail=True)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  unittest.main(testRunner=xmlrunner.XmlTestRunner(sys.stdout))
