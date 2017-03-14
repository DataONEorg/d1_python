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
"""Unit tests for Session.
"""

# Stdlib
import hashlib
import logging
import sys

# 3rd party
import responses
import requests

# D1
import d1_common.logging_context
from d1_common.test_case_with_url_compare import TestCaseWithURLCompare
import d1_common.types.exceptions

# App
sys.path.append('..')
import mock_get # noqa: E402
import mock_post # noqa: E402
import session # noqa: E402
import shared_settings # noqa: E402


class TestSession(TestCaseWithURLCompare):
  def setUp(self):
    mock_get.init(shared_settings.MN_RESPONSES_URL)
    mock_post.init(shared_settings.MN_RESPONSES_URL)

  def tearDown(self):
    pass

  def _get_hash(self, pid):
    s = session.Session(shared_settings.MN_RESPONSES_URL)
    response = s.GET(['object', pid])
    return hashlib.sha1(response.content).hexdigest()

  def _get_response(self, pid):
    s = session.Session(shared_settings.MN_RESPONSES_URL)
    return s.GET(['object', pid])

  def _post(self, query_dict, header_dict, body):
    s = session.Session(
      shared_settings.MN_RESPONSES_URL, query={
        'default_query': 'test',
      }
    )
    return s.POST(['post'], query=query_dict, headers=header_dict, data=body)

  def _post_fields(self, fields_dict):
    s = session.Session(shared_settings.MN_RESPONSES_URL)
    return s.POST(['post'], fields=fields_dict)

  @responses.activate
  def test_005(self):
    """HTTP GET is successful
    Mocked GET returns object bytes uniquely tied to given PID.
    """
    a_pid = 'pid_hy7tf83453y498'
    b_pid = 'pid_09y68gh73n60'
    c_pid = 'pid_987i075058679589060'
    a_hash = self._get_hash(a_pid)
    b_hash = self._get_hash(b_pid)
    c_hash = self._get_hash(c_pid)
    self.assertNotEqual(a_hash, b_hash)
    self.assertNotEqual(b_hash, c_hash)
    self.assertNotEqual(a_hash, c_hash)
    a1_hash = self._get_hash(a_pid)
    c1_hash = self._get_hash(c_pid)
    c2_hash = self._get_hash(c_pid)
    a2_hash = self._get_hash(a_pid)
    self.assertEqual(a_hash, a1_hash)
    self.assertEqual(a_hash, a2_hash)
    self.assertEqual(c_hash, c1_hash)
    self.assertEqual(c_hash, c2_hash)

  @responses.activate
  def test_010(self):
    """Successful HTTP GET returns 200 OK"""
    response = self._get_response('pid1')
    self.assertEqual(response.status_code, 200)

  @responses.activate
  def test_020(self):
    """HTTP GET 404"""
    response = self._get_response('404')
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.text, 'Return code: 404')

  def test_050(self):
    """HTTP GET against http://some.bogus.address/ raises ConnectionError"""
    s = session.Session('http://some.bogus.address')
    logger = logging.getLogger()
    with d1_common.logging_context.LoggingContext(logger):
      logger.setLevel(logging.ERROR)
      self.assertRaises(requests.exceptions.ConnectionError, s.GET, '/')

  @responses.activate
  def test_100(self):
    """HTTP POST is successful
    Roundtrip for body, headers and query params.
    """
    body_str = 'body_abc'
    query_dict = {'abcd': '1234', 'efgh': '5678'}
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    response = self._post(query_dict, header_dict, body_str)
    r_dict = response.json()
    self.assertEqual(r_dict['body_str'], body_str)
    self.assertIn('abcd', r_dict['query_dict'])
    self.assertEqual(r_dict['query_dict']['abcd'], ['1234'])
    self.assertIn('ijkl', r_dict['header_dict'])
    self.assertEqual(r_dict['header_dict']['ijkl'], '9876')
    self.assertIn('mnop', r_dict['header_dict'])
    self.assertEqual(r_dict['header_dict']['mnop'], '5432')
    self.assertIn('Content-Length', r_dict['header_dict'])
    self.assertEqual(
      r_dict['header_dict']['Content-Length'], str(len(body_str))
    )

  @responses.activate
  def test_102(self):
    """Query params passed to Session() and individual POST are combined
    """
    body_str = 'body_abc'
    query_dict = {'abcd': '1234', 'efgh': '5678'}
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    response = self._post(query_dict, header_dict, body_str)
    r_dict = response.json()
    self.assertEqual(r_dict['body_str'], body_str)
    self.assertIn('abcd', r_dict['query_dict'])
    self.assertEqual(r_dict['query_dict']['abcd'], ['1234'])
    self.assertIn('default_query', r_dict['query_dict'])
    self.assertEqual(r_dict['query_dict']['default_query'], ['test'])

  @responses.activate
  def test_103(self):
    """Roundtrip for HTML Form fields"""
    field_dict = {
      'post_data_1': '1234',
      'post_data_2': '5678',
    }
    response = self._post_fields(field_dict)
    r_dict = response.json()
    # pprint.pprint(r_dict)
    self.assertIn('Content-Type', r_dict['header_dict'])
    self.assertIn('multipart/form-data', r_dict['header_dict']['Content-Type'])
    self.assertIn('post_data_1', r_dict['body_str'])
    self.assertIn('post_data_2', r_dict['body_str'])
    self.assertIn('1234', r_dict['body_str'])
    self.assertIn('5678', r_dict['body_str'])

  @responses.activate
  def test_200(self):
    """cURL command line retains query parameters and headers"""
    query_dict = {'abcd': '1234', 'efgh': '5678'}
    header_dict = {'ijkl': '9876', 'mnop': '5432'}
    s = session.Session(shared_settings.MN_RESPONSES_URL)
    curl_str = s.get_curl_command_line(
      'POST',
      'http://some.bogus.address',
      query=query_dict,
      headers=header_dict,
    )
    self.assertEqual(
      curl_str,
      'curl -X POST -H "ijkl: 9876" -H "mnop: 5432" http://some.bogus.address?abcd=1234&efgh=5678',
    )
