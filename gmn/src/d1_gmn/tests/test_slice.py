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
"""Test slicing / paging of multi-page result set

Slicing is tested via getLogRecords().
"""

from __future__ import absolute_import

import datetime
import random

# import logging
# import pytest
import responses

import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.sample


@d1_test.d1_test_case.reproducible_random_decorator('TestSlice')
# @pytest.mark.skip('SLOOOOOW')
class TestSlice(d1_gmn.tests.gmn_test_case.GMNTestCase):
  # def setup_class(self):
  #   with d1_gmn.tests.gmn_mock.disable_auth():
  #     self._total_int = mn_client_v1_v2.getLogRecords(
  #       start=0, count=0, fromDate=fromDate
  #     ).total
  #     assert self._total_int >= 2000, 'Need >= 2000 logEntry records for testing'
  #     single_slice_log = mn_client_v1_v2.getLogRecords(
  #       start=0, count=self._total_int, fromDate=fromDate
  #     )
  #     assert len(single_slice_log.logEntry) == self._total_int

  def _test(self, mn_client_v1_v2, fromDate=None, vary_size=False):
    count_int = 789
    with d1_gmn.tests.gmn_mock.disable_auth():
      total_int = mn_client_v1_v2.getLogRecords(
        start=0, count=0, fromDate=fromDate
      ).total
      # logging.debug('total_int={}'.format(total_int))
      assert total_int >= 2000, 'Need >= 2000 logEntry records for testing'
      single_slice_log = mn_client_v1_v2.getLogRecords(
        start=0, count=total_int, fromDate=fromDate
      )
      assert len(single_slice_log.logEntry) == total_int

      start_int = 0
      multi_slice_list = []
      while True:
        # logging.debug('in_start={}'.format(start_int))
        vary_count_in = count_int + (random.randint(0, 2) if vary_size else 0)
        log_pyxb = mn_client_v1_v2.getLogRecords(
          start=start_int, count=vary_count_in, fromDate=fromDate
        )
        # self.dump_pyxb(log_pyxb)
        multi_slice_list.extend(log_pyxb.logEntry)
        # logging.debug(
        #   'out_start={} out_count={} out_total={}'.
        #   format(log_pyxb.start, log_pyxb.count, log_pyxb.total)
        # )
        start_int += log_pyxb.count
        if start_int >= log_pyxb.total:
          break

      i = 0
      for a, b in zip(single_slice_log.logEntry, multi_slice_list):
        i += 1
        # print i
        a_xml = self.format_pyxb(a)
        b_xml = self.format_pyxb(b)
        assert a_xml == b_xml

  @responses.activate
  def test_1000(self, mn_client_v1_v2):
    """Retrieving an *unfiltered* result set in many small slices of *equal* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(mn_client_v1_v2)

  @responses.activate
  def test_1010(self, mn_client_v1_v2):
    """Retrieving a *filtered* result set in many small slices of *equal* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(
      mn_client_v1_v2, fromDate=datetime.datetime(2000, 5, 6, 15, 16, 17, 18)
    )

  @responses.activate
  def test_1020(self, mn_client_v1_v2):
    """Retrieving an *unfiltered* result set in many small slices of *varying* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(mn_client_v1_v2, vary_size=True)

  @responses.activate
  def test_1030(self, mn_client_v1_v2):
    """Retrieving a *filtered* result set in many small slices of *varying* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(
      mn_client_v1_v2, fromDate=datetime.datetime(2000, 5, 6, 15, 16, 17, 18),
      vary_size=True
    )
