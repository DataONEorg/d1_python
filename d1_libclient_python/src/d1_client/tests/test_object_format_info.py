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
"""Module d1_client.tests.test_object_format_info
=================================================

Unit tests for ObjectFormatInfo.

:Created: 2012-10-25
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib
import StringIO
import sys

# D1
from d1_common.test_case_with_url_compare import TestCaseWithURLCompare

# App
sys.path.append('..')
import d1_client.object_format_info # noqa: E402

# Typical mapping (format id, mimetype, extension):
# netCDF-3,application/netcdf,.nc

CSV_TEST_VALID = """formatIdentifier,mimeType,extension
abcd,efgh,ijkl
"""

CSV_TEST_INVALID = """formatIdentifier,mimeType,extension

Blank line above.
"""


class TestObjectFormatInfo(TestCaseWithURLCompare):
  def setUp(self):
    self.i = d1_client.object_format_info.ObjectFormatInfo()

  def test_100(self):
    """init()"""
    pass # Successful setup of the test means that the class initialized ok.

  def test_200(self):
    """content_type_from_format_id()"""
    self.assertEqual(
      self.i.content_type_from_format_id('netCDF-3'), 'application/netcdf'
    )

  def test_300(self):
    """filename_extension_from_format_id()"""
    self.assertEqual(
      self.i.filename_extension_from_format_id('netCDF-3'), '.nc'
    )

  def test_400(self):
    """read_csv_file()"""
    self.i.read_csv_file()
    self.assertEqual(
      self.i.filename_extension_from_format_id('netCDF-3'), '.nc'
    )

  def test_500(self):
    """read_csv_file(new_csv)"""
    self.i.read_csv_file(StringIO.StringIO(CSV_TEST_VALID))
    self.assertEqual(self.i.filename_extension_from_format_id('abcd'), 'ijkl')

  def test_600(self):
    """singleton"""
    j = d1_client.object_format_info.ObjectFormatInfo()
    j.read_csv_file(StringIO.StringIO(CSV_TEST_VALID))
    self.assertEqual(self.i.filename_extension_from_format_id('abcd'), 'ijkl')

  def test_700(self):
    """bad_csv_file"""
    self.assertRaises(
      Exception, self.i.read_csv_file, StringIO.StringIO(CSV_TEST_INVALID)
    )
