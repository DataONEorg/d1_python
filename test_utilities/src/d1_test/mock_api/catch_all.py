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
"""Mock any requests not specifically supported in the other mock API handlers

This provides a simple way to perform a basic check of API wrappers without
writing specific mock handlers. It disables PyXB deserialization in the client
and returns a dict with an echo of the request.

If the echoed information is not checked, only the presence of the wrapper and
being able to call it without error is tested.

Note: The catch_all handler cannot be used together with the mock APIs as it
patches the _read_dataone_* methods that the other APIs rely on, and redirects
them to mock_read_response() in this module.

A DataONEException can be triggered by adding a custom header. See
d1_exception.py

Usage:

import d1_test.mock_api.catch_all as mock_catch_all

@mock_catch_all.activate
def test_0010(self):
  mock_catch_all.add_callback(config.CN_RESPONSES_BASE_URL)
  echo_dict = self.client.getFormat('valid_format_id')
  ...
"""

import base64
import functools
import json
import logging
import pprint
import re
import unittest

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.url
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util
import mock
import responses


def activate(fun):
  @functools.wraps(fun)
  @responses.activate
  def wrap(*args, **kwargs):
    with mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_dataone_type_response',
        mock_read_response
    ), mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_boolean_404_response',
        mock_read_response
    ), mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_boolean_response',
        mock_read_response
    ), mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_boolean_401_response',
        mock_read_response
    ), mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_stream_response',
        mock_read_response
    ), mock.patch(
        'd1_client.baseclient.DataONEBaseClient._read_json_response',
        mock_read_response
    ):
      return fun(*args, **kwargs)

  return wrap


def add_callback(base_url):
  for method in [
      responses.DELETE, responses.GET, responses.HEAD, responses.OPTIONS,
      responses.PATCH, responses.POST, responses.PUT
  ]:
    responses.add_callback(
      method,
      re.compile('^{}'.format(base_url)), callback=_request_callback,
      content_type=''
    )


def assert_expected_echo(received_echo_dict, expected_echo_dict):
  test_case = unittest.TestCase('__init__')
  _dict_key_val_to_unicode(received_echo_dict)
  _dict_key_val_to_unicode(expected_echo_dict)
  _delete_volatile_keys(received_echo_dict)
  _delete_volatile_keys(expected_echo_dict)
  logging.debug(
    'received_echo_dict: {}'.format(pprint.pformat(received_echo_dict))
  )
  # Check the remaining values, which should all be static.
  test_case.maxDiff = None
  test_case.assertDictEqual(received_echo_dict, expected_echo_dict)


def _delete_volatile_keys(echo_dict):
  """Delete keys that have values that may differ between calls"""
  for key_path in [
    ['request', 'body_base64'],
    ['request', 'header_dict', 'Accept'],
    ['request', 'header_dict', 'Accept-Encoding'],
    ['request', 'header_dict', 'User-Agent'],
    ['request', 'header_dict', 'Charset'],
    ['request', 'header_dict', 'Connection'],
    ['request', 'header_dict', 'Content-Length'],
    ['request', 'header_dict', 'Content-Type'],
    ['request', 'header_dict'],
  ]:
    _delete_key(echo_dict, key_path)


def _delete_key(echo_dict, key_path):
  d = echo_dict
  for key in key_path[:-1]:
    try:
      d = d[key]
    except KeyError:
      return
  try:
    del d[key_path[-1]]
  except KeyError:
    pass


def _dict_key_val_to_unicode(d):
  if isinstance(d, dict):
    return {
      _str_to_unicode(k): _dict_key_val_to_unicode(v) for k, v in d.items()
    }
  elif isinstance(d, list):
    return [_str_to_unicode(v) for v in d]
  elif isinstance(d, basestring):
    return _str_to_unicode(d)
  else:
    return d


def _str_to_unicode(s):
  return s if isinstance(s, unicode) else s.decode('utf8')


@classmethod
def mock_read_response(
    d1_client_cls, response, d1_type_name=None, vendorSpecific=None,
    response_is_303_redirect=False
):
  if response.headers['Content-Type'] == d1_common.const.CONTENT_TYPE_JSON:
    return {
      'request': response.json(),
      'wrapper': {
        'class_name': d1_client_cls.__name__,
        'expected_type': d1_type_name,
        'vendor_specific_dict': vendorSpecific,
        'received_303_redirect': response_is_303_redirect,
      }
    }
  else:
    raise d1_common.types.exceptions.deserialize(response.content)


def _request_callback(request):
  logging.debug('Received callback. url="{}"'.format(request.url))
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return regular response
  try:
    body_str = request.body.read()
  except AttributeError:
    body_str = request.body
  version_tag, endpoint_str, param_list, query_dict, pyxb_bindings = (
    d1_test.mock_api.util.parse_rest_url(request.url)
  )
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_JSON,
  }
  body_dict = {
    'body_base64': base64.b64encode(body_str or ''),
    'version_tag': version_tag,
    'endpoint_str': endpoint_str,
    'param_list': param_list,
    'query_dict': query_dict,
    'pyxb_namespace': str(pyxb_bindings.Namespace),
    'header_dict': dict(request.headers),
  }
  return 200, header_dict, json.dumps(body_dict)
