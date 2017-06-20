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

import datetime

import pytest

import d1_common.date_time

import d1_test.d1_test_case

# App


class TestDateTime(d1_test.d1_test_case.D1TestCase):
  def _test_date_naive(self):
    return datetime.datetime(1999, 3, 19, 1, 2, 3, tzinfo=None)

  def _test_date_MST(self):
    class tz_mst(datetime.tzinfo):
      def utcoffset(self, dt):
        return datetime.timedelta(hours=-7)

    return datetime.datetime(1999, 3, 19, 1, 2, 3, tzinfo=tz_mst())

  def _test_date_YEKT(self):
    class tz_yekt(datetime.tzinfo):
      def utcoffset(self, dt):
        return datetime.timedelta(hours=6)

    return datetime.datetime(1999, 3, 19, 1, 2, 3, tzinfo=tz_yekt())

  def _test_date_UTC(self):
    class tz_utc(datetime.tzinfo):
      def utcoffset(self, dt):
        return datetime.timedelta(0)

    return datetime.datetime(1999, 3, 19, 1, 2, 3, tzinfo=tz_utc())

  # to_seconds_since_epoch()

  def test_1000(self):
    """to_seconds_since_epoch() assumes naive datetime is in UTC"""
    # Used http://www.epochconverter.com/ to verify.
    dt = self._test_date_naive()
    assert d1_common.date_time.to_seconds_since_epoch(dt) == 921805323

  def test_1010(self):
    """to_seconds_since_epoch() honors timezone (MST, UTC-7)"""
    # Used http://www.epochconverter.com/ to verify.
    dt = self._test_date_MST()
    assert d1_common.date_time.to_seconds_since_epoch(dt) == 921805323 + (
      7 * 3600
    )

  def test_1020(self):
    """to_seconds_since_epoch() honors timezone (YEKT, UTC+6)"""
    # Used http://www.epochconverter.com/ to verify.
    dt = self._test_date_YEKT()
    assert d1_common.date_time.to_seconds_since_epoch(dt) == 921805323 - (
      6 * 3600
    )

  # to_http_datetime()

  def test_1030(self):
    """to_http_datetime() assumes naive datetime is in UTC"""
    dt = self._test_date_naive()
    dt_str = 'Fri, 19 Mar 1999 01:02:03 GMT'
    assert d1_common.date_time.to_http_datetime(dt) == dt_str

  def test_1040(self):
    """to_http_datetime() honors timezone (MST, UTC-7)"""
    dt = self._test_date_MST()
    dt_str = 'Fri, 19 Mar 1999 08:02:03 GMT'
    assert d1_common.date_time.to_http_datetime(dt) == dt_str

  def test_1050(self):
    """to_http_datetime() honors timezone (YEKT, UTC+6)"""
    dt = self._test_date_YEKT()
    dt_str = 'Thu, 18 Mar 1999 19:02:03 GMT'
    assert d1_common.date_time.to_http_datetime(dt) == dt_str

  # from_http_datetime()

  def _from_http_datetime(self, that_fateful_day_in_november_94):
    dt = d1_common.date_time.from_http_datetime(that_fateful_day_in_november_94)
    assert dt == d1_common.date_time.create_utc_datetime(1994, 11, 6, 8, 49, 37)

  def test_1060(self):
    """from_http_datetime(): RFC 822, updated by RFC 1123"""
    self._from_http_datetime('Sun, 06 Nov 1994 08:49:37 GMT')

  def test_1070(self):
    """from_http_datetime(): RFC 850, obsoleted by RFC 1036"""
    self._from_http_datetime('Sunday, 06-Nov-94 08:49:37 GMT')

  def test_1080(self):
    """from_http_datetime(): ANSI C's asctime() format"""
    self._from_http_datetime('Sun Nov  6 08:49:37 1994')

  # is_utc()

  def test_1090(self):
    """is_utc() is false for naive datetime"""
    dt = self._test_date_naive()
    assert not d1_common.date_time.is_utc(dt)

  def test_1100(self):
    """is_utc() is false for timezone aware datetime not at UTC (MST, UTC-7)"""
    dt = self._test_date_MST()
    assert not d1_common.date_time.is_utc(dt)

  def test_1110(self):
    """is_utc() is false for timezone aware datetime not at UTC (YEKT, UTC+6)"""
    dt = self._test_date_YEKT()
    assert not d1_common.date_time.is_utc(dt)

  def test_1120(self):
    """is_utc() is true for timezone aware datetime at UTC"""
    dt = self._test_date_UTC()
    assert d1_common.date_time.is_utc(dt)

  # normalize_datetime_to_utc()

  def test_1130(self):
    """normalize_datetime_to_utc() raises TypeError for naive datetime and no timezone arg"""
    dt = self._test_date_naive()
    with pytest.raises(TypeError):
      d1_common.date_time.normalize_datetime_to_utc(dt)

  def test_1140(self):
    """normalize_datetime_to_utc() does raise exception for non-conflicting timezones"""
    dt = self._test_date_YEKT()
    d1_common.date_time.normalize_datetime_to_utc(dt, 6 * 60)

  def test_1150(self):
    """normalize_datetime_to_utc() raises TypeError conflicting timezones"""
    dt = self._test_date_YEKT()
    with pytest.raises(TypeError):
      d1_common.date_time.normalize_datetime_to_utc(dt, 3 * 60)

  def test_1160(self):
    """normalize_datetime_to_utc() returns correct result for timezone aware datetime"""
    dt = self._test_date_YEKT()
    dt_utc = d1_common.date_time.normalize_datetime_to_utc(dt)
    assert dt == dt_utc
    assert dt_utc.utcoffset() == datetime.timedelta(0)

  def test_1170(self):
    """normalize_datetime_to_utc() returns correct result for naive datetime and timezone arg"""
    dt = self._test_date_naive()
    dt_utc_norm = d1_common.date_time.normalize_datetime_to_utc(dt, 3 * 60)
    dt_utc = d1_common.date_time.create_utc_datetime(1999, 3, 18, 22, 2, 3)
    assert dt_utc_norm == dt_utc
