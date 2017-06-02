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

from __future__ import absolute_import

import StringIO
import tempfile
import unittest

import responses

#import d1_test.mock_api.util as mock_util
import d1_test.util
import d1_test.mock_api.get as mock_get

import d1_client.mnclient_2_0
import d1_client_cli.impl.cli
import d1_client_cli.impl.cli_util as cli_util
import d1_client_cli.impl.cli_client
import d1_client_cli.impl.cli_exceptions
import d1_client_cli.impl.operation_validator


class TestCLIUtil(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    pass # d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  # confirm()

  def test_0010(self):
    """confirm(): default=no, answer=no"""
    self._test_confirm(
      default='no', answer='no', expected_prompt='[yes/NO]',
      expected_result=False
    )

  def test_0020(self):
    """confirm(): default=no, answer=yes"""
    self._test_confirm(
      default='no', answer='yes', expected_prompt='[yes/NO]',
      expected_result=True
    )

  def test_0030(self):
    """confirm(): default=no, answer=unset"""
    self._test_confirm(
      default='no', expected_prompt='[yes/NO]', expected_result=False
    )

  def test_0040(self):
    """confirm(): default=yes, answer=no"""
    self._test_confirm(
      default='yes', answer='no', expected_prompt='[YES/no]',
      expected_result=False
    )

  def test_0050(self):
    """confirm(): default=yes, answer=yes"""
    self._test_confirm(
      default='yes', answer='yes', expected_prompt='[YES/no]',
      expected_result=True
    )

  def test_0060(self):
    """confirm(): default=yes, answer=unset"""
    self._test_confirm(
      default='yes', answer='yes', expected_prompt='[YES/no]',
      expected_result=True
    )

  def test_0070(self):
    """confirm(): default=unset, answer=no"""
    self._test_confirm(answer='no', expected_result=False)

  def test_0080(self):
    """confirm(): default=unset, answer=yes"""
    self._test_confirm(answer='yes', expected_result=True)

  def test_0090(self):
    """confirm(): default=unset, answer=unset"""
    self._test_confirm(allow_blank=True)

  def _test_confirm(
      self, default=None, answer=None, allow_blank=False, expected_prompt=None,
      expected_result=None
  ):
    test_prompt = 'Test Prompt'
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with d1_test.util.mock_raw_input(answer or ''):
        is_confirmed = cli_util.confirm(
          test_prompt, default=default or '', allow_blank=allow_blank
        )
        self.assertEqual(expected_result, is_confirmed)
    self.assertIn(
      '{} {}'.format(test_prompt, expected_prompt or '').strip(),
      out_stream.getvalue()
    )

  # output()

  def test_0100(self):
    """output(): Output to screen when no file path is provided"""
    msg_str = 'line1\nline2\n'
    with d1_test.util.capture_std() as (out_stream, err_stream):
      cli_util.output(StringIO.StringIO(msg_str), path=None)
    self.assertEqual(msg_str, out_stream.getvalue())

  def test_0110(self):
    """output(): Output to file when file path is provided"""
    msg_str = 'line1\nline2\n'
    with d1_test.util.capture_std() as (out_stream, err_stream):
      with tempfile.NamedTemporaryFile() as tmp_file:
        tmp_file_path = tmp_file.name
      cli_util.output(StringIO.StringIO(msg_str), path=tmp_file_path)
    self.assertEqual('', out_stream.getvalue())
    with open(tmp_file_path, 'r') as tmp_file:
      self.assertEqual(msg_str, tmp_file.read())

  def test_0120(self):
    """output(): Raises CLIError on invalid path"""
    msg_str = 'line1\nline2\n'
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.CLIError,
      cli_util.output,
      StringIO.StringIO(msg_str),
      path='/some/invalid/path',
    )

  # assert_file_exists()

  def test_0130(self):
    """assert_file_exists(): Returns silently if path references a file"""
    with tempfile.NamedTemporaryFile() as tmp_file:
      self.assertIsNone(cli_util.assert_file_exists(tmp_file.name))

  def test_0140(self):
    """assert_file_exists(): Raises InvalidArguments if path is invalid"""
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.InvalidArguments,
      cli_util.assert_file_exists, '/'
    )

  # copy_file_like_object_to_file()

  def test_0150(self):
    """copy_file_like_object_to_file(): Copies flo to file when path is valid"""
    msg_str = 'line1\nline2\n'
    with tempfile.NamedTemporaryFile() as tmp_file:
      tmp_file_path = tmp_file.name
    cli_util.copy_file_like_object_to_file(
      StringIO.StringIO(msg_str), tmp_file_path
    )
    with open(tmp_file_path, 'r') as tmp_file:
      self.assertEqual(msg_str, tmp_file.read())

  def test_0160(self):
    """copy_file_like_object_to_file(): Raises InvalidArguments if path is invalid"""
    msg_str = 'line1\nline2\n'
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.CLIError,
      cli_util.copy_file_like_object_to_file, msg_str, '/'
    )

  # copy_requests_stream_to_file()

  @responses.activate
  def test_0170(self):
    """copy_requests_stream_to_file(): Copies Requests Response body to file when path is valid"""
    responses_base_url = 'http://responses/mn'
    mock_get.add_callback(responses_base_url)
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(responses_base_url)
    response = client.get('test_pid_1')
    with tempfile.NamedTemporaryFile() as tmp_file:
      cli_util.copy_requests_stream_to_file(response, tmp_file.name)
      expected_sciobj_str = client.get('test_pid_1').content
      self.assertEqual(len(expected_sciobj_str), 258)
      self.assertEqual(expected_sciobj_str, tmp_file.read())

  @responses.activate
  def test_0171(self):
    """copy_requests_stream_to_file(): Raises InvalidArguments if path is invalid"""
    responses_base_url = 'http://responses/mn'
    mock_get.add_callback(responses_base_url)
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(responses_base_url)
    response = client.get('test_pid_1')
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.CLIError,
      cli_util.copy_requests_stream_to_file, response, '/an/invalid/path'
    )

  # print()

  def test_0180(self):
    """print()"""
    with d1_test.util.capture_std() as (out_stream, err_stream):
      msg = 'test_msg'
      cli_util.print_debug(msg)
      cli_util.print_error(msg)
      cli_util.print_warn(msg)
      cli_util.print_info(msg)
    self.assertEquals(
      'DEBUG    test_msg\n'
      'ERROR    test_msg\n'
      'WARN     test_msg\n'
      '         test_msg\n',
      out_stream.getvalue(),
    )
