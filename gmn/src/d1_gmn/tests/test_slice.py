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
import logging
import multiprocessing
import random

# import logging
# import pytest
import responses

import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.xml

import d1_test.sample

SLICE_COUNT = 7


def _assert_pyxb_objects_are_equivalent(arg_tup):
  a_pyxb, b_pyxb, i, item_count = arg_tup
  # logging.debug('Checking sliced items. {}/{}'.format(i + 1, item_count))
  assert d1_common.xml.is_equivalent_pyxb(a_pyxb, b_pyxb)


@d1_test.d1_test_case.reproducible_random_decorator('TestSlice')
class TestSlice(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _test(
      self, mn_client_v1_v2, useGetLogRecords=False, fromDate=None,
      randomize_slice_counts=False
  ):
    if useGetLogRecords:
      slicable_api_func = mn_client_v1_v2.getLogRecords
      iterable_attr = 'logEntry'
    else:
      slicable_api_func = mn_client_v1_v2.listObjects
      iterable_attr = 'objectInfo'

    with d1_gmn.tests.gmn_mock.disable_auth():
      total_int = slicable_api_func(start=0, count=0, fromDate=fromDate).total
      logging.debug('total_int={}'.format(total_int))
      assert total_int >= 500, 'Insufficient number of objects available for test'
      single_slice_pyxb = slicable_api_func(
        start=0, count=total_int, fromDate=fromDate
      )
      # The single slice contains the same number of items as was returned as
      # the total.
      single_slice_pyxb_list = getattr(single_slice_pyxb, iterable_attr)
      assert len(single_slice_pyxb_list) == total_int

      count_int = total_int / SLICE_COUNT
      start_int = 0
      multi_slice_pyxb_list = []
      while True:
        # logging.debug('in_start={}'.format(start_int))
        vary_count_in = count_int + (
          random.randint(0, 2) if randomize_slice_counts else 0
        )
        multiple_slice_pyxb = slicable_api_func(
          start=start_int, count=vary_count_in, fromDate=fromDate
        )
        # self.dump_pyxb(log_pyxb)
        multi_slice_pyxb_list.extend(
          getattr(multiple_slice_pyxb, iterable_attr)
        )
        # logging.debug(
        #   'out_start={} out_count={} out_total={}'.
        #   format(log_pyxb.start, log_pyxb.count, log_pyxb.total)
        # )
        start_int += multiple_slice_pyxb.count
        if start_int >= multiple_slice_pyxb.total:
          break

      assert len(single_slice_pyxb_list) == len(multi_slice_pyxb_list), (
        'Retrieving multiple smaller slices did not give the same item count '
        'as retrieving a single large slice'
      )

      item_count = len(multi_slice_pyxb_list)
      arg_list = zip(
        single_slice_pyxb_list,
        multi_slice_pyxb_list,
        range(item_count),
        [item_count] * item_count,
      )
      logging.info(
        'Comparing PyXB object pairs. pair_count={}'.format(len(arg_list))
      )
      pool = multiprocessing.Pool()
      pool.map(_assert_pyxb_objects_are_equivalent, arg_list)

      # i = 0
      # for a_pyxb, b_pyxb in zip(getattr(single_slice_pyxb, iterable_attr), multi_slice_pyxb_list):
      #   i += 1
      #   logging.debug('Checking sliced items. {}/{}'.format(i + 1, len(multi_slice_pyxb_list)))
      #   assert d1_common.xml.is_equivalent_pyxb(a_pyxb, b_pyxb)

  @responses.activate
  def test_1000(self, mn_client_v1_v2, true_false):
    """Retrieving an *unfiltered* result set in many small slices of *equal* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(mn_client_v1_v2, true_false)

  @responses.activate
  def test_1010(self, mn_client_v1_v2, true_false):
    """Retrieving a *filtered* result set in many small slices of *equal* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(
      mn_client_v1_v2, true_false,
      fromDate=datetime.datetime(2000, 5, 6, 15, 16, 17, 18)
    )

  @responses.activate
  def test_1020(self, mn_client_v1_v2, true_false):
    """Retrieving an *unfiltered* result set in many small slices of *varying*
    size (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(mn_client_v1_v2, true_false, randomize_slice_counts=True)

  @responses.activate
  def test_1030(self, mn_client_v1_v2, true_false):
    """Retrieving a *filtered* result set in many small slices of *varying* size
    (except for the last one which is smaller), gives the same result as
    retrieving everything in a single call without slicing.
    """
    self._test(
      mn_client_v1_v2, true_false,
      fromDate=datetime.datetime(2000, 5, 6, 15, 16, 17, 18),
      randomize_slice_counts=True
    )
