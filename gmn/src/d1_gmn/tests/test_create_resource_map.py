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

import io
import logging

import pytest
import responses

import d1_gmn.app.resource_map
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.const
import d1_common.resource_map

import d1_test.instance_generator.identifier as identifier
import d1_test.instance_generator.random_data as random_data
import d1_test.instance_generator.system_metadata as sysmeta

import django.test

# # Long test
# NUM_CREATE = 1000
# MAX_AGGR_SIZE = 50
# MAX_REDUCE_SIZE = 10
# # 0.2 = 20% chance of creating a resource map
# MAP_CHANCE = 0.2

# Fast test
NUM_CREATE = 100
MAX_AGGR_SIZE = 5
MAX_REDUCE_SIZE = 10
# 0.2 = 20% chance of creating a resource map
MAP_CHANCE = 0.2


class TestCreateResourceMap(d1_gmn.tests.gmn_test_case.GMNTestCase):
  # Having these methods at the top seems to confuse PyCharm's detection of test
  # framework. It creates plain Python instead of pytest test runners.
  def _create_objects(self, client):
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = []
      for i in range(10):
        pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.create_obj(client)
        pid_list.append(pid)
    return pid_list

  def _create_objects_by_list(self, client, pid_list):
    with d1_gmn.tests.gmn_mock.disable_auth():
      for pid in pid_list:
        self.create_obj(client, pid, sid=None)

  def _create_resource_map(self, client, pid_list, ore_pid=None):
    ore_pid = (ore_pid or identifier.generate_pid('PID_ORE_'))
    ore = d1_common.resource_map.createSimpleResourceMap(
      ore_pid, scimeta_pid=pid_list[0], sciobj_pid_list=pid_list[1:]
    )
    ore_xml = ore.serialize_to_transport()
    sysmeta_pyxb = sysmeta.generate_from_file(
      client,
      io.BytesIO(ore_xml),
      {
        'identifier': ore_pid,
        'formatId': d1_common.const.ORE_FORMAT_ID,
        'replica': None,
      },
    )
    # self.dump(sysmeta_pyxb)
    self.call_d1_client(
      client.create, ore_pid, io.BytesIO(ore_xml), sysmeta_pyxb
    )
    return ore_pid

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='block',
  )
  def test_1000(self, gmn_client_v2):
    """MNStorage.create(): "block" mode: Creating a resource map after
    creating its aggregated objects is supported
    """
    pid_list = self._create_objects(gmn_client_v2)
    ore_pid = self._create_resource_map(gmn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='block',
  )
  def test_1010(self, gmn_client_v2):
    """MNStorage.create(): "block" mode: Creating a resource map before
    creating its aggregated objects raises InvalidRequest
    """
    pid_list = [identifier.generate_pid('PID_AGGR_') for _ in range(10)]
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      self._create_resource_map(gmn_client_v2, pid_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='open',
  )
  def test_1020(self, gmn_client_v2):
    """MNStorage.create(): "open" mode: Creating a resource map after
    creating its aggregated objects is supported
    """
    pid_list = self._create_objects(gmn_client_v2)
    ore_pid = self._create_resource_map(gmn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='open',
  )
  def test_1030(self, gmn_client_v2):
    """MNStorage.create(): "open" mode: Creating a resource map before
    creating its aggregated objects is supported
    """
    pid_list = [identifier.generate_pid('PID_AGGR_') for _ in range(10)]
    ore_pid = self._create_resource_map(gmn_client_v2, pid_list)
    member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(
      ore_pid
    )
    assert sorted(pid_list) == sorted(member_list)

  @responses.activate
  @django.test.override_settings(
    RESOURCE_MAP_CREATE='open',
  )
  def test_1040(self, gmn_client_v1_v2, none_true):
    """MNStorage.create(): "open" mode: Creating a random series of objects
    and resource maps

    - Some PIDs aggregated in multiple maps
    - Some maps aggregating each other
    - Maps created both before and after their aggregated PIDs
    - Some maps containing references to themselves
    """
    avail_pid_set = [identifier.generate_pid() for _ in range(NUM_CREATE)]
    uncreated_pid_set = avail_pid_set[:]

    while True:
      pid = random_data.random_choice_pop(uncreated_pid_set)
      aggr_list = random_data.random_sized_sample(
        avail_pid_set, 2, max_size=MAX_AGGR_SIZE
      )
      if not uncreated_pid_set or not aggr_list:
        break
      random_data.random_sized_sample_pop(
        avail_pid_set, 0, max_size=MAX_REDUCE_SIZE
      )
      is_ore = random_data.random_bool_factor(MAP_CHANCE)
      if is_ore:
        self._create_resource_map(gmn_client_v1_v2, aggr_list, pid)
      else:
        self.create_obj(gmn_client_v1_v2, pid, sid=none_true)
      logging.info(
        'uncreated={} available={} ORE={} aggr_list={}'.format(
          len(uncreated_pid_set), len(avail_pid_set), is_ore, len(aggr_list)
        )
      )
