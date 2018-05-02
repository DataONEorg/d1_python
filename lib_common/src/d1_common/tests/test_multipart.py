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

import requests_toolbelt
import responses

import d1_common.multipart

import d1_test.d1_test_case
import d1_test.mock_api.post as mock_post

import d1_client.session as session


class TestMultipart(d1_test.d1_test_case.D1TestCase):
  def _post_fields(self, fields_dict):
    mock_post.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    s = session.Session(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    return s.POST(['post'], fields=fields_dict)

  @responses.activate
  def test_1000(self):
    """Parse and normalize multipart str"""
    field_dict = {
      'bcd': '333',
      'abc': '111',
      'cde': '444',
      'efg': '555',
      'def': '222',
    }
    mmp_stream = requests_toolbelt.MultipartEncoder(fields=field_dict)
    body_part_tup = d1_common.multipart.parse_str(
      mmp_stream.read(), mmp_stream.content_type
    )
    body_str = d1_common.multipart.normalize(body_part_tup)
    self.sample.assert_equals(body_str, 'parse_and_normalize')
