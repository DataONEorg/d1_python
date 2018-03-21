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
:mod:`tier_1_mn_read_get`
=========================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import context
import pytest
import test_client
import test_utilities

import d1_common.const
import d1_common.types.exceptions

import d1_test_case


class Test050Get(d1_test_case.D1TestCase):
  def validate_object(self, object_info):
    """Get object and verify retrieved information against its ObjectInfo.
    """
    # The ObjectInfo records were retrieved during the listObjects tests.
    client = test_client.TestClient(context.node['baseurl'])
    pid = object_info.identifier.value()
    # Verify checksum and checksum algorithm.
    response = client.get(context.TOKEN, pid)
    checksum_from_get = test_utilities.calculate_checksum_on_string(
      response, object_info.checksum.algorithm
    )
    assert object_info.checksum.value() == checksum_from_get
    # Verify object size.
    response = client.get(context.TOKEN, pid)
    object_size = test_utilities.get_size(response)
    assert object_size == object_info.size

  def test_010_get_object_by_invalid_pid(self):
    """404 NotFound when attempting to get non-existing object.
    """
    client = test_client.TestClient(context.node['baseurl'])
    with pytest.raises(d1_common.types.exceptions.NotFound):
      client.get(context.TOKEN, '_invalid_pid_')

  def test_020_get_object_by_valid_pid(self):
    """Successful retrieval of known objects.
    """
    # Verify that objects learned about in earlier slicing tests can be
    # retrieved and that their checksums match what listObjects reported.
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        self.validate_object(object_info)
