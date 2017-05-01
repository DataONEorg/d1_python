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
"""Utilities for unit- and integration tests"""

import StringIO
import contextlib
import logging
import sys

import mock


@contextlib.contextmanager
def capture_std():
  new_out, new_err = StringIO.StringIO(), StringIO.StringIO()
  old_out, old_err = sys.stdout, sys.stderr
  try:
    sys.stdout, sys.stderr = new_out, new_err
    yield sys.stdout, sys.stderr
  finally:
    sys.stdout, sys.stderr = old_out, old_err


@contextlib.contextmanager
def capture_log():
  stream = StringIO.StringIO()
  try:
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    stream_handler = logging.StreamHandler(stream)
    logger.addHandler(stream_handler)
    yield stream
  finally:
    logger.removeHandler(stream_handler)


@contextlib.contextmanager
def mock_raw_input(answer_str):
  with mock.patch(
      '__builtin__.raw_input',
      side_effect=_mock_raw_input_side_effect,
      return_value=answer_str,
  ):
    yield


def _mock_raw_input_side_effect(prompt_str):
  sys.stdout.write(prompt_str)
  return mock.DEFAULT
