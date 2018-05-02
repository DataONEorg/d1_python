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
"""Test MNRead.listObjects()

TODO: Test PUBLIC_OBJECT_LIST setting for both True and False
"""

import datetime
import random

import freezegun
import pytest
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common
import d1_common.types.exceptions

import d1_test
import d1_test.d1_test_case


@d1_test.d1_test_case.reproducible_random_decorator('TestListObjects')
@freezegun.freeze_time('1967-05-27')
class TestListObjects(d1_gmn.tests.gmn_test_case.GMNTestCase):
  @responses.activate
  def test_1000(self, gmn_client_v1_v2):
    """listObjects(): Slicing: start=0, count=0 returns empty slice with
    correct total object count
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      object_list_pyxb = gmn_client_v1_v2.listObjects(start=0, count=0)
      self.sample.assert_equals(
        object_list_pyxb, 'number_of_objects', gmn_client_v1_v2
      )

  @responses.activate
  def test_1010(self, gmn_client_v1_v2):
    """listObjects(): Slicing: Retrieve front section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      object_list_pyxb = gmn_client_v1_v2.listObjects(start=0, count=21)
      self.sample.assert_equals(
        object_list_pyxb, 'front_section', gmn_client_v1_v2
      )

  @responses.activate
  def test_1020(self, gmn_client_v1_v2):
    """listObjects(): Slicing: Retrieve middle section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      object_list_pyxb = gmn_client_v1_v2.listObjects(start=612, count=15)
      self.sample.assert_equals(
        object_list_pyxb, 'middle_section', gmn_client_v1_v2
      )

  @responses.activate
  def test_1030(self, gmn_client_v1_v2):
    """listObjects(): Slicing: Retrieve exact end section
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_objects = self.get_total_objects(gmn_client_v1_v2)
      object_list_pyxb = gmn_client_v1_v2.listObjects(
        start=n_objects - 1, count=1
      )
      self.sample.assert_equals(
        object_list_pyxb, 'exact_end_section', gmn_client_v1_v2
      )

  @responses.activate
  def test_1040(self, gmn_client_v1_v2):
    """listObjects(): Slicing: Specifying more objects than are
    available returns the available objects
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      n_objects = self.get_total_objects(gmn_client_v1_v2)
      # Slice indexes are zero based.
      object_list_pyxb = gmn_client_v1_v2.listObjects(
        start=n_objects - 10, count=100
      )
      self.sample.assert_equals(
        object_list_pyxb, 'count_beyond_end_section', gmn_client_v1_v2
      )

  @responses.activate
  def test_1050(self, gmn_client_v1_v2):
    """listObjects(): Slicing: Specifying start above raises InvalidRequest
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      with pytest.raises(d1_common.types.exceptions.InvalidRequest):
        n_objects = self.get_total_objects(gmn_client_v1_v2)
        gmn_client_v1_v2.listObjects(start=n_objects + 1234, count=10000)

  @responses.activate
  def test_1060(self, gmn_client_v1_v2):
    """MNRead.listObjects(): DID filter: Unknown DID returns an empty
    list
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      object_list_pyxb = gmn_client_v1_v2.listObjects(identifier='bogus_did')
      self.sample.assert_equals(
        object_list_pyxb, 'pid_filter_unknown', gmn_client_v1_v2
      )

  @responses.activate
  def test_1070(self, gmn_client_v1_v2):
    """MNRead.listObjects(): DID filter: Existing DID returns a list
    with a single item
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid = random.choice(self.get_pid_list())
      object_list_pyxb = gmn_client_v1_v2.listObjects(identifier=pid)
      self.sample.assert_equals(
        object_list_pyxb, 'pid_filter_existing', gmn_client_v1_v2
      )

  @responses.activate
  def test_1080(self, gmn_client_v1_v2):
    """MNRead.listObjects(): DID filter: SID returns list of
    the objects in the chain
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      sid = random.choice(self.get_sid_list())
      object_list_pyxb = gmn_client_v1_v2.listObjects(identifier=sid)
      self.sample.assert_equals(
        object_list_pyxb, 'sid_filter', gmn_client_v1_v2
      )

  @responses.activate
  def test_1090(self, gmn_client_v1_v2):
    """MNRead.listObjects(): Date range query: Get all objects uploaded in 1980
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      newest_log = gmn_client_v1_v2.listObjects(
        fromDate=datetime.datetime(1980, 1, 1),
        toDate=datetime.datetime(1980, 12, 31), start=0, count=1
      )
      n_match = newest_log.total
      oldest_log = gmn_client_v1_v2.listObjects(
        fromDate=datetime.datetime(1980, 1, 1),
        toDate=datetime.datetime(1980, 12, 31), start=n_match - 1, count=1
      )
      # Verify that first and last records are both in 1980 and that first doc
      # is the newest, as GMN sorts on timestamp descending.
      self.sample.assert_equals(
        '\n\n'.join([self.format_pyxb(v) for v in (newest_log, oldest_log)]),
        'date_range_first_last',
        gmn_client_v1_v2,
      )

  @responses.activate
  def test_1100(self, gmn_client_v1_v2):
    """MNRead.listObjects(): Date range query: Using a date range in the
    future returns empty list
    """
    with d1_gmn.tests.gmn_mock.disable_auth():
      object_list_pyxb = gmn_client_v1_v2.listObjects(
        fromDate=datetime.datetime(2500, 1, 1),
        toDate=datetime.datetime(3000, 12, 31), start=0, count=1
      )
      self.sample.assert_equals(
        object_list_pyxb,
        'date_range_in_the_future',
        gmn_client_v1_v2,
      )

  @responses.activate
  def test_1110(self, gmn_client_v1_v2):
    """MNRead.listObjects(): Date range query: End date before start date
    raises InvalidRequest
    """
    with pytest.raises(d1_common.types.exceptions.InvalidRequest):
      with d1_gmn.tests.gmn_mock.disable_auth():
        gmn_client_v1_v2.listObjects(
          fromDate=datetime.datetime(1692, 5, 1),
          toDate=datetime.datetime(1445, 9, 2), start=0, count=1
        )

  @responses.activate
  def test_1120(self, gmn_client_v1_v2):
    """MNRead.listObjects(): replicaStatus filter"""
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = self.get_pid_list()
      rnd_pid = random.choice(pid_list)

      n_obj_reg_1 = self.get_total_objects(
        gmn_client_v1_v2, replicaStatus=False
      )
      n_obj_rep_1 = self.get_total_objects(gmn_client_v1_v2, replicaStatus=True)

      self.convert_to_replica(rnd_pid)

      n_obj_reg_2 = self.get_total_objects(
        gmn_client_v1_v2, replicaStatus=False
      )
      n_obj_rep_2 = self.get_total_objects(gmn_client_v1_v2, replicaStatus=True)

      self.sample.assert_equals(
        [n_obj_reg_1, n_obj_rep_1, n_obj_reg_2, n_obj_rep_2],
        'replica_status_filter', gmn_client_v1_v2
      )
