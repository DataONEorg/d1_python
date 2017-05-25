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

import urlparse

import d1_client.mnclient_2_0
import d1_common.types.dataoneTypes_v1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.types.exceptions
import d1_common.util
import d1_test.mock_api.django_client
import d1_test.mock_api.get
import gmn.tests.gmn_test_case
import gmn.tests.gmn_test_client
import requests
import responses

BASE_URL = 'http://mock/mn'
# Mocked 3rd party server for object byte streams
REMOTE_URL = 'http://remote/'
INVALID_URL = 'http://invalid/'


class TestProxyMode(gmn.tests.gmn_test_case.D1TestCase):
  """GMN can handle storage of the object bytes itself, or it can defer
  storage of the object bytes to another web server (proxy mode). The mode is
  selectable on a per object basis.

  Create a sciobj that wraps object bytes stored on a 3rd party server. We use
  Responses to simulate the 3rd party server.

  If {redirect_bool} is True, a 302 redirect operation is added. To get to the
  object bytes, the client must follow the redirect.
  """

  # @classmethod
  # def setUpClass(cls):
  #   pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    d1_test.mock_api.django_client.add_callback(BASE_URL)
    d1_test.mock_api.get.add_callback(REMOTE_URL)

  def create_and_compare(
      self, client, binding, redirect_bool, use_invalid_url=False
  ):
    pid = self.random_pid()
    created_sciobj_str, created_sysmeta_pyxb = self.gen_sysmeta_and_create_proxied_sciobj(
      client, binding, pid, redirect_bool, use_invalid_url
    )
    response = client.get(
      pid,
      vendorSpecific=self.
      include_subjects(gmn.tests.gmn_test_case.GMN_TEST_SUBJECT_TRUSTED),
    )
    retrieved_sysmeta_pyxb = client.getSystemMetadata(
      pid,
      vendorSpecific=self.
      include_subjects(gmn.tests.gmn_test_case.GMN_TEST_SUBJECT_TRUSTED),
    )
    self.assertEqual(len(response.content), 1024)
    self.assertEqual(created_sciobj_str, response.content)
    self.assertEqual(
      created_sysmeta_pyxb.checksum.value(),
      retrieved_sysmeta_pyxb.checksum.value()
    )
    self.assert_sci_obj_checksum_matches_sysmeta(
      response, retrieved_sysmeta_pyxb
    )

  def gen_sysmeta_and_create_proxied_sciobj(
      self, client, binding, pid, redirect_bool, use_invalid_url
  ):
    sciobj_str = self.get_remote_sciobj_bytes(pid)
    sysmeta_pyxb = self.generate_sysmeta(
      binding, pid, sciobj_str, gmn.tests.gmn_test_case.GMN_TEST_SUBJECT_PUBLIC
    )
    object_stream_url = (
      'http://invalid/v2/object/{}'.format(pid)
      if use_invalid_url else self.get_remote_sciobj_url(pid)
    )
    self.create_proxied_sciobj(client, object_stream_url, sysmeta_pyxb, pid)
    return sciobj_str, sysmeta_pyxb

  def create_proxied_sciobj(self, client, object_stream_url, sysmeta_pyxb, pid):
    headers = self.include_subjects(
      gmn.tests.gmn_test_case.GMN_TEST_SUBJECT_TRUSTED
    )
    headers['VENDOR-GMN-REMOTE-URL'] = object_stream_url
    client.create(pid, '', sysmeta_pyxb, vendorSpecific=headers)

  def get_remote_sciobj_url(self, pid):
    return urlparse.urljoin(REMOTE_URL, 'v2/object/{}'.format(pid))

  def get_remote_sciobj_bytes(self, pid):
    sciobj_url = self.get_remote_sciobj_url(pid)
    return requests.get(sciobj_url).content

  @responses.activate
  def test_0010_v1(self):
    """v1 create(): Proxy mode: Object is directly accessible at the given URL.
    """
    client = d1_client.mnclient.MemberNodeClient(BASE_URL)
    self.create_and_compare(client, v1, redirect_bool=False)

  @responses.activate
  def test_0020_v2(self):
    """v2 create(): Proxy mode: Object is directly accessible at the given URL.
    """
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
    self.create_and_compare(client, v2, redirect_bool=False)

  @responses.activate
  def test_0030_v1(self):
    """v2 create(): Proxy mode: Passing invalid url raises InvalidRequest"""
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.InvalidRequest,
      self.create_and_compare,
      client,
      v2,
      redirect_bool=False,
      use_invalid_url=True,
    )

  # TODO: Test redirects
