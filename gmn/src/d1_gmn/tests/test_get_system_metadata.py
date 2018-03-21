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
"""Test MNRead.getSystemMetadata()
"""

import io

import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.checksum
import d1_common.system_metadata
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.sciobj
import d1_test.mock_api.django_client
import d1_test.mock_api.get


class TestGetSystemMetadata(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self):
    """getSystemMetadata(): Non-existing object raises NotFound"""

    def test(client):
      with pytest.raises(d1_common.types.exceptions.NotFound):
        client.getSystemMetadata('_invalid_pid_')

    with d1_gmn.tests.gmn_mock.disable_auth():
      test(self.client_v1)
      test(self.client_v2)

  @responses.activate
  def test_1010(self):
    """SysMeta: Roundtrip of fully populated System Metadata"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Prepare fully populated sysmeta
      orig_sysmeta_pyxb = self.sample.load_xml_to_pyxb(
        'systemMetadata_v2_0.xml'
      )
      pid = d1_test.instance_generator.identifier.generate_pid()
      sciobj_bytes = d1_test.instance_generator.sciobj.generate_reproducible_sciobj_bytes(
        pid
      )
      orig_sysmeta_pyxb.checksum = d1_common.checksum.create_checksum_object_from_string(
        sciobj_bytes
      )
      orig_sysmeta_pyxb.size = len(sciobj_bytes)
      orig_sysmeta_pyxb.obsoletes = None
      orig_sysmeta_pyxb.obsoletedBy = None
      orig_sysmeta_pyxb.identifier = pid
      # orig_sysmeta_pyxb.replica = None
      orig_sysmeta_pyxb.submitter = 'public'
      orig_sysmeta_pyxb.serialVersion = 1
      orig_sysmeta_pyxb.originMemberNode = 'urn:node:mnDevGMN'
      orig_sysmeta_pyxb.authoritativeMemberNode = 'urn:node:mnDevGMN'
      orig_sysmeta_pyxb.archived = False
      # Create
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        self.call_d1_client(
          self.client_v2.create, pid,
          io.BytesIO(sciobj_bytes), orig_sysmeta_pyxb
        )
      # Retrieve
      recv_sysmeta_pyxb = self.call_d1_client(
        self.client_v2.getSystemMetadata, pid
      )
      # Compare
      d1_common.system_metadata.normalize_in_place(
        orig_sysmeta_pyxb, reset_timestamps=True
      )
      d1_common.system_metadata.normalize_in_place(
        recv_sysmeta_pyxb, reset_timestamps=True
      )
      # self.kdiff_pyxb(orig_sysmeta_pyxb, recv_sysmeta_pyxb)
      assert d1_common.system_metadata. \
        are_equivalent_pyxb(orig_sysmeta_pyxb, recv_sysmeta_pyxb)
