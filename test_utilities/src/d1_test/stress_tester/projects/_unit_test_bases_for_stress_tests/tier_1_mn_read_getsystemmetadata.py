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
:mod:`tier_1_mn_read_getsystemmetadata`
=======================================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import context
import pytest
import test_client

import d1_common.const
import d1_common.types.exceptions

import d1_test_case


class Test080GetSystemMetadata(d1_test_case.D1TestCase):
  def test_010_get_sysmeta_by_invalid_pid(self):
    """404 NotFound when attempting to get non-existing SysMeta.
    """
    client = test_client.TestClient(context.node['baseurl'])
    with pytest.raises(d1_common.types.exceptions.NotFound):
      client.getSystemMetadata(context.TOKEN, '_invalid_pid_')

  def test_020_get_sysmeta_by_valid_pid(self):
    """Successful retrieval of valid SysMeta objects.
    """
    client = test_client.TestClient(context.node['baseurl'])
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        pid = object_info.identifier.value()
        sys_meta = client.getSystemMetadata(context.TOKEN, pid)
        # Verify that identifier in SysMeta matches the one that was retrieved.
        assert object_info.identifier.value() == sys_meta.identifier.value()
        # Verify that object format matches listObjects.
        assert object_info.objectFormat == sys_meta.objectFormat
        # Verify that date matches listObjects.
        assert object_info.dateSysMetadataModified == sys_meta.dateSysMetadataModified
        # Verify that size matches listObjects.
        assert object_info.size == sys_meta.size
        # Verify that checksum and checksum algorithm matches listObjects.
        assert object_info.checksum.value() == sys_meta.checksum.value()
        assert object_info.checksum.algorithm == sys_meta.checksum.algorithm
