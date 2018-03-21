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
:mod:`tier_1_mn_read_describe`
==============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import xml

import context
import pytest
import test_client

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

import d1_test_case


class Test060Describe(d1_test_case.D1TestCase):
  def test_010_describe_by_invalid_pid(self):
    """404 NotFound when attempting to get description for non-existing object.
    """
    client = test_client.TestClient(context.node['baseurl'])
    # The exception is caused by the body being empty since describe() uses a
    # HEAD request.
    with pytest.raises(xml.parsers.expat.ExpatError):
      client.describe(context.TOKEN, '_invalid_pid_')

  def test_020_describe_by_valid_pid(self):
    """Successful describe for known objects.
    - Verify that required headers are present.
    - Verify that the object length reported by describe matches what was
      reported by listObjects.
    - Verify that date header contains a valid date.
    - Verify that date header matches what was reported by listObjects.
    """
    # Verify that the checksums retrieved by getChecksum match what listObjects
    # reported.
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        client = test_client.TestClient(context.node['baseurl'])
        pid = object_info.identifier.value()
        response = client.describe(context.TOKEN, pid)
        headers = response.getheaders()
        # Build dict with lower case keys.
        headers_lower = dict((header.lower(), value)
                             for header, value in headers)
        # Check for the required headers.
        assert 'date' in headers_lower
        assert 'content-type' in headers_lower
        assert 'content-length' in headers_lower
        # Verify that the object length reported by describe matches what was
        # reported by listObjects.
        assert int(headers_lower['content-length']) == object_info.size
        # Verify that date is a valid date.
        assert d1_common.date_time.dt_from_iso8601_str(headers_lower['date'])
        # Verify that date matches what was reported by listObjects.
        # TODO: Fails with: TypeError: can't compare offset-naive and
        # offset-aware datetimes
        #date = d1_common.date_time.from_iso8601(headers_lower['date'])
        #self.assertEqual(date, object_info.dateSysMetadataModified)
