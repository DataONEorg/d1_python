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

import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.instance_generator.access_policy
import d1_test.instance_generator.identifier
import d1_test.instance_generator.node_ref
import d1_test.instance_generator.person
import d1_test.instance_generator.random_data
import d1_test.instance_generator.replica
import d1_test.instance_generator.replication_policy
import d1_test.instance_generator.replication_status
import d1_test.instance_generator.subject
import d1_test.instance_generator.system_metadata
import d1_test.mock_api.catch_all
import d1_test.mock_api.get_format
import d1_test.mock_api.list_formats


@d1_test.d1_test_case.reproducible_random_decorator('TestCNClient')
class TestMNClient(d1_test.d1_test_case.D1TestCase):
  sysmeta_pyxb = d1_test.sample.load_xml_to_pyxb(
    'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
  )

  # MNStorage.updateSystemMetadata()

  @d1_test.mock_api.catch_all.activate
  def test_1000(self, mn_client_v2):
    """MNStorage.updateSystemMetadata(): Generates expected REST query"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    received_echo_dict = mn_client_v2.updateSystemMetadata(
      'valid_pid', TestMNClient.sysmeta_pyxb
    )
    d1_test.mock_api.catch_all.assert_expected_echo(
      received_echo_dict, 'update_system_metadata', mn_client_v2
    )

  @d1_test.mock_api.catch_all.activate
  def test_1010(self, mn_client_v2):
    """MNStorage.updateSystemMetadata(): Converts DataONEException XML doc to exception"""
    d1_test.mock_api.catch_all.add_callback(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    with pytest.raises(d1_common.types.exceptions.NotFound):
      mn_client_v2.updateSystemMetadata(
        'valid_pid', TestMNClient.sysmeta_pyxb, {'trigger': '404'}
      )
