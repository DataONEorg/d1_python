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
import logging

import pytest

import d1_common.date_time as dt

import d1_test.d1_test_case

T1 = 1999, 1, 2, 3, 4, 5, 789000
T2 = 1999, 3, 4, 5, 6, 7, 901000

TZ_MST = dt.FixedOffset('MST', -7)
TZ_YEKT = dt.FixedOffset('YEKT', 6)

T1_NAIVE = datetime.datetime(*T1, tzinfo=None)
T2_NAIVE = datetime.datetime(*T2, tzinfo=None)

T1_UTC = datetime.datetime(*T1, tzinfo=dt.UTC())
T2_UTC = datetime.datetime(*T2, tzinfo=dt.UTC())

T1_MST = datetime.datetime(*T1, tzinfo=TZ_MST)
T1_YEKT = datetime.datetime(*T1, tzinfo=TZ_YEKT)

# Converted to timestamp with http://www.epochconverter.com/
T1_UTC_EPOCH = 915246245.789

# The same point in time in different tz
T_ABS_1 = datetime.datetime(
  2050, 7, 18, 10, 11, 12, 230000, dt.FixedOffset('TZ1', -5, 30)
)
T_ABS_2 = datetime.datetime(
  2050, 7, 18, 21, 41, 12, 230000, dt.FixedOffset('TZ1', 7)
)


@pytest.fixture(scope='function', params=[None, dt.UTC(), TZ_MST, TZ_YEKT])
def tz_fixture(request):
  yield request.param


@pytest.fixture(
  scope='function',
  params=[T1_NAIVE, T2_NAIVE, T1_UTC, T2_UTC, T1_MST, T1_YEKT]
)
def dt_fixture(request):
  yield request.param


@pytest.fixture(
  scope='function',
  params=[
    # Nearest 500 ms
    (
      0.5, datetime.datetime(2020, 10, 11, 14, 10, 10, 100000),
      datetime.datetime(2020, 10, 11, 14, 10, 10, 0)
    ),
    (
      0.5, datetime.datetime(2020, 10, 11, 14, 25, 10, 300000),
      datetime.datetime(2020, 10, 11, 14, 25, 10, 500000)
    ),
    (
      0.5, datetime.datetime(2020, 10, 11, 14, 44, 10, 500000),
      datetime.datetime(2020, 10, 11, 14, 44, 10, 500000)
    ),
    (
      0.5, datetime.datetime(2020, 10, 11, 14, 45, 10, 800000),
      datetime.datetime(2020, 10, 11, 14, 45, 11, 0)
    ),
    # Nearest 2 seconds
    (
      2, datetime.datetime(2020, 10, 11, 14, 10, 10, 100000),
      datetime.datetime(2020, 10, 11, 14, 10, 10, 0)
    ),
    (
      2, datetime.datetime(2020, 10, 11, 14, 10, 11, 300000),
      datetime.datetime(2020, 10, 11, 14, 10, 12, 0)
    ),
    (
      2, datetime.datetime(2020, 10, 11, 14, 44, 15, 500000),
      datetime.datetime(2020, 10, 11, 14, 44, 16, 0)
    ),
    (
      2, datetime.datetime(2020, 10, 11, 14, 45, 16, 700000),
      datetime.datetime(2020, 10, 11, 14, 45, 16, 0)
    ),
    # Nearest 10 seconds
    (
      10, datetime.datetime(2020, 10, 11, 14, 10, 10, 100000),
      datetime.datetime(2020, 10, 11, 14, 10, 10, 0)
    ),
    (
      10, datetime.datetime(2020, 10, 11, 14, 25, 25, 300000),
      datetime.datetime(2020, 10, 11, 14, 25, 30, 0)
    ),
    (
      10, datetime.datetime(2020, 10, 11, 14, 44, 44, 500000),
      datetime.datetime(2020, 10, 11, 14, 44, 40, 0)
    ),
    (
      10, datetime.datetime(2020, 10, 11, 14, 45, 45, 700000),
      datetime.datetime(2020, 10, 11, 14, 45, 50, 0)
    ),
    # Nearest half hour
    (
      30 * 60, datetime.datetime(2020, 10, 11, 14, 10, 10, 100000),
      datetime.datetime(2020, 10, 11, 14, 0, 0)
    ),
    (
      30 * 60, datetime.datetime(2020, 10, 11, 14, 25, 10, 300000),
      datetime.datetime(2020, 10, 11, 14, 30, 0)
    ),
    (
      30 * 60, datetime.datetime(2020, 10, 11, 14, 44, 10, 500000),
      datetime.datetime(2020, 10, 11, 14, 30, 0)
    ),
    (
      30 * 60, datetime.datetime(2020, 10, 11, 14, 45, 10, 700000),
      datetime.datetime(2020, 10, 11, 15, 0, 0)
    ),
    # Nearest 1 day
    (
      24 * 60 * 60, datetime.datetime(2020, 4, 11, 8, 10, 10, 100000),
      datetime.datetime(2020, 4, 11)
    ),
    (
      24 * 60 * 60, datetime.datetime(2020, 4, 11, 14, 25, 10, 300000),
      datetime.datetime(2020, 4, 12)
    ),
    (
      24 * 60 * 60, datetime.datetime(2020, 4, 11, 16, 44, 10, 500000),
      datetime.datetime(2020, 4, 12)
    ),
    (
      24 * 60 * 60, datetime.datetime(2020, 4, 11, 21, 45, 10, 700000),
      datetime.datetime(2020, 4, 12)
    ),
  ]
)
def rounding_fixture(request):
  yield request.param


# noinspection PyShadowingNames
class TestDateTime(d1_test.d1_test_case.D1TestCase):

  #
  # Check
  #

  def test_1000(self):
    """has_tz(): Returns false for naive dt"""
    assert not dt.has_tz(T1_NAIVE)

  def test_1010(self):
    """has_tz(): Returns True for dt that has tz"""
    assert dt.has_tz(T1_MST)
    assert dt.has_tz(T2_UTC)
    assert dt.has_tz(T1_YEKT)

  def test_1020(self):
    """is_utc(): Returns False for naive dt"""
    assert not dt.is_utc(T1_NAIVE)

  def test_1030(self):
    """is_utc(): Returns False for dt with tz other than UTC"""
    assert not dt.is_utc(T1_MST)

  def test_1040(self):
    """is_utc(): Returns True for dt in UTC"""
    assert dt.is_utc(T2_UTC)

  def test_1050(self):
    """ts_from_dt(): Assumes naive dt to be in UTC"""
    assert dt.ts_from_dt(T1_NAIVE) == dt.ts_from_dt(T1_UTC)

  def test_1060(self):
    """ts_from_dt(): Includes tz"""
    assert dt.ts_from_dt(T1_MST) != dt.ts_from_dt(T1_UTC)

  def test_1070(self, dt_fixture):
    """dt_from_ts():
    - Naive dt is assumed to be at UTC
    - Round trips preserve original value
    """
    dt_utc = dt.normalize_datetime_to_utc(dt_fixture)
    assert dt.dt_from_ts(dt.ts_from_dt(dt_fixture), dt_fixture.tzinfo) == dt_utc

  def test_1080(self, rounding_fixture, tz_fixture):
    """round_to_nearest()"""
    round_sec, t, t_rounded = rounding_fixture
    t = t.replace(tzinfo=tz_fixture)
    t_rounded = t_rounded.replace(tzinfo=tz_fixture)
    logging.debug(
      'round_sec={} t={} t_rounded={}'.format(round_sec, t, t_rounded)
    )
    assert dt.round_to_nearest(t, round_sec) == t_rounded

  def test_1090(self, rounding_fixture, tz_fixture):
    """are_equal(): Returns True if two naive dts are equal to within the fuzz
    factor
    """
    round_sec, t, t_rounded = rounding_fixture
    t = t.replace(tzinfo=tz_fixture)
    t_rounded = t_rounded.replace(tzinfo=tz_fixture)
    logging.debug(
      'round_sec={} t={} t_rounded={}'.format(round_sec, t, t_rounded)
    )
    assert dt.are_equal(t, t_rounded, round_sec)

  def test_1100(self):
    """are_equal(): Returns True when comparing the same point in time specified
    in two different tz
    """
    assert dt.are_equal(T_ABS_1, T_ABS_2)

  #
  # Conversion
  #

  def test_1110(self):
    """ts_from_dt(): Assumes naive datetime is in UTC"""
    assert dt.ts_from_dt(T1_NAIVE) == T1_UTC_EPOCH

  def test_1120(self):
    """ts_from_dt(): Includes timezone (MST, UTC-7)"""
    assert dt.ts_from_dt(T1_MST) == T1_UTC_EPOCH + 7 * 3600

  def test_1130(self):
    """ts_from_dt(): Includes timezone (YEKT, UTC+6)"""
    assert dt.ts_from_dt(T1_YEKT) == T1_UTC_EPOCH - 6 * 3600

  def test_1140(self):
    """http_datetime_str_from_dt(): Assumes naive datetime is in UTC"""
    assert dt.http_datetime_str_from_dt(
      T1_NAIVE
    ) == 'Sat, 02 Jan 1999 03:04:05 GMT'

  def test_1150(self):
    """http_datetime_str_from_dt(): Inludes timezone (MST, UTC-7)"""
    assert dt.http_datetime_str_from_dt(
      T1_MST
    ) == 'Sat, 02 Jan 1999 10:04:05 GMT'

  def test_1160(self):
    """http_datetime_str_from_dt() includes timezone (YEKT, UTC+6)"""
    assert dt.http_datetime_str_from_dt(
      T1_YEKT
    ) == 'Fri, 01 Jan 1999 21:04:05 GMT'

  def _from_http_datetime(self, that_fateful_day_in_november_94):
    d = dt.dt_from_http_datetime_str(that_fateful_day_in_november_94)
    assert d == dt.create_utc_datetime(1994, 11, 6, 8, 49, 37)

  def test_1170(self):
    """from_http_datetime(): RFC 822, updated by RFC 1123"""
    self._from_http_datetime('Sun, 06 Nov 1994 08:49:37 GMT')

  def test_1180(self):
    """from_http_datetime(): RFC 850, obsoleted by RFC 1036"""
    self._from_http_datetime('Sunday, 06-Nov-94 08:49:37 GMT')

  def test_1190(self):
    """from_http_datetime(): ANSI C's asctime() format"""
    self._from_http_datetime('Sun Nov  6 08:49:37 1994')

  def test_1200(self):
    """is_utc(): Returns False for naive datetime"""
    assert not dt.is_utc(T1_NAIVE)

  def test_1210(self):
    """is_utc(): Returns False for timezone aware datetime not in UTC (MST, UTC-7)"""
    assert not dt.is_utc(T1_MST)

  def test_1220(self):
    """is_utc(): Returns False for timezone aware datetime not in UTC (YEKT, UTC+6)"""
    assert not dt.is_utc(T1_YEKT)

  def test_1230(self):
    """is_utc(): Returns True for datetime with tz in UTC"""
    assert dt.is_utc(T2_UTC)

  def test_1240(self):
    """normalize_datetime_to_utc(): Adjusts for tz"""
    t1_utc = dt.normalize_datetime_to_utc(T_ABS_1)
    t2_utc = dt.normalize_datetime_to_utc(T_ABS_2)
    assert dt.is_utc(t1_utc)
    assert dt.is_utc(t2_utc)
    assert dt.are_equal(t1_utc, t2_utc)

  def test_1250(self):
    """normalize_datetime_to_utc(): Assumes that naive dt is in UTC"""
    utc_dt = dt.normalize_datetime_to_utc(T2_NAIVE)
    assert dt.is_utc(utc_dt)
    assert dt.are_equal(utc_dt, T2_NAIVE)

  def test_1260(self):
    """normalize_datetime_to_utc(): Includes tz"""
    utc_dt = dt.normalize_datetime_to_utc(T1_YEKT)
    assert dt.is_utc(utc_dt)
    assert dt.are_equal(utc_dt, T1_YEKT)
