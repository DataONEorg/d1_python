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

import responses

import d1_test.d1_test_case
import d1_test.mock_api.create
import d1_test.sample


class TestMNClient(d1_test.d1_test_case.D1TestCase):
  def setup_class(self):
    self.sysmeta_pyxb = d1_test.sample.load_xml_to_pyxb(
      'BAYXXX_015ADCP015R00_20051215.50.9_SYSMETA.xml'
    )

  #=========================================================================
  # MNCore
  #=========================================================================

  @responses.activate
  def test_1000(self, mn_client_v1):
    """MNCore.createResponse(): Generates a correctly encoded Multipart document
    and Content-Type header
    """
    d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)

    response = mn_client_v1.createResponse(
      '1234', b'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    assert response.status_code == 200
    echo_dict = d1_test.mock_api.create.unpack_echo_header(response.headers)
    # TODO: echo_dict is currently a JSON str
    # echo_dict['identifier'] = (
    #   d1_common.types.dataoneTypes.CreateFromDocument(response.content).value()
    # )
    self.sample.assert_equals(echo_dict, 'mmp_encoding', mn_client_v1)

  @responses.activate
  def test_1010(self, mn_client_v1):
    """MNCore.create(): Returned Identifier object is correctly parsed"""
    d1_test.mock_api.create.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    identifier_pyxb = mn_client_v1.create(
      '1234', 'BAYXXX_015ADCP015R00_20051215.50.9', self.sysmeta_pyxb
    )
    assert identifier_pyxb.value() == 'echo-post'
