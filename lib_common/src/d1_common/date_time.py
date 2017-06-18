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
"""

from __future__ import absolute_import

import calendar
import datetime
import email.utils
import sys

# 3rd party
try:
  import iso8601
except ImportError as e:
  sys.stderr.write('Import error: {}\n'.format(str(e)))
  sys.stderr.write('pip install iso8601\n')
  raise


# D1
class UTC(datetime.tzinfo):
  """Date-times in DataONE are required to have timezone information that is
  fixed to UTC. A naive Python datetime can be fixed to UTC by attaching it
  to this tzinfo based class."""

  def utcoffset(self, dt):
    return datetime.timedelta(0)

  def tzname(self, dt):
    return 'UTC'

  def dst(self, dt):
    return datetime.timedelta(0)


# ==============================================================================


def to_seconds_since_epoch(dt):
  """Convert datetime to epoch time / Unix timestamp. This is the number of
  seconds since Midnight, January 1st, 1970, UTC.
  - Takes timezone information into account if included in the datetime.
  - A naive datetime (no timezone information) is assumed to be in UTC.
  """
  return calendar.timegm(dt.utctimetuple())


def ts_to_dt(ts, tz=None):
  return datetime.datetime.fromtimestamp(ts, tz)


def to_http_datetime(dt):
  """Format datetime to the preferred HTTP Full Date format, which is a
  fixed-length subset of that defined by RFC 1123.
  - http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1
  - Takes timezone information into account if included in the datetime.
  - A naive datetime (no timezone information) is assumed to be in UTC.
  """
  epoch_seconds = to_seconds_since_epoch(dt)
  return email.utils.formatdate(epoch_seconds, localtime=False, usegmt=True)


def to_xsd_datetime(dt):
  """Format datetime to a valid xs:dateTime. (YYYY-MM-DDTHH:MM:SS.mmm+00:00)
  The date_time must be UTC.
  :arg dt: Native Python datetime in UTC.
  :type dt: Python datetime with tzinfo set to UTC.
  :returns: xs:dateTime
  :return type: str
  """
  if not is_utc(dt):
    raise Exception('date_time must be UTC')
  return dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')


def from_http_datetime(http_full_datetime):
  """Parse HTTP Full Date formats. Each of the allowed formats are supported:
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


def from_iso8601(iso8601_string):
  """Create Python datetime from ISO8601 formatted string.
  Can raise d1_common.date_time.iso8601.ParseError.
  """
  return iso8601.parse_date(iso8601_string)


def is_utc(dt):
  """Check that datetime contains time zone information and that the
  timezone is UTC.
  """
  if dt.tzinfo is None:
    return False
  try:
    utc_offset = dt.utcoffset()
  except:
    return False
  if utc_offset:
    return False
  return True


def create_utc_datetime(*datetime_parts):
  return datetime.datetime(*datetime_parts, tzinfo=UTC())


def normalize_datetime_to_utc(dt, timezone=None):
  """Adjust datetime to UTC by applying the timezone offset to the datetime and
  setting the timezone to UTC.

  :param dt: Datetime with or without timezone information.
  :type dt: datetime.datetime
  :param timezone: Timezone specified as offset from UTC in minutes.
  :type timezone: int

  - Raises TypeError if datetime contains timezone, the timezone parameter is
    provided, and the two are in conflict.
  - Raises TypeError if datetime does not contain timezone information and the
    timezone parameter is not provided.
  - If datetime does not contain timezone information, the timezone parameter
    must be provided.
  - If datetime is already UTC, does nothing.
  """
  tz_dt_present = dt.tzinfo is not None
  tz_arg_present = timezone is not None

  if not tz_dt_present and not tz_arg_present:
    raise TypeError(
      'Timezone information must be provided either within '
      'datetime or as timezone argument'
    )

  if tz_dt_present and tz_arg_present and dt.utcoffset() != \
      datetime.timedelta(minutes=timezone):
    raise TypeError(
      'Timezone information was provided both within datetime '
      'and as timezone argument and the two were in conflict'
    )

  if tz_dt_present:
    dt -= dt.utcoffset()

  if tz_arg_present:
    dt -= datetime.timedelta(minutes=timezone)

  return cast_datetime_to_utc(dt)


def cast_datetime_to_utc(dt):
  """Set timezone to UTC without adjusting the date-time. Warning: If the
  date-time is naive and not in UTC, or if it is aware and not at UTC, this
  will change the actual moment in time that is represented. See also
  normalize_datetime_to_utc()."""
  return dt.replace(tzinfo=UTC())


def strip_timezone(dt):
  """Create a naive datetime by stripping away any timezone information. This
  is necessary for passing the datetime to some functions that cannot handle
  timezone information. Warning: If the date-time is not in UTC, this will
  change the actual moment in time that is represented."""
  return dt.replace(tzinfo=None)


def utc_now():
  """Now in the UTC timezone."""
  return cast_datetime_to_utc(datetime.datetime.utcnow())


def round_date_time(dt, n_round_sec=1):
  """Round a datetime to {round_seconds}.
  E.g.:
  1 = closest second
  60 = closest minute
  """
  # assert is_utc(dt), (
  #   'All date-times used in DataONE types are required to be timezone-aware '
  #   'and be set to UTC'
  # )
  dt = strip_timezone(dt)
  n_sec = (dt - dt.min).seconds
  n_half_round_sec = (n_sec + n_round_sec / 2) // n_round_sec**2
  return dt + datetime.timedelta(0, n_half_round_sec - n_sec, -dt.microsecond)
