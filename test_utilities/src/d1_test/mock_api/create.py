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
"""Mock a generic POST request by echoing the posted body.

A DataONEException can be triggered by adding a custom header. See
d1_exception.py
"""

import base64
import logging
import re
import urllib.parse

import responses

import d1_common.checksum
import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.url
import d1_common.util

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util

CREATE_ENDPOINT_RX = r'v([123])/object'


def add_callback(base_url):
  responses.add_callback(
    responses.POST,
    re.compile(
      r'^' + d1_common.url.joinPathElements(base_url, CREATE_ENDPOINT_RX)
    ),
    callback=_request_callback,
    content_type='',
  )


def _request_callback(request):
  """Echo an MN.create() POST. Return a valid Identifier XML doc in the
  body to satisfy the requirements for create() and echo of the POSTed
  information in headers (serialized to Base64 encoded JSON).
  """
  logging.debug('Received callback. url="{}"'.format(request.url))
  # Return DataONEException if triggered
  exc_response_tup = d1_test.mock_api.d1_exception.trigger_by_header(request)
  if exc_response_tup:
    return exc_response_tup
  # Return regular response
  try:
    body_bytes = request.body.read()
  except AttributeError:
    body_bytes = request.body

  assert isinstance(body_bytes, bytes)

  url_obj = urllib.parse.urlparse(request.url)

  # header_dict = {
  #   'Content-Type':
  #     d1_common.const.CONTENT_TYPE_XML,
  #   'Echo-Body-Base64':
  #     base64.standard_b64encode(body_bytes).decode('utf-8'),
  #   'Echo-Query-Base64':
  #     base64.standard_b64encode(
  #       d1_common.util.serialize_to_normalized_pretty_json(
  #         urllib.parse.parse_qs(url_obj.query)
  #       ).encode('utf-8')
  #     ).decode('utf-8'),
  #   'Echo-Header-Base64':
  #     base64.standard_b64encode(
  #       d1_common.util.serialize_to_normalized_pretty_json(
  #         dict(request.headers)
  #       ).encode('utf-8')
  #     ).decode('utf-8'),
  # }

  header_dict = pack_echo_header(body_bytes, request.headers, url_obj)

  return (
    200, header_dict,
    d1_common.types.dataoneTypes.identifier('echo-post').toxml('utf-8'),
  )


def pack_echo_header(body_bytes, headers, url_obj):
  return {
    'Content-Type':
      d1_common.const.CONTENT_TYPE_XML,
    'Echo-POST-JSON-Base64':
      base64.standard_b64encode(
        d1_common.util.serialize_to_normalized_pretty_json({
          'query': urllib.parse.parse_qs(url_obj.query),
          'headers': dict(headers),
          # TODO: Need to include body, but it must be normalized. As it is, the
          # MMP parts arrive in random order
          # 'body': body_bytes,
        }).encode('utf-8')
      ).decode('ascii')
  }


def unpack_echo_header(header_dict):
  return (
    base64.standard_b64decode(
      header_dict['Echo-POST-JSON-Base64'].encode('ascii')
    ).decode('utf-8')
  )

  # TODO: MMP normalization

  # echo_dict = json.loads(
  #   base64.standard_b64decode(header_dict['Echo-POST-JSON-Base64'].encode('ascii')).decode('utf-8')
  # )
  #
  # multipart_decoder = requests_toolbelt.MultipartDecoder(
  #   echo_dict['body'].encode('utf-8'),
  #   echo_dict['headers']['Content-Type'],
  # )
  #
  # serialized_mmp_list = [
  #   (dict(p.headers), 'SHA-1/{}'.format(
  #     d1_common.checksum.format_checksum(
  #       d1_common.checksum.create_checksum_object_from_string(
  #         p.text.encode('utf-8')
  #       )
  #     )
  #   )) for p in multipart_decoder.parts
  # ]
  # echo_dict['body'] = serialized_mmp_list
  # return echo_dict
