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

import hashlib
import logging

import freezegun
import pytest
import requests
import responses

import d1_common.logging_context
import d1_common.types.exceptions
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.get as mock_get
import d1_test.mock_api.post as mock_post
import d1_test.sample

import d1_client.session as session


@d1_test.d1_test_case.reproducible_random_decorator('TestSession')
@freezegun.freeze_time('1945-01-02')
class TestSession(d1_test.d1_test_case.D1TestCase):
  def _get_hash(self, pid):
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    s = session.Session(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    response = s.GET(['object', pid])
    return hashlib.sha1(response.content).hexdigest()

  def _get_response(self, pid, header_dict=None):
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    s = session.Session(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    return s.GET(['object', pid], headers=header_dict or {})

  def _post(self, query_dict, header_dict, body):
    mock_post.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    s = session.Session(
      d1_test.d1_test_case.MOCK_MN_BASE_URL, query={
        'default_query': 'test',
      }
    )
    return s.POST(['post'], query=query_dict, headers=header_dict, data=body)

  def _post_fields(self, fields_dict):
    mock_post.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    s = session.Session(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    return s.POST(['post'], fields=fields_dict)

  @responses.activate
  def test_1000(self):
    """HTTP GET is successful
    Mocked GET returns object bytes uniquely tied to given PID
    """
    a_pid = 'pid_hy7tf83453y498'
    b_pid = 'pid_09y68gh73n60'
    c_pid = 'pid_987i075058679589060'
    a_hash = self._get_hash(a_pid)
    b_hash = self._get_hash(b_pid)
    c_hash = self._get_hash(c_pid)
    assert a_hash != b_hash
    assert b_hash != c_hash
    assert a_hash != c_hash
    a1_hash = self._get_hash(a_pid)
    c1_hash = self._get_hash(c_pid)
    c2_hash = self._get_hash(c_pid)
    a2_hash = self._get_hash(a_pid)
    assert a_hash == a1_hash
    assert a_hash == a2_hash
    assert c_hash == c1_hash
    assert c_hash == c2_hash

  @responses.activate
  def test_1010(self):
    """Successful HTTP GET returns 200 OK"""
    response = self._get_response('pid1')
    assert response.status_code == 200

  @responses.activate
  def test_1020(self):
    """HTTP GET 404"""
    response = self._get_response('valid_pid', header_dict={'trigger': '404'})
    assert response.status_code == 404
    self.sample.assert_equals(response.text, 'get_404')

  @responses.activate
  def test_1030(self):
    """HTTP GET against http://some.bogus.address/ raises ConnectionError"""
    s = session.Session('http://some.bogus.address')
    logger = logging.getLogger()
    with d1_common.logging_context.LoggingContext(logger):
      logger.setLevel(logging.ERROR)
      with pytest.raises(requests.exceptions.ConnectionError):
        s.GET('/')

  @responses.activate
  def test_1040(self):
    """HTTP POST is successful
    Roundtrip for body, headers and query params
    """
    body_bytes = b'test_body'
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    response = self._post({}, header_dict, body_bytes)
    r_dict = response.json()
    d1_test.sample.assert_equals(r_dict, 'post_roundtrip')

  @responses.activate
  def test_1050(self):
    """Query params passed to Session() and individual POST are correctly
    combined"""
    mock_post.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    body_bytes = b'test_body'
    query_dict = {'abcd': '1234', 'efgh': '5678'}
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    response = self._post(query_dict, header_dict, body_bytes)
    r_dict = response.json()
    d1_test.sample.assert_equals(r_dict, 'post_roundtrip_query')

  @responses.activate
  def test_1060(self):
    """Roundtrip for HTML Form fields"""
    field_dict = {
      'post_data_1': '1234',
      'post_data_2': '5678',
    }
    response = self._post_fields(field_dict)
    r_dict = response.json()
    d1_test.sample.assert_equals(r_dict, 'post_roundtrip_form_fields')

  @responses.activate
  def test_1070(self):
    """cURL command line retains query parameters and headers"""
    query_dict = {'abcd': '1234', 'efgh': '5678'}
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    s = session.Session(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    curl_str = s.get_curl_command_line(
      'POST',
      'http://some.bogus.address',
      query=query_dict,
      headers=header_dict,
    )
    d1_test.sample.assert_equals(curl_str, 'curl_command_line')
