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
:mod:`tier_1_mn_read_listobjects`
=================================

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


class Test030ListObjects(d1_test_case.D1TestCase):
  def assert_counts(self, object_list, start, count, total):
    assert object_list.start == start
    assert object_list.count == count
    assert object_list.total == total
    assert len(object_list.objectInfo) == count

  def test_010_get_object_count(self):
    """Get object count.
    """
    client = test_client.TestClient(context.node['baseurl'])

    object_list = client.listObjects(context.TOKEN, start=0, count=0)

    assert object_list.start == 0
    assert object_list.count == 0
    # The server is required to have at least 15 objects to pass this test.
    # Without a few objects to perform tests on, many of the remaining tests in
    # the suite become meaningless.
    assert object_list.total >= 15

    context.object_total = object_list.total

  def test_020_validate_object_count_1(self):
    """Provided object count is correct (1).
    """
    # Get a slice that contains the last object.
    client = test_client.TestClient(context.node['baseurl'])
    object_list = client.listObjects(
      context.TOKEN, start=context.object_total - 1,
      count=d1_common.const.DEFAULT_SLICE_SIZE
    )
    self.assert_counts(
      object_list, context.object_total - 1, 1, object_list.total
    )

  def test_020_validate_object_count_2(self):
    """Provided object count is correct (2).
    """
    # - Get a slice that contains any objects after the last object. If this
    # returns anything, the initially obtained object count was wrong.
    # - Verify that server responds correctly when more than the available number
    # of objects are requsted.
    client = test_client.TestClient(context.node['baseurl'])
    object_list = client.listObjects(
      context.TOKEN, start=context.object_total,
      count=d1_common.const.DEFAULT_SLICE_SIZE
    )
    self.assert_counts(object_list, context.object_total, 0, object_list.total)

  def test_030_get_slices(self):
    """Get test object slices.
    3 slices are needed, each with 5 objects. They are picked from the
    beginning, center and end of the available range.
    """
    client = test_client.TestClient(context.node['baseurl'])
    for start in (0, context.object_total / 2, context.object_total - 5):
      object_list = client.listObjects(context.TOKEN, start=start, count=5)
      # Each slice should be 5 objects, starting at the requested start.
      self.assert_counts(object_list, start, 5, context.object_total)
      # Store the slices for later tests.
      try:
        context.slices.append(object_list)
      except AttributeError:
        context.slices = [object_list]

  def test_040_invalid_request_negative_start(self):
    """Negative 'start' parameter returns InvalidRequest.
    """
    # It's common to forget to check for negative numbers when validating
    # indexes.
    client = test_client.TestClient(context.node['baseurl'])
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      client.listObjects(
        context.TOKEN, start=-1, count=d1_common.const.DEFAULT_SLICE_SIZE
      )

  def test_050_invalid_request_invalid_count(self):
    """count parameter higher than DEFAULT_SLICE_SIZE returns InvalidRequest.
    """
    client = test_client.TestClient(context.node['baseurl'])
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      client.listObjects(
        context.TOKEN, count=d1_common.const.DEFAULT_SLICE_SIZE + 1
      )

  def test_060_invalid_request_negative_count(self):
    """Negative 'count' parameter returns InvalidRequest.
    """
    client = test_client.TestClient(context.node['baseurl'])
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      client.listObjects(context.TOKEN, count=-1)

  def test_070_date_range_1(self):
    """fromDate and toDate parameters are accepted separately and
    limit the number of returned objects.
    """
    # Find two unique datetimes.
    dates = []
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        dates.append(object_info.dateSysMetadataModified)
    dates.sort()
    # Check that there are at least two unique timestamps. This test is not
    # applicable if all objects share the same timestamp.
    if dates[0] == dates[-1]:
      context.non_unique_timestamps = True
      return
    else:
      context.non_unique_timestamps = False

    client = test_client.TestClient(context.node['baseurl'])
    # It is now known that there are objects with at least two different
    # timestamps on the node, so filtering on the lowest timestamp must
    # eliminate at least one object.
    object_list = client.listObjects(context.TOKEN, fromDate=dates[-1])
    assert object_list.count < context.object_total
    # Filtering on the highest timestamp must eliminate at least one object.
    object_list = client.listObjects(context.TOKEN, toDate=dates[0])
    assert object_list.count < context.object_total

  def test_075_date_range_2(self):
    """fromDate and toDate correctly split the number of returned
    objects.
    """
    # Find middle timestamp.
    dates = []
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        dates.append(object_info.dateSysMetadataModified)
    dates.sort()
    client = test_client.TestClient(context.node['baseurl'])
    middle_date = dates[7]
    # Get object count for objects with timestamps lower than middle_date.
    low = client.listObjects(context.TOKEN, toDate=middle_date).total
    # Get object count for objects with timestamps higher or equal to
    # middle_date.
    high = client.listObjects(context.TOKEN, fromDate=middle_date).total
    # Check that the separate totals match the total number of objects in the
    # collection.
    assert low + high == context.object_total

  def test_080_date_range_3(self):
    """fromDate and toDate parameters are accepted together and
    limit the number of returned objects.
    """
    # Find two unique datetimes.
    dates = []
    for object_list in context.slices:
      for object_info in object_list.objectInfo:
        dates.append(object_info.dateSysMetadataModified)
    dates.sort()
    # A range query between the lowest and highest datetime in the range must
    # include at last the number of objects that were included in the three
    # slices.
    client = test_client.TestClient(context.node['baseurl'])
    object_list = client.listObjects(
      context.TOKEN, fromDate=dates[0], toDate=dates[-1],
      count=d1_common.const.DEFAULT_SLICE_SIZE
    )
    assert object_list.count >= len(dates)
