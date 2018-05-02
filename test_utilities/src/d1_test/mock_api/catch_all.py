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
  mock_catch_all.add_callback(d1_test.d1_test_case.MOCK_CN_MN_BASE_URL)
  echo_dict = self.client.getFormat('valid_format_id')
  ...
"""

import base64
import logging
import re

import decorator
import mock
import responses

import d1_common.const
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.d1_exception
import d1_test.mock_api.util
import d1_test.sample


def activate(func):
  @responses.activate
  def wrapper(func2, *args, **kwargs):
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
      return func2(*args, **kwargs)

  return decorator.decorator(wrapper, func)


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


def assert_expected_echo(received_echo_dict, name_postfix_str, client=None):
  # _dict_key_val_to_unicode(received_echo_dict)
  _delete_volatile_keys(received_echo_dict)
  d1_test.sample.assert_equals(
    received_echo_dict, name_postfix_str, client, 'echo'
  )


def delete_volatile_post_keys(echo_dict):
  """Delete keys that have values that may differ between POST calls"""
  del_key(echo_dict, ['request', 'body_base64'])
  del_key(echo_dict, ['request', 'header_dict', 'Content-Type'])


def del_key(d, key_path):
  k = key_path[0]
  if k in d:
    if len(key_path) > 1:
      del_key(d[k], key_path[1:])
    else:
      del d[k]


def _delete_volatile_keys(echo_dict):
  """Delete keys that have values that may differ between calls"""
  del_key(echo_dict, ['request', 'body_base64'])
  del_key(echo_dict, ['request', 'header_dict', 'Accept'])
  del_key(echo_dict, ['request', 'header_dict', 'Accept-Encoding'])
  del_key(echo_dict, ['request', 'header_dict', 'User-Agent'])
  del_key(echo_dict, ['request', 'header_dict', 'Charset'])
  del_key(echo_dict, ['request', 'header_dict', 'Connection'])
  del_key(echo_dict, ['request', 'header_dict', 'Content-Length'])
  del_key(echo_dict, ['request', 'header_dict', 'Content-Type'])
  del_key(echo_dict, ['request', 'header_dict'])


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
  version_tag, endpoint_str, param_list, query_dict, client = (
    d1_test.mock_api.util.parse_rest_url(request.url)
  )
  header_dict = {
    'Content-Type': d1_common.const.CONTENT_TYPE_JSON,
  }
  if isinstance(body_str, str):
    body_str = body_str.encode('utf-8')
  body_dict = {
    'body_base64':
      str(base64.standard_b64encode(body_str)) if body_str else None,
    'version_tag':
      version_tag,
    'endpoint_str':
      endpoint_str,
    'param_list':
      param_list,
    'query_dict':
      query_dict,
    'pyxb_namespace':
      str(client.bindings.Namespace),
    'header_dict':
      dict(request.headers),
  }
  return 200, header_dict, d1_common.util.serialize_to_normalized_pretty_json(
    body_dict
  )
