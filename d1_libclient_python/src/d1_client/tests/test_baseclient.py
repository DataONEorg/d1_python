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

import unittest

import d1_client.baseclient
import d1_client.tests.util
import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.exceptions
import d1_test.instance_generator
import d1_test.instance_generator.random_data
import d1_test.mock_api.catch_all
import d1_test.mock_api.describe
import d1_test.mock_api.generate_identifier
import d1_test.mock_api.get
import d1_test.mock_api.get_log_records
import d1_test.mock_api.get_system_metadata
import d1_test.mock_api.is_authorized
import d1_test.mock_api.list_objects
import d1_test.mock_api.ping
import requests.structures
import responses
import shared_settings


class TestDataONEBaseClient(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.baseclient.DataONEBaseClient(
      shared_settings.MN_RESPONSES_URL
    )

  def test_0010(self):
    """Able to instantiate DataONEBaseClient"""
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
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0][, count=1000]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.getLogRecords

  @responses.activate
  def test_0040(self):
    d1_test.mock_api.get_log_records.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertIsInstance(
      self.client.getLogRecords(),
      d1_common.types.dataoneTypes_v1_1.Log,
    )

  @responses.activate
  def test_0050(self):
    """MNRead.getLogRecords(): Returned type is Log"""
    d1_test.mock_api.get_log_records.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    # getLogRecords() verifies that the returned type is Log.
    return self.client.getLogRecords()

  @responses.activate
  def test_0060(self):
    """MNRead.getLogRecords(): Log has at least two entries"""
    d1_test.mock_api.get_log_records.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    log = self.client.getLogRecords()
    self.assertTrue(len(log.logEntry) >= 2)

  # CNCore.ping()
  # MNCore.ping()

  @responses.activate
  def test_0070(self):
    """ping(): Returns True"""
    d1_test.mock_api.ping.add_callback(shared_settings.MN_RESPONSES_URL)
    self.assertTrue(self.client.ping())

  @responses.activate
  def test_0080(self):
    """ping(): Passing a trigger header triggers a DataONEException"""
    d1_test.mock_api.ping.add_callback(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.ping,
      vendorSpecific={'trigger': '404'}
    )

  # CNRead.get()
  # MNRead.get()

  @responses.activate
  def test_0090(self):
    """CNRead.get(): Unknown PID raises NotFound"""
    d1_test.mock_api.get.add_callback(shared_settings.MN_RESPONSES_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.get, 'unknown_pid'
    )

  @responses.activate
  def test_0100(self):
    """MNRead.get(): Returns valid response on valid PID"""
    d1_test.mock_api.get.add_callback(shared_settings.MN_RESPONSES_URL)
    self.client.get('valid_pid')

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  @responses.activate
  def test_0110(self):
    """CNRead.getSystemMetadata(): Returns SystemMetadata type"""
    d1_test.mock_api.get_system_metadata.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    sysmeta_pyxb = self.client.getSystemMetadata('valid_pid')
    self.assertTrue(
      isinstance(
        sysmeta_pyxb, d1_common.types.dataoneTypes_v1_1.SystemMetadata
      )
    )

  @responses.activate
  def test_0120(self):
    """MNRead.getSystemMetadata(): Unknown PID raises NotFound"""
    d1_test.mock_api.get_system_metadata.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.getSystemMetadata,
      'unknown_pid'
    )

  # CNRead.describe()
  # MNRead.describe()

  @responses.activate
  def test_0130(self):
    """CNRead.describe(): GET request returns dict of D1 custom headers"""
    d1_test.mock_api.describe.add_callback(shared_settings.MN_RESPONSES_URL)
    description_dict = self.client.describe('good_pid')
    self.assertIsInstance(
      description_dict, requests.structures.CaseInsensitiveDict
    )
    self.assertIn('Last-Modified', description_dict)
    del description_dict['Last-Modified']
    expected_dict = {
      'Content-Length': '1024',
      'DataONE-SerialVersion': '3',
      'DataONE-Checksum': 'SHA-1,d4fa5f2a63c0df10d5e3b07f586d58dbb8e98d39',
      'DataONE-FormatId': u'application/octet-stream',
      u'Content-Type': 'application/octet-stream'
    }
    self.assertEqual(dict(description_dict), expected_dict)

  @responses.activate
  def test_0140(self):
    """CNRead.describe(): HEAD request for unknown PID raises NotFound"""
    d1_test.mock_api.describe.add_callback(shared_settings.MN_RESPONSES_URL)
    # describe() is a HEAD request, which can't return a body, so we use a
    # header representation of the DataONEException. This checks that
    # DataONEException headers are detected, deserialized and raised as
    # exceptions.
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.describe, 'unknown_pid'
    )

  # CNCore.listObjects()
  # MNCore.listObjects()

  @responses.activate
  def test_0150(self):
    """listObjects(): Returns a valid ObjectList that contains at least 3 entries"""
    d1_test.mock_api.list_objects.add_callback(shared_settings.MN_RESPONSES_URL)
    object_list_pyxb = self.client.listObjects()
    self.assertIsInstance(
      object_list_pyxb, d1_common.types.dataoneTypes_v1_1.ObjectList
    )
    self.assertEqual(object_list_pyxb.count, len(object_list_pyxb.objectInfo))
    entry = object_list_pyxb.objectInfo[0]
    self.assertIsInstance(
      entry.identifier, d1_common.types.dataoneTypes_v1_1.Identifier
    )
    self.assertIsInstance(
      entry.formatId, d1_common.types.dataoneTypes_v1_1.ObjectFormatIdentifier
    )

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  @d1_test.mock_api.catch_all.activate
  def test_0160(self):
    """CNRegister.generateIdentifier(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.MN_RESPONSES_URL)
    scheme_str = (
      'scheme_' + d1_test.instance_generator.random_data.random_3_words()
    )
    fragment_str = (
      'fragment_' + d1_test.instance_generator.random_data.random_3_words()
    )
    received_echo_dict = self.client.generateIdentifier(
      scheme_str, fragment_str
    )
    expected_echo_dict = {
      'request': {
        'endpoint_str': 'generate',
        'param_list': [],
        'pyxb_namespace': 'http://ns.dataone.org/service/types/v1.1',
        'query_dict': {},
        'version_tag': 'v1'
      },
      'wrapper': {
        'class_name': 'DataONEBaseClient',
        'expected_type': 'Identifier',
        'received_303_redirect': False,
        'vendor_specific_dict': None
      }
    }

    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, expected_echo_dict
    )

  @d1_test.mock_api.catch_all.activate
  def test_0170(self):
    """CNgenerateIdentifier.generateIdentifier(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(shared_settings.MN_RESPONSES_URL)
    scheme_str = (
      'scheme_' + d1_test.instance_generator.random_data.random_3_words()
    )
    fragment_str = (
      'fragment_' + d1_test.instance_generator.random_data.random_3_words()
    )

    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.generateIdentifier,
      scheme_str, fragment_str, vendorSpecific={'trigger': '404'}
    )

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  @responses.activate
  def test_0180(self):
    """isAuthorized(): Returns 200 for a readable PID"""
    d1_test.mock_api.is_authorized.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertTrue(self.client.isAuthorized('authorized_pid', 'read'))

  @responses.activate
  def test_0190(self):
    """isAuthorized(): Raises NotAuthorized for unauthorized PID"""
    d1_test.mock_api.is_authorized.add_callback(
      shared_settings.MN_RESPONSES_URL
    )
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized, self.client.isAuthorized,
      'unauthorized_pid', 'read'
    )
