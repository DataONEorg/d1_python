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
"""Test conversions of System Metadata between PyXB and database
"""

from __future__ import absolute_import

import d1_client.mnclient_2_0
import d1_common.system_metadata
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml
import d1_test.mock_api.django_client
import d1_test.mock_api.get
import responses
import tests.d1_test_case
import tests.util

BASE_URL = 'http://mock/mn'
# Mocked 3rd party server for object byte streams
REMOTE_URL = 'http://remote/'
INVALID_URL = 'http://invalid/'


class TestSysMeta(tests.d1_test_case.D1TestCase):
  def setUp(self):
    d1_common.util.log_setup(is_debug=True)
    d1_test.mock_api.django_client.add_callback(BASE_URL)
    d1_test.mock_api.get.add_callback(REMOTE_URL)

  @responses.activate
  def test_0010(self):
    """v2 SysMeta: Roundtrip of fully populated System Metadata"""
    # Prepare fully populated sysmeta
    orig_sysmeta_pyxb = tests.util.read_test_xml('systemMetadata_v2_0.xml')
    #print d1_common.xml.pretty_pyxb(orig_sysmeta_pyxb)
    pid = self.random_pid()
    sciobj_str = 'sciobj bytes for pid="{}"'.format(pid)
    orig_sysmeta_pyxb.checksum = self.create_checksum_object_from_string(
      sciobj_str
    )
    orig_sysmeta_pyxb.size = len(sciobj_str)
    orig_sysmeta_pyxb.obsoletes = None
    orig_sysmeta_pyxb.obsoletedBy = None
    orig_sysmeta_pyxb.identifier = pid
    orig_sysmeta_pyxb.replica = None
    orig_sysmeta_pyxb.submitter = 'public'
    orig_sysmeta_pyxb.serialVersion = 1
    orig_sysmeta_pyxb.originMemberNode = 'urn:node:mnDevGMN'
    orig_sysmeta_pyxb.authoritativeMemberNode = 'urn:node:mnDevGMN'
    orig_sysmeta_pyxb.archived = False
    # Create
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
    client.create(
      pid, sciobj_str, orig_sysmeta_pyxb, vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    # Retrieve
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
    retrieved_sysmeta_pyxb = client.getSystemMetadata(
      pid, vendorSpecific=self.
      include_subjects(tests.gmn_test_client.GMN_TEST_SUBJECT_TRUSTED)
    )
    # Compare
    d1_common.system_metadata.normalize(
      orig_sysmeta_pyxb, reset_timestamps=True
    )
    d1_common.system_metadata.normalize(
      retrieved_sysmeta_pyxb, reset_timestamps=True
    )
    # self.kdiff_pyxb(orig_sysmeta_pyxb, retrieved_sysmeta_pyxb)
    self.assertTrue(
      d1_common.system_metadata.
      is_equivalent_pyxb(orig_sysmeta_pyxb, retrieved_sysmeta_pyxb)
    )
