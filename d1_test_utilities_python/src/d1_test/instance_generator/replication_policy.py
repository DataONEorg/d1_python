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
"""
Module d1_instance_generator.replicationpolicy
==============================================

:Synopsis: Generate random replication policy objects.
:Created: 2011-08-03
:Author: DataONE (Vieglais)
"""

# Stdlib
import random

# D1
import d1_common.types.dataoneTypes

# App
import random_data


def generate():
  res = d1_common.types.dataoneTypes.replicationPolicy()
  n = random.randint(1, 10)
  nodes = []
  for i in xrange(0, n):
    nodes.append(
      u"preferredMemberNode_" +
      random_data.random_unicode_string_no_whitespace(5, 10)
    )
  res.preferredMemberNode = nodes
  n = random.randint(1, 10)
  nodes = []
  for i in xrange(0, n):
    nodes.append(
      u"blockedMemberNode_" +
      random_data.random_unicode_string_no_whitespace(5, 10)
    )
  res.blockedMemberNode = nodes
  res.replicationAllowed = random_data.random_bool()
  if res.replicationAllowed:
    res.numberReplicas = random.randint(1, 10)
  else:
    res.numberReplicas = 0
  return res
