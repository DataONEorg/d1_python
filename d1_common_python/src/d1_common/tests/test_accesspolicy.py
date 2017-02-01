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
"""
Module d1_common.tests.test_accesspolicy
=======================================

Unit tests for serialization and de-serialization of the AccessPolicy type.

:Created: 2011-03-03
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import logging
import sys
import unittest
import xml.sax

# 3rd party
import pyxb

# D1
from d1_common import xmlrunner
from d1_common.types import dataoneTypes

# App
import util


EXPECTED_ACCESSPOLICY_GMN = \
u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:accessPolicy xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <allow>
        <subject>subject0</subject>
        <subject>subject1</subject>
        <permission>read</permission>
        <permission>read</permission>
    </allow>
    <allow>
        <subject>subject2</subject>
        <subject>subject3</subject>
        <permission>read</permission>
        <permission>read</permission>
    </allow>
</d1:accessPolicy>
"""

EXPECTED_ACCESSPOLICY_GMN_2 = \
u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:accessPolicy xmlns:d1="http://ns.dataone.org/service/types/v2"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v2">
    <allow>
        <subject>subject0</subject>
        <subject>subject1</subject>
        <permission>read</permission>
        <permission>read</permission>
    </allow>
    <allow>
        <subject>subject2</subject>
        <subject>subject3</subject>
        <permission>read</permission>
        <permission>read</permission>
    </allow>
</d1:accessPolicy>
"""

# Invalid permission.
EXPECTED_ACCESSPOLICY_BAD = \
u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:accessPolicy xmlns:d1="http://ns.dataone.org/service/types/v1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://ns.dataone.org/service/types/v1">
    <allow>
        <subject>subject0</subject>
        <subject>subject1</subject>
        <permission>readx</permission>
    </allow>
    <allow>
        <subject>subject2</subject>
        <subject>subject3</subject>
        <permission>read</permission>
        <permission>read</permission>
    </allow>
</d1:accessPolicy>
"""


class TestAccessPolicy(unittest.TestCase):
  def deserialize_and_check(self, doc, shouldfail=False):
    try:
      dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise

  def test_serialization_gmn(self):
    """Deserialize: XML -> AccessPolicy (GMN)"""
    util.deserialize_and_check(EXPECTED_ACCESSPOLICY_GMN)

  def test_serialization_bad_1(self):
    """Deserialize: XML -> AccessPolicy (bad)"""
    util.deserialize_and_check(EXPECTED_ACCESSPOLICY_BAD, shouldfail=True)
