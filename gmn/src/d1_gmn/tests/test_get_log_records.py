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
"""Test MNRead.getLogRecords()
"""

from __future__ import absolute_import

import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator.system_metadata


@d1_test.d1_test_case.reproducible_random_decorator('TestGetLogRecords')
class TestGetLogRecords(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_0001(self):
    """getLogRecords():"""

  #   def test(mn_client_v1_v2):
  #     for _ in range(100):
  #       pid = self.random_pid()
  #       sciobj_str = d1_test.d1_test_case.generate_reproducible_sciobj_str(pid)
  #       options = {
  #         'identifier': mn_client_v1_v2.bindings.Identifier(pid),
  #       }
  #       # rnd_sysmeta_pyxb = (
  #       #   d1_test.instance_generator.system_metadata.generate_from_flo(
  #       #     StringIO.StringIO(sciobj_str), options
  #       #   )
  #       # )
  #       #
  #       # self.dump_pyxb(rnd_sysmeta_pyxb)
  #       #
  #       # mn_client_v1_v2.create(pid, StringIO.StringIO(sciobj_str), rnd_sysmeta_pyxb)
  #
  #     #       pid, sid, sciobj_str, send_sysmeta_pyxb = (
  #     #         self.generate_sciobj_with_defaults(mn_client_v1_v2)
  #     #       )
  #     #       send_checksum = d1_common.checksum.create_checksum_object_from_string(
  #     #         sciobj_str, algorithm_str
  #     #       )
  #     #       send_sysmeta_pyxb.checksum = send_checksum
  #     #       mn_client_v1_v2.create(pid, StringIO.StringIO(sciobj_str), send_sysmeta_pyxb)
  #     #       recv_checksum = mn_client_v1_v2.getChecksum(pid, algorithm_str)
  #     #       d1_common.checksum.are_checksums_equal(
  #     #         send_sysmeta_pyxb.checksum, recv_checksum
  #     #       )
  #     #
  #     # # MNCore.getLogRecords(session[, fromDate][, toDate][, event][,
  #     idFilter][, start=0][, count=1000]) → Log¶
  #     MNCore.getLogRecords(session[, fromDate][, toDate][, event][,
  #     idFilter][, start=0][, count=1000]) → Log¶
  #     #
  #     # test(self.client_v1)
  #
  #   with d1_gmn.tests.gmn_mock.disable_auth():
  #     test(self.client_v2)
  #
  # # def test_0010(self):
  # #   """MNRead.getLogRecords(): replicaStatus filter"""
  # #   # Create two objects, one local and one replica
  # #   local_pid = self.create_obj(self.client_v2)[0]
  # #   replica_pid = self.create_obj(self.client_v2)[0]
  # #   self.convert_to_replica(replica_pid)
  # #   # No replicationStatus filter returns both objects
  # #   object_list_pyxb = self.client_v2.getLogRecords()
  # #   self.assertListEqual(
  # #     sorted([replica_pid, local_pid]),
  # #     self.log_to_pid_list(object_list_pyxb),
  # #   )
  # #   # replicationStatus=True returns both objects
  # #   object_list_pyxb = self.client_v2.getLogRecords()
  # #   self.assertListEqual(
  # #     sorted([replica_pid, local_pid]),
  # #     self.log_to_pid_list(object_list_pyxb),
  # #   )
  # #   # replicationStatus=False returns only the local object
  # #   object_list_pyxb = self.client_v2.getLogRecords(replicaStatus=False)
  # #   self.assertListEqual(
  # #     [local_pid],
  # #     self.log_to_pid_list(object_list_pyxb),
  # #   )
  # #   # Check header.
  # #   self.assert_object_list_slice(
  # #     object_list, 0, OBJECTS_TOTAL_DATA, OBJECTS_TOTAL_DATA
  # #   )
  #
  # #   def test_1100_D(self):
  # #     """Event log is populated.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     logRecords = mn_client_v1_v2.getLogRecords(
  # #       count=d1_common.const.MAX_LISTOBJECTS,
  # #     )
  # #     self.assertEqual(len(logRecords.logEntry), EVENTS_TOTAL)
  # #     self.assertIn(
  # #       ('hdl:10255/dryad.654/mets.xml', 'create'),
  # #       [(o.identifier.value(), o.event) for o in logRecords.logEntry],
  # #     )
  # #
  # # qwe
  # #
  # #
  # #   @responses.activate
  # #   def test_1500_v1(self):
  # #     """getLogRecords(): Get event count
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1500(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1500_v2(self):
  # #     """getLogRecords(): Get event count
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1500(mn_client_v1_v2)
  # #
  # #   def _test_1500(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=0, count=0,
  # #     )
  # #     self.assert_log_slice(log, 0, 0, EVENTS_TOTAL_1500)
  # #
  # #   @responses.activate
  # #   def test_1510_v1(self):
  # #     """getLogRecords(): Slicing: Starting at 0 and getting half of the
  # #     available events.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1510(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1510_v2(self):
  # #     """getLogRecords(): Slicing: Starting at 0 and getting half of the
  # #     available events.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1510(mn_client_v1_v2)
  # #
  # #   def _test_1510(self, mn_client_v1_v2):
  # #     object_cnt_half = EVENTS_TOTAL / 2
  # #     # Starting at 0 and getting half of the available objects.
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=0, count=object_cnt_half,
  # #     )
  # #     self.assert_log_slice(log, 0, object_cnt_half, EVENTS_TOTAL_1500)
  # #
  # #   @responses.activate
  # #   def test_1520_v1(self):
  # #     """getLogRecords(): Slicing: From center and more than are available
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1520(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1520_v2(self):
  # #     """getLogRecords(): Slicing: From center and more than are available
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1520(mn_client_v1_v2)
  # #
  # #   def _test_1520(self, mn_client_v1_v2):
  # #     object_cnt_half = EVENTS_TOTAL_1500 / 2
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=object_cnt_half, count=d1_common.const.MAX_LISTOBJECTS,
  # #
  # #     )
  # #     self.assert_log_slice(
  # #       log, object_cnt_half, EVENTS_TOTAL_1500 - object_cnt_half,
  # #       EVENTS_TOTAL_1500
  # #     )
  # #
  # #   @responses.activate
  # #   def test_1530_v1(self):
  # #     """getLogRecords(): Slicing: Starting above number of events that are
  # #     available.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1530(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1530_v2(self):
  # #     """getLogRecords(): Slicing: Starting above number of events that are
  # #     available.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1530(mn_client_v1_v2)
  # #
  # #   def _test_1530(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=EVENTS_TOTAL_1500 * 2, count=1,
  # #     )
  # #     self.assert_log_slice(log, EVENTS_TOTAL_1500 * 2, 0, EVENTS_TOTAL_1500)
  # #
  # #   @responses.activate
  # #   def test_1550_v1(self):
  # #     """getLogRecords(): Date range query: Get all events from the 1990s.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1550(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1550_v2(self):
  # #     """getLogRecords(): Date range query: Get all events from the 1990s.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1550(mn_client_v1_v2)
  # #
  # #   def _test_1550(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       count=d1_common.const.MAX_LISTOBJECTS,
  # #       fromDate=datetime.datetime(1990, 1, 1),
  # #       toDate=datetime.datetime(1999, 12, 31),
  # #     )
  # #     self.assert_log_slice(
  # #       log, 0, EVENTS_TOTAL_EVENT_UNI_TIME_IN_1990S,
  # #       EVENTS_TOTAL_EVENT_UNI_TIME_IN_1990S
  # #     )
  # #
  # #   @responses.activate
  # #   def test_1560_v1(self):
  # #     """getLogRecords(): Date range query: Get first 10 objects from the
  # #     1990s.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1560(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1560_v2(self):
  # #     """getLogRecords(): Date range query: Get first 10 objects from the
  # #     1990s.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1560(mn_client_v1_v2)
  # #
  # #   def _test_1560(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=0, count=10, fromDate=datetime.datetime(1990, 1, 1),
  # #       toDate=datetime.datetime(1999, 12, 31),
  # #     )
  # #     self.assert_log_slice(log, 0, 10, EVENTS_TOTAL_EVENT_UNI_TIME_IN_1990S)
  # #
  # #   @responses.activate
  # #   def test_1570_v1(self):
  # #     """getLogRecords(): Date range query: Get all events from the 1990s,
  # #     filtered by event type.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1570(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1570_v2(self):
  # #     """getLogRecords(): Date range query: Get all events from the 1990s,
  # #     filtered by event type.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1570(mn_client_v1_v2)
  # #
  # #   def _test_1570(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=0, count=d1_common.const.MAX_LISTOBJECTS,
  # #       fromDate=datetime.datetime(1990, 1, 1),
  # #       toDate=datetime.datetime(1999, 12, 31), event='delete',
  # #
  # #     )
  # #     self.assert_log_slice(
  # #       log, 0, EVENTS_DELETES_UNI_TIME_IN_1990S, EVENTS_DELETES_UNI_TIME_IN_1990S
  # #     )
  # #
  # #   @responses.activate
  # #   def test_1580_v1(self):
  # #     """getLogRecords(): Date range query: Get 10 first events from
  # #     non-existing date range.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1580(mn_client_v1_v2)
  # #
  # #   @responses.activate
  # #   def test_1580_v2(self):
  # #     """getLogRecords(): Date range query: Get 10 first events from
  # #     non-existing date range.
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1580(mn_client_v1_v2)
  # #
  # #   def _test_1580(self, mn_client_v1_v2):
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       start=0, count=d1_common.const.MAX_LISTOBJECTS,
  # #       fromDate=datetime.datetime(2500, 1, 1),
  # #       toDate=datetime.datetime(2500, 12, 31),
  # #     )
  # #     self.assert_log_slice(log, 0, 0, 0)
  # #
  # #   @responses.activate
  # #   def test_1591_v1(self):
  # #     """create() of object causes a new create event to be written for the
  # #     given PID
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient.MemberNodeClient(GMN_URL)
  # #     self._test_1591(self.client_v1)
  # #
  # #   @responses.activate
  # #   def test_1591_v2(self):
  # #     """create() of object causes a new create event to be written for the
  # #     given PID
  # #     """
  # #     mn_client_v1_v2 = d1_client.mnclient_2_0.MemberNodeClient_2_0(GMN_URL)
  # #     self._test_1591(self.client_v2)
  # #
  # #   def _test_1591(self, mn_client_v1_v2):
  # #     pid = self.random_pid()
  # #     self.create(mn_client_v1_v2, pid)
  # #     log = mn_client_v1_v2.getLogRecords(
  # #       pidFilter=pid,
  # #     )
  # #     self.assertEqual(len(log.logEntry), 1)
  # #     self.assertEqual(log.logEntry[0].event, 'create')
  # #     self.assertEqual(log.logEntry[0].identifier.value(), pid)
