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
"""Utilities for handling date-times in DataONE

These functions are guaranteed not to modify their datetime arguments (datetime
objects are immutable).
"""

import datetime
import email.utils
import logging

import iso8601


class UTC(datetime.tzinfo):
  """timezoneinfo derived class that represents the UTC timezone

  - Date-times in DataONE should have timezone information that is fixed to
  UTC. A naive Python datetime can be fixed to UTC by attaching it to this
  timezoneinfo based class.
  """

  def __repr__(self):
    return self.tzname(0)

  def utcoffset(self, dt):
    return datetime.timedelta(0)

  def tzname(self, dt):
    return 'UTC'

  def dst(self, dt):
    return datetime.timedelta(0)


# ==============================================================================


class FixedOffset(datetime.tzinfo):
  """timezoneinfo derived class that represents any timezone as fixed offset in
  minutes east from UTC

  - Date-times in DataONE should have timezone information that is fixed to
  UTC. A naive Python datetime can be fixed to UTC by attaching it to this
  timezoneinfo based class.
  - See the UTC class for representing timezone in UTC.
  """

  def __init__(self, name, offset_hours=0, offset_minutes=0):
    self.__offset = datetime.timedelta(
      hours=offset_hours, minutes=offset_minutes
    )
    self.__name = name

  def __repr__(self):
    return '{} {}'.format(str(self.__offset), self.__name)

  def utcoffset(self, dt):
    return self.__offset

  def tzname(self, dt):
    return self.__name

  def dst(self, dt):
    return datetime.timedelta(0)


# ==============================================================================

#
# Checks
#


def has_tz(dt):
  """Return True if datetime has timezone (is not naive)"""
  return dt.tzinfo is not None


def is_utc(dt):
  """Return True if datetime has timezone and the timezone is in UTC
  """
  return dt.utcoffset() == datetime.timedelta(0)


def are_equal(a_dt, b_dt, n_round_sec=1):
  """Compare two datetimes for equality with fuzz factor

  - A naive datetime (no timezone information) is assumed to be in in UTC.
  - Since different systems may handle and store timestamps with different
  resolution, they often cannot be safely compared directly.
  """
  ra_dt = round_to_nearest(a_dt, n_round_sec)
  rb_dt = round_to_nearest(b_dt, n_round_sec)
  logging.debug('Rounded:')
  logging.debug('{} -> {}'.format(a_dt, ra_dt))
  logging.debug('{} -> {}'.format(b_dt, rb_dt))
  return cast_naive_datetime_to_utc(ra_dt) == cast_naive_datetime_to_utc(rb_dt)


#
# Conversions
#


def ts_from_dt(dt):
  """Convert datetime to Unix timestamp

  - A Unix timestamp is the number of seconds since Midnight, January 1st, 1970,
  UTC.
  - If the datetime contains sub-second values, the returned value will be a
  float with fraction.
  - Timezone is included if present.
  - A naive datetime (no timezone information) is assumed to be in in UTC.
  """
  dt = normalize_datetime_to_utc(dt)
  return (dt - create_utc_datetime(1970, 1, 1)).total_seconds()


def dt_from_ts(ts, tz=None):
  """Convert Unix timestamp to datetime

  - A Unix timestamp is the number of seconds since Midnight, January 1st, 1970,
  UTC.
  - If timezone is supplied, the datetime is returned set to that timezone.
  - If timezone is not supplied, a naive datetime is returned.
  """
  return datetime.datetime.fromtimestamp(ts, tz)


def http_datetime_str_from_dt(dt):
  """Format datetime to the preferred HTTP Full Date format, which is a
  fixed-length subset of that defined by RFC 1123

  - http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1
  - Timezone is included if present.
  - A naive datetime (no timezone information) is assumed to be in in UTC.
  """
  epoch_seconds = ts_from_dt(dt)
  return email.utils.formatdate(epoch_seconds, localtime=False, usegmt=True)


def xsd_datetime_str_from_dt(dt):
  """Format datetime to a xs:dateTime string
  (YYYY-MM-DDATETIMEHH:MM:SS.mmm+00:00)

  - Timezone is included if present.
  """
  return dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')


def dt_from_http_datetime_str(http_full_datetime):
  """Parse HTTP Full Date formats and return as datetime

  - Each of the allowed formats are supported:
  Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
  Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
  Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
  http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1
  - HTTP Full Dates are always in UTC.
  - The returned datetime is timezone aware and fixed to UTC.
  """
  date_parts = list(email.utils.parsedate(http_full_datetime)[:6])
  year = date_parts[0]
  if year <= 99:
    year = year + 2000 if year < 50 else year + 1900
  return create_utc_datetime(year, *date_parts[1:])


def dt_from_iso8601_str(iso8601_string, tz=UTC()):
  """Create Python datetime from ISO8601 formatted string

  Can raise d1_common.date_time.iso8601.ParseError.

  - A naive datetime (no timezone information) is assumed to be in {tz}, which
  is UTC by default.
  - {tz}=None: Return naive ISO8601 string as naive datetime.
  """
  return iso8601.parse_date(iso8601_string, tz)


#
# Timezone operations
#


def normalize_datetime_to_utc(dt):
  """Adjust datetime to UTC by applying the timezone offset to the datetime and
  setting the timezone to UTC

  - If timezone is already in UTC, returns the datetime unmodified.
  - A naive datetime (no timezone information) is assumed to be in in UTC.
  """
  if has_tz(dt):
    dt -= dt.utcoffset()
  return cast_datetime_to_utc(dt)


def normalize_datetime_to_naive_utc(dt):
  """Adjust datetime to naive UTC by applying any timezone offset to the
  datetime and removing the timezone

  - If timezone already in UTC, only removes the timezone.
  - If timezone is not set, returns the datetime unmodified.
  """
  dt = normalize_datetime_to_utc(dt)
  return strip_timezone(dt)


def cast_datetime_to_utc(dt):
  """Set timezone to UTC without adjusting the date-time

  - Warning: This will change the actual moment in time that is represented if
  the datetime is set to another timezone or if it is a naive datetime that
  represents a date and time not in UTC.
  - See also normalize_datetime_to_utc()."""
  return dt.replace(tzinfo=UTC())


def cast_naive_datetime_to_utc(dt):
  """If datetime is naive, set it to UTC

  - datetime with timezone remain unchanged.
  - Warning: This will change the actual moment in time that is represented if
  the datetime is naive and represents a date and time not in UTC.
  - See also normalize_datetime_to_utc().
  """
  if has_tz(dt):
    return dt
  return dt.replace(tzinfo=UTC())


def cast_naive_datetime_to_tz(dt, tz=UTC()):
  """If datetime is naive, set it to {tz}

  - {tz} should be a class derived from datetime.tzinfo.
  - {tz=None}: Set to UTC.
  - datetime with timezone remain unchanged.
  - Warning: This will change the actual moment in time that is represented if
  the datetime is naive and represents a date and time not in UTC.
  - See also normalize_datetime_to_utc().
  """
  if has_tz(dt):
    return dt
  return dt.replace(tzinfo=tz)


def strip_timezone(dt):
  """Set datetime to naive by stripping away any timezone information
  """
  return dt.replace(tzinfo=None)


#
# Misc
#


def utc_now():
  """Return the current time in the UTC timezone"""
  return cast_datetime_to_utc(datetime.datetime.utcnow())


def date_utc_now():
  """Return the current date as an ISO 8601 string in the UTC timezone"""
  return utc_now().date().isoformat()


def create_utc_datetime(*datetime_parts):
  """Create a datetime with timezone set to UTC"""
  return datetime.datetime(*datetime_parts, tzinfo=UTC())


def round_to_nearest(dt, n_round_sec=1.0):
  """Round datetime up or down to nearest {n_round_sec}.

  Any timezone is preserved but ignored in the rounding.

  Examples:
  {n_round_sec}=0.1: nearest 10th of a second.
  {n_round_sec}=1: nearest second.
  {n_round_sec}=30: nearest half hour.
  """
  ts = ts_from_dt(strip_timezone(dt)) + n_round_sec / 2.0
  res = dt_from_ts(ts - (ts % n_round_sec))
  return res.replace(tzinfo=dt.tzinfo)
