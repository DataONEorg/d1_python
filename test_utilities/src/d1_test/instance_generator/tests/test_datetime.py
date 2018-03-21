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

import datetime

import d1_test.d1_test_case
import d1_test.instance_generator.date_time as dates

#===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestDateTime')
class TestDateTime(d1_test.d1_test_case.D1TestCase):
  def test_10001(self):
    """random_date(): Returns random datetime.date objects"""
    random_date_list = [dates.random_date() for _ in range(10)]
    assert len(set(random_date_list)) >= 8
    list([isinstance(x, datetime.date) for x in random_date_list])
    self.sample.assert_equals(random_date_list, 'inst_gen_random_date')

  def test_10002(self):
    """random_datetime(): Returns random datetime.datetime objects"""
    random_datetime_list = [dates.random_datetime() for _ in range(10)]
    assert len(set(random_datetime_list)) >= 8
    list([isinstance(x, datetime.date) for x in random_datetime_list])
    self.sample.assert_equals(random_datetime_list, 'inst_gen_random_datetime')
