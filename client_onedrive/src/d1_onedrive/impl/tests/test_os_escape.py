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
"""Test OS specific escape functions
"""

import d1_onedrive.impl.os_escape

import d1_test.d1_test_case


class TestOsEscape(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """windows_filename_from_identifier()"""
    result = d1_onedrive.impl.os_escape.windows_filename_from_identifier(
      'doi/10.5063/\\/:?'
    )
    assert result == 'doi%2F10.5063%2F%5C%2F%3A%3F'

  def test_1010(self):
    """windows_identifier_from_filename()"""
    result = d1_onedrive.impl.os_escape.windows_identifier_from_filename(
      'doi%2F10.5063%2F%5C%2F%3A%3F'
    )
    assert result == 'doi/10.5063/\\/:?'

  def test_1020(self):
    """posix_filename_from_identifier()"""
    result = d1_onedrive.impl.os_escape.posix_filename_from_identifier(
      'doi/10.5063/\\/:?'
    )
    assert result == 'doi%2F10.5063%2F%5C%2F:%3F'

  def test_1030(self):
    """posix_identifier_from_filename()"""
    result = d1_onedrive.impl.os_escape.posix_identifier_from_filename(
      'doi%2F10.5063%2F%5C%2F:%3F'
    )
    assert result == 'doi/10.5063/\\/:?'
