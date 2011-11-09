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

:Created: 2011-03-03
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest
import xml.sax

# 3rd party.
import pyxb

# D1.
from d1_common import xmlrunner
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App
import util

EG_OBJECTLOCATIONLIST_GMN = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://ns.dataone.org/service/types/v1">
<identifier>testobj</identifier>
<objectLocation><nodeIdentifier>test1</nodeIdentifier><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""

# TODO.
EG_OBJECTLOCATIONLIST_KNB = """"""

# Bad version.
EG_BAD_OBJECTLOCATIONLIST_1 = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://ns.dataone.org/service/types/v999">
<identifier>hdl:10255/dryad.1073/mets.xml</identifier>
<objectLocation><nodeIdentifier>test1</nodeIdentifier><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""

# Missing nodeIdentifier.
EG_BAD_OBJECTLOCATIONLIST_2 = """<?xml version="1.0" ?>
<ns1:objectLocationList xmlns:ns1="http://ns.dataone.org/service/types/v1">
<identifier>hdl:10255/dryad.1073/mets.xml</identifier>
<objectLocation><baseURL>http://localhost:8000</baseURL><url>http://localhost:8000/object/testobj</url></objectLocation>
<objectLocation><nodeIdentifier>test2</nodeIdentifier><baseURL>http://testbogus.com/mn/something</baseURL><url>http://testbogus.com/mn/something/testobj</url></objectLocation>
</ns1:objectLocationList>"""


class TestObjectLocationList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      obj = dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_deserialize_gmn(self):
    '''Deserialize: XML -> ObjectLocationList (GMN)'''
    util.deserialize_and_check(EG_OBJECTLOCATIONLIST_GMN)

  def test_deserialize_knb(self):
    '''Deserialize: XML -> ObjectLocationList (KNB)'''
    #util.deserialize_and_check(EG_OBJECTLOCATIONLIST_KNB)

  def test_deserialize_bad_1(self):
    '''Deserialize: XML -> ObjectLocationList (bad 1)'''
    util.deserialize_and_check(EG_BAD_OBJECTLOCATIONLIST_1, shouldfail=True)

  def test_deserialize_bad_2(self):
    '''Deserialize: XML -> ObjectLocationList (bad 2)'''
    util.deserialize_and_check(EG_BAD_OBJECTLOCATIONLIST_2, shouldfail=True)

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
