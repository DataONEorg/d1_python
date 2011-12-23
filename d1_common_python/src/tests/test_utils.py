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
Module d1_common.tests.test_utils
=================================

Unit tests for various utilities.

:Created: 2011-01-21
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import codecs
import datetime
import logging
import os
import sys
import unittest

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
from d1_common import xmlrunner
import d1_common.util

# App
import util


class TestUtils(unittest.TestCase):
  def test_010(self):
    '''to_http_datetime()'''
    dt = datetime.datetime(1999, 3, 19, 1, 2, 3)
    dt_str = 'Fri, 19 Mar 1999 08:02:03 GMT' # adjusted to GMT
    self.assertEqual(d1_common.util.to_http_datetime(dt), dt_str)

  # from_http_datetime()

  def _from_http_datetime(self, that_fateful_day_in_november_94):
    dt = d1_common.util.from_http_datetime(that_fateful_day_in_november_94)
    self.assertEqual(dt, datetime.datetime(1994, 11, 6, 8, 49, 37))

  def test_020(self):
    '''from_http_datetime(): RFC 822, updated by RFC 1123'''
    self._from_http_datetime('Sun, 06 Nov 1994 08:49:37 GMT')

  def test_021(self):
    '''from_http_datetime(): RFC 850, obsoleted by RFC 1036'''
    self._from_http_datetime('Sunday, 06-Nov-94 08:49:37 GMT')

  def test_022(self):
    '''from_http_datetime(): ANSI C's asctime() format'''
    self._from_http_datetime('Sun Nov  6 08:49:37 1994')

  # Checksum

  def test_030(self):
    '''are_checksums_equal(): Same checksum, same algorithm'''
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'SHA-1'
    self.assertTrue(d1_common.util.are_checksums_equal(c1, c2))

  def test_031(self):
    '''are_checksums_equal(): Same checksum, different algorithm'''
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertFalse(d1_common.util.are_checksums_equal(c1, c2))

  def test_032(self):
    '''are_checksums_equal(): Different checksum, same algorithm'''
    c1 = dataoneTypes.Checksum('BAADF00DX')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertFalse(d1_common.util.are_checksums_equal(c1, c2))

  def test_033(self):
    '''are_checksums_equal(): Case insensitive checksum comparison'''
    c1 = dataoneTypes.Checksum('baadf00d')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    self.assertTrue(d1_common.util.are_checksums_equal(c1, c2))

  # Path elements.

  def testEncodePathElement(self):
    fpath = os.path.abspath(os.path.dirname(__file__))
    ftest = os.path.join(fpath, 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt')
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodePathElement(v))

  def testEncodeQueryElement(self):
    fpath = os.path.abspath(os.path.dirname(__file__))
    ftest = os.path.join(fpath, 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt')
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodeQueryElement(v))

  def testEncodeURL(self):
    data = [
      ('a', '"#<>[]^`{}|'), ('b', '-&=&='), ('c', 'http://example.com/data/mydata?row=24')
    ]
    expected = 'a=%22%23%3C%3E%5B%5D%5E%60%7B%7D%7C&b=-%26%3D%26%3D&c=http://example.com/data/mydata?row%3D24'
    test = d1_common.util.urlencode(data)
    self.assertEqual(test, expected)

  def test_stripElementSlashes(self):
    self.assertEqual('element', d1_common.util.stripElementSlashes('/element'))
    self.assertEqual('element', d1_common.util.stripElementSlashes('//element/'))
    self.assertEqual('element', d1_common.util.stripElementSlashes('element/'))
    self.assertEqual('ele/ment', d1_common.util.stripElementSlashes('/ele/ment/'))
    self.assertEqual('ele//ment', d1_common.util.stripElementSlashes('ele//ment'))
    self.assertEqual('', d1_common.util.stripElementSlashes('/'))
    self.assertEqual('', d1_common.util.stripElementSlashes('//'))

  def test_joinPathElements(self):
    self.assertEqual('a/b', d1_common.util.joinPathElements('a', 'b'))
    self.assertEqual('a/b/c', d1_common.util.joinPathElements('a/', '/b', 'c'))

  def test_normalizeTarget(self):
    '''normalizeTarget()'''
    u0 = "http://some.server/base/mn/"
    u1 = "http://some.server/base/mn"
    u2 = "http://some.server/base/mn?"
    u3 = "http://some.server/base/mn/?"
    self.assertEqual(u0, d1_common.util.normalizeTarget(u0))
    self.assertEqual(u0, d1_common.util.normalizeTarget(u1))
    self.assertEqual(u0, d1_common.util.normalizeTarget(u2))
    self.assertEqual(u0, d1_common.util.normalizeTarget(u3))

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

  s = TestUtils
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
