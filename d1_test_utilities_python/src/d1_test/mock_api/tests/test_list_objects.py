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

import unittest

# D1
import d1_client.mnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

# 3rd party
import responses

# D1
import d1_common.types.dataoneTypes_v2_0

# App
import d1_test.mock_api.list_objects as mock_object_list
import d1_test.mock_api.tests.settings as settings


class TestMockObjectList(unittest.TestCase):
  def setUp(self):
    d1_common.util.log_setup(is_debug=True)
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=settings.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.listObjects() returns a DataONE ObjectList PyXB object"""
    mock_object_list.init(settings.MN_RESPONSES_BASE_URL)
    self.assertIsInstance(
      self.client.listObjects(), d1_common.types.dataoneTypes_v2_0.ObjectList
    )

  @responses.activate
  def test_0011(self):
    """mock_api.listObjects() returns a populated ObjectList"""
    mock_object_list.init(settings.MN_RESPONSES_BASE_URL)
    object_list = self.client.listObjects()
    self.assertEqual(len(object_list.objectInfo), 100)
    for object_info in object_list.objectInfo:
      self.assertEqual(object_info.formatId, 'text/plain')
      break

  @responses.activate
  def test_0012(self):
    """mock_api.listObjects(): Passing a trigger header triggers a DataONEException"""
    mock_object_list.init(settings.MN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.ServiceFailure, self.client.listObjects,
      vendorSpecific={'trigger': '500'}
    )

  # TODO: More tests
