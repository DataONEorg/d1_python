#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Test MNStorage.create() and MNStorage.update() with Resource Map."""
import logging

import pytest
import responses

import d1_gmn.app.resource_map
import d1_gmn.tests.gmn_test_case

import d1_common.types
import d1_common.types.exceptions

import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data

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
    @responses.activate
    @django.test.override_settings(RESOURCE_MAP_CREATE='block')
    def test_1000(self, gmn_client_v2):
        """MNStorage.create(): "block" mode: Creating a resource map after creating its
        aggregated objects is supported."""
        pid_list = self.create_multiple_objects(gmn_client_v2)
        ore_pid = self.create_resource_map(gmn_client_v2, pid_list)
        member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(ore_pid)
        assert sorted(pid_list) == sorted(member_list)

    @responses.activate
    @django.test.override_settings(RESOURCE_MAP_CREATE='block')
    def test_1010(self, gmn_client_v2):
        """MNStorage.create(): "block" mode: Creating a resource map before creating its
        aggregated objects raises InvalidRequest."""
        pid_list = [
            d1_test.instance_generator.identifier.generate_pid('PID_AGGR_')
            for _ in range(10)
        ]
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
            self.create_resource_map(gmn_client_v2, pid_list)

    @responses.activate
    @django.test.override_settings(RESOURCE_MAP_CREATE='open')
    def test_1020(self, gmn_client_v2):
        """MNStorage.create(): "open" mode: Creating a resource map after creating its
        aggregated objects is supported."""
        pid_list = self.create_multiple_objects(gmn_client_v2)
        ore_pid = self.create_resource_map(gmn_client_v2, pid_list)
        member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(ore_pid)
        assert sorted(pid_list) == sorted(member_list)

    @responses.activate
    @django.test.override_settings(RESOURCE_MAP_CREATE='open')
    def test_1030(self, gmn_client_v2):
        """MNStorage.create(): "open" mode: Creating a resource map before creating its
        aggregated objects is supported."""
        pid_list = [
            d1_test.instance_generator.identifier.generate_pid('PID_AGGR_')
            for _ in range(10)
        ]
        ore_pid = self.create_resource_map(gmn_client_v2, pid_list)
        member_list = d1_gmn.app.resource_map.get_resource_map_members_by_map(ore_pid)
        assert sorted(pid_list) == sorted(member_list)

    @responses.activate
    @django.test.override_settings(RESOURCE_MAP_CREATE='open')
    def test_1040(self, gmn_client_v1_v2, none_true):
        """MNStorage.create(): "open" mode: Creating a random series of objects and
        resource maps.

        - Some PIDs aggregated in multiple maps
        - Some maps aggregating each other
        - Maps created both before and after their aggregated PIDs
        - Some maps containing references to themselves

        """
        avail_pid_set = [
            d1_test.instance_generator.identifier.generate_pid()
            for _ in range(NUM_CREATE)
        ]
        uncreated_pid_set = avail_pid_set[:]

        while True:
            pid = d1_test.instance_generator.random_data.random_choice_pop(
                uncreated_pid_set
            )
            aggr_list = d1_test.instance_generator.random_data.random_sized_sample(
                avail_pid_set, 2, max_size=MAX_AGGR_SIZE
            )
            if not uncreated_pid_set or not aggr_list:
                break
            d1_test.instance_generator.random_data.random_sized_sample_pop(
                avail_pid_set, 0, max_size=MAX_REDUCE_SIZE
            )
            is_ore = d1_test.instance_generator.random_data.random_bool_factor(
                MAP_CHANCE
            )
            if is_ore:
                self.create_resource_map(gmn_client_v1_v2, aggr_list, pid)
            else:
                self.create_obj(gmn_client_v1_v2, pid, sid=none_true)
            logging.info(
                'uncreated={} available={} ORE={} aggr_list={}'.format(
                    len(uncreated_pid_set), len(avail_pid_set), is_ore, len(aggr_list)
                )
            )
