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
"""Test handling of datetime (dt) with and without timezone (tz)

When a datetime with timezone is stored in a PyXB binding object, it is adjusted
so that timezone is in UTC while still representing the same absolute point in
time. This is because PyXB sits on top of the XML DOM, where xs:dateTime objects
are always in UTC, even though they can be in any timezone when serialized in
XML.

This behavior is convenient for DataONE in general, since DataONE requires (at
least wants to require) all datetimes to be in UTC, but it means that PyXB
cannot be used for generating most XML documents required for testing handling
of datetime and timezone in GMN. Since d1_client also generates XML with PyXB,
this renders the regular test procedures, based on django_client which wraps
d1_client, and much of the GMNTestCase functionality unusable for most of these
tests.
"""

# import freezegun
# import pytest
import logging

import responses

import d1_gmn.tests.gmn_direct
# import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case
import d1_gmn.tests.gmn_test_client

import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.wrap.access_policy
import d1_common.wrap.simple_xml
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.date_time
import d1_test.instance_generator.identifier

# import datetime


# @freezegun.freeze_time('2001-05-27')
@d1_test.d1_test_case.reproducible_random_decorator('TestTimeZone')
class TestTimeZone(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _generate_sciobj(self, client, tz_type='utc'):
    pid, sid, sciobj_bytes, sysmeta_pyxb = self.generate_sciobj_with_defaults(
      client
    )

    uploaded_dt = d1_test.instance_generator.date_time.random_datetime(tz_type)
    modified_dt = d1_test.instance_generator.date_time.random_datetime(tz_type)

    logging.debug('tz_type={}'.format(tz_type))
    logging.debug('  {}'.format(uploaded_dt))
    logging.debug('  {}'.format(modified_dt))

    sysmeta_pyxb.dateUploaded = uploaded_dt
    sysmeta_pyxb.dateSysMetadataModified = modified_dt

    return pid, sid, sciobj_bytes, sysmeta_pyxb, uploaded_dt, modified_dt

  def _assert_sysmeta_in_utc(self, version_tag, sysmeta_sample_name):
    send_sysmeta_xml = self.sample.load(sysmeta_sample_name)
    with d1_gmn.tests.gmn_mock.isolated_whitelisted_subj() as isolated_subj:
      with d1_common.wrap.simple_xml.wrap(send_sysmeta_xml) as send_sysmeta:
        pid = d1_test.instance_generator.identifier.generate_pid()
        send_sysmeta.set_element_text('identifier', pid)
        send_sysmeta.replace_by_xml(
          '''<accessPolicy><allow>
          <subject>{}</subject><permission>changePermission</permission>
          </allow></accessPolicy>
          '''.format(isolated_subj)
        )
        send_uploaded_dt = send_sysmeta.get_element_dt('dateUploaded')
        send_modified_dt = send_sysmeta.get_element_dt(
          'dateSysMetadataModified'
        )
        send_replica_verified_list = send_sysmeta.get_element_list_by_name(
          'replicaVerified'
        )
        send_sysmeta_xml = send_sysmeta.get_pretty_xml().encode('utf-8')

      d1_gmn.tests.gmn_direct.create(
        version_tag, b'body-contents', send_sysmeta_xml
      )
      resp_dict = d1_gmn.tests.gmn_direct.get_system_metadata(version_tag, pid)

      with d1_common.wrap.simple_xml.wrap(
          resp_dict['body_str']) as recv_sysmeta:
        recv_uploaded_dt = recv_sysmeta.get_element_dt('dateUploaded')
        recv_modified_dt = recv_sysmeta.get_element_dt(
          'dateSysMetadataModified'
        )
        recv_replica_verified_list = recv_sysmeta.get_element_list_by_name(
          'replicaVerified'
        )

      assert d1_common.date_time.is_utc(recv_uploaded_dt)
      assert d1_common.date_time.is_utc(recv_modified_dt)
      logging.debug(
        'send_uploaded_dt="{}" recv_uploaded_dt="{}"'.format(
          send_uploaded_dt, recv_uploaded_dt
        )
      )
      d1_common.date_time.are_equal(send_uploaded_dt, recv_uploaded_dt)
      d1_common.date_time.are_equal(send_modified_dt, recv_modified_dt)

      assert len(send_replica_verified_list) == len(recv_replica_verified_list)
      for a_dt, b_dt in zip(send_replica_verified_list,
                            recv_replica_verified_list):
        d1_common.date_time.are_equal(
          d1_common.date_time.dt_from_iso8601_str(a_dt.text),
          d1_common.date_time.dt_from_iso8601_str(b_dt.text)
        )

  def _assert_object_list_in_utc(self, version_tag, sysmeta_sample_name):
    send_sysmeta_xml = self.sample.load_utf8_to_str(sysmeta_sample_name)
    with d1_gmn.tests.gmn_mock.isolated_whitelisted_subj() as isolated_subj:
      with d1_common.wrap.simple_xml.wrap(send_sysmeta_xml) as send_sysmeta:
        pid = d1_test.instance_generator.identifier.generate_pid()
        send_sysmeta.set_element_text('identifier', pid)
        send_sysmeta.replace_by_xml(
          '''<accessPolicy><allow>
          <subject>{}</subject><permission>changePermission</permission>
          </allow></accessPolicy>
          '''.format(isolated_subj)
        )
        send_sysmeta_xml = send_sysmeta.get_pretty_xml().encode('utf-8')

      d1_gmn.tests.gmn_direct.create(
        version_tag, b'body-contents', send_sysmeta_xml
      )
      resp_dict = d1_gmn.tests.gmn_direct.list_objects(version_tag)

      with d1_common.wrap.simple_xml.wrap(
          resp_dict['body_str']) as recv_sysmeta:
        el_list = recv_sysmeta.get_element_list_by_name(
          'dateSysMetadataModified'
        )
        assert len(el_list) == 1
        for el in el_list:
          dt = d1_common.date_time.dt_from_iso8601_str(el.text)
          assert d1_common.date_time.is_utc(dt)

  def _assert_log_entry_in_utc(self, version_tag, sysmeta_sample_name):
    send_sysmeta_xml = self.sample.load_utf8_to_str(sysmeta_sample_name)
    with d1_gmn.tests.gmn_mock.isolated_whitelisted_subj() as isolated_subj:
      with d1_common.wrap.simple_xml.wrap(send_sysmeta_xml) as send_sysmeta:
        pid = d1_test.instance_generator.identifier.generate_pid()
        send_sysmeta.set_element_text('identifier', pid)
        send_sysmeta.replace_by_xml(
          '''<accessPolicy><allow>
          <subject>{}</subject><permission>changePermission</permission>
          </allow></accessPolicy>
          '''.format(isolated_subj)
        )
        send_sysmeta_xml = send_sysmeta.get_pretty_xml().encode('utf-8')

      d1_gmn.tests.gmn_direct.create(
        version_tag, b'body-contents', send_sysmeta_xml
      )
      resp_dict = d1_gmn.tests.gmn_direct.get_log_records(version_tag)

      with d1_common.wrap.simple_xml.wrap(
          resp_dict['body_str']) as recv_sysmeta:
        el_list = recv_sysmeta.get_element_list_by_name('dateLogged')
        assert len(el_list) == 1
        for el in el_list:
          logging.debug('el.text="{}"'.format(el.text))
          dt = d1_common.date_time.dt_from_iso8601_str(el.text)
          assert d1_common.date_time.is_utc(dt)

  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """PyXB accepts dt with tz for xs:dateTime types and normalizes timezone to
    UTC
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb, uploaded_dt, modified_dt = (
      self._generate_sciobj(gmn_client_v1_v2, 'random_not_utc')
    )
    # Starting with dt that has tz but is not in UTC
    assert d1_common.date_time.has_tz(uploaded_dt)
    assert d1_common.date_time.has_tz(modified_dt)
    assert not d1_common.date_time.is_utc(uploaded_dt)
    assert not d1_common.date_time.is_utc(modified_dt)
    # Reading the dts back from PyXB, they are now in UTC, but adjusted to
    # represent the same absolute point in time.
    assert d1_common.date_time.is_utc(sysmeta_pyxb.dateUploaded)
    assert d1_common.date_time.is_utc(sysmeta_pyxb.dateSysMetadataModified)
    assert d1_common.date_time.are_equal(uploaded_dt, sysmeta_pyxb.dateUploaded)
    assert d1_common.date_time.are_equal(
      modified_dt, sysmeta_pyxb.dateSysMetadataModified
    )

  @responses.activate
  def test_1010(self, gmn_client_v2):
    """PyXB accepts dt without tz for xs:dateTime types and returns it
    unmodified and without tz
    """
    pid, sid, sciobj_bytes, sysmeta_pyxb, uploaded_dt, modified_dt = (
      self._generate_sciobj(gmn_client_v2, 'naive')
    )
    # Starting with dt without tz
    assert not d1_common.date_time.has_tz(uploaded_dt)
    assert not d1_common.date_time.has_tz(modified_dt)
    # Reading the dts back from PyXB, they are still without tz
    assert not d1_common.date_time.has_tz(sysmeta_pyxb.dateUploaded)
    assert not d1_common.date_time.has_tz(sysmeta_pyxb.dateSysMetadataModified)
    # Generating the XML doc, the xs:dateTime strings are still without tz
    xml_doc = d1_common.xml.serialize_to_transport(sysmeta_pyxb)
    with d1_common.wrap.simple_xml.wrap(xml_doc) as xml:
      assert xml.get_element_dt('dateUploaded') == uploaded_dt
      assert xml.get_element_dt('dateSysMetadataModified') == modified_dt

  @responses.activate
  def test_1020(self):
    """PyXB deserializes XML doc with naive dt for xs:dateTime types and
    returns dt unmodified and without tz
    """
    sysmeta_pyxb = self.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0.tz_naive.xml'
    )
    assert str(sysmeta_pyxb.dateUploaded) == '1933-03-03 13:13:13.333300'

  @responses.activate
  def test_1030(self):
    """PyXB deserializes XML doc with non-UTC dt for xs:dateTime types and
    returns dt as normalized to UTC
    """
    sysmeta_pyxb = self.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0.tz_non_utc.xml'
    )
    assert str(sysmeta_pyxb.dateUploaded) == '1933-03-04 00:46:13.333300+00:00'

  @responses.activate
  def test_1040(self):
    """PyXB deserializes XML doc with UTC dt for xs:dateTime types and
    returns dt unmodified and with tz
    """
    sysmeta_pyxb = self.sample.load_xml_to_pyxb(
      'systemMetadata_v2_0.tz_utc.xml'
    )
    assert str(sysmeta_pyxb.dateUploaded) == '1933-03-03 13:13:13.333300+00:00'

  # SysMeta dt

  @responses.activate
  def test_1050(self, tag_v1_v2):
    """SysMeta with naive dt are accepted and assumed to be in UTC
    """
    self._assert_sysmeta_in_utc(tag_v1_v2, 'systemMetadata_v2_0.tz_naive.xml')

  def test_1060(self, tag_v1_v2):
    """SysMeta with ts in UTC are accepted and returned unchanged
    """
    self._assert_sysmeta_in_utc(tag_v1_v2, 'systemMetadata_v2_0.tz_utc.xml')

  @responses.activate
  def test_1070(self, tag_v1_v2):
    """SysMeta with ts where tz is other than UTC are accepted and returned in
    UTC
    """
    self._assert_sysmeta_in_utc(tag_v1_v2, 'systemMetadata_v2_0.tz_non_utc.xml')

  # ObjectList

  @responses.activate
  def test_1080(self, tag_v1_v2):
    """ObjectList with naive dt are accepted and assumed to be in UTC
    """
    self._assert_object_list_in_utc(
      tag_v1_v2, 'systemMetadata_v2_0.tz_naive.xml'
    )

  def test_1090(self, tag_v1_v2):
    """ObjectList with ts in UTC are accepted and returned unchanged
    """
    self._assert_object_list_in_utc(tag_v1_v2, 'systemMetadata_v2_0.tz_utc.xml')

  @responses.activate
  def test_1100(self, tag_v1_v2):
    """ObjectList with ts where tz is other than UTC are accepted and returned in
    UTC
    """
    self._assert_object_list_in_utc(
      tag_v1_v2, 'systemMetadata_v2_0.tz_non_utc.xml'
    )

  # Log

  @responses.activate
  def test_2110(self, tag_v1_v2):
    """Log timestamps are in UTC"""
    self._assert_log_entry_in_utc(
      tag_v1_v2, 'systemMetadata_v2_0.tz_non_utc.xml'
    )
