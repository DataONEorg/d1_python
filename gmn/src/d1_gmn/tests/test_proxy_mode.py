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
"""GMN can handle storage of the object bytes itself, or it can defer storage of
the object bytes to another web server (proxy mode). The mode is selectable on a
per object basis
"""

import io
import os

import pytest
import requests
import responses

import d1_gmn.app.sciobj_store
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.mock_api.get


class TestProxyMode(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def setup_method(self, method):
    super().setup_method(method)
    d1_test.mock_api.get.add_callback(d1_test.d1_test_case.MOCK_REMOTE_BASE_URL)

  def create_and_check_proxy_obj(
      self, client, do_redirect, use_invalid_url=False
  ):
    """Create a sciobj that wraps object bytes stored on a 3rd party server. We
    use Responses to simulate the 3rd party server

    If {do_redirect} is True, a 302 redirect operation is added. This tests
    that GMN is able to follow redirects when establishing the proxy stream.
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      # Create

      pid = d1_test.instance_generator.identifier.generate_pid()
      if do_redirect:
        pid = d1_test.mock_api.get.decorate_pid_for_redirect(pid)

      if not use_invalid_url:
        proxy_url = self.get_remote_sciobj_url(pid, client)
      else:
        proxy_url = self.get_invalid_sciobj_url(pid, client)

      pid, sid, send_sciobj_bytes, send_sysmeta_pyxb = self.generate_sciobj_with_defaults(
        client, pid
      )
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        self.call_d1_client(
          client.create, pid,
          io.BytesIO(send_sciobj_bytes), send_sysmeta_pyxb,
          vendorSpecific=self.vendor_proxy_mode(proxy_url)
        )

      # Check

      # Object was not stored locally
      sciobj_path = d1_gmn.app.sciobj_store.get_abs_sciobj_file_path_by_pid(pid)
      assert not os.path.isfile(sciobj_path)

      received_sciobj_bytes = self.call_d1_client(
        client.get, pid, vendorSpecific=self.vendor_proxy_mode(proxy_url)
      ).content

      self.sample.assert_equal_str(send_sciobj_bytes, received_sciobj_bytes)
      # assert send_sciobj_bytes == received_sciobj_bytes

  def get_remote_sciobj_url(self, pid, client):
    return d1_common.url.joinPathElements(
      d1_test.d1_test_case.MOCK_REMOTE_BASE_URL,
      d1_common.type_conversions.get_version_tag_by_bindings(client.bindings),
      'object',
      d1_common.url.encodePathElement(pid),
    )

  def get_invalid_sciobj_url(self, pid, client):
    return d1_common.url.joinPathElements(
      d1_test.d1_test_case.MOCK_INVALID_BASE_URL,
      d1_common.type_conversions.get_version_tag_by_bindings(client.bindings),
      'object',
      d1_common.url.encodePathElement(pid),
    )

  def get_remote_sciobj_bytes(self, pid):
    sciobj_url = self.get_remote_sciobj_url(pid)
    return requests.get(sciobj_url).content

  @responses.activate
  def test_1000(self):
    """create(): Proxy mode: Create and retrieve proxied object"""
    self.create_and_check_proxy_obj(self.client_v1, do_redirect=False)

  @responses.activate
  def test_1010(self):
    """create(): Proxy mode: Create and retrieve proxied object"""
    self.create_and_check_proxy_obj(self.client_v2, do_redirect=False)

  @responses.activate
  def test_1020(self):
    """create(): Proxy mode: Create and retrieve proxied object with redirect"""
    self.create_and_check_proxy_obj(self.client_v1, do_redirect=True)

  @responses.activate
  def test_1030(self):
    """create(): Proxy mode: Create and retrieve proxied object with redirect"""
    self.create_and_check_proxy_obj(self.client_v2, do_redirect=True)

  @responses.activate
  def test_1040(self):
    """create(): Proxy mode: Passing invalid url raises InvalidRequest"""
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      self.create_and_check_proxy_obj(
        self.client_v2,
        self.v2,
        # do_redirect=False,
        use_invalid_url=True,
      )
