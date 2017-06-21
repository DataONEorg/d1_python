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

import pytest
import pyxb

import d1_common.system_metadata
import d1_common.xml

import d1_test.d1_test_case

# logging.basicConfig(level=logging.DEBUG)


class TestSystemMetadata(d1_test.d1_test_case.D1TestCase):
  sm_pyxb = d1_test.sample.load_xml_to_pyxb('systemMetadata_v2_0.xml')

  def test_1000(self):
    """PyXB performs schema validation on sysmeta object and raises
    pyxb.PyXBException on invalid XML doc
    """
    with pytest.raises(pyxb.PyXBException):
      self.sample.load_xml_to_pyxb('systemMetadata_v1_0.invalid.xml')

  def test_1010(self):
    """is_equivalent() Returns False for modified sysmeta"""
    modified_pyxb = self.sample.load_xml_to_pyxb('systemMetadata_v2_0.xml')
    modified_pyxb.identifier = 'modifiedIdentifier'
    assert not d1_common.system_metadata.is_equivalent_pyxb(
      self.sm_pyxb, modified_pyxb
    )

  def test_1020(self):
    """is_equivalent() Returns True for duplicated sysmeta"""
    assert d1_common.system_metadata.is_equivalent_pyxb(
      self.sm_pyxb, self.sm_pyxb
    )

  def test_1030(self):
    """is_equivalent() Returns True for sysmeta where elements that can occur in
    any order without changing the meaning of the doc have been shuffled
    around
    """
    swizzled_pyxb = self.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0.swizzled.xml'
    )
    assert d1_common.system_metadata.is_equivalent_pyxb(
      self.sm_pyxb, swizzled_pyxb
    )
