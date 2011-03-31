#!/usr/bin/env python
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
Module d1_common.tests.test_datetime_span
=========================================

Unit tests for DateTimeSpan class.

:Created: 2011-03-25
:Author: DataONE (dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest
import StringIO
import datetime

from d1_common import xmlrunner
from d1_common.datetime_span import DateTimeSpan, ParseError


class FixedOffset(datetime.tzinfo):
  """Fixed offset in minutes east from UTC."""

  def __init__(self, offset, name):
    self.__offset = datetime.timedelta(minutes=offset)
    self.__name = name

  def utcoffset(self, dt):
    return self.__offset

  def tzname(self, dt):
    return self.__name

  def dst(self, dt):
    return ZERO

# Commented values are valid, but not handled by the iso8601 parser used by
# DateTimeSpan.
VALID_ISO8601_DATES = [
  '1994-11-05T08:15:30-05:00',
  '1994-11-05T13:15:30Z',
  '2008-02-12T12:23:34',
  '2008-02-12T12:23:34Z',
  '2008-02-12T13:23:34+01',
  '2008-02-12T11:23:34-01',
  #  '19930214T131030',
  #  '20080212T122334',
  #  '2008T1223',
]


class TestDateTimeSpan(unittest.TestCase):
  def test_init_without_args(self):
    '''Verify that the object can be instantiated without arguments.
    '''
    self.assertTrue(DateTimeSpan())
    dts = DateTimeSpan()
    self.assertFalse(dts.first)
    self.assertFalse(dts.second)

  def test_init_with_span(self):
    for iso_date in VALID_ISO8601_DATES:
      self.assertTrue(DateTimeSpan('{0}/{0}'.format(iso_date)))

  def test_init_with_invalid_span(self):
    self.assertRaises(ParseError, DateTimeSpan, 'invalid')

  def test_read_property(self):
    dts = DateTimeSpan('{0}/{1}'.format(VALID_ISO8601_DATES[0], VALID_ISO8601_DATES[1]))
    self.assertTrue(isinstance(dts.first, datetime.datetime))
    self.assertTrue(isinstance(dts.second, datetime.datetime))
    # TODO: Check that the datetime is correct. One way to do that is to find
    # out where the tzinfo based class "FixedOffset" comes from, so that a
    # datetime object that corresponds to the one that datetime.datetime holds
    # can be built.

  def test_iso_read_property(self):
    dts = DateTimeSpan('{0}/{1}'.format(VALID_ISO8601_DATES[2], VALID_ISO8601_DATES[3]))
    self.assertEquals(dts.first_iso, '2008-02-12T12:23:34+00:00')
    self.assertEquals(dts.second_iso, '2008-02-12T12:23:34+00:00')

  def interval_as_path_element_iso(self):
    dts = DateTimeSpan('{0}/{1}'.format(VALID_ISO8601_DATES[0], VALID_ISO8601_DATES[1]))
    self.assertEquals(
      dts.path_element, '1994-11-05T08:15:30-05:00%2F1994-11-05T13:15:30%2B00:00'
    )

  def test_update_by_path_element(self):
    dts = DateTimeSpan()
    dts.update_span_with_path_element(
      '1994-11-05T08:15:30-05:00%2F1994-11-05T13:15:30%2B00:00'
    )
    self.assertEquals(dts.first_iso, '1994-11-05T08:15:30-05:00')
    self.assertEquals(dts.second_iso, '1994-11-05T13:15:30+00:00')

#===============================================================================

if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
