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

import responses

import d1_test.d1_test_case
import d1_test.mock_api.list_objects as mock_list_objects

import d1_client.d1client
import d1_client.iter.objectlist_multi

MAX_OBJECTS = 20


class TestIterObjectListIterator(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """Object List iteration"""
    mock_list_objects.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)

    api_major = d1_client.d1client.get_version_tag_by_d1_client(mn_client_v1_v2)

    object_list_iter = d1_client.iter.objectlist_multi.ObjectListIteratorMulti(
      d1_test.d1_test_case.MOCK_MN_BASE_URL, page_size=13, max_workers=2,
      max_queue_size=10, api_major=api_major
    )

    i = 0

    for i, object_info_pyxb in enumerate(object_list_iter):
      assert isinstance(object_info_pyxb, mn_client_v1_v2.bindings.ObjectInfo)

    assert i == mock_list_objects.N_TOTAL - 1
