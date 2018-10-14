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

import io

import freezegun
import OpenSSL
import pytest

import d1_common
import d1_common.const

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.mock_api.catch_all

import d1_client.cnclient_2_0


@d1_test.d1_test_case.reproducible_random_decorator('TestCNClient20')
@freezegun.freeze_time('2030-02-01')
class TestCNClient_2_0(d1_test.d1_test_case.D1TestCase):
  def test_1000(self, cn_client_v2):
    """__init__()"""
    assert isinstance(
      cn_client_v2, d1_client.cnclient_2_0.CoordinatingNodeClient_2_0
    )

  # CNCore.delete(session, id) → Identifier

  @d1_test.mock_api.catch_all.activate
  def test_1010(self, cn_client_v2):
    """delete(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v2.delete('valid_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'delete', cn_client_v2
    )

  # CNView.view(session, theme, id) → OctetStream

  @d1_test.mock_api.catch_all.activate
  def test_1020(self, cn_client_v2):
    """view(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v2.view('valid_theme', 'valid_pid')
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'view', cn_client_v2
    )

  # CNView.listViews(session) → OptionList

  @d1_test.mock_api.catch_all.activate
  def test_1030(self, cn_client_v2):
    """listViews(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    received_echo_dict = cn_client_v2.listViews()
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'list_views', cn_client_v2
    )

  # CNDiagnostic.echoCredentials(session) → SubjectInfo

  @d1_test.mock_api.catch_all.activate
  def test_1040(self, cn_client_v2):
    """echoCredentials(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    subject_info = cn_client_v2.echoCredentials()
    d1_test.mock_api.catch_all.assert_expected_echo(
      subject_info, 'echo_credentials_echo', cn_client_v2
    )

  def test_1050(self):
    """echoCredentials(): Live test against prod env: Invalid cert"""
    live_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      base_url=d1_common.const.URL_DATAONE_ROOT, cert_pem_path=self.sample.
      get_path('cert_with_equivalents_invalid_serialization.pem')
    )
    with pytest.raises(OpenSSL.SSL.Error) as exc_info:
      live_client.echoCredentials()
    assert 'SSL_CTX_use_PrivateKey_file' in str(exc_info)

  # CNDiagnostic.echoSystemMetadata(session, sysmeta) → SystemMetadata

  @d1_test.mock_api.catch_all.activate
  def test_1060(self, cn_client_v2):
    """echoSystemMetadata(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    sysmeta_pyxb = self.sample.load_xml_to_pyxb('systemMetadata_v2_0.xml')
    recv_sysmeta_pyxb = cn_client_v2.echoSystemMetadata(sysmeta_pyxb)
    d1_test.mock_api.catch_all.assert_expected_echo(
      recv_sysmeta_pyxb, 'system_metadata_echo', cn_client_v2
    )

  def test_1070(self):
    """echoSystemMetadata(): Live test against prod env"""
    sysmeta_pyxb = self.sample.load_xml_to_pyxb('systemMetadata_v2_0.xml')
    live_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      base_url=d1_common.const.URL_DATAONE_ROOT
    )
    recv_sysmeta_pyxb = live_client.echoSystemMetadata(sysmeta_pyxb)
    self.sample.assert_equals(recv_sysmeta_pyxb, 'system_metadata_live')

  # CNDiagnostic.echoIndexedObject(session, queryEngine, sysmeta, object) → OctetStream

  @d1_test.mock_api.catch_all.activate
  def test_1080(self, cn_client_v2):
    """echoIndexedObject(): Generates expected REST call"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_CN_BASE_URL
    )
    pid, sid, sciobj_bytes, sysmeta_pyxb = (
      d1_test.instance_generator.sciobj.
      generate_reproducible_sciobj_with_sysmeta(cn_client_v2)
    )
    echo_dict = cn_client_v2.echoIndexedObject(
      'solr', sysmeta_pyxb, io.BytesIO(sciobj_bytes)
    )
    d1_test.mock_api.catch_all.delete_volatile_post_keys(echo_dict)
    self.sample.assert_equals(echo_dict, 'echo_indexed_object_echo')

  def test_1090(
      self,
  ):
    """echoIndexedObject(): Live test against prod env"""
    live_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      base_url=d1_common.const.URL_DATAONE_ROOT
    )
    pid, sid, sciobj_bytes, sysmeta_pyxb = (
      d1_test.instance_generator.sciobj.
      generate_reproducible_sciobj_with_sysmeta(live_client)
    )
    response = live_client.echoIndexedObject(
      'solr', sysmeta_pyxb, io.BytesIO(sciobj_bytes)
    )
    self.sample.assert_equals(response.content, 'echo_indexed_object_live')
