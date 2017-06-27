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

from __future__ import absolute_import

import d1_test.d1_test_case
import d1_test.instance_generator.date_time as dates

#===============================================================================


@d1_test.d1_test_case.reproducible_random_decorator('TestDateTime')
class TestDateTime(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """random_date(): Dates are random"""
    random_date_list = [dates.random_date().isoformat() for _ in range(10)]
    self.sample.assert_equals(
      random_date_list, 'inst_gen_random_date_unrestricted'
    )

  def test_1010(self):
    """random_date(): Dates are random, with restricted time span"""
    random_date_list = [
      dates.random_date(100, 200).isoformat() for _ in range(10)
    ]
    self.sample.assert_equals(
      random_date_list, 'inst_gen_random_date_restricted'
    )
