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

import datetime
import random

import d1_common.date_time
import d1_common.types.dataoneTypes

import d1_test.d1_test_case


def random_date():
  """Return a random date within the span of 1970 to ~2070
  """
  dt = random_datetime()
  return datetime.date(dt.year, dt.month, dt.day)


def random_datetime(tz_type='utc'):
  """Return a random datetime within the span of 1970 to ~2070 using the
  specified timezone type. See generate_tz() for {tz_type}.
  """
  century_sec = 60 * 60 * 24 * 365 * 100
  return d1_test.d1_test_case.D1TestCase.dt_from_ts(
    random.random() * century_sec, generate_tz(tz_type)
  )


def reproducible_datetime(did_str, tz_type='utc'):
  """Return a reproducible datetime within the span of 1970 to ~2070 using the
  specified timezone type. See generate_tz() for {tz_type}.
  """
  with d1_test.d1_test_case.reproducible_random_context(did_str):
    return random_datetime(tz_type)


def generate_tz(tz_type='utc'):
  """Generate a timezone
  - {tz_type} = 'naive': Return None (use to create a "naive" datetime).
  - {tz_type} = 'utc': Return tz in UTC.
  - {tz_type} = 'random': Return tz at a random positive or negative offset.
  - {tz_type} = 'random_not_utc': Return tz at a random positive or negative
    offset that is not in UTC (not 0).
  - {tz_type} = (other object): Return the supplied object, which must be an
    instance of a class derived from datetime.tzinfo.
  """
  if isinstance(tz_type, datetime.tzinfo):
    return tz_type
  assert isinstance(tz_type, str)
  if tz_type == 'naive':
    return None
  elif tz_type == 'utc':
    return d1_common.date_time.UTC()
  elif tz_type == 'random':
    return d1_common.date_time.FixedOffset(
      'RND_TZ', random.randint(-11, 11), random.randint(0, 59)
    )
  elif tz_type == 'random_not_utc':
    while True:
      tz = generate_tz('random')
      if tz.utcoffset(0) != datetime.timedelta(0):
        return tz
  else:
    assert False
