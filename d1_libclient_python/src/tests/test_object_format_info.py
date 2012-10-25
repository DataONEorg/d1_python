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
'''Module d1_client.tests.test_object_format_info
=================================================

Unit tests for ObjectFormatInfo.

:Created: 2012-10-25
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import sys
import unittest

# D1.
from d1_common.testcasewithurlcompare import TestCaseWithURLCompare

# App.
import d1_client.object_format_info
import testing_utilities
import testing_context

# Typical mapping (format id, mimetype, extension):
# netCDF-3,application/netcdf,.nc


class TestObjectFormatInfo(TestCaseWithURLCompare):
  def setUp(self):
    self.i = d1_client.object_format_info.ObjectFormatInfo()

  def test_100_init(self):
    pass # Successful setup of the test means that the class initialized ok.

  def test_200_mimetype_from_format_id(self):
    self.assertEqual(self.i.mimetype_from_format_id('netCDF-3'), 'application/netcdf')

  def test_300_filename_extension_from_format_id(self):
    self.assertEqual(self.i.filename_extension_from_format_id('netCDF-3'), '.nc')

  def test_400_reread_csv_file(self):
    self.i.reread_csv_file()
    self.assertEqual(self.i.filename_extension_from_format_id('netCDF-3'), '.nc')

  def test_500_reread_csv_file_new_csv(self):
    self.i.reread_csv_file('csv_test.csv')
    self.assertEqual(self.i.filename_extension_from_format_id('abcd'), 'ijkl')

  def test_600_singleton(self):
    j = d1_client.object_format_info.ObjectFormatInfo()
    j.reread_csv_file('csv_test.csv')
    self.assertEqual(self.i.filename_extension_from_format_id('abcd'), 'ijkl')

  def test_700_bad_csv_file(self):
    try:
      self.i.reread_csv_file('csv_test_bad.csv')
    except Exception as e:
      self.assertTrue(str(e).startswith('Error in CSV file.'))
    else:
      self.assertTrue(False, "Expected exception")

#===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  #parser.add_option('--d1-root', dest='d1_root', action='store', type='string', default='http://0.0.0.0:8000/cn/') # default=d1_common.const.URL_DATAONE_ROOT
  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='http://cn-dev.dataone.org/cn/'
  )
  #parser.add_option('--gmn-url', dest='gmn_url', action='store', type='string', default='http://0.0.0.0:8000/')
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestObjectFormatInfo
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
