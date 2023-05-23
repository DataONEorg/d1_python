# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""GMN can handle storage of the object bytes itself, or it can defer storage of the
object bytes to another web server (proxy mode).

The mode is selectable on a per object basis

"""
import base64
import json
import re

import django.test
import freezegun
import pytest
import requests
import responses

import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_gmn.app.proxy
import d1_gmn.app.sciobj_store
import d1_gmn.tests.gmn_test_case
import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.mock_api.catch_all
import d1_test.mock_api.get
import d1_gmn.tests.gmn_mock

AUTH_USERNAME = "Auth user name"
AUTH_PASSWORD = "Auth user password !@#$%"


@d1_test.d1_test_case.reproducible_random_decorator("TestProxyMode")
@freezegun.freeze_time("1999-09-09")
class TestProxyMode(d1_gmn.tests.gmn_test_case.GMNTestCase):
    @responses.activate
    def create_and_check_proxy_obj(self, client, do_redirect, use_invalid_url=False):
        """Create a sciobj that wraps object bytes stored on a 3rd party server. We use
        Responses to simulate the 3rd party server.

        If ``do_redirect`` is True, a 302 redirect operation is added. This tests that
        GMN is able to follow redirects when establishing the proxy stream.

        """

        # Use the MNRead.get() mock API to simulate a remote 3rd party server that holds
        # proxy objects.
        d1_test.mock_api.get.add_callback(
            d1_test.d1_test_case.MOCK_REMOTE_BASE_URL
        )

        # Create a proxy object.
        pid = d1_test.instance_generator.identifier.generate_pid()

        if not use_invalid_url:
            proxy_url = self.get_remote_sciobj_url(pid, client)
        else:
            proxy_url = self.get_invalid_sciobj_url(pid, client)

        pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
            client, pid, sid=True, vendor_dict=self.vendor_proxy_mode(proxy_url)
        )

        # Check that object was not stored locally
        assert not d1_gmn.app.sciobj_store.is_existing_sciobj_file(pid)

        # Retrieve the proxy object and check it
        response = self.call_d1_client(client.get, pid)
        recv_sciobj_bytes = response.content
        assert recv_sciobj_bytes == sciobj_bytes
        return response

    def get_remote_sciobj_url(self, pid, client):
        return d1_common.url.joinPathElements(
            d1_test.d1_test_case.MOCK_REMOTE_BASE_URL,
            d1_common.type_conversions.get_version_tag_by_pyxb_binding(
                client.pyxb_binding
            ),
            "object",
            d1_common.url.encodePathElement(pid),
        )

    def get_invalid_sciobj_url(self, pid, client):
        return d1_common.url.joinPathElements(
            d1_test.d1_test_case.MOCK_INVALID_BASE_URL,
            d1_common.type_conversions.get_version_tag_by_pyxb_binding(
                client.pyxb_binding
            ),
            "object",
            d1_common.url.encodePathElement(pid),
        )

    def get_remote_sciobj_bytes(self, pid, client):
        sciobj_url = self.get_remote_sciobj_url(pid, client)
        return requests.get(sciobj_url).content

    def decode_basic_auth(self, basic_auth_str):
        """Decode a Basic Authentication header to (username, password)."""
        m = re.match(r"Basic (.*)", basic_auth_str)
        return (
            base64.standard_b64decode(m.group(1).encode("utf-8"))
            .decode("utf-8")
            .split(":")
        )

    def test_1000(self, gmn_client_v1_v2):
        """create(): Proxy mode: Create and retrieve proxy object, no redirect."""
        self.create_and_check_proxy_obj(gmn_client_v1_v2, do_redirect=False)

    def test_1020(self, gmn_client_v1_v2):
        """create(): Proxy mode: Create and retrieve proxy object with redirect."""
        self.create_and_check_proxy_obj(gmn_client_v1_v2, do_redirect=True)

    def test_1040(self):
        """create(): Proxy mode: Passing invalid url raises InvalidRequest."""
        with pytest.raises(d1_common.types.exceptions.InvalidRequest):
            self.create_and_check_proxy_obj(
                self.client_v2,
                self.v2,
                # do_redirect=False,
                use_invalid_url=True,
            )

    @django.test.override_settings(
        PROXY_MODE_BASIC_AUTH_ENABLED=False,
        PROXY_MODE_BASIC_AUTH_USERNAME=AUTH_USERNAME,
        PROXY_MODE_BASIC_AUTH_PASSWORD=AUTH_PASSWORD,
        PROXY_MODE_STREAM_TIMEOUT=30,
    )
    def test_1050(self):
        """get(): Authentication headers: Not passed to remote server when
        AUTH_ENABLED=False.

        We check this implicitly by checking that the method that generates the
        Authentication header IS NOT called.
        """
        with d1_gmn.tests.gmn_mock.detect_proxy_auth() as m:
            self.create_and_check_proxy_obj(self.client_v2, do_redirect=False)
            assert m.call_count == 0

    @django.test.override_settings(
        PROXY_MODE_BASIC_AUTH_ENABLED=True,
        PROXY_MODE_BASIC_AUTH_USERNAME=AUTH_USERNAME,
        PROXY_MODE_BASIC_AUTH_PASSWORD=AUTH_PASSWORD,
        PROXY_MODE_STREAM_TIMEOUT=30,
    )
    def test_1060(self):
        """get(): Authentication headers: Passed to remote server when
        AUTH_ENABLED=True.

        We check this implicitly by checking that the method that generates the
        Authentication header IS called.
        """
        with d1_gmn.tests.gmn_mock.detect_proxy_auth() as m:
            self.create_and_check_proxy_obj(self.client_v2, do_redirect=False)
            assert m.call_count ==1

    @django.test.override_settings(
        PROXY_MODE_BASIC_AUTH_ENABLED=True,
        PROXY_MODE_BASIC_AUTH_USERNAME=AUTH_USERNAME,
        PROXY_MODE_BASIC_AUTH_PASSWORD=AUTH_PASSWORD,
        PROXY_MODE_STREAM_TIMEOUT=30,
    )
    def test_1070(self):
        """_mk_http_basic_auth_header(): Returns a correctly encoded basic auth
        header value.
        """
        auth_str = d1_gmn.app.proxy._mk_http_basic_auth_header()["Authorization"]
        user_str, pw_str = self.decode_basic_auth(auth_str)
        assert user_str == AUTH_USERNAME
        assert pw_str == AUTH_PASSWORD
