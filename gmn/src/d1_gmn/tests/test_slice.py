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
"""

import datetime
import logging
import multiprocessing
import random

import responses

import d1_gmn.app.models
import d1_gmn.app.util
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_common.xml

import d1_test.d1_test_case
import d1_test.sample

import django.test

SLICE_COUNT = 23


def _assert_pyxb_objects_are_equivalent(arg_tup):
  a_pyxb, b_pyxb, i, item_count = arg_tup
  a_str = d1_common.xml.serialize_to_xml_str(a_pyxb)
  b_str = d1_common.xml.serialize_to_xml_str(b_pyxb)
  if not d1_common.xml.are_equivalent(a_str, b_str):
    raise AssertionError(
      'PyXB objects are not equivalent.\na="{}"\nb="{}"\n'.format(a_str, b_str)
    )


@d1_test.d1_test_case.reproducible_random_decorator('TestSlice')
class TestSlice(d1_gmn.tests.gmn_test_case.GMNTestCase):
  """Retrieving a filtered result set in many small slices gives the same result
  as retrieving everything in a single call without slicing.

  The small slices are retrieved with slight variations in size, so that some
  slices are same size as previous, and some are different.

  Slicing is tested through getLogRecords() and listObjects().
  """

  def _get_api_func(self, client, use_get_log_records):
    if use_get_log_records:
      return client.getLogRecords, 'logEntry'
    else:
      return client.listObjects, 'objectInfo'

  @responses.activate
  def test_1000(self, gmn_client_v1_v2, true_false):
    from_date = datetime.datetime(2000, 5, 6, 15, 16, 17, 18)

    slicable_api_func, iterable_attr = self._get_api_func(
      gmn_client_v1_v2, use_get_log_records=true_false
    )

    with d1_gmn.tests.gmn_mock.disable_auth():
      total_int = slicable_api_func(start=0, count=0, fromDate=from_date).total
      # logging.debug('total_int={}'.format(total_int))
      assert total_int >= 500, 'Insufficient number of objects available for test'
      single_slice_pyxb = slicable_api_func(
        start=0, count=total_int, fromDate=from_date
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
        vary_count_in = count_int + random.randint(0, 2)
        multiple_slice_pyxb = slicable_api_func(
          start=start_int, count=vary_count_in, fromDate=from_date
        )
        # self.dump(log_pyxb)
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
      arg_list = list(
        zip(
          single_slice_pyxb_list,
          multi_slice_pyxb_list,
          list(range(item_count)),
          [item_count] * item_count,
        )
      )
      logging.info(
        'Comparing single large slice with multiple small slices. pair_count={}'
        .format(len(arg_list))
      )
      pool = multiprocessing.Pool()
      pool.map(_assert_pyxb_objects_are_equivalent, arg_list)

  @responses.activate
  def test_1010(self, gmn_client_v1_v2, true_false):
    """"""
    slicable_api_func, iterable_attr = self._get_api_func(
      gmn_client_v1_v2, use_get_log_records=true_false
    )
    with django.test.override_settings(MAX_SLICE_ITEMS=5):
      with d1_gmn.tests.gmn_mock.disable_auth():
        slice_pyxb = slicable_api_func(start=0, count=100)
        iterable_pyxb = getattr(slice_pyxb, iterable_attr)
        assert len(iterable_pyxb) == 5
