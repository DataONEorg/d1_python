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
"""Generate random DateTime
"""

from __future__ import absolute_import

import datetime
import random

import d1_common.date_time

import d1_test.d1_test_case


def random_date(earliest=0, latest=1e10):
  """Generate a random date somewhere between earliest and latest.
  """
  tstamp = random.randrange(earliest, latest)
  dt = datetime.datetime.utcfromtimestamp(tstamp)
  return d1_common.date_time.create_utc_datetime(
    dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
    random.randint(0, 1000)
  )


def generate():
  """Generate a d1_common.types.dataoneTypes.DateTime with a random datetime"""
  return d1_common.types.dataoneTypes.DateTime(random_date())


def from_did(did_str):
  """Generate a date reproducible by PID or SID
  Span is 1970 to ~2070.
  """
  century_sec = 60 * 60 * 24 * 365 * 100
  with d1_test.d1_test_case.reproducible_random_context(did_str):
    return d1_common.date_time.ts_to_dt(
      random.randint(0, century_sec),
      tz=d1_common.date_time.UTC(),
    )
