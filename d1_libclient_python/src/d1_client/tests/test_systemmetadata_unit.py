#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from service.mn.sysmeta_store import sysmeta
# from d1_client import d1client

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
'''Module d1_client.tests.systemmetadata.py
===========================================

Unit tests for SystemMetadata

:Created: 2012-3-11
:Author: DataONE (Flynn)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest
from mock import patch, PropertyMock

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
sys.path.append('..')
import d1_client.systemmetadata
import testing_utilities
import testing_context


class nodes():
  def __init__(self):
    self.text = 'test'


class TestSystemMetadata(TestCaseWithURLCompare):
  def setUp(self):
    self.sysmeta_doc = open(
      './d1_testdocs/BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    ).read()
    self.sysmeta = d1_client.systemmetadata.SystemMetadata(self.sysmeta_doc)

  @patch('systemmetadata.xml.etree.ElementTree.fromstring')
  def test_parse(self, mock_fromstring):
    mock_fromstring.return_value = 'test'
    self.sysmeta._parse(self.sysmeta_doc)
    self.assertEqual(self.sysmeta.etree, 'test')

  def test__repr__(self):
    output = self.sysmeta.__repr__()
    self.assertEqual(output, self.sysmeta_doc)

  @patch('d1_common.util.pretty_xml')
  @patch('xml.etree.ElementTree.tostring')
  def test_toXml(self, mock_tostring, mock_pretty):
    mock_pretty.return_value = 'test'
    output = self.sysmeta.toXml()
    self.assertEqual('test', output)

  @patch('xml.etree.ElementTree.tostring')
  def test_toXml_assert_called_pretty_xml(self, mock_tostring):
    with patch('d1_common.util.pretty_xml') as mocked_method:
      mock_tostring.return_value = 'test'
      output = self.sysmeta.toXml()
      mocked_method.assert_called_once_with('test')

  @patch('xml.etree.ElementTree.tostring')
  def test_toXml_assert_not_called_pretty_xml(self, mock_tostring):
    with patch('d1_common.util.pretty_xml') as mocked_method:
      mock_tostring.return_value = 'test'
      self.sysmeta.toXml(pretty=False)
      self.assertFalse(mocked_method.called)

  @patch('systemmetadata.xml.etree.ElementTree.fromstring')
  @patch('d1_common.util.pretty_xml')
  def test_toXml_assert_called_tostring(self, mock_tostring, mock_fromstring):
    mock_fromstring.return_value = 'test'
    self.sysmeta = d1_client.systemmetadata.SystemMetadata(self.sysmeta_doc)
    with patch('xml.etree.ElementTree.tostring') as mocked_method:
      mock_tostring.return_value = 'test'
      output = self.sysmeta.toXml()
      mocked_method.assert_called_once_with('test', 'utf-8')

  @patch('systemmetadata.xml.etree.ElementTree.Element.findall')
  def test_getValues(self, mock_find):
    mock_find.return_value = [nodes()]
    self.sysmeta._getValues('test')

  @patch('systemmetadata.xml.etree.ElementTree.Element.findall')
  def test_getValues_multiple(self, mock_find):
    mock_find.return_value = [nodes()]
    self.sysmeta._getValues('test', multiple=True)

  def test_toXml_assert_called_findall(self):
    with patch('systemmetadata.xml.etree.ElementTree.Element.findall') as mocked_method:
      self.sysmeta._getValues('test')
      mocked_method.assert_called_once_with('test')

  def DO_NOT_test_pid(self, ):
    with patch(
      'd1_client.systemmetadata.SystemMetadata',
      new_callable=PropertyMock
    ) as mock_get:
      mock_get.return_value = self.sysmeta.__getattr__('pid')
      pid = self.sysmeta.pid()
      self.assertTrue('system_pid', pid)
