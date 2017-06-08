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

from __future__ import absolute_import

import responses

import d1_test.d1_test_case
import d1_test.mock_api.list_nodes as list_nodes


class TestMockObjectList(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_0010(self, cn_client_v1_v2):
    """mock_api.listNodes() returns a DataONE ObjectList PyXB object"""
    list_nodes.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    print type(cn_client_v1_v2.listNodes())
    print type(cn_client_v1_v2.bindings.NodeList)
    if not isinstance(
        cn_client_v1_v2.listNodes(), cn_client_v1_v2.bindings.NodeList
    ):
      pass

  # @responses.activate
  # def test_0011(self):
  #   """mock_api.listNodes() returns a populated ObjectList"""
  #   mock_object_list.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
  #   object_list = self.client.listNodes()
  #   self.assertEqual(len(object_list.objectInfo), 100)
  #   for object_info in object_list.objectInfo:
  #     self.assertEqual(object_info.formatId, 'text/plain')
  #     break
  #
  # @responses.activate
  # def test_0012(self):
  #   """mock_api.listNodes(): Passing a trigger header triggers a DataONEException"""
  #   mock_object_list.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
  #   self.assertRaises(
  #     d1_common.types.exceptions.ServiceFailure, self.client.listNodes,
  #     vendorSpecific={'trigger': '500'}
  #   )
  #
  # # TODO: More tests
