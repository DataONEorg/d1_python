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

import unittest

import d1_client_cli.impl.cli
import d1_client_cli.impl.cli_client
import d1_client_cli.impl.cli_exceptions
import d1_client_cli.impl.operation_validator
import d1_common.system_metadata
import d1_common.util
import d1_common.xml


class TestCLIExceptions(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    cli = d1_client_cli.impl.cli.CLI()
    cli.do_set('verbose true')

  def test_0010(self):
    """InvalidArguments(): Successfully instantiated and raised"""
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.InvalidArguments, lambda: self._raise(
        d1_client_cli.impl.cli_exceptions.InvalidArguments('test_message')
      )
    )

  def test_0020(self):
    """InvalidArguments(): Returns string"""
    msg_str = 'test_message'
    ex = d1_client_cli.impl.cli_exceptions.InvalidArguments(msg_str)
    self.assertEqual(msg_str, str(ex))

  def test_0030(self):
    """CLIError(): Successfully instantiated and raised"""
    self.assertRaises(
      d1_client_cli.impl.cli_exceptions.CLIError, lambda: self.
      _raise(d1_client_cli.impl.cli_exceptions.CLIError('test_message'))
    )

  def test_0040(self):
    """CLIError(): Returns string"""
    msg_str = 'test_message'
    ex = d1_client_cli.impl.cli_exceptions.CLIError(msg_str)
    self.assertEqual(msg_str, str(ex))

  def _raise(self, ex):
    raise ex
