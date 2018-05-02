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

import io

import pytest

import d1_test.d1_test_case

import d1_client.object_format_info

# Typical mapping (format id, mimetype, extension):
# netCDF-3,application/netcdf,.nc

CSV_TEST_VALID = """formatIdentifier,mimeType,extension
abcd,efgh,ijkl
"""

CSV_TEST_INVALID = """formatIdentifier,mimeType,extension

Blank line above.
"""


class TestObjectFormatInfo(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    # TODO: All setup_class() should be changed to fixtures.
    self.i = d1_client.object_format_info.ObjectFormatInfo()

  def test_1000(self):
    """init()"""
    pass # Successful setup of the test means that the class initialized ok.

  def test_1010(self):
    """content_type_from_format_id()"""
    assert self.i.content_type_from_format_id(
      'netCDF-3'
    ) == 'application/netcdf'

  def test_1020(self):
    """filename_extension_from_format_id()"""
    assert self.i.filename_extension_from_format_id('netCDF-3') == '.nc'

  def test_1030(self):
    """read_csv_file()"""
    self.i.read_csv_file()
    assert self.i.filename_extension_from_format_id('netCDF-3') == '.nc'

  def test_1040(self):
    """read_csv_file(new_csv)"""
    self.i.read_csv_file(io.StringIO(CSV_TEST_VALID))
    assert self.i.filename_extension_from_format_id('abcd') == 'ijkl'

  def test_1050(self):
    """singleton"""
    j = d1_client.object_format_info.ObjectFormatInfo()
    j.read_csv_file(io.StringIO(CSV_TEST_VALID))
    assert self.i.filename_extension_from_format_id('abcd') == 'ijkl'

  def test_1060(self):
    """bad_csv_file"""
    with pytest.raises(Exception):
      self.i.read_csv_file(io.StringIO(CSV_TEST_INVALID))
