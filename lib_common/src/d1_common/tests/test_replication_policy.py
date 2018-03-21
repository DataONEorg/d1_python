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

import copy

import d1_common.replication_policy
import d1_common.xml

import d1_test.d1_test_case


class TestReplicationPolicy(d1_test.d1_test_case.D1TestCase):
  sm_with_rp_pyxb = d1_test.sample.load_xml_to_pyxb('systemMetadata_v2_0.xml')
  sm_without_rp_pyxb = d1_test.sample.load_xml_to_pyxb(
    'sysmeta_variation_3.xml'
  )
  rp_pyxb = d1_test.sample.load_xml_to_pyxb(
    'systemMetadata_v2_0.xml'
  ).replicationPolicy
  rp_swiz_pyxb = d1_test.sample.load_xml_to_pyxb(
    'systemMetadata_v2_0.swizzled.xml'
  ).replicationPolicy

  def test_1000(self):
    """has_replication_policy()"""
    assert d1_common.replication_policy.has_replication_policy(
      self.sm_with_rp_pyxb
    )
    assert not d1_common.replication_policy.has_replication_policy(
      self.sm_without_rp_pyxb
    )

  def test_1010(self):
    """normalize(): Normalize policy without conflict"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    self.sample.assert_equals(self.rp_swiz_pyxb, 'normalize_swiz')
    d1_common.replication_policy.normalize(rp_swiz_pyxb)
    self.sample.assert_equals(rp_swiz_pyxb, 'normalize_normalized')

  def test_1020(self):
    """pyxb_to_dict()"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    rp_dict = d1_common.replication_policy.pyxb_to_dict(rp_swiz_pyxb)
    self.sample.assert_equals(rp_dict, 'pyxb_to_dict')

  def test_1030(self):
    """dict_to_pyxb()"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    rp_dict_1 = d1_common.replication_policy.pyxb_to_dict(rp_swiz_pyxb)
    rp_pyxb_2 = d1_common.replication_policy.dict_to_pyxb(rp_dict_1)
    rp_dict_2 = d1_common.replication_policy.pyxb_to_dict(rp_pyxb_2)
    assert rp_dict_1 == rp_dict_2

  def test_1040(self):
    """add_node(): Add node without conflict"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    d1_common.replication_policy.add_preferred(
      rp_swiz_pyxb, 'add_preferred_urn'
    )
    self.sample.assert_equals(rp_swiz_pyxb, 'add_node')

  def test_1050(self):
    """add_node(): Add node with conflict"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    d1_common.replication_policy.add_preferred(rp_swiz_pyxb, 'add_urn')
    d1_common.replication_policy.add_blocked(rp_swiz_pyxb, 'add_urn')
    # Assert add_urn not in preferred
    self.sample.assert_equals(rp_swiz_pyxb, 'add_node_conflict')

  def test_1060(self):
    """normalize(): Normalize without conflict"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    self.sample.assert_equals(self.rp_swiz_pyxb, 'normalize_swiz')
    d1_common.replication_policy.normalize(rp_swiz_pyxb)
    self.sample.assert_equals(rp_swiz_pyxb, 'normalize_normalized')

  def test_1070(self):
    """normalize(): Normalize with conflict"""
    rp_swiz_pyxb = copy.deepcopy(self.rp_swiz_pyxb)
    rp_dict = d1_common.replication_policy.pyxb_to_dict(rp_swiz_pyxb)
    rp_dict['pref'].add('add_urn')
    rp_dict['block'].add('add_urn')
    rp_pyxb = d1_common.replication_policy.dict_to_pyxb(rp_dict)
    self.sample.assert_equals(rp_pyxb, 'normalize_swiz_conflict_before')
    d1_common.replication_policy.normalize(rp_pyxb)
    self.sample.assert_equals(rp_pyxb, 'normalize_swiz_conflict_after')

  def test_1080(self):
    """sysmeta_set_default_rp(): Existing RP"""
    sm_pyxb = copy.deepcopy(self.sm_with_rp_pyxb)
    d1_common.replication_policy.sysmeta_set_default_rp(sm_pyxb)
    self.sample.assert_equals(sm_pyxb, 'sysmeta_set_default_rp_existing')

  def test_1090(self):
    """sysmeta_set_default_rp(): New RP"""
    sm_pyxb = copy.deepcopy(self.sm_without_rp_pyxb)
    d1_common.replication_policy.sysmeta_set_default_rp(sm_pyxb)
    self.sample.assert_equals(sm_pyxb, 'sysmeta_set_default_rp_new')

  def test_1100(self):
    """add_node(): Add node without existing RP"""
    sm_pyxb = copy.deepcopy(self.sm_without_rp_pyxb)
    d1_common.replication_policy.sysmeta_add_preferred(sm_pyxb, 'add_pref_urn')
    self.sample.assert_equals(sm_pyxb, 'add_node_without_existing')

  def test_1110(self):
    """sysmeta_add_preferred()"""
    sm_pyxb = copy.deepcopy(self.sm_with_rp_pyxb)
    d1_common.replication_policy.sysmeta_add_preferred(sm_pyxb, 'add_urn')
    d1_common.replication_policy.sysmeta_add_blocked(sm_pyxb, 'add_urn')
    # Assert add_urn not in preferred
    self.sample.assert_equals(sm_pyxb, 'sysmeta_add_preferred_conflict')
