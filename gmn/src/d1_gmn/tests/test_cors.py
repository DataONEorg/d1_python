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
"""Test Cross-Origin Resource Sharing (CORS) Headers
"""
import freezegun
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case


@d1_test.d1_test_case.reproducible_random_decorator('TestCors')
@freezegun.freeze_time('1961-01-02')
class TestCors(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """No CORS headers are included in 404 caused by non-existing endpoint"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.GET(['bogus', 'endpoint'])
    self.sample.assert_equals(response, 'get_bogus_endpoint', gmn_client_v1_v2)

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """Invalid method against endpoint raises 405 Method Not Allowed and returns
    regular and CORS headers with allowed methods (POST /object/invalid_pid)
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.POST(['object', 'invalid_pid'])
    self.sample.assert_equals(response, 'post_object_pid', gmn_client_v1_v2)

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """listObjects(): The expected CORS headers are included in regular
    response
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.GET(['object'], params={'count': '10'})
    self.sample.assert_equals(response, 'get_listobjects', gmn_client_v1_v2)

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """get(): The expected CORS headers are included in regular response"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(gmn_client_v1_v2)
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.GET(['object', pid])
    self.sample.assert_equals(response, 'get_valid_object', gmn_client_v1_v2)

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """listObjects(): OPTIONS request returns expected headers"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.OPTIONS(['object'])
    self.sample.assert_equals(
      response, 'list_objects_options', gmn_client_v1_v2
    )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """get(): OPTIONS request returns expected headers"""
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(gmn_client_v1_v2)
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.OPTIONS(['object', pid])
    self.sample.assert_equals(response, 'get_options', gmn_client_v1_v2)

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """Invalid method against endpoint raises 405 Method Not Allowed and returns
    regular and CORS headers with allowed methods (PUT /object/)
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      response = gmn_client_v1_v2.PUT(['object'])
    self.sample.assert_equals(response, 'put_object_list', gmn_client_v1_v2)
