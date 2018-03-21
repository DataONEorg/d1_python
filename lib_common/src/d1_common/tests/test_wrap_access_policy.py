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
"""Test the AccessPolicy context manager"""

import d1_common.types.dataoneTypes
import d1_common.wrap.access_policy
import d1_common.xml

import d1_test.d1_test_case
import d1_test.sample


class TestAccessPolicyWrapper(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    # ap_pyxb = d1_test.sample.load_xml_to_pyxb('accessPolicy_v1_0.redundant.xml')
    self.sysmeta_pyxb = d1_test.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0.tz_non_utc.xml'
    )

  def test_1000(self):
    """__init__(): Correctly initialized from AccessPolicy PyXB obj"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert not ap.is_empty()
      self.sample.assert_equals(ap.get_normalized_perm_list(), 'init')

  def test_1010(self):
    """clear(): All permissions are removed"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert not ap.is_empty()
      ap.clear()
      assert ap.is_empty()

  def test_1020(self):
    """get_access_policy_pyxb()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      ap_pyxb = ap.get_normalized_pyxb()
      assert isinstance(ap_pyxb, d1_common.types.dataoneTypes.AccessPolicy)
      self.sample.assert_equals(ap_pyxb, 'get_access_policy_pyxb')

  def test_1030(self):
    """get_normalized_perm_list()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      norm_perm_list = ap.get_normalized_perm_list()
      self.sample.assert_equals(norm_perm_list, 'get_normalized_perm_list')

  def test_1040(self):
    """get_highest_perm_str()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert ap.get_highest_perm_str('subj3') == 'changePermission'
      assert ap.get_highest_perm_str('subj4') == 'write'

  def test_1050(self):
    """get_effective_perm_list()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert ap.get_effective_perm_list('subj3') == [
        'read', 'write', 'changePermission'
      ]
      assert ap.get_effective_perm_list('subj4') == ['read', 'write']

  def test_1060(self):
    """get_subjects_with_equal_or_higher_perm()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert ap.get_subjects_with_equal_or_higher_perm('write') == {
        'subj1', 'subj2', 'subj3', 'subj4', 'subj5', 'subj6'
      }

  def test_1070(self):
    """is_public()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert ap.is_public()
      ap.clear()
      assert not ap.is_public()
      ap.add_public_read()
      assert ap.is_public()

  def test_1080(self):
    """is_private(), is_empty()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert not ap.is_private()
      assert not ap.is_empty()
      ap.clear()
      assert ap.is_private()
      assert ap.is_empty()
      ap.add_perm('newsubj', 'write')
      assert not ap.is_private()
      assert not ap.is_empty()

  def test_1090(self):
    """are_equivalent_pyxb()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      other_pyxb = self.sample.load_xml_to_pyxb(
        'systemMetadata_v2_0.tz_non_utc.xml'
      )
      assert ap.are_equivalent_pyxb(other_pyxb.accessPolicy)
      other_pyxb = self.sample.load_xml_to_pyxb('sysmeta_variation_1.xml')
      assert not ap.are_equivalent_pyxb(other_pyxb.accessPolicy)

  def test_1100(self):
    """are_equivalent_xml()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      # self.sample.save_obj(self.sysmeta_pyxb.accessPolicy, 'accessPolicy_v1_0.xml')
      other_xml = self.sample.load_utf8_to_str(
        'accessPolicy_v1_0.redundant.xml'
      )
      assert not ap.are_equivalent_xml(other_xml)
      other_xml = self.sample.load_utf8_to_str('accessPolicy_v1_0.xml')
      assert ap.are_equivalent_xml(other_xml)

  def test_1110(self):
    """subj_has_perm()"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      assert ap.subj_has_perm('subj3', 'read')
      assert ap.subj_has_perm('subj3', 'changePermission')
      assert ap.subj_has_perm('subj4', 'write')
      assert not ap.subj_has_perm('subj4', 'changePermission')

  def test_1120(self):
    """add_perm(): Add permissions for existing subj"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      assert ap.get_effective_perm_list('public') == ['read']
      ap.add_perm('public', 'changePermission')
      after_dict = ap.get_normalized_perm_list()
      assert ap.get_effective_perm_list('public') == [
        'read', 'write', 'changePermission'
      ]
      self.sample.assert_diff_equals(
        before_dict, after_dict, 'add_perm_existing'
      )

  def test_1130(self):
    """add_perm(): Add permissions for new subj"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.add_perm('newsubj', 'write')
      after_dict = ap.get_normalized_perm_list()
      assert ap.get_effective_perm_list('newsubj') == ['read', 'write']
      self.sample.assert_diff_equals(before_dict, after_dict, 'add_perm_new')

  def test_1140(self):
    """remove_perm(): No change if subj exists but does not have the perm"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_perm('public', 'changePermission')
      after_dict = ap.get_normalized_perm_list()
      assert before_dict == after_dict

  def test_1150(self):
    """remove_perm(): No change if subj does not exist"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_perm('public', 'changePermission')
      after_dict = ap.get_normalized_perm_list()
      assert before_dict == after_dict

  def test_1160(self):
    """remove_perm(): Removing read removes subj entirely"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_perm('subj4', 'read')
      after_dict = ap.get_normalized_perm_list()
      self.sample.assert_diff_equals(
        before_dict, after_dict, 'remove_perm_read'
      )

  def test_1170(self):
    """remove_perm(): Lower perms remain after removing higher"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_perm('subj5', 'changePermission')
      after_dict = ap.get_normalized_perm_list()
      self.sample.assert_diff_equals(
        before_dict, after_dict, 'remove_perm_lower'
      )

  def test_1180(self):
    """remove_subj(): Remove known subj"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_subj('subj5')
      after_dict = ap.get_normalized_perm_list()
      self.sample.assert_diff_equals(
        before_dict, after_dict, 'remove_subj_known'
      )

  def test_1190(self):
    """remove_subj(): No change if subj does not exist"""
    with d1_common.wrap.access_policy.wrap_sysmeta_pyxb(
        self.sysmeta_pyxb
    ) as ap:
      before_dict = ap.get_normalized_perm_list()
      ap.remove_subj('newsubj')
      after_dict = ap.get_normalized_perm_list()
      assert before_dict == after_dict

  # Module level wrappers

  def test_2000(self):
    """module level is_empty()"""
    assert not d1_common.wrap.access_policy.is_empty(
      self.sysmeta_pyxb.accessPolicy
    )

  def test_2010(self):
    """module level get_normalized_perm_list()"""
    d = d1_common.wrap.access_policy.get_normalized_perm_list(
      self.sysmeta_pyxb.accessPolicy
    )
    self.sample.assert_equals(d, 'module_get_normalized_perm_list')
