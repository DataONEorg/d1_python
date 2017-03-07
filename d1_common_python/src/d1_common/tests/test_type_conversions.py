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
"""Test DataONE type conversions
"""

# Stdlib
import os
import unittest

# 3rd party
import d1_common.xml

# App
import d1_common.type_conversions as c
import d1_common.util


class TestTypeConversions(unittest.TestCase):
  def _read_xml(self, file_name):
    test_docs_path = os.path.join(
      os.path.abspath(os.path.dirname(__file__)), 'test_docs'
    )
    return open(os.path.join(test_docs_path, file_name)).read()

  def _print_pretty_xml_obj(self, xml_obj):
    print d1_common.xml.pretty_xml(xml_obj.toxml())

  def _print_pretty_xml_str(self, xml_str):
    print d1_common.xml.pretty_xml(xml_str)

  def test_0010(self):
    """is_v1()"""
    systemMetadata_v1_0_str = self._read_xml('systemMetadata_v1_0.xml')
    self.assertTrue(c.str_is_v1(systemMetadata_v1_0_str))
    self.assertFalse(c.str_is_v2(systemMetadata_v1_0_str))

  def test_0020(self):
    """is_v2()"""
    systemMetadata_v2_0_str = self._read_xml('systemMetadata_v2_0.xml')
    self.assertTrue(c.str_is_v2(systemMetadata_v2_0_str))
    self.assertFalse(c.str_is_v1(systemMetadata_v2_0_str))

  def test_0030(self):
    """v1 XML string to PyXB conversion and type check"""
    systemMetadata_v1_0_str = self._read_xml('systemMetadata_v1_0.xml')
    systemMetadata_v1_0_pyxb = c.str_to_pyxb(systemMetadata_v1_0_str)
    self.assertTrue(c.pyxb_is_v1(systemMetadata_v1_0_pyxb))

  def test_0040(self):
    """v2 XML string to PyXB conversion and type check"""
    systemMetadata_v2_0_str = self._read_xml('systemMetadata_v2_0.xml')
    systemMetadata_v2_0_pyxb = c.str_to_pyxb(systemMetadata_v2_0_str)
    self.assertTrue(c.pyxb_is_v2(systemMetadata_v2_0_pyxb))
    self.assertFalse(c.pyxb_is_v1(systemMetadata_v2_0_pyxb))

  def test_0050(self):
    """LogEntry v1 to v2"""
    logEntry_v1_0_str = self._read_xml('logEntry_v1_0.xml')
    logEntry_v2_str = c.str_to_v2_str(logEntry_v1_0_str)
    self.assertTrue(c.str_is_v2(logEntry_v2_str))
    self.assertFalse(c.str_is_v1(logEntry_v2_str))

  def test_0060(self):
    """LogEntry v2 to v1"""
    logEntry_v2_0_str = self._read_xml('logEntry_v2_0.xml')
    logEntry_v1_str = c.str_to_v1_str(logEntry_v2_0_str)
    self.assertTrue(c.str_is_v1(logEntry_v1_str))
    self.assertFalse(c.str_is_v2(logEntry_v1_str))

  def test_0070(self):
    """Log v2 to v1"""
    log_v2_0_str = self._read_xml('log_v2_0.xml')
    log_v1_str = c.str_to_v1_str(log_v2_0_str)
    self.assertTrue(c.str_is_v1(log_v1_str))
    self.assertFalse(c.str_is_v2(log_v1_str))

  def test_0080(self):
    """Node v2 to v1"""
    node_v2_0_str = self._read_xml('node_v2_0.xml')
    node_v1_str = c.str_to_v1_str(node_v2_0_str)
    self.assertTrue(c.str_is_v1(node_v1_str))
    self.assertFalse(c.str_is_v2(node_v1_str))

  def test_0090(self):
    """NodeList v2 to v1"""
    node_list_v2_0_str = self._read_xml('nodeList_v2_0.xml')
    node_list_v1_str = c.str_to_v1_str(node_list_v2_0_str)
    self.assertTrue(c.str_is_v1(node_list_v1_str))
    self.assertFalse(c.str_is_v2(node_list_v1_str))

  def test_0100(self):
    """SystemMetadata v2 to v1"""
    systemMetadata_v2_0_str = self._read_xml('systemMetadata_v2_0.xml')
    systemMetadata_v1_str = c.str_to_v1_str(systemMetadata_v2_0_str)
    self.assertTrue(c.str_is_v1(systemMetadata_v1_str))
    self.assertFalse(c.str_is_v2(systemMetadata_v1_str))
