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

from __future__ import absolute_import

import base64
import json

import requests_toolbelt
import responses

import d1_common.const
import d1_common.types.dataoneTypes
import d1_common.util

import d1_test.d1_test_case
import d1_test.mock_api.create
import d1_test.sample


class TestMNClient(d1_test.d1_test_case.D1TestCase):
  sysmeta_pyxb = d1_test.sample.load_xml_to_pyxb(
    'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
  )
  sysmeta_xml = d1_test.sample.load_xml_to_pyxb(
    'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
  )
  obj = 'test'
  pid = '1234'

  #=========================================================================
  # MNCore
  #=========================================================================

  @responses.activate
  def test_1000(self, mn_client_v1):
    """MNCore.createResponse(): Generates a correctly encoded Multipart document
    and Content-Type header
    """
    d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)

    response = mn_client_v1.createResponse(
      '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    assert response.status_code == 200

    identifier_pyxb = d1_common.types.dataoneTypes.CreateFromDocument(
      response.content
    )
    assert identifier_pyxb.value() == 'echo-post'
    echo_body_str = base64.b64decode(response.headers['Echo-Body-Base64'])
    echo_query_dict = json.loads(
      base64.b64decode(response.headers['Echo-Query-Base64'])
    )
    echo_header_dict = json.loads(
      base64.b64decode(response.headers['Echo-Header-Base64'])
    )
    assert isinstance(echo_body_str, basestring)
    assert isinstance(echo_query_dict, dict)
    assert isinstance(echo_header_dict, dict)

    multipart_decoder = requests_toolbelt.MultipartDecoder(
      echo_body_str, echo_header_dict['Content-Type']
    )

    assert len(multipart_decoder.parts) == 3

    assert dict(multipart_decoder.parts[0].headers) == \
      {
        'Content-Disposition':
          'form-data; name="sysmeta"; filename="sysmeta.xml"'
      }
    assert '<?xml' in multipart_decoder.parts[0].content
    assert '<identifier>BAYXXX_015ADCP015R00_20051215.50.9</identifier>' in \
      multipart_decoder.parts[0].content

    assert dict(multipart_decoder.parts[1].headers) == \
      {
        'Content-Disposition':
          'form-data; name="object"; filename="content.bin"'
      }
    assert multipart_decoder.parts[1].content == 'BAYXXX_015ADCP015R00_20051215.50.9'

    assert dict(multipart_decoder.parts[2].headers) == \
      {'Content-Disposition': 'form-data; name="pid"'}
    assert multipart_decoder.parts[2].content == '1234'

  @responses.activate
  def test_1010(self, mn_client_v1):
    """MNCore.create(): Returned Identifier object is correctly parsed"""
    d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    identifier_pyxb = mn_client_v1.create(
      '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    assert identifier_pyxb.value() == 'echo-post'
