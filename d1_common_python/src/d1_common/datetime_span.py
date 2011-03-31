# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_common.datetime_span
==============================

:Created: 2011-03-25
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6

Represent a ISO8601 time interval. A time interval has a defined
start and end. This is as opposed to a time duration, which defines
only how much time is in an interval.
'''

import re
import datetime
import util

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise


class ParseError(Exception):
  '''Raised on ISO8601 parse error.
  '''
  pass


class DateTimeSpan(object):
  def __init__(self, interval=None):
    '''Constructor for DateTimeSpan.
    '''
    self.ISODATESEPARATOR = "/"
    self.datetime_first = None
    self.datetime_second = None
    if interval is not None:
      self.update_span_with_interval_iso(interval)

  def __unicode__(self):
    return unicode(self.interval_iso)

  def __str__(self):
    return self.interval_iso

  def _parse_iso(self, datetime_):
    try:
      return iso8601.parse_date(datetime_)
    except (iso8601.iso8601.ParseError, TypeError):
      raise ParseError('Invalid ISO8601 datetime \'{0}\''.format(datetime_))

  def update_span_with_datetime(self, datetime_first, datetime_second):
    if datetime_first is not None:
      self.datetime_first = datetime_first
    if datetime_second is not None:
      self.datetime_second = datetime_second

  def update_span_with_iso(self, iso_first, iso_second):
    if iso_first is not None:
      _self.datetime_first = self._parse_iso(iso_first)
    if iso_second is not None:
      self.datetime_second = self._parse_iso(iso_second)

  def update_span_with_interval_iso(self, interval):
    parts = interval.split(self.ISODATESEPARATOR)
    if len(parts) != 2:
      raise ParseError(
        'Invalid span (found {0} "{1}" separators)'.format(
          len(parts), self.ISODATESEPARATOR)
      )
    self.datetime_first = self._parse_iso(parts[0])
    self.datetime_second = self._parse_iso(parts[1])

  def update_span_with_path_element(self, interval_path_element):
    '''Set the span using a path element.
    '''
    interval = util.decodePathElement(interval_path_element)
    self.update_span_with_interval_iso(interval)

  @property
  def first(self):
    '''Return first datetime value as datetype object.
    '''
    return self.datetime_first

  @property
  def first_iso(self):
    '''Return first datetime value encoded in ISO8601 format.
    '''
    return datetime.datetime.isoformat(self.datetime_first)

  @property
  def second(self):
    '''Return second datetime value as datetype object.
    '''
    return self.datetime_second

  @property
  def second_iso(self):
    '''Return second datetime value encoded in ISO8601 format.
    '''
    return datetime.datetime.isoformat(self.datetime_second)

  @property
  def interval_iso(self):
    '''Return interval.
    '''
    return '{1}{0}{2}'.format(self.ISODATESEPARATOR, self.first_iso, self.second_iso)

  @property
  def interval_as_path_element_iso(self):
    '''Return interval encoded as a URL path element.
    '''
    return util.encodePathElement(self.interval_iso)
