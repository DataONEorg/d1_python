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
"""Test serialization and de-serialization of the ObjectList type
"""

# Stdlib
import unittest

# App
import d1_common.object_format
import util


class TestObjectFormat(unittest.TestCase):
  def setUp(self):
    self.ofl_pyxb = util.read_test_xml('objectFormatList_v2_0.xml')

  def test_010(self):
    """pyxb_to_dict()"""
    ofl_dict = d1_common.object_format.pyxb_to_dict(self.ofl_pyxb)
    self.assertEqual(len(ofl_dict), 117)

    expected_text_xml_dict = {
      'extension': u'html',
      'format_name': u'Hypertext Markup Language',
      'format_type': u'DATA',
      'media_type': {
        'name': u'text/html',
        'property_list': []
      }
    }

    self.assertDictEqual(ofl_dict['text/html'], expected_text_xml_dict)
