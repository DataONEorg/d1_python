#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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

sys.path.append('..')
import d1_client.mnclient
import d1_client.logrecorditerator
import d1_common.types.generated.dataoneTypes as dataoneTypes
import src.d1_client


# These tests are disabled because they require a MN that permits access to
# log records.\
class client():
  def __init__(self):
    return


class logentry():
  def __init__(self):
    return


class TestLogRecordIterator(unittest.TestCase):
  '''
    '''

  def setUp(self):
    self.base_url = "http://127.0.0.1:8000"
    self.client = d1_client.d1baseclient.DataONEBaseClient(self.base_url)
    from_date = datetime.date(2015, 3, 1)
    to_date = datetime.date(2015, 3, 2)
    self.iterator = d1_client.logrecorditerator.LogRecordIterator(
      self.client, from_date, to_date,
      start=100, pageSize=2000
    )

  def test__iter__(self):
    log_iter = self.iterator.__iter__()
    self.assertIsNone(log_iter._log_records, None)
    self.assertEqual(log_iter._from_date, datetime.date(2015, 3, 1))
    self.assertEqual(log_iter._to_date, datetime.date(2015, 3, 2))
    self.assertEqual(log_iter._start, 100)
    self.assertEqual(log_iter._page_size, 2000)
    self.assertEqual(log_iter._log_records_idx, 0)
    self.assertEqual(log_iter._n_log_records, 0)

  @patch('d1_client.d1baseclient.DataONEBaseClient.getLogRecords')
  @patch('d1_client.d1baseclient.DataONEBaseClient.getLogRecords.logEntry')
  def test_load_more(self, mock_logentry, mock_log):
    mock_log.return_value = '1'
    mock_logentry.return_value = logentry()
    output = self.iterator._load_more()
    self.assertEqual(output, 10)

  def _test_100(self):
    '''PageSize=20, start=0'''
    self._log_record_iterator_test(20, 0)

  def _test_110(self):
    '''PageSize=1, start=63'''
    self._log_record_iterator_test(1, 63)

  def _test_120(self):
    '''PageSize=2000, start=0'''
    self._log_record_iterator_test(2000, 0)

  def _test_130(self):
    '''PageSize=20, start=20, fromDate=2005-01-01'''
    self._log_record_iterator_test(2000, 0, from_date=datetime.datetime(2005, 1, 1))

  def _log_record_iterator_test(self, page_size, start, from_date=None, to_date=None):
    client = d1_client.mnclient.MemberNodeClient(base_url=self.base_url)
    total = self._get_log_total_count(client, from_date, to_date)
    log_record_iterator = d1_client.logrecorditerator.LogRecordIterator(
      client, pageSize=page_size,
      start=start,
      fromDate=from_date,
      toDate=to_date
    )
    cnt = 0
    for event in log_record_iterator:
      self.assertTrue(isinstance(event.event, dataoneTypes.Event))
      # print "Event    = %s" % event.event
      # print "Timestamp  = %s" % event.dateLogged.isoformat()
      # print "IP Addres  = %s" % event.ipAddress
      # print "Identifier = %s" % event.identifier.value()
      # print "User agent = %s" % event.userAgent
      # print "Subject  = %s" % event.subject.value()
      # print '-' * 79
      cnt += 1
    self.assertEqual(cnt, total - start)

  def _get_log_total_count(self, client, from_date, to_date):
    return client.getLogRecords(
      start=0, count=0, fromDate=from_date,
      toDate=to_date
    ).total


if __name__ == '__main__':
  logging.getLogger("").setLevel(logging.DEBUG)
  unittest.main()
