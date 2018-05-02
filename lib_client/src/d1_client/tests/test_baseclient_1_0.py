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

import pytest
import requests.structures
import responses

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
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

import d1_client.baseclient


class TestDataONEBaseClient(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """__init__()"""
    base_client = d1_client.baseclient.DataONEBaseClient(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    assert isinstance(base_client, d1_client.baseclient.DataONEBaseClient)

  def test_1010(self):
    """slice_sanity_check()"""
    cn_mn_client_v1 = d1_client.baseclient.DataONEBaseClient(
      "http://bogus.target/mn"
    )
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      cn_mn_client_v1._slice_sanity_check(-1, 0)
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      cn_mn_client_v1._slice_sanity_check(0, -1)
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      cn_mn_client_v1._slice_sanity_check(10, 'invalid_int')

  def test_1020(self):
    """date_span_sanity_check()"""
    cn_mn_client_v1 = d1_client.baseclient.DataONEBaseClient(
      "http://bogus.target/mn"
    )
    old_date = d1_common.date_time.create_utc_datetime(1970, 4, 3)
    new_date = d1_common.date_time.create_utc_datetime(2010, 10, 11)
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      cn_mn_client_v1._date_span_sanity_check(new_date, old_date)
    assert cn_mn_client_v1._date_span_sanity_check(old_date, new_date) is None

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords
  # MNCore.getLogRecords(session[, fromDate][, toDate][, event][, start=0][, count=1000]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/MN_APIs.html#MNCore.getLogRecords

  @responses.activate
  def test_1030(self, cn_mn_client_v1):
    """MNCore.getLogRecords(): Returned type is Log"""
    d1_test.mock_api.get_log_records.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    assert isinstance(
      cn_mn_client_v1.getLogRecords(), cn_mn_client_v1.bindings.Log
    )

  @responses.activate
  def test_1040(self, cn_mn_client_v1):
    """MNCore.getLogRecords(): Log has at least two entries"""
    d1_test.mock_api.get_log_records.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    log = cn_mn_client_v1.getLogRecords()
    assert len(log.logEntry) >= 2

  # CNCore.ping()
  # MNCore.ping()

  @responses.activate
  def test_1050(self, cn_mn_client_v1):
    """ping(): Returns True"""
    d1_test.mock_api.ping.add_callback(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)
    assert cn_mn_client_v1.ping()

  @responses.activate
  def test_1060(self, cn_mn_client_v1):
    """ping(): Passing a trigger header triggers a DataONEException"""
    d1_test.mock_api.ping.add_callback(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.ping(vendorSpecific={'trigger': '404'})

  # CNRead.get()
  # MNRead.get()

  @responses.activate
  def test_1070(self, cn_mn_client_v1):
    """CNRead.get(): Unknown PID raises NotFound"""
    d1_test.mock_api.get.add_callback(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.get('<NotFound>pid')

  @responses.activate
  def test_1080(self, cn_mn_client_v1):
    """MNRead.get(): Returns valid response on valid PID"""
    d1_test.mock_api.get.add_callback(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)
    cn_mn_client_v1.get('valid_pid')

  # CNRead.getSystemMetadata()
  # MNRead.getSystemMetadata()

  @responses.activate
  def test_1090(self, cn_mn_client_v1):
    """CNRead.getSystemMetadata(): Returns SystemMetadata type"""
    d1_test.mock_api.get_system_metadata.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    sysmeta_pyxb = cn_mn_client_v1.getSystemMetadata('valid_pid')
    assert isinstance(sysmeta_pyxb, cn_mn_client_v1.bindings.SystemMetadata)

  @responses.activate
  def test_1100(self, cn_mn_client_v1):
    """MNRead.getSystemMetadata(): Unknown PID raises NotFound"""
    d1_test.mock_api.get_system_metadata.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.getSystemMetadata('<NotFound>pid')

  # CNRead.describe()
  # MNRead.describe()

  @responses.activate
  def test_1110(self, cn_mn_client_v1):
    """CNRead.describe(): GET request returns dict of D1 custom headers"""
    d1_test.mock_api.describe.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    description_dict = cn_mn_client_v1.describe('good_pid')
    assert isinstance(description_dict, requests.structures.CaseInsensitiveDict)
    assert 'Last-Modified' in description_dict
    del description_dict['Last-Modified']
    self.sample.assert_equals(description_dict, 'describe_returns_dict')

  @responses.activate
  def test_1120(self, cn_mn_client_v1):
    """CNRead.describe(): HEAD request for unknown PID raises NotFound"""
    d1_test.mock_api.describe.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    # describe() is a HEAD request, which can't return a body, so we use a
    # header representation of the DataONEException. This checks that
    # DataONEException headers are detected, deserialized and raised as
    # exceptions.
    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.describe('<NotFound>pid')

  # CNCore.listObjects()
  # MNCore.listObjects()

  @responses.activate
  def test_1130(self, cn_mn_client_v1):
    """listObjects(): Returns a valid ObjectList that contains at least 3 entries"""
    # cn_mn_client_v1 = api
    d1_test.mock_api.list_objects.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    object_list_pyxb = cn_mn_client_v1.listObjects()
    assert isinstance(object_list_pyxb, cn_mn_client_v1.bindings.ObjectList)
    assert object_list_pyxb.count == len(object_list_pyxb.objectInfo)
    entry = object_list_pyxb.objectInfo[0]
    assert isinstance(entry.identifier, cn_mn_client_v1.bindings.Identifier)
    assert isinstance(
      entry.formatId, cn_mn_client_v1.bindings.ObjectFormatIdentifier
    )

  # CNCore.generateIdentifier()
  # MNStorage.generateIdentifier()

  @responses.activate
  def test_1140(self, cn_mn_client_v1):
    """CNRegister.generateIdentifier(): Generates expected REST query"""
    d1_test.mock_api.generate_identifier.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    fragment_str = (
      'fragment_' + d1_test.instance_generator.random_data.random_3_words()
    )
    identifier_pyxb = cn_mn_client_v1.generateIdentifier('UUID', fragment_str)
    self.sample.assert_equals(
      identifier_pyxb, 'generate_identifier', cn_mn_client_v1
    )

  @responses.activate
  def test_1150(self, cn_mn_client_v1):
    """CNRegister.generateIdentifier(): Converts DataONEException XML doc to
    exception"""
    d1_test.mock_api.generate_identifier.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    scheme_str = (
      'scheme_' + d1_test.instance_generator.random_data.random_3_words()
    )
    fragment_str = (
      'fragment_' + d1_test.instance_generator.random_data.random_3_words()
    )

    with pytest.raises(d1_common.types.exceptions.NotFound):
      cn_mn_client_v1.generateIdentifier(
        scheme_str, fragment_str, vendorSpecific={'trigger': '404'}
      )

  # CNAuthorization.isAuthorized()
  # MNAuthorization.isAuthorized()

  @responses.activate
  def test_1160(self, cn_mn_client_v1):
    """isAuthorized(): Returns 200 for a readable PID"""
    d1_test.mock_api.is_authorized.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    assert cn_mn_client_v1.isAuthorized('authorized_pid', 'read')

  @responses.activate
  def test_1170(self, cn_mn_client_v1):
    """isAuthorized(): Returns True if authorized, else False"""
    d1_test.mock_api.is_authorized.add_callback(
      d1_test.d1_test_case.MOCK_CN_MN_BASE_URL
    )
    assert cn_mn_client_v1.isAuthorized('authorized_pid', 'read')
    assert not cn_mn_client_v1.isAuthorized(
      'unauthorized_pid', 'read', vendorSpecific={'trigger': '401'}
    )
