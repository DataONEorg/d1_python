# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Utilities for handling date-times in DataONE.

Timezones (tz):

- A datetime object can be **tz-naive** or **tz-aware**.

- **tz-naive**: The datetime does not include timezone information. As such, it does
  not by itself fully specify an absolute point in time. The exact point in time
  depends on in which timezone the time is specified, and the information may not be
  accessible to the end user. However, as timezones go from GMT-12 to GMT+14, and when
  including a possible daylight saving offset of 1 hour, a tz-naive datetime will
  always be within 14 hours of the real time.

- **tz-aware**: The datetime includes a timezone, specified as an abbreviation or as a
  hour and minute offset. It specifies an exact point in time.

"""

import datetime
import email.utils
import logging

import iso8601

logger = logging.getLogger(__name__)


class UTC(datetime.tzinfo):
    """datetime.tzinfo based class that represents the UTC timezone.

    Date-times in DataONE should have timezone information that is fixed to UTC. A naive
    Python datetime can be fixed to UTC by attaching it to this datetime.tzinfo based
    class.

    """

    def __repr__(self):
        return self.tzname()

    def utcoffset(self, dt):
        """Returns:

        UTC offset of zero

        """
        return datetime.timedelta(0)

    def tzname(self, dt=None):
        """Returns:

        str: "UTC"

        """
        return 'UTC'

    def dst(self, dt=None):
        """Args: dt: Ignored.

        Returns:   timedelta(0), meaning that daylight saving is never in effect.

        """
        return datetime.timedelta(0)


# ==============================================================================


class FixedOffset(datetime.tzinfo):
    """datetime.tzinfo derived class that represents any timezone as fixed offset in
    minutes east of UTC.

    - Date-times in DataONE should have timezone information that is fixed to UTC. A
      naive Python datetime can be fixed to UTC by attaching it to this datetime.tzinfo
      based class.
    - See the UTC class for representing timezone in UTC.

    """

    def __init__(self, name, offset_hours=0, offset_minutes=0):
        """Args: name: str Name of the timezone this offset represents.

        offset_hours:
          Number of hours offset from UTC.

        offset_minutes:
          Number of minutes offset from UTC.

        """
        self.__offset = datetime.timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def __repr__(self):
        return '{} {}'.format(str(self.__offset), self.__name)

    def utcoffset(self, dt):
        """Args: dt: Ignored.

        Returns:
          datetime.timedelta : The time offset from UTC.

        """
        return self.__offset

    def tzname(self, dt):
        """Args: dt: Ignored.

        Returns:   Name of the timezone this offset represents.

        """
        return self.__name

    def dst(self, dt=None):
        """Args: dt: Ignored.

        Returns:   timedelta(0), meaning that daylight saving is never in effect.

        """
        return datetime.timedelta(0)


# ==============================================================================

#
# Checks
#


def is_valid_iso8601(iso8601_str):
    """Determine if string is a valid ISO 8601 date, time, or datetime.

    Args:
      iso8601_str : str
        String to check.

    Returns:
      bool : ``True`` if string is a valid ISO 8601 date, time, or datetime.

    """
    try:
        iso8601.parse_date(iso8601_str)
    except iso8601.ParseError:
        return False
    return True


def has_tz(dt):
    """Determine if datetime has timezone (is not naive)

    Args:
      dt : datetime

    Returns:
      bool
        - **True**: ``datetime`` is tz-aware.
        - **False**: ``datetime`` is tz-naive.

    """
    return dt.tzinfo is not None


def is_utc(dt):
    """Determine if datetime has timezone and the timezone is in UTC.

    Args:
      dt : datetime

    Returns:
      bool : ``True`` if datetime has timezone and the timezone is in UTC

    """
    return dt.utcoffset() == datetime.timedelta(0)


def are_equal(a_dt, b_dt, round_sec=1):
    """Determine if two datetimes are equal with fuzz factor.

    A naive datetime (no timezone information) is assumed to be in in UTC.

    Args:
      a_dt: datetime
        Timestamp to compare.

      b_dt: datetime
        Timestamp to compare.

      round_sec: int or float
        Round the timestamps to the closest second divisible by this value before
        comparing them.

        E.g.:

        - ``n_round_sec`` = 0.1: nearest 10th of a second.
        - ``n_round_sec`` = 1: nearest second.
        - ``n_round_sec`` = 30: nearest half minute.

        Timestamps may lose resolution or otherwise change slightly as they go through
        various transformations and storage systems. This again may cause timestamps
        that
        have been processed in different systems to fail an exact equality compare even
        if
        they were initially the same timestamp. This rounding avoids such problems as
        long
        as the error introduced to the original timestamp is not higher than the
        rounding
        value. Of course, the rounding also causes a loss in resolution in the values
        compared, so should be kept as low as possible. The default value of 1 second
        should
        be a good tradeoff in most cases.

    Returns:
      bool
        - **True**: If the two datetimes are equal after being rounded by
          ``round_sec``.

    """
    ra_dt = round_to_nearest(a_dt, round_sec)
    rb_dt = round_to_nearest(b_dt, round_sec)
    logger.debug('Rounded:')
    logger.debug('{} -> {}'.format(a_dt, ra_dt))
    logger.debug('{} -> {}'.format(b_dt, rb_dt))
    return normalize_datetime_to_utc(ra_dt) == normalize_datetime_to_utc(rb_dt)


#
# Conversions
#


def ts_from_dt(dt):
    """Convert datetime to POSIX timestamp.

    Args:
      dt : datetime

        - Timezone aware datetime: The tz is included and adjusted to UTC (since
          timestamp is always in UTC).

        - Naive datetime (no timezone information): Assumed to be in UTC.

    Returns:
      int or float
        - The number of seconds since Midnight, January 1st, 1970, UTC.
        - If ``dt`` contains sub-second values, the returned value will be a float with
          fraction.

    See Also:
      ``dt_from_ts()`` for the reverse operation.

    """
    dt = normalize_datetime_to_utc(dt)
    return (dt - create_utc_datetime(1970, 1, 1)).total_seconds()


def dt_from_ts(ts, tz=None):
    """Convert POSIX timestamp to a timezone aware datetime.

    Args:
      ts : int or float, optionally with fraction
        The number of seconds since Midnight, January 1st, 1970, UTC.

      tz : datetime.tzinfo
        - If supplied: The dt is adjusted to that tz before being returned. It does not
          affect the ts, which is always in UTC.

        - If not supplied: the dt is returned in UTC.

    Returns:
      datetime
        Timezone aware datetime, in UTC.

    See Also:
      ``ts_from_dt()`` for the reverse operation.

    """
    return datetime.datetime.fromtimestamp(ts, tz or UTC())


def http_datetime_str_from_dt(dt):
    """Format datetime to HTTP Full Date format.

    Args:
      dt : datetime

        - tz-aware: Used in the formatted string.
        - tz-naive: Assumed to be in UTC.

    Returns:
      str
        The returned format is a is fixed-length subset of that defined by RFC 1123 and
        is
        the preferred format for use in the HTTP Date header. E.g.:

        ``Sat, 02 Jan 1999 03:04:05 GMT``

    See Also:
      - http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1

    """
    epoch_seconds = ts_from_dt(dt)
    return email.utils.formatdate(epoch_seconds, localtime=False, usegmt=True)


def xsd_datetime_str_from_dt(dt):
    """Format datetime to a xs:dateTime string.

    Args:
      dt : datetime

        - tz-aware: Used in the formatted string.
        - tz-naive: Assumed to be in UTC.

    Returns:
      str
        The returned format can be used as the date in xs:dateTime XML elements. It
        will
        be on the form ``YYYY-MM-DDTHH:MM:SS.mmm+00:00``.

    """
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')


def dt_from_http_datetime_str(http_full_datetime):
    """Parse HTTP Full Date formats and return as datetime.

    Args:
      http_full_datetime : str
        Each of the allowed formats are supported:

        - Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
        - Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
        - Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format

        HTTP Full Dates are always in UTC.

    Returns:
      datetime
        The returned datetime is always timezone aware and in UTC.

    See Also:
      http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.3.1

    """
    date_parts = list(email.utils.parsedate(http_full_datetime)[:6])
    year = date_parts[0]
    if year <= 99:
        year = year + 2000 if year < 50 else year + 1900
    return create_utc_datetime(year, *date_parts[1:])


def dt_from_iso8601_str(iso8601_str):
    """Parse ISO8601 formatted datetime string.

    Args:
      iso8601_str: str
        ISO 8601 formatted datetime.

        - tz-aware: Used in the formatted string.
        - tz-naive: Assumed to be in UTC.
        - Partial strings are accepted as long as they're on the general form.
          Everything from just ``2014`` to ``2006-10-20T15:34:56.123+02:30`` will work.
          The sections that are not present in the string are set to zero in the
          returned datetime.
        - See ``test_iso8601.py`` in the iso8601 package for examples.

    Returns:
      datetime
        The returned datetime is always timezone aware and in UTC.

    Raises:
      d1_common.date_time.iso8601.ParseError
        If ``iso8601_string` is not on the general form of ISO 8601.

    """
    return iso8601.parse_date(iso8601_str)


#
# Timezone operations
#


def normalize_datetime_to_utc(dt):
    """Adjust datetime to UTC.

    Apply the timezone offset to the datetime and set the timezone to UTC.

    This is a no-op if the datetime is already in UTC.

    Args:
      dt : datetime
        - tz-aware: Used in the formatted string.
        - tz-naive: Assumed to be in UTC.

    Returns:
      datetime
        The returned datetime is always timezone aware and in UTC.

    Notes:
      This forces a new object to be returned, which fixes an issue with
      serialization to XML in PyXB. PyXB uses a mixin together with
      datetime to handle the XML xs:dateTime. That type keeps track of
      timezone information included in the original XML doc, which conflicts if we
      return it here as part of a datetime mixin.

    See Also:
      ``cast_naive_datetime_to_tz()``

    """

    return datetime.datetime(
        *dt.utctimetuple()[:6], microsecond=dt.microsecond, tzinfo=datetime.timezone.utc
    )


def cast_naive_datetime_to_tz(dt, tz=UTC()):
    """If datetime is tz-naive, set it to ``tz``. If datetime is tz-aware, return it
    unmodified.

    Args:
      dt : datetime
        tz-naive or tz-aware datetime.

      tz : datetime.tzinfo
        The timezone to which to adjust tz-naive datetime.

    Returns:
      datetime
        tz-aware datetime.

    Warning:
      This will change the actual moment in time that is represented if the datetime is
      naive and represents a date and time not in ``tz``.

    See Also:
      ``normalize_datetime_to_utc()``

    """
    if has_tz(dt):
        return dt
    return dt.replace(tzinfo=tz)


def strip_timezone(dt):
    """Make datetime tz-naive by stripping away any timezone information.

    Args:
      dt : datetime
      - tz-aware: Used in the formatted string.
      - tz-naive: Returned unchanged.

    Returns:
      datetime
        tz-naive datetime.

    """
    return dt.replace(tzinfo=None)


#
# Misc
#


def utc_now():
    """Returns: tz-aware datetime: The current local date and time adjusted to the UTC
    timezone.

    Notes:
      - Local time is retrieved from the local machine clock.
      - Relies on correctly set timezone on the local machine.
      - Relies on current tables for Daylight Saving periods.
      - Local machine timezone can be checked with: ``$ date +'%z %Z'``.

    """
    return datetime.datetime.now(datetime.timezone.utc)


def date_utc_now_iso():
    """Returns:

    str : The current local date as an ISO 8601 string in the UTC timezone
      Does not include the time.

    """
    return utc_now().date().isoformat()


def local_now():
    """Returns:

    tz-aware datetime : The current local date and time in the local timezone

    """
    return datetime.datetime.now(datetime.timezone.utc).astimezone()


def local_now_iso():
    """Returns:

    str : The current local date and time as an ISO 8601 string in the local timezone

    """
    return local_now().isoformat()


def to_iso8601_utc(dt):
    """Args: dt: datetime.

    Returns:    str: ISO 8601 string in the UTC timezone

    """
    return dt.isoformat()


def create_utc_datetime(*datetime_parts):
    """Create a datetime with timezone set to UTC.

    Args:
      tuple of int: year, month, day, hour, minute, second, microsecond

    Returns:
      datetime

    """
    return datetime.datetime(*datetime_parts, tzinfo=UTC())


def round_to_nearest(dt, n_round_sec=1.0):
    """Round datetime up or down to nearest divisor.

    Round datetime up or down to nearest number of seconds that divides evenly by
    the divisor.

    Any timezone is preserved but ignored in the rounding.

    Args:
      dt: datetime

      n_round_sec : int or float
        Divisor for rounding

    Examples:
      - ``n_round_sec`` = 0.1: nearest 10th of a second.
      - ``n_round_sec`` = 1: nearest second.
      - ``n_round_sec`` = 30: nearest half minute.

    """
    ts = ts_from_dt(strip_timezone(dt)) + n_round_sec / 2.0
    res = dt_from_ts(ts - (ts % n_round_sec))
    return res.replace(tzinfo=dt.tzinfo)
