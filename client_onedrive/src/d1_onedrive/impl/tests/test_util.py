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
"""Test utility functions
"""

import d1_onedrive.impl.util
import mock

import d1_test.d1_test_case


class TestUtil(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """ensure_dir_exists()"""
    with mock.patch('os.makedirs') as mock_makedirs:
      d1_onedrive.impl.util.ensure_dir_exists('/abc/de/f')
      mock_makedirs.assert_called_with('/abc/de/f')

  def test_1010(self):
    """string_from_path_elements()"""
    assert d1_onedrive.impl.util.string_from_path_elements(['abc', 'de',
                                                            'f']) == 'abc/de/f'

  def test_1020(self):
    """is_root()"""
    assert d1_onedrive.impl.util.is_root(['', ''])
    assert not d1_onedrive.impl.util.is_root(['a', ''])

  def test_1030(self):
    """os_format()"""
    with mock.patch('platform.system', return_value='Linux'):
      assert d1_onedrive.impl.util.os_format('a\nb\n') == \
        b'a\nb\n'
    with mock.patch('platform.system', return_value='Windows'):
      assert d1_onedrive.impl.util.os_format('a\nb\n') == \
        b'\xff\xfea\x00\r\x00\n\x00b\x00\r\x00\n\x00'
