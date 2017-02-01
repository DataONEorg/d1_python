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
Module d1_common.tests.test_checksum
====================================

Unit tests for serialization and de-serialization of the Checksum type.

:Created: 2011-03-03
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import unittest
import xml.sax

# 3rd party
import pyxb

# D1
import d1_common.const
import d1_common.types.dataoneTypes as dataoneTypes
import d1_common.checksum

# App

EG_CHECKSUM_GMN = (
  """<?xml version="1.0" ?><ns1:checksum algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  'SHA-1', '3f56de593b6ffc536253b799b429453e3673fc19'
)

# TODO.
EG_CHECKSUM_KNB = ("""""", '', '')

EG_BAD_CHECKSUM_1 = (
  """<?xml version="1.0" ?><ns1:checksum invalid_attribute="invalid" algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)

EG_BAD_CHECKSUM_2 = (
  """<?xml version="1.0" ?><ns1:checksumINVALID algorithm="SHA-1" xmlns:ns1="http://ns.dataone.org/service/types/v1">3f56de593b6ffc536253b799b429453e3673fc19</ns1:checksum>""",
  '', ''
)


class TestChecksum(unittest.TestCase):
  def deserialize_checksum_and_check(self, doc, shouldfail=False):
    try:
      obj = dataoneTypes.CreateFromDocument(doc[0])
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if shouldfail:
        return
      else:
        raise
    else:
      self.assertEqual(obj.algorithm, doc[1])
      self.assertEqual(obj.value(), doc[2])

  def test_100(self):
    """Deserialize: XML -> Checksum (GMN)"""
    self.deserialize_checksum_and_check(EG_CHECKSUM_GMN)

  def test_110(self):
    """Deserialize: XML -> Checksum (bad 1)"""
    self.deserialize_checksum_and_check(EG_BAD_CHECKSUM_1, shouldfail=True)

  def test_120(self):
    """Deserialize: XML -> Checksum (bad 2)"""
    self.deserialize_checksum_and_check(EG_BAD_CHECKSUM_2, shouldfail=True)

  def test_130(self):
    """Serialization: Checksum -> XML -> Checksum.
    """
    checksum_obj_in = dataoneTypes.checksum('1' * 32)
    checksum_obj_in.algorithm = 'MD5'
    checksum_xml = checksum_obj_in.toxml()
    checksum_obj_out = dataoneTypes.CreateFromDocument(checksum_xml)
    self.assertEqual(checksum_obj_in.value(), checksum_obj_out.value())
    self.assertEqual(checksum_obj_in.algorithm, checksum_obj_out.algorithm)

  def test_200(self):
    """checksums_are_equal(): Same checksum, same algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'SHA-1'
    self.assertTrue(d1_common.checksum.checksums_are_equal(c1, c2))

  def test_210(self):
    """checksums_are_equal(): Same checksum, different algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertFalse(d1_common.checksum.checksums_are_equal(c1, c2))

  def test_220(self):
    """checksums_are_equal(): Different checksum, same algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00DX')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertFalse(d1_common.checksum.checksums_are_equal(c1, c2))

  def test_230(self):
    """checksums_are_equal(): Case insensitive checksum comparison"""
    c1 = dataoneTypes.Checksum('baadf00d')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertTrue(d1_common.checksum.checksums_are_equal(c1, c2))

  def test_240(self):
    """get_checksum_calculator_by_dataone_designator() returns a checksum calculator"""
    calculator = d1_common.checksum.get_checksum_calculator_by_dataone_designator('SHA-1')
    calculator.update('test')
    self.assertTrue(calculator.hexdigest())

  def test_250(self):
    """get_checksum_calculator_by_dataone_designator() raises on invalid algorithm"""
    self.assertRaises(
      Exception, d1_common.checksum.get_checksum_calculator_by_dataone_designator,
      'SHA-224-bogus'
    )
