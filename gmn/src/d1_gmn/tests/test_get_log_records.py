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
"""Test MNCore.getLogRecords()
"""

import datetime

import freezegun
import pytest
import responses

import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common
import d1_common.types
import d1_common.types.exceptions
import d1_common.xml

import d1_test.sample


@d1_test.d1_test_case.reproducible_random_decorator('TestGetLogRecords')
@freezegun.freeze_time('1977-05-27')
class TestGetLogRecords(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def norm_entry_id(self, log):
    for log_entry_pyxb in log.logEntry:
      log_entry_pyxb.entryId = '1'

  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: start=0, count=0 returns empty slice with
    correct total event count
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(start=0, count=0)
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'number_of_events', gmn_client_v1_v2)

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: Retrieve front section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(start=0, count=3)
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'front_section', gmn_client_v1_v2)

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: Retrieve middle section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_events = self.get_total_log_records(gmn_client_v1_v2)
      log = gmn_client_v1_v2.getLogRecords(start=n_events // 2, count=7)
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'middle_section', gmn_client_v1_v2)

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: Retrieve exact end section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_events = self.get_total_log_records(gmn_client_v1_v2)
      log = gmn_client_v1_v2.getLogRecords(start=n_events - 1, count=1)
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'exact_end_section', gmn_client_v1_v2)

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: Specifying more events than are
    available returns the available events
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_events = self.get_total_log_records(gmn_client_v1_v2)
      log = gmn_client_v1_v2.getLogRecords(start=n_events - 10, count=100)
      self.norm_entry_id(log)
      self.sample.assert_equals(
        log, 'count_beyond_end_section', gmn_client_v1_v2
      )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """getLogRecords(): Slicing: Specifying start above available events
    raises InvalidRequest
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_events = self.get_total_log_records(gmn_client_v1_v2)
      with pytest.raises(d1_common.types.exceptions.InvalidRequest):
        gmn_client_v1_v2.getLogRecords(start=n_events + 1234, count=10000)

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): event type filter: Unknown event returns an empty
    list

    In v2, event type is not an enum.
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(event='bogus_event')
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'event_filter_unknown', gmn_client_v1_v2)

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): event type filter: known event returns list of
    requested size with total equal to the number of events of the type
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(event='update', count=10)
      self.norm_entry_id(log)
      self.sample.assert_equals(log, 'event_filter_update', gmn_client_v1_v2)

  @responses.activate
  def test_1080(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): Date range query: Get all events from 1979
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      newest_log = gmn_client_v1_v2.getLogRecords(
        fromDate=datetime.datetime(1979, 1, 1),
        toDate=datetime.datetime(1979, 12, 31), start=0, count=1
      )
      n_match = newest_log.total
      oldest_log = gmn_client_v1_v2.getLogRecords(
        fromDate=datetime.datetime(1979, 1, 1),
        toDate=datetime.datetime(1979, 12, 31), start=n_match - 1, count=1
      )
      # Verify that first and last records are both in 1979 and that first doc
      # is the newest, as GMN sorts on timestamp descending.
      self.norm_entry_id(newest_log)
      self.norm_entry_id(oldest_log)
      self.sample.assert_equals(
        '\n\n'.join([self.format_pyxb(v) for v in (newest_log, oldest_log)]),
        'date_range_first_last',
        gmn_client_v1_v2,
      )

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): Date range query: Using a date range in the
    future returns empty list
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(
        fromDate=datetime.datetime(2500, 1, 1),
        toDate=datetime.datetime(3000, 12, 31), start=0, count=1
      )
      self.norm_entry_id(log)
      self.sample.assert_equals(
        log,
        'date_range_in_the_future',
        gmn_client_v1_v2,
      )

  @responses.activate
  def test_1100(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): Date range query: End date before start date
    raises InvalidRequest
    """
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      with d1_gmn.tests.gmn_mock.disable_auth():
        gmn_client_v1_v2.getLogRecords(
          fromDate=datetime.datetime(1692, 5, 1),
          toDate=datetime.datetime(1445, 9, 2), start=0, count=1
        )

  @responses.activate
  @freezegun.freeze_time('2388-08-28')
  def test_1110(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): create() of object causes a new create event to
    be added for the given PID
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_create_events_before = self.get_total_log_records(
        gmn_client_v1_v2, event='create'
      )
      pid, sid, sciobj_bytes, sysmeta_pyxb = self.create_obj(
        gmn_client_v1_v2, now_dt=datetime.datetime(2388, 8, 28)
      )
      n_create_events_after = self.get_total_log_records(
        gmn_client_v1_v2, event='create'
      )
      assert n_create_events_after == n_create_events_before + 1
      # Verify that the most recent record now matches the object that was created
      event_pyxb = gmn_client_v1_v2.getLogRecords(start=0, count=1)
      self.sample.assert_equals(
        '\n'.join([
          'pid: {}'.format(pid),
          'sid: {}'.format(sid),
          'sysmeta: {}'.
          format(d1_common.xml.serialize_to_xml_str(sysmeta_pyxb)),
          'create_event: {}'.
          format(d1_common.xml.serialize_to_xml_str(event_pyxb)),
        ]),
        'new_create_event',
        gmn_client_v1_v2,
      )

  @responses.activate
  def test_1120(self, gmn_client_v1_v2):
    """MNCore.getLogRecords(): v1: SID is not resolved, so idFilter with SID
    returns empty list. v2: SID is resolved, so idFilter returns records for all
    objects in chain.
    """
    sid = self.get_sid_with_min_chain_length()
    with d1_gmn.tests.gmn_mock.disable_auth():
      log = gmn_client_v1_v2.getLogRecords(idFilter=sid)
      self.sample.assert_equals(log, 'id_filter_with_sid', gmn_client_v1_v2)
