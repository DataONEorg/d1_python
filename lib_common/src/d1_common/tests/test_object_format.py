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

import d1_common.object_format

import d1_test.d1_test_case


class TestObjectFormat(d1_test.d1_test_case.D1TestCase):
  ofl_pyxb = d1_test.sample.load_xml_to_pyxb('objectFormatList_v2_0.xml')

  def test_1000(self):
    """pyxb_to_dict()"""
    ofl_dict = d1_common.object_format.pyxb_to_dict(self.ofl_pyxb)
    assert len(ofl_dict) == 117

    expected_text_xml_dict = {
      'extension': 'html',
      'format_name': 'Hypertext Markup Language',
      'format_type': 'DATA',
      'media_type': {
        'name': 'text/html',
        'property_list': []
      }
    }

    assert ofl_dict['text/html'] == expected_text_xml_dict
