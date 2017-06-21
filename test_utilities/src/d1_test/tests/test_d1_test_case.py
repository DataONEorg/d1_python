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
from __future__ import print_function

import logging

import d1_test.d1_test_case


class TestTestUtils(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """capture_output():"""
    expected_output_str = 'test_output'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      print(expected_output_str, end='')
    received_output_str = out_stream.getvalue()
    assert expected_output_str == received_output_str

  def test_1010(self):
    """capture_log():"""
    expected_log_str = 'test_log'
    with d1_test.d1_test_case.capture_log() as log_stream:
      logging.error(expected_log_str)
    received_log_str = log_stream.getvalue()
    assert expected_log_str + '\n' == received_log_str

  def test_1020(self):
    """mock_raw_input():"""
    expected_prompt_str = 'user prompt'
    expected_answer_str = 'user answer'
    with d1_test.d1_test_case.capture_std() as (out_stream, err_stream):
      with d1_test.d1_test_case.mock_raw_input(expected_answer_str):
        received_answer_str = raw_input(expected_prompt_str)
    received_prompt_str = out_stream.getvalue()
    assert expected_prompt_str == received_prompt_str
    assert expected_answer_str == received_answer_str
