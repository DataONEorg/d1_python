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
"""Test generation of AccessControl in SysMeta
"""
import d1_cli.impl.access_control as access_control
import d1_cli.impl.cli_exceptions as cli_exceptions
import freezegun
import pytest

import d1_test.d1_test_case


@d1_test.d1_test_case.reproducible_random_decorator('TestAccessControl')
@freezegun.freeze_time('1967-05-27')
class TestAccessControl(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """AccessControl(): __init__()"""
    a = access_control.AccessControl()
    assert len(a.allow) == 0

  def test_1010(self):
    """clear(): Removes all allowed subjects"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', None)
    a.add_allowed_subject('subject_3', None)
    a.clear()
    assert len(a.allow) == 0

  def test_1020(self):
    """add_allowed_subject(): Single subject added without specified permission
    is retained and defaults to read"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    assert len(a.allow) == 1
    assert 'subject_1' in a.allow
    assert a.allow['subject_1'] == 'read'

  def test_1030(self):
    """Adding subject that already exists updates its permission"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    assert len(a.allow) == 1
    assert 'subject_1' in a.allow
    assert a.allow['subject_1'] == 'read'
    a.add_allowed_subject('subject_1', 'write')
    assert len(a.allow) == 1
    assert 'subject_1' in a.allow
    assert a.allow['subject_1'] == 'write'

  def test_1040(self):
    """add_allowed_subject(): Subject added with invalid permission raises
    exception InvalidArguments"""
    a = access_control.AccessControl()
    with pytest.raises(cli_exceptions.InvalidArguments):
      a.add_allowed_subject('subject_1', 'invalid_permission')
    assert len(a.allow) == 0

  def test_1050(self):
    """add_allowed_subject(): Multiple subjects with different permissions are
    correctly retained"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    assert len(a.allow) == 3
    assert 'subject_1' in a.allow
    assert a.allow['subject_1'] == 'read'
    assert 'subject_2' in a.allow
    assert a.allow['subject_2'] == 'write'
    assert 'subject_3' in a.allow
    assert a.allow['subject_3'] == 'changePermission'

  def test_1060(self):
    """remove_allowed_subject()"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    a.remove_allowed_subject('subject_3')
    assert len(a.allow) == 2
    assert not ('subject_3' in a.allow)

  def test_1070(self):
    """str() returns formatted string representation"""
    a = access_control.AccessControl()
    a.add_allowed_subject('subject_1', None)
    a.add_allowed_subject('subject_2', 'write')
    a.add_allowed_subject('subject_3', 'changePermission')
    self.sample.assert_equals(str(a), 'string_repr')
    # actual = []
    # for s in str(a).split('\n'):
    #   actual.append(s.strip())
    # assert actual[1] == 'read                          "subject_1"'
    # assert actual[2] == 'write                         "subject_2"'
    # assert actual[3] == 'changePermission              "subject_3"'

  def test_1080(self):
    """_confirm_special_subject_write(): Allows setting if user answers 'yes"""
    a = access_control.AccessControl()
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with d1_test.d1_test_case.mock_input('yes'):
        a._confirm_special_subject_write('public', 'write')
    prompt_str = out_stream.getvalue()
    assert 'WARN     It is not recommended to give write access to public. ' \
    'Continue? [yes/NO] ' == prompt_str

  def test_1090(self):
    """_confirm_special_subject_write(): Raises InvalidArguments if user answers
    'no"""
    a = access_control.AccessControl()
    with d1_test.d1_test_case.capture_std():
      with d1_test.d1_test_case.mock_input('no'):
        with pytest.raises(cli_exceptions.InvalidArguments):
          a._confirm_special_subject_write(
            'public',
            'write',
          )
