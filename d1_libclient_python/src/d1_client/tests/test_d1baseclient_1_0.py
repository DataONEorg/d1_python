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
'''Module d1_client.tests.test_d1baseclient
===========================================

:Synopsis: Unit tests for d1_client.d1baseclient.
:Created: 2011-01-20
:Author: DataONE (Vieglais, Dahl)
'''

# TODO: Tests disabled with "WAITING_FOR_TEST_ENV_" are disabled until a
# stable testing environment is available.

# Stdlib.
import logging
import sys
import unittest

# D1.
sys.path.append('..')
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.types.dataoneTypes as dataoneTypes
import d1_client.d1baseclient

# App.
import settings


class TestDataONEBaseClientV1(TestCaseWithURLCompare):
  def test_010_v1(self):
    '''_slice_sanity_check()'''
    client = d1_client.d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, -1, 0
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 0, -1
    )
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._slice_sanity_check, 10,
      'invalid_int'
    )

  def test_020_v1(self):
    '''_date_span_sanity_check()'''
    client = d1_client.d1baseclient.DataONEBaseClient("http://bogus.target/mn")
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest, client._date_span_sanity_check, new_date,
      old_date
    )
    self.assertEqual(None, client._date_span_sanity_check(old_date, new_date))

  def test_030_v1(self):
    '''_rest_url()'''
    client = d1_client.d1baseclient.DataONEBaseClient(
      "http://bogus.target/mn", version='v1'
    )
    self.assertEqual(
      '/mn/v1/object/1234xyz',
      client._rest_url('object/%(pid)s', pid='1234xyz')
    )
    self.assertEqual(
      '/mn/v1/object/1234%2Fxyz',
      client._rest_url('object/%(pid)s', pid='1234/xyz')
    )
    self.assertEqual(
      '/mn/v1/meta/1234xyz',
      client._rest_url('meta/%(pid)s', pid='1234xyz')
    )
    self.assertEqual('/mn/v1/log', client._rest_url('log'))

  def test_040_v1(self):
    '''get_schema_version()'''
    client = d1_client.d1baseclient.DataONEBaseClient(settings.CN_URL)
    version = client.get_schema_version()
    self.assertTrue(version in ('v1', 'v2', 'v3'))

  # CNCore.getLogRecords()
  # MNCore.getLogRecords()

  def _getLogRecords_v1(self, base_url):
    '''getLogRecords() returns a valid Log. CNs will return an empty log for public connections'''
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    log = client.getLogRecords()
    self.assertTrue(isinstance(log, d1_common.types.dataoneTypes.Log))
    return log

  def test_110_v1(self):
    '''CNCore.getLogRecords()'''
    # 10/17/13: Currently broken. Add back in, in 1/2 year.
    # self._getLogRecords_v1(CN_URL)

  def test_120_v1(self):
    '''MNRead.getLogRecords()'''
    log = self._getLogRecords_v1(settings.MN_URL)
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  def _ping_v1(self, base_url):
    '''ping()'''
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    self.assertTrue(client.ping())

  def test_200_v1(self):
    '''ping() CN'''
    self._ping_v1(settings.CN_URL)

  def test_210_v1(self):
    '''ping() MN'''
    self._ping_v1(settings.MN_URL)

  # CNRead.get()
  # MNRead.get()

  def _get_v1(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    response = client.get(pid)
    self.assertTrue(response.read() > 0)

  def WAITING_FOR_TEST_ENV_test_410(self):
    '''CNRead.get()'''
    self._get(settings.CN_URL)
    self.assertRaises(d1_common.types.exceptions.NotFound, self._get, settings.CN_URL, True)

  def WAITING_FOR_TEST_ENV_test_420(self):
    '''MNRead.get()'''
    self._get(settings.MN_URL)
    self.assertRaises(d1_common.types.exceptions.NotFound, self._get, settings.MN_URL, True)

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  def _get_sysmeta(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    sysmeta = client.getSystemMetadata(pid)
    self.assertTrue(isinstance(sysmeta, d1_common.types.dataoneTypes_v1_1.SystemMetadata))

  def WAITING_FOR_TEST_ENV_test_510(self):
    '''CNRead.getSystemMetadata()'''
    self._get_sysmeta(settings.CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, settings.CN_URL, True
    )

  def WAITING_FOR_TEST_ENV_test_520(self):
    '''MNRead.getSystemMetadata()'''
    self._get_sysmeta(settings.MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_sysmeta, settings.MN_URL, True
    )

  # CNRead.describe()
  # MNRead.describe()

  def _describe(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_4589734958791283794565'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    headers = client.describe(pid)

  def WAITING_FOR_TEST_ENV_test_610(self):
    '''CNRead.describe()'''
    self._describe(settings.CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      settings.CN_URL,
      invalid_pid=True
    )

  def WAITING_FOR_TEST_ENV_test_620(self):
    '''MNRead.describe()'''
    self._describe(settings.MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure,
      self._describe,
      settings.MN_URL,
      invalid_pid=True
    )

  # CNRead.getChecksum()
  # MNRead.getChecksum()

  def _get_checksum(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    checksum = client.getChecksum(pid)
    self.assertTrue(isinstance(checksum, d1_common.types.dataoneTypes_v1_1.Checksum))

  def WAITING_FOR_TEST_ENV_test_710(self):
    '''CNRead.getChecksum()'''
    self._get_checksum(settings.CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, settings.CN_URL, True
    )

  def WAITING_FOR_TEST_ENV_test_720(self):
    '''MNRead.getChecksum()'''
    self._get_checksum(settings.MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._get_checksum, settings.MN_URL, True
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  def _listObjects(self, baseURL):
    '''listObjects() returns a valid ObjectList that contains at least 3 entries'''
    client = d1_client.d1baseclient.DataONEBaseClient(baseURL)
    list = client.listObjects(start=0, count=10, fromDate=None, toDate=None)
    self.assertTrue(isinstance(list, d1_common.types.dataoneTypes_v1_1.ObjectList))
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

  def WAITING_FOR_TEST_ENV_test_810(self):
    '''CNCore.listObjects()'''
    self._listObjects(settings.CN_URL)

  def WAITING_FOR_TEST_ENV_test_820(self):
    '''MNCore.listObjects()'''
    self._listObjects(settings.MN_URL)

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  def _test_1050_A(self):
    '''generateIdentifier(): Returns a valid identifier that matches scheme and fragment'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    client = d1_client.d1baseclient.DataONEBaseClient(self.options.gmn_url)
    identifier = client.generateIdentifier('UUID', testing_context.test_fragment)
    testing_context.generated_identifier = identifier.value()

  def _test_1050_B(self):
    '''generateIdentifier(): Returns a different, valid identifier when called second time'''
    testing_context.test_fragment = 'test_reserve_identifier_' + \
        d1_instance_generator.random_data.random_3_words()
    identifier = self.client.generateIdentifier('UUID', testing_context.test_fragment)
    self.assertNotEqual(testing_context.generated_identifier, identifier.value())

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  def _is_authorized(self, base_url, invalid_pid=False):
    client = d1_client.d1baseclient.DataONEBaseClient(base_url)
    if invalid_pid:
      pid = '_bogus_pid_845434598734598374534958'
    else:
      pid = testing_utilities.get_random_valid_pid(client)
    auth = client.isAuthorized(pid, 'read')
    self.assertTrue(isinstance(auth, bool))

  def WAITING_FOR_TEST_ENV_test_910(self):
    '''CNAuthorization.isAuthorized()'''
    self._is_authorized(settings.CN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, settings.CN_URL, True
    )

  def WAITING_FOR_TEST_ENV_test_920(self):
    '''MNAuthorization.isAuthorized()'''
    self._is_authorized(settings.MN_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self._is_authorized, settings.MN_URL, True
    )
