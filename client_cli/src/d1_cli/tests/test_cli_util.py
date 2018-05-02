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
"""Test CLI utilities
"""

import io
import tempfile

import d1_cli.impl.cli
import d1_cli.impl.cli_client
import d1_cli.impl.cli_exceptions
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.operation_validator
import pytest
import responses

import d1_test.d1_test_case
import d1_test.mock_api.get as mock_get

import d1_client.mnclient_2_0


class TestCLIUtil(d1_test.d1_test_case.D1TestCase):
  def setup_method(self):
    cli = d1_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  # confirm()

  def test_1000(self):
    """confirm(): default=no, answer=no"""
    self._test_confirm(
      default='no', answer='no', expected_prompt='[yes/NO]',
      expected_result=False
    )

  def test_1010(self):
    """confirm(): default=no, answer=yes"""
    self._test_confirm(
      default='no', answer='yes', expected_prompt='[yes/NO]',
      expected_result=True
    )

  def test_1020(self):
    """confirm(): default=no, answer=unset"""
    self._test_confirm(
      default='no', expected_prompt='[yes/NO]', expected_result=False
    )

  def test_1030(self):
    """confirm(): default=yes, answer=no"""
    self._test_confirm(
      default='yes', answer='no', expected_prompt='[YES/no]',
      expected_result=False
    )

  def test_1040(self):
    """confirm(): default=yes, answer=yes"""
    self._test_confirm(
      default='yes', answer='yes', expected_prompt='[YES/no]',
      expected_result=True
    )

  def test_1050(self):
    """confirm(): default=yes, answer=unset"""
    self._test_confirm(
      default='yes', answer='yes', expected_prompt='[YES/no]',
      expected_result=True
    )

  def test_1060(self):
    """confirm(): default=unset, answer=no"""
    self._test_confirm(answer='no', expected_result=False)

  def test_1070(self):
    """confirm(): default=unset, answer=yes"""
    self._test_confirm(answer='yes', expected_result=True)

  def test_1080(self):
    """confirm(): default=unset, answer=unset"""
    self._test_confirm(allow_blank=True)

  def _test_confirm(
      self, default=None, answer=None, allow_blank=False, expected_prompt=None,
      expected_result=None
  ):
    test_prompt = 'Test Prompt'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with d1_test.d1_test_case.mock_input(answer or ''):
        is_confirmed = cli_util.confirm(
          test_prompt, default=default or '', allow_blank=allow_blank
        )
        assert expected_result == is_confirmed
    assert '{} {}'.format(test_prompt, expected_prompt or '').strip() in \
      out_stream.getvalue()

  # output()

  def test_1090(self):
    """output(): Output to screen when no file path is provided"""
    msg_str = 'line1\nline2\n'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      cli_util.output(io.StringIO(msg_str), path=None)
    assert msg_str == out_stream.getvalue()

  def test_1100(self):
    """output(): Output to file when file path is provided"""
    msg_str = 'line1\nline2\n'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file_path = tmp_file.name
      cli_util.output(io.StringIO(msg_str), path=tmp_file_path)
    assert '' == out_stream.getvalue()
    with open(tmp_file_path, 'r') as tmp_file:
      assert msg_str == tmp_file.read()

  def test_1110(self):
    """output(): Raises CLIError on invalid path"""
    msg_str = 'line1\nline2\n'
    with pytest.raises(d1_cli.impl.cli_exceptions.CLIError):
      cli_util.output(
        io.StringIO(msg_str),
        path='/some/invalid/path',
      )

  # assert_file_exists()

  def test_1120(self):
    """assert_file_exists(): Returns silently if path references a file"""
    with tempfile.NamedTemporaryFile() as tmp_file:
      assert cli_util.assert_file_exists(tmp_file.name) is None

  def test_1130(self):
    """assert_file_exists(): Raises InvalidArguments if path is invalid"""
    with pytest.raises(d1_cli.impl.cli_exceptions.InvalidArguments):
      cli_util.assert_file_exists('/')

  # copy_file_like_object_to_file()

  def test_1140(self):
    """copy_file_like_object_to_file(): Copies f to file when path is valid"""
    msg_str = 'line1\nline2\n'
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    cli_util.copy_file_like_object_to_file(
      io.BytesIO(msg_str.encode('utf-8')), tmp_file_path
    )
    with open(tmp_file_path, 'r') as tmp_file:
      assert msg_str == tmp_file.read()

  def test_1150(self):
    """copy_file_like_object_to_file(): Raises InvalidArguments if path is invalid"""
    msg_str = 'line1\nline2\n'
    with pytest.raises(d1_cli.impl.cli_exceptions.CLIError):
      cli_util.copy_file_like_object_to_file(msg_str, '/')

  # copy_requests_stream_to_file()

  @responses.activate
  def test_1160(self):
    """copy_requests_stream_to_file(): Copies Requests Response body to file when path is valid"""
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    response = client.get('test_pid_1')
    with tempfile.NamedTemporaryFile() as tmp_file:
      cli_util.copy_requests_stream_to_file(response, tmp_file.name)
      tmp_file.seek(0)
      got_sciobj_bytes = tmp_file.read()
      expected_sciobj_bytes = client.get('test_pid_1').content
      self.sample.assert_equals(got_sciobj_bytes, 'copy_stream_to_file')
      assert got_sciobj_bytes == expected_sciobj_bytes

  @responses.activate
  def test_1170(self):
    """copy_requests_stream_to_file(): Raises InvalidArguments if path is invalid"""
    mock_get.add_callback(d1_test.d1_test_case.MOCK_MN_BASE_URL)
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      d1_test.d1_test_case.MOCK_MN_BASE_URL
    )
    response = client.get('test_pid_1')
    with pytest.raises(d1_cli.impl.cli_exceptions.CLIError):
      cli_util.copy_requests_stream_to_file(response, '/an/invalid/path')

  # print()

  def test_1180(self):
    """print()"""
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      msg = 'test_msg'
      cli_util.print_debug(msg)
      cli_util.print_error(msg)
      cli_util.print_warn(msg)
      cli_util.print_info(msg)
      self.sample.assert_equals(out_stream.getvalue(), 'print')
    # assert 'DEBUG    test_msg\n' \
    #   'ERROR    test_msg\n' \
    #   'WARN     test_msg\n' \
    #   '         test_msg\n' == \
    #
