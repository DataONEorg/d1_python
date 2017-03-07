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
"""Module d1_client.tests.test_logrecorditerator
================================================

Unit tests for LogRecordIterator.

:Created:
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import datetime
import logging
import unittest
import sys

# D1
import d1_common.types.dataoneTypes as dataoneTypes

# App
sys.path.append('..')
import d1_client.mnclient # noqa: E402
import d1_client.logrecorditerator # noqa: E402
import d1_client.cnclient # noqa: E402
import shared_settings # noqa: E402

# These tests are disabled because they require a MN that permits access to
# log records.

MAX_OBJECTS = 20


class TestLogRecordIterator(unittest.TestCase):
  """"""

  def setUp(self):
    pass

  def test_100(self):
    """PageSize=5, start=0"""
    self._log_record_iterator_test(5, 0)

  def _test_110(self):
    """PageSize=1, start=63"""
    self._log_record_iterator_test(1, 6)

  def _test_130(self):
    """PageSize=5, start=10, fromDate=2005-01-01"""
    self._log_record_iterator_test(
      2000, 0, from_date=datetime.datetime(2005, 1, 1)
    )

  def _log_record_iterator_test(
      self, page_size, start, from_date=None, to_date=None
  ):
    client = d1_client.mnclient.MemberNodeClient(
      base_url=shared_settings.MN_RESPONSES_URL
    )
    total = self._get_log_total_count(client, from_date, to_date)
    log_record_iterator = d1_client.logrecorditerator.LogRecordIterator(
      client, pageSize=page_size, start=start, fromDate=from_date,
      toDate=to_date
    )
    cnt = 0
    for event in log_record_iterator:
      self.assertIsInstance(event.event, dataoneTypes.Event)
      logging.info("Event      = {}".format(event.event))
      logging.info("Timestamp  = {}".format(event.dateLogged.isoformat()))
      logging.info("IP Addres  = {}".format(event.ipAddress))
      logging.info("Identifier = {}".format(event.identifier.value()))
      logging.info("User agent = {}".format(event.userAgent))
      logging.info("Subject    = {}".format(event.subject.value()))
      logging.info('-' * 79)
      cnt += 1

      if cnt == MAX_OBJECTS:
        total = MAX_OBJECTS
        break

    self.assertEqual(cnt, total - start)

  def _get_log_total_count(self, client, from_date, to_date):
    return client.getLogRecords(
      start=0, count=0, fromDate=from_date, toDate=to_date
    ).total
