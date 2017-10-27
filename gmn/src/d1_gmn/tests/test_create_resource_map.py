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
"""Test MNStorage.create() and MNStorage.update() with Resource Map
"""

from __future__ import absolute_import

import StringIO

import pytest
import responses

import d1_gmn.app.resource_map
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.const
import d1_common.resource_map

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.system_metadata

import d1_client.mnclient_2_0

import django
import django.test


class TestCreateResourceMap(d1_gmn.tests.gmn_test_case.GMNTestCase):
  # Having these methods at the top seems to confuse PyCharm's detection of test
  # framework. It creates plain Python instead of pytest test runners.
  def _create_objects(self, client):
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = []
      for i in range(10):
        pid, sid, send_sciobj_str, send_sysmeta_pyxb = self.create_obj(client)
        pid_list.append(pid)
    return pid_list

  def _create_resource_map(self, mn_client_v2, pid_list):
    ore_pid = d1_test.instance_generator.identifier.generate_pid('PID_ORE_')
    ore = d1_common.resource_map.createSimpleResourceMap(
      ore_pid, pid_list[0], pid_list[1:]
    )
    ore_xml = ore.serialize()
    sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_from_file(
      mn_client_v2,
      StringIO.StringIO(ore_xml),
      {
        'identifier': ore_pid,
        'formatId': d1_common.const.ORE_FORMAT_ID,
        'replica': None,
      },
    )
    # self.dump_pyxb(sysmeta_pyxb)
    self.call_d1_client(
      mn_client_v2.create, ore_pid, StringIO.StringIO(ore_xml), sysmeta_pyxb
    )
    return ore_pid

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='block',
  )
  def test_1000(self):
    """MNStorage.create(): "block" mode: Creating a resource map after
    creating its aggregated objects is supported
    """
    mn_client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_BASE_URL
    )

    pid_list = self._create_objects(mn_client_v2)
    ore_pid = self._create_resource_map(mn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='block',
  )
  def test_1010(self):
    """MNStorage.create(): "block" mode: Creating a resource map before
    creating its aggregated objects raises InvalidRequest
    """
    mn_client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    pid_list = [
      d1_test.instance_generator.identifier.generate_pid('PID_AGGR_')
      for _ in range(10)
    ]
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      self._create_resource_map(mn_client_v2, pid_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='open',
  )
  def test_1020(self):
    """MNStorage.create(): "open" mode: Creating a resource map after
    creating its aggregated objects is supported
    """
    mn_client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_BASE_URL
    )

    pid_list = self._create_objects(mn_client_v2)
    ore_pid = self._create_resource_map(mn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='open',
  )
  def test_1030(self):
    """MNStorage.create(): "open" mode: Creating a resource map before
    creating its aggregated objects is supported
    """
    mn_client_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_BASE_URL
    )
    pid_list = [
      d1_test.instance_generator.identifier.generate_pid('PID_AGGR_')
      for _ in range(10)
    ]
    ore_pid = self._create_resource_map(mn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)
