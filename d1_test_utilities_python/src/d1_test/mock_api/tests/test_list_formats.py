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
import d1_client.cnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

# 3rd party
import responses

# D1
import d1_common.types.dataoneTypes_v2_0

# App
import d1_test.mock_api.list_formats as mock_object_format_list
import d1_test.mock_api.tests.settings as settings


class TestMockObjectFormatList(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
      base_url=settings.CN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.listFormats() returns a objectFormatList PyXB object"""
    mock_object_format_list.add_callback(settings.CN_RESPONSES_BASE_URL)
    self.assertIsInstance(
      self.client.listFormats(),
      d1_common.types.dataoneTypes_v2_0.ObjectFormatList,
    )

  @responses.activate
  def test_0020(self):
    """mock_api.listFormats() returns a populated objectFormatList"""
    mock_object_format_list.add_callback(settings.CN_RESPONSES_BASE_URL)
    object_format_list = self.client.listFormats()
    self.assertEqual(len(object_format_list.objectFormat), 100)
    for object_format in object_format_list.objectFormat:
      self.assertEqual(object_format.formatId, 'format_id_0')
      break

  @responses.activate
  def test_0030(self):
    """mock_api.listFormats(): Passing a trigger header triggers a DataONEException"""
    mock_object_format_list.add_callback(settings.CN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotFound, self.client.listFormats,
      vendorSpecific={'trigger': '404'}
    )
