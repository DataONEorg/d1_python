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
"""Generate random ReplicationPolicy
"""

import random

import d1_common.types.dataoneTypes

import d1_test.instance_generator.random_data


def generate(min_pref=0, max_pref=4, min_block=0, max_block=4):
  n_pref = random.randint(min_pref, max_pref)
  n_block = random.randint(min_block, max_block)
  if not (n_pref or n_block):
    return
  rp_pyxb = d1_common.types.dataoneTypes.replicationPolicy()
  rp_pyxb.preferredMemberNode = [
    d1_test.instance_generator.random_data.random_mn() for _ in range(n_pref)
  ] or None
  rp_pyxb.blockedMemberNode = [
    d1_test.instance_generator.random_data.random_mn() for _ in range(n_block)
  ] or None
  rp_pyxb.replicationAllowed = d1_test.instance_generator.random_data.random_bool()
  if rp_pyxb.replicationAllowed:
    rp_pyxb.numberReplicas = random.randint(1, 10)
  else:
    rp_pyxb.numberReplicas = 0
  return rp_pyxb
