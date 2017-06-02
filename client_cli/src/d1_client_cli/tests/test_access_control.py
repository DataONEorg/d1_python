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

import unittest

import d1_client_cli.impl.access_control as access_control
import d1_client_cli.impl.cli_exceptions as cli_exceptions
import d1_test.util

#===============================================================================


class TestAccessControl(unittest.TestCase):
  def test_0010(self):
    """AccessControl(): The access_control object can be instantiated"""
    a = access_control.AccessControl()
    self.assertEqual(len(a.allow), 0)

  def test_0020(self):
    """clear(): Removes all allowed subjects"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', None)
    a.add_allowed_subject('subject_3', None)
    a.clear()
    self.assertEqual(len(a.allow), 0)

  def test_0030(self):
    """add_allowed_subject(): Single subject added without specified permission
    is retained and defaults to read"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')

  def test_0040(self):
    """Adding subject that already exists updates its permission"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')
    a.add_allowed_subject('subject_1', 'write')
    self.assertEqual(len(a.allow), 1)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'write')

  def test_0050(self):
    """add_allowed_subject(): Subject added with invalid permission raises
    exception InvalidArguments"""
    a = access_control.AccessControl()
    self.assertRaises(
      cli_exceptions.InvalidArguments, a.add_allowed_subject, 'subject_1',
      'invalid_permission'
    )
    self.assertEqual(len(a.allow), 0)

  def test_0060(self):
    """add_allowed_subject(): Multiple subjects with different permissions are
    correctly retained"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    self.assertEqual(len(a.allow), 3)
    self.assertTrue('subject_1' in a.allow)
    self.assertEqual(a.allow['subject_1'], 'read')
    self.assertTrue('subject_2' in a.allow)
    self.assertEqual(a.allow['subject_2'], 'write')
    self.assertTrue('subject_3' in a.allow)
    self.assertEqual(a.allow['subject_3'], 'changePermission')

  def test_0070(self):
    """remove_allowed_subject()"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    a.remove_allowed_subject('subject_3')
    self.assertEqual(len(a.allow), 2)
    self.assertFalse('subject_3' in a.allow)

  def test_0080(self):
    """str() returns formatted string representation"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    actual = []
    for s in str(a).split('\n'):
      actual.append(s.strip())
    self.assertEquals(actual[1], 'read                          "subject_1"')
    self.assertEquals(actual[2], 'write                         "subject_2"')
    self.assertEquals(actual[3], 'changePermission              "subject_3"')

  def test_0090(self):
    """_confirm_special_subject_write(): Allows setting if user answers 'yes"""
    a = access_control.AccessControl()
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with d1_test.util.mock_raw_input('yes'):
        a._confirm_special_subject_write('public', 'write')
    prompt_str = out_stream.getvalue()
    self.assertEqual(
      'WARN     It is not recommended to give write access to public. '
      'Continue? [yes/NO] ',
      prompt_str,
    )

  def test_0100(self):
    """_confirm_special_subject_write(): Raises InvalidArguments if user answers
    'no"""
    a = access_control.AccessControl()
    with d1_test.util.capture_std():
      with d1_test.util.mock_raw_input('no'):
        self.assertRaises(
          cli_exceptions.InvalidArguments,
          a._confirm_special_subject_write,
          'public',
          'write',
        )