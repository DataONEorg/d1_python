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
"""Unit tests for iter/objectlistmt
"""

# Stdlib
import sys
import unittest

# 3rd party
import responses

# App
sys.path.append('..')
import shared_settings # noqa: E402
import mock_object_list # noqa: E402
import iter.objectlistmt # noqa: E402

# These tests are disabled because they require a MN that permits access to
# log records.

MAX_OBJECTS = 20


class TestIterLogRecordMultithreaded(unittest.TestCase):
  """

  """

  def setUp(self):
    pass

  @responses.activate
  def test_100(self):
    mock_object_list.init(shared_settings.MN_RESPONSES_URL)

    object_list_iterator = iter.objectlistmt.multi_object_list_iterator(
      shared_settings.MN_RESPONSES_URL, page_size=123, max_workers=2,
      max_queue=10
    )

    print '4' * 100
    for object_info_pyxb in object_list_iterator:
      print '5' * 100
      print object_info_pyxb # .toxml()

    # client = d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url=shared_settings.MN_URL)
    # object_list_pyxb = client.listObjects(start=30, count=100)
    # print object_list_pyxb.count
    # for object_info_pyxb in object_list_pyxb.objectInfo:
    #   print object_info_pyxb.toxml()

    # assert resp.json() == {'value': 6}
    #
    # assert len(responses.calls) == 1
    # assert responses.calls[0].request.url == 'http://calc.com/sum'
    # assert responses.calls[0].response.text == '{"value": 6}'
    # assert (
    #   responses.calls[0].response.headers['request-id'] ==
    #   '728d329e-0e86-11e4-a748-0c84dc037c13'
    # )

    # def test_100(self):
    #   print 'test'
    #   """PageSize=5, start=0"""
    #   self._log_record_iterator_test(5, 0)
    # #
    # # def _test_110(self):
    # #   """PageSize=1, start=63"""
    # #   self._log_record_iterator_test(1, 6)
    # #
    # # def _test_130(self):
    # #   """PageSize=5, start=10, fromDate=2005-01-01"""
    # #   self._log_record_iterator_test(
    # #     2000, 0, from_date=datetime.datetime(2005, 1, 1)
    # #   )
    # #
    # def _log_record_iterator_test(
    #   self, page_size, start, from_date=None,
    #   to_date=None
    # ):
    #   client = d1_client.mnclient.MemberNodeClient(base_url=shared_settings.MN_URL)
    #   log_record_iterator = d1_client.logrecorditerator.LogRecordIterator(
    #     client,
    #     pageSize=page_size,
    #     start=start,
    #     fromDate=from_date,
    #     toDate=to_date
    #   )
    #   cnt = 0
    #   for event in log_record_iterator:
    #     self.assertIsInstance(event.event, dataoneTypes.Event)
    #     logging.info("Event      = {}".format(event.event))
    #     logging.info("Timestamp  = {}".format(event.dateLogged.isoformat()))
    #     logging.info("IP Addres  = {}".format(event.ipAddress))
    #     logging.info("Identifier = {}".format(event.identifier.value()))
    #     logging.info("User agent = {}".format(event.userAgent))
    #     logging.info("Subject    = {}".format(event.subject.value()))
    #     logging.info('-' * 79)
    #     cnt += 1
    #
    #     if cnt == MAX_OBJECTS:
    #       nTotalLogRecords = MAX_OBJECTS
    #       break
    #
    #   nTotalLogRecords = self._get_log_total_count(client, from_date, to_date)
    #   self.assertEqual(cnt, nTotalLogRecords - start)
    #
  def _get_log_total_count(self, client, from_date=None, to_date=None):
    return client.getLogRecords(
      start=0, count=0, fromDate=from_date, toDate=to_date
    ).total
