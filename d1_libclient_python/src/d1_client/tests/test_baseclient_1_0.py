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
"""Module d1_client.tests.test_baseclient_v1
==============================================

:Synopsis: Unit tests for d1_client.baseclient.
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
"""

# Stdlib
import sys
import unittest

# D1
import d1_client.tests.util
import d1_common.test_case_with_url_compare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes_v1_1
import d1_test.instance_generator

# App
sys.path.append('..')
import d1_client.baseclient # noqa: E402
import shared_context # noqa: E402
import shared_settings # noqa: E402


class TestDataONEBaseClientV1(
    d1_common.test_case_with_url_compare.TestCaseWithURLCompare
):
  def test_010(self):
    """_slice_sanity_check()"""
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

  def test_020(self):
    """_date_span_sanity_check()"""
    client = d1_client.baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check,
      new_date, old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  # CNCore.getLogRecords()
  # MNCore.getLogRecords()

  def _getLogRecords(self, base_url):
    """getLogRecords() returns a valid Log. CNs will return an empty log for public connections"""
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    log = client.getLogRecords()
    self.assertIsInstance(log, d1_common.types.dataoneTypes_v1_1.Log)
    # checksum, d1_common.types.dataoneTypes_v1_1.Checksum
    return log

  def test_110(self):
    """CNCore.getLogRecords()"""
    # 10/17/13: Currently broken. Add back in, in 1/2 year.
    # self._getLogRecords_v1(CN_URL)

  def test_120(self):
    """MNRead.getLogRecords()"""
    log = self._getLogRecords(shared_settings.MN_RESPONSES_URL)
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  def _ping(self, base_url):
    """ping()"""
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    self.assertTrue(client.ping())

  def test_200(self):
    """ping() CN"""
    self._ping(shared_settings.CN_RESPONSES_URL)

  def test_210(self):
    """ping() MN"""
    self._ping(shared_settings.MN_RESPONSES_URL)

  # CNRead.get()
  # MNRead.get()

  def _get_v1(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = d1_client.tests.util.get_random_valid_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_410(self):
    """CNRead.get()"""
    self._get(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_420(self):
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
      pid = d1_client.tests.util.get_random_valid_pid(client)
    sysmeta_pyxb = client.getSystemMetadata(pid)
    self.assertIsInstance(
      sysmeta_pyxb, d1_common.types.dataoneTypes_v1_1.SystemMetadata
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_510(self):
    """CNRead.getSystemMetadata()"""
    self._get_sysmeta(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_520(self):
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
      pid = d1_client.tests.util.get_random_valid_pid(client)
    # headers =
    client.describe(pid)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_610(self):
    """CNRead.describe()"""
    self._describe(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.CN_RESPONSES_URL, invalid_pid=True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_620(self):
    """MNRead.describe()"""
    self._describe(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self._describe,
      shared_settings.MN_RESPONSES_URL, invalid_pid=True
    )

  # CNRead.getChecksum()
  # MNRead.getChecksum()

  def _get_checksum(self, base_url, invalid_pid=False):
    client = d1_client.baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = d1_client.tests.util.get_random_valid_pid(client)
    checksum = client.getChecksum(pid)
    self.assertTrue(
      isinstance(checksum, d1_common.types.dataoneTypes_v1_1.Checksum)
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_710(self):
    """CNRead.getChecksum()"""
    self._get_checksum(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_720(self):
    """MNRead.getChecksum()"""
    self._get_checksum(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum,
      shared_settings.MN_RESPONSES_URL, True
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
  def test_810(self):
    """CNCore.listObjects()"""
    self._listObjects(shared_settings.CN_RESPONSES_URL)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_820(self):
    """MNCore.listObjects()"""
    self._listObjects(shared_settings.MN_RESPONSES_URL)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  @unittest.skip("TODO: Check why disabled")
  def test_1050_A(self):
    """generateIdentifier(): Returns a valid identifier that matches scheme and fragment"""
    shared_context.test_fragment = (
      'test_reserve_identifier_' +
      d1_test.instance_generator.random_data.random_3_words()
    )
    client = d1_client.baseclient.DataONEBaseClient(self.options.gmn_url)
    identifier = client.generateIdentifier('UUID', shared_context.test_fragment)
    shared_context.generated_identifier = identifier.value()

  @unittest.skip("TODO: Check why disabled")
  def test_1050_B(self):
    """generateIdentifier(): Returns a different, valid identifier when called second time"""
    shared_context.test_fragment = (
      'test_reserve_identifier_' +
      d1_test.instance_generator.random_data.random_3_words()
    )
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
      pid = d1_client.tests.util.get_random_valid_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertIsInstance(auth, bool)

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_910(self):
    """CNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.CN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.CN_RESPONSES_URL, True
    )

  @unittest.skip(
    "TODO: Skipped due to waiting for test env. Should set up test env or remove"
  )
  def test_920(self):
    """MNAuthorization.isAuthorized()"""
    self._is_authorized(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized,
      shared_settings.MN_RESPONSES_URL, True
    )
