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
:mod:`tier_3_mn_storage_create`
===============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import datetime
import io
import random
import uuid
import xml.sax.saxutils

import context
import test_client
import test_utilities

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions

import d1_test_case


class Test310Create(d1_test_case.D1TestCase):
  def test_(self):
    pass

  def generate_sysmeta(
      self, pid, size, checksum_algorithm, checksum, create_date
  ):
    return """<?xml version="1.0" encoding="utf-8"?>
<D1:systemMetadata xmlns:D1="http://dataone.org/service/types/0.5.1">
  <identifier>{0}</identifier>
  <objectFormat>eml://ecoinformatics.org/eml-2.0.0</objectFormat>
  <size>{1}</size>
  <submitter>test</submitter>
  <rightsHolder>test</rightsHolder>
  <checksum algorithm="{2}">{3}</checksum>
  <dateUploaded>{4}</dateUploaded>
  <dateSysMetadataModified>{4}</dateSysMetadataModified>
  <originMemberNode>MN1</originMemberNode>
  <authoritativeMemberNode>MN1</authoritativeMemberNode>
</D1:systemMetadata>
""".format(
      xml.sax.saxutils.escape(pid), size, checksum_algorithm, checksum,
      datetime.datetime.isoformat(create_date)
    ).encode('utf-8')

  def generate_random_file(self, num_bytes):
    return io.StringIO(
      "".join(chr(random.randrange(0, 255)) for i in range(num_bytes))
    )

  def test_020_create_object(self):
    """Create a single test object.
    """
    client = test_client.TestClient(context.node['baseurl'])

    #scidata_path = test_utilities.get_resource_path(
    #  'd1_testdocs/test_objects/hdl%3A10255%2Fdryad.167%2Fmets.xml')
    #sysmeta_path = test_utilities.get_resource_path(
    #  'd1_testdocs/test_objects/hdl%3A10255%2Fdryad.167%2Fmets.xml.sysmeta')

    context.pid_created = '__invalid_test_object__' + str(uuid.uuid1())

    context.scidata_size = 1024**2 + random.randint(0, 1024)
    context.checksum_algorithm = 'SHA-1'

    context.scidata_file = self.generate_random_file(context.scidata_size)

    context.scidata_file.seek(0)
    context.checksum = test_utilities.calculate_checksum_on_string(
      context.scidata_file, context.checksum_algorithm
    )

    context.sysmeta_file = self.generate_sysmeta(
      context.pid_created, context.scidata_size, context.checksum_algorithm,
      context.checksum, d1_common.date_time.utc_now()

    )

    context.scidata_file.seek(0)
    client.create(
      context.TOKEN, context.pid_created, context.scidata_file,
      context.sysmeta_file
    )

  def test_030_object_exists(self):
    """Verify that created object can be retrieved and that its checksum
    matches.
    """
    client = test_client.TestClient(context.node['baseurl'])
    response = client.get(context.TOKEN, context.pid_created)
    # Calculate the checksum.
    checksum = test_utilities.calculate_checksum_on_string(
      response, context.checksum_algorithm
    )
    assert context.checksum == checksum

  def test_040_log_records_total_increased_by_one(self):
    """Total number of log records increased by one.
    """
    client = test_client.TestClient(context.node['baseurl'])
    log_records = client.getLogRecords(
      context.TOKEN, datetime.datetime(1800, 1, 1), 0, 0
    )
    assert context.log_records_total == log_records.total + 1

  def test_070_describe_returns_correct_header(self):
    """Successful describe for newly created object.
    - Verify that required headers are present.
    """
    # TODO: Requests returns case insensitive header dict
    client = test_client.TestClient(context.node['baseurl'])
    response = client.describe(context.TOKEN, context.pid_created)
    headers = response.getheaders()
    # Build dict with lower case keys.
    headers_lower = dict((header.lower(), value) for header, value in headers)
    # Check for the required headers.
    # Verify that date is a valid date.
    assert d1_common.date_time.dt_from_iso8601_str(headers_lower['date'])
    assert 'content-type' in headers_lower
    assert 'content-length' in headers_lower

  def test_080_total_number_of_objects_increased_by_one(self):
    """Total number of objects reported by listObjects increased by one.
    """
    client = test_client.TestClient(context.node['baseurl'])
    object_list = client.listObjects(context.TOKEN, start=0, count=0)
    assert object_list.total == context.object_total + 1

  # TODO:
  #- Verify that the object length reported by describe matches what was
  #reported by listObjects.
  #- Verify that date header contains a valid date.
  #- Verify that date header matches what was reported by listObjects.
