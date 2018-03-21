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
"""Generate random Replica
"""

import random

import d1_common.types.dataoneTypes

import d1_test.instance_generator.date_time
import d1_test.instance_generator.random_data

REPLICA_STATUS_LIST = [
  d1_common.types.dataoneTypes.ReplicationStatus.queued,
  d1_common.types.dataoneTypes.ReplicationStatus.requested,
  d1_common.types.dataoneTypes.ReplicationStatus.completed,
  d1_common.types.dataoneTypes.ReplicationStatus.failed,
  d1_common.types.dataoneTypes.ReplicationStatus.invalidated,
]


def generate(min_replicas=0, max_replicas=5):
  n_replicas = random.randint(min_replicas, max_replicas)
  replica_list = []
  for _ in range(n_replicas):
    replica_pyxb = generate_single()
    replica_list.append(replica_pyxb)
  return replica_list or None


def generate_single():
  replica_pyxb = d1_common.types.dataoneTypes.replica()
  replica_pyxb.replicaMemberNode = d1_test.instance_generator.random_data.random_mn()
  replica_pyxb.replicationStatus = random.choice(REPLICA_STATUS_LIST)
  replica_pyxb.replicaVerified = d1_test.instance_generator.date_time.random_datetime()
  return replica_pyxb
