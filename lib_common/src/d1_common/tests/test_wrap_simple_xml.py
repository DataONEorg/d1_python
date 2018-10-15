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
"""Test the SimpleXML context manager
"""

import datetime
import xml.etree.ElementTree as ET

import pytest

import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.wrap.simple_xml
import d1_common.xml

import d1_test.d1_test_case
import d1_test.sample


class TestSimpleXMLWrapper(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    self.sysmeta_xml = d1_test.sample.load_utf8_to_str(
      'systemMetadata_v2_0.tz_non_utc.xml'
    )

  def test_1000(self):
    """get_xml()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      d1_test.sample.assert_equals(xml.get_xml(), 'get_xml')

  def test_1010(self):
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      """get_xml_below_element()"""
      d1_test.sample.assert_equals(
        xml.get_xml_below_element('accessPolicy'), 'get_xml_below_element'
      )

  def test_1020(self):
    """get_element_list_by_attr_key()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      assert [
        el.tag for el in xml.get_element_list_by_attr_key('replicationAllowed')
      ] == ['replicationPolicy']

  def test_1030(self):
    """get_element_by_attr_key(): Valid selection returns element"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      assert xml.get_element_by_attr_key(
        'replicationAllowed'
      ).tag == 'replicationPolicy'

  def test_1040(self):
    """get_element_by_attr_key(): Non-existing element raises
    SimpleXMLWrapperException"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      with pytest.raises(d1_common.wrap.simple_xml.SimpleXMLWrapperException):
        xml.get_element_by_attr_key('replicationAllowed', 100)

  def test_1050(self):
    """get_element_text(): Returns XML element text, root child"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      assert xml.get_element_text('rightsHolder') == 'test_rights_holder'

  def test_1060(self):
    """get_element_text(): Returns XML element text, nested"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      assert xml.get_element_text('preferredMemberNode', 2) == 'node2'

  def test_1070(self):
    """get_element_text(): Non-existing element raises
    SimpleXMLWrapperException"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      with pytest.raises(d1_common.wrap.simple_xml.SimpleXMLWrapperException):
        xml.get_element_text('preferredMemberNode', 3)

  def test_1080(self):
    """set_element_text()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      xml.set_element_text(
        'preferredMemberNode', '__preferredMemberNode__2__', 2
      )
      d1_test.sample.assert_equals(xml.get_xml(), 'set_element_text')

  def test_1090(self):
    """get_element_dt()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      dt = xml.get_element_dt('dateUploaded')
      d1_common.date_time.are_equal(
        dt,
        datetime.datetime(
          1933, 3, 3, 13, 13, 13, 333300,
          tzinfo=d1_common.date_time.FixedOffset(
            '-11:33', offset_hours=-11, offset_minutes=33
          )
        )
      )
      assert isinstance(dt, datetime.datetime)

  def test_1100(self):
    """set_element_dt()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      xml.set_element_dt(
        'dateUploaded',
        datetime.datetime(
          1911, 2, 3, 4, 5, 6, 7890, tzinfo=d1_common.date_time.FixedOffset(
            '-2:30', offset_hours=-2, offset_minutes=30
          )
        )
      )
      assert xml.get_element_text(
        'dateUploaded'
      ) == '1911-02-03T04:05:06.007890-01:30'

  def test_1110(self):
    """remove_children()"""
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      assert xml.get_element_list_by_name('preferredMemberNode')
      assert xml.get_element_list_by_name('blockedMemberNode')
      xml.remove_children('replicationPolicy')
      d1_test.sample.assert_equals(xml.get_xml(), 'remove_children')
      assert not xml.get_element_list_by_name('preferredMemberNode')
      assert not xml.get_element_list_by_name('blockedMemberNode')

  def test_1120(self):
    """replace_by_etree()"""
    new_replication_policy_el = ET.fromstring(
      '''
    <replicationPolicy a="b" c="d">
      <preferredMemberNode>new_preferred</preferredMemberNode>
      <blockedMemberNode>new_blocked</blockedMemberNode>
    </replicationPolicy>
    '''
    )
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      xml.replace_by_etree(new_replication_policy_el)
      assert len(xml.get_element_list_by_name('preferredMemberNode')) == 1
      assert len(xml.get_element_list_by_name('blockedMemberNode')) == 1
      assert xml.get_element_by_name('replicationPolicy').attrib['a'] == 'b'
      assert xml.get_element_by_name('replicationPolicy').attrib['c'] == 'd'
      d1_test.sample.assert_equals(xml.get_xml(), 'replace_by_etree')

  def test_1130(self):
    """replace_by_xml()"""
    new_replication_policy_xml = '''
    <replicationPolicy a="b" c="d">
      <preferredMemberNode>new_preferred</preferredMemberNode>
      <blockedMemberNode>new_blocked</blockedMemberNode>
    </replicationPolicy>
    '''
    with d1_common.wrap.simple_xml.wrap(self.sysmeta_xml) as xml:
      xml.replace_by_xml(new_replication_policy_xml)
      assert len(xml.get_element_list_by_name('preferredMemberNode')) == 1
      assert len(xml.get_element_list_by_name('blockedMemberNode')) == 1
      d1_test.sample.assert_equals(xml.get_xml(), 'replace_by_xml')
