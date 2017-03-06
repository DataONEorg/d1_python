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

# Stdlib
import logging
import mock
import StringIO
import sys
import unittest

# 3rd party
import responses # pip install responses
import requests

# D1
import d1_common.test_case_with_url_compare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

# App
sys.path.append('..')
import d1_client.baseclient
import mock_log_records
import shared_settings


class TestDataONEBaseClient(
  d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
  def setUp(self):
    mock_log_records.init(shared_settings.MN_RESPONSES_URL)
    self.client = d1_client.baseclient.DataONEBaseClient(
      shared_settings.MN_RESPONSES_URL
    )

  def test_0010(self):
    """Able to instantiate DataONEBaseClient
    """
    base_client = d1_client.baseclient.DataONEBaseClient(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertTrue(
      isinstance(base_client, d1_client.baseclient.DataONEBaseClient)
    )

  def test_0020(self):
    """slice_sanity_check()"""
    client = d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, -1,
      0
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 0,
      -1
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 10,
      'invalid_int'
    )

  def test_0030(self):
    """date_span_sanity_check()"""
    client = d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check,
      new_date, old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0][, count=1000]) → Log
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html#MNCore.getLogRecords

  @responses.activate
  def test_0100(self):
    log_records_pyxb = self.client.getLogRecords()
    print log_records_pyxb.toxml()

  def _getLogRecords(self):
    """getLogRecords() returns a valid Log."""
    # getLogRecords() verifies that the returned type is Log.
    return client.getLogRecords()

  def test_0550(self):
    """getLogRecords()"""
    self._getLogRecords(shared_settings.CN_RESPONSES_URL)

  @unittest.skip(
    "Need a permanent MN that allows public access to getLogRecords"
  )
  def test_0700(self):
    """MNRead.getLogRecords()"""
    log = self._getLogRecords(shared_settings.MN_RESPONSES_URL)
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  def _ping(self, base_url):
    """ping()"""
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    self.assertTrue(client.ping())

  def test_0710(self):
    """ping() CN"""
    self._ping(shared_settings.CN_RESPONSES_URL)

  def test_0720(self):
    """ping() MN"""
    self._ping(shared_settings.MN_RESPONSES_URL)

  # CNRead.get()
  # MNRead.get()

  def _get(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = util.get_random_valid_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  def test_0730(self):
    """CNRead.get()"""
    self._get(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get,
      shared_settings.MN_RESPONSES_URL, True
    )

  def test_0440(self):
    """MNRead.get()"""
    self._get(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get,
      shared_settings.MN_RESPONSES_URL, True
    )

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  def _get_sysmeta(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = util.get_random_valid_pid(client)
    sysmeta_pyxb = client.getSystemMetadata(pid)
    self.assertTrue(
      isinstance(
        sysmeta_pyxb, d1_common.types.dataoneTypes_v1_1.SystemMetadata
      )
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0510(self):
    """CNRead.getSystemMetadata()"""
    self._get_sysmeta(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0800(self):
    """MNRead.getSystemMetadata()"""
    self._get_sysmeta(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta,
      shared_settings.MN_RESPONSES_URL, True
    )

  # CNRead.describe()
  # MNRead.describe()

  def _describe(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_4589734958791283794565'
    else:
      pid = util.get_random_valid_pid(client)
    headers = client.describe(pid)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0610(self):
    """CNRead.describe()"""
    self._describe(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.CN_RESPONSES_URL, invalid_pid=True
    )

  @unittest.skip("TODO: Check why this has been disabled")
  def test_0620(self):
    """MNRead.describe()"""
    self._describe(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.MN_RESPONSES_URL, invalid_pid=True
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  def _listObjects(self, baseURL):
    """listObjects() returns a valid ObjectList that contains at least 3 entries"""
    client = d1_client.baseclient.DataONEBaseClient(baseURL)
    list = client.listObjects(start=0, count=10, fromDate=None, toDate=None)
    self.assertTrue(
      isinstance(list, d1_common.types.dataoneTypes_v1_1.ObjectList)
    )
    self.assertEqual(list.count, len(list.objectInfo))
    entry = list.objectInfo[0]
    self.assertTrue(
      isinstance(
        entry.identifier, d1_common.types.dataoneTypes_v1_1.Identifier
      )
    )
    self.assertTrue(
      isinstance(
        entry.formatId, d1_common.types.dataoneTypes_v1_1.ObjectFormatIdentifier
      )
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0810(self):
    """CNCore.listObjects()"""
    self._listObjects(shared_settings.CN_RESPONSES_URL)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0820(self):
    """MNCore.listObjects()"""
    self._listObjects(shared_settings.MN_RESPONSES_URL)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  @unittest.skip("TODO: Check why this is skipped")
  def test_1050_A(self):
    """generateIdentifier(): Returns a valid identifier that matches scheme and fragment"""
    shared_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    client = d1_client.baseclient.DataONEBaseClient(self.options.gmn_url)
    identifier = client.generateIdentifier('UUID', shared_context.test_fragment)
    shared_context.generated_identifier = identifier.value()

  @unittest.skip("TODO: Check why this is skipped")
  def test_1050_B(self):
    """generateIdentifier(): Returns a different, valid identifier when called second time"""
    shared_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    identifier = self.client.generateIdentifier(
      'UUID', shared_context.test_fragment
    )
    self.assertNotEqual(shared_context.generated_identifier, identifier.value())

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  def _is_authorized(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = util.get_random_valid_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertIsInstance(auth, bool)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0910(self):
    """CNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_0920(self):
    """MNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.MN_RESPONSES_URL, True
    )
