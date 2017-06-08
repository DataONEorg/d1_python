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
"""Generate random replica objects
"""

from __future__ import absolute_import

import random

import d1_common.types.dataoneTypes

import d1_test.instance_generator.dates
import d1_test.instance_generator.random_data


def generate():
  res = d1_common.types.dataoneTypes.replica()
  res.replicaMemberNode = (
    u"mn_" +
    d1_test.instance_generator.random_data.random_unicode_string_no_whitespace(
      5, 10
    )
  )
  res.replicationStatus = d1_common.types.dataoneTypes.ReplicationStatus.completed
  res.replicaVerified = d1_test.instance_generator.dates.now()
  return res


def generate_list(min=1, max=10):
  n = random.randint(min, max)
  res = []
  for i in xrange(0, n):
    res.append(generate())
  return res
