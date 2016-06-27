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
'''Module d1_client.tests.test_logrecorditerator
================================================

Unit tests for LogRecordIterator.

:Created:
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

import datetime
import logging
import unittest
import urlparse
import sys
from mock import patch, PropertyMock

# sys.path.append('..')
import d1_client.mnclient_2_0
import d1_client.logrecorditerator
# import d1_common.types.dataoneTypes_v2_0 as dataoneTypes
import d1_client


# These tests are disabled because they require a MN that permits access to
# log records.

class client(object):
  def __init__(self):
    return


class logrecords(object):
  def __init__(self):
    self.logEntry = 'test'


class logentry(logrecords):
  def __init__(self):
    self.le = 10


class TestLogRecordIterator(unittest.TestCase):
  '''
    '''

  def setUp(self):
    self.base_url = "http://127.0.0.1:8000"
    self.client = d1_client.d1baseclient.DataONEBaseClient(self.base_url)
    from_date = datetime.date(2015, 3, 1)
    to_date = datetime.date(2015, 3, 2)
    self.iterator = d1_client.logrecorditerator.LogRecordIterator(
      self.client, from_date,
      to_date, start=100,
      pageSize=2000
    )

  @unittest.skip("Need to set up stable test env")
  def test_0010(self):
    """Test iterator"""
    log_iter = self.iterator.__iter__()
    self.assertIsNone(log_iter._log_records, None)
    self.assertEqual(log_iter._from_date, datetime.date(2015, 3, 1))
    self.assertEqual(log_iter._to_date, datetime.date(2015, 3, 2))
    self.assertEqual(log_iter._start, 100)
    self.assertEqual(log_iter._page_size, 2000)
    self.assertEqual(log_iter._log_records_idx, 0)
    self.assertEqual(log_iter._n_log_records, 0)

  @unittest.skip("Need to set up stable test env")
  @patch('d1_client.d1baseclient.DataONEBaseClient.getLogRecords')
  def test_0020(self, mock_logentry):
    """Load more"""
    mock_logentry.return_value = logrecords()
    self.iterator._load_more()
    self.assertEqual(self.iterator._start, 104)

  @unittest.skip("Need to set up stable test env")
  @patch.object(d1_client.logrecorditerator, 'LogRecordIterator')
  @patch('d1_client.logrecorditerator.LogRecordIterator._load_more')
  def test_0030(self, mock_load, mock_iter):
    """Next"""
    self.iterator._n_log_records = 1
    self.iterator._log_records_idx = 1
    mock_iter._log_records.return_value = logrecords()
    log_entry = self.iterator.next()
    self.assertEqual(log_entry, 2)
