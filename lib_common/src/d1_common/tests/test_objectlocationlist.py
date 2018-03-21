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

import xml.sax

import pyxb

import d1_test.d1_test_case


class TestObjectLocationList(d1_test.d1_test_case.D1TestCase):
  parameterize_dict = {
    'test_1000': [
      dict(filename='object_list_gmn_valid.xml', raises_pyxb_exc=False),
      dict(filename='object_list_invalid_1.xml', raises_pyxb_exc=True),
    ],
  }

  def test_1000(self, filename, raises_pyxb_exc):
    """Deserialize various ObjectLocationList XML docs"""
    try:
      self.sample.load_utf8_to_str(filename)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if not raises_pyxb_exc:
        raise
