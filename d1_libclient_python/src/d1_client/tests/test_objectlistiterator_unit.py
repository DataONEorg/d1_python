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
'''Module d1_client.tests.test_objectlistiterator
=================================================

Unit tests for objectlistiterator.

:Created:
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

import logging
import unittest
import urlparse
import sys

sys.path.append('..')
import d1_client.mnclient
import d1_client.objectlistiterator
import d1_common.types.dataoneTypes_v2_0 as dataoneTypes
from mock import patch, PropertyMock

import pyxb.binding


class _object_list(object):
  def __init__(self):
    self.objectInfo = ['test']


class TestObjectListIterator(unittest.TestCase):
  '''
    '''

  @patch.object(d1_client.objectlistiterator.ObjectListIterator, '_loadMore')
  @patch('d1_client.mnclient.MemberNodeClient')
  def setUp(self, mock_mn, mock_ol):
    logging.basicConfig(level=logging.DEBUG)
    mock_mn.return_value = 'mock_mn'
    #         client = d1_client.mnclient.MemberNodeClient(base_url=base_url)
    self.ol = d1_client.objectlistiterator.ObjectListIterator(mock_mn, max=200)

  def test__iter__(self):
    olist = self.ol.__iter__()
    self.assertEqual(olist._czero, 0)
    self.assertEqual(olist._pageoffs, 0)
    self.assertEqual(olist._maxitem, 200)
    self.assertIsNone(olist._object_list)
    self.assertEqual(olist._pagesize, 200)
    self.assertEqual(olist._citem, 0)
    self.assertIsNone(olist._fromDate)
    self.assertEqual(olist._client.return_value, 'mock_mn')

  @unittest.skip("TODO:")
  @patch.object(d1_client.objectlistiterator.ObjectListIterator, '_loadMore')
  def DO_NOT_test_next(self, mock_load):
    with patch.object(
      d1_client.objectlistiterator, 'ObjectListIterator'
    ) as mock_info:
      mock_info.return_value = _object_list()
      next_obj = self.ol.next()

  @patch.object(d1_client.mnclient.MemberNodeClient, 'listObjects')
  @patch('pyxb.RequireValidWhenParsing')
  def test_load_more(self, mock_pyxb, mock_list):
    base_url = "https://cn.dataone.org/cn"
    client = d1_client.mnclient.MemberNodeClient(base_url=base_url)
    self.ol = d1_client.objectlistiterator.ObjectListIterator(client, max=200)
    mock_list.return_value = ['test']
    self.ol._loadMore()
    self.assertEqual(self.ol._object_list, ['test'])

  def test_len(self):
    with patch('d1_client.objectlistiterator.ObjectListIterator') as mock_list:
      mock_list._maxitem = 200
      max_item = self.ol.__len__()
      self.assertEqual(max_item, 200)

  #     def test_objectlistiterator(self):
  #         '''Walk over the list of log entries available from a given node.
  #         '''
  #         base_url = "https://cn.dataone.org/cn"
  #         if len(sys.argv) > 1:
  #             target = sys.argv[1]
  #         client = d1_client.mnclient.MemberNodeClient(base_url=base_url)
  #         ol = d1_client.objectlistiterator.ObjectListIterator(client, max=200)
  #         counter = 0
  #         for o in ol:
  #             counter += 1
  #             self.assertIsInstance(o, dataoneTypes.ObjectInfo)
  #             self.assertTrue(
  #                 isinstance(
  #                     o.identifier.value(),
  #                     dataoneTypes.NonEmptyNoWhitespaceString800))
  #             self.assertTrue(
  #                 isinstance(
  #                     o.dateSysMetadataModified,
  #                     pyxb.binding.datatypes.dateTime))
  #             self.assertTrue(
  #                 isinstance(
  #                     o.formatId,
  #                     dataoneTypes.ObjectFormatIdentifier))
  #             self.assertTrue(
  #                 isinstance(
  #                     o.size,
  #                     pyxb.binding.datatypes.unsignedLong))
  #             self.assertTrue(
  #                 isinstance(
  #                     o.checksum.value(),
  #                     pyxb.binding.datatypes.string))
  #             self.assertTrue(
  #                 isinstance(
  #                     o.checksum.algorithm,
  #                     dataoneTypes.ChecksumAlgorithm))
  #         self.assertEqual(counter, 200)
