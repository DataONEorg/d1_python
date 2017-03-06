#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Test serialization and de-serialization of the ObjectLocationList type.
"""

# Stdlib
import unittest
import xml.sax

# 3rd party
import pyxb

# D1
from d1_common.types import dataoneTypes

# App
import util

EG_OBJECTLOCATIONLIST_GMN = """<?xml version="1.0" encoding="UTF-8"?>
<d1:objectLocationList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <identifier>identifier0</identifier>
    <objectLocation>
        <nodeIdentifier>nodeIdentifier0</nodeIdentifier>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <version>version0</version>
        <version>version1</version>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
    <objectLocation>
        <nodeIdentifier>nodeIdentifier1</nodeIdentifier>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <version>version2</version>
        <version>version3</version>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
</d1:objectLocationList>
"""

# TODO.
EG_OBJECTLOCATIONLIST_KNB = """"""

# Missing version.
EG_BAD_OBJECTLOCATIONLIST_1 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:objectLocationList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <identifier>identifier0</identifier>
    <objectLocation>
        <nodeIdentifier>nodeIdentifier0</nodeIdentifier>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
    <objectLocation>
        <nodeIdentifier>nodeIdentifier1</nodeIdentifier>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <version>version2</version>
        <version>version3</version>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
</d1:objectLocationList>
"""

# Missing nodeIdentifier.
EG_BAD_OBJECTLOCATIONLIST_2 = """<?xml version="1.0" encoding="UTF-8"?>
<d1:objectLocationList xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <identifier>identifier0</identifier>
    <objectLocation>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <version>version0</version>
        <version>version1</version>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
    <objectLocation>
        <nodeIdentifier>nodeIdentifier1</nodeIdentifier>
        <baseURL>http://www.oxygenxml.com/</baseURL>
        <version>version2</version>
        <version>version3</version>
        <url>http://www.oxygenxml.com/</url>
        <preference>0</preference>
    </objectLocation>
</d1:objectLocationList>
"""


class TestObjectLocationList(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_deserialize_gmn(self):
    """Deserialize: XML -> ObjectLocationList (GMN)"""
    util.deserialize_and_check(EG_OBJECTLOCATIONLIST_GMN)

  def test_deserialize_knb(self):
    """Deserialize: XML -> ObjectLocationList (KNB)"""
    #util.deserialize_and_check(EG_OBJECTLOCATIONLIST_KNB)

  def test_deserialize_bad_1(self):
    """Deserialize: XML -> ObjectLocationList (bad 1)"""
    util.deserialize_and_check(EG_BAD_OBJECTLOCATIONLIST_1, shouldfail=True)

  def test_deserialize_bad_2(self):
    """Deserialize: XML -> ObjectLocationList (bad 2)"""
    util.deserialize_and_check(EG_BAD_OBJECTLOCATIONLIST_2, shouldfail=True)
