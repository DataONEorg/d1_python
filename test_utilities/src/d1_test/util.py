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
import codecs
import contextlib
import logging
import os
import random
import subprocess
import sys
import tempfile
import xml

import d1_common.types
import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.util
import d1_common.xml
import mock
import pyxb


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
  logger = None
  stream_handler = None
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


def get_test_filepath(filename):
  return os.path.join(d1_common.util.abs_path('test_docs'), filename)


def read_test_file(filename, mode_str='rb'):
  with open(get_test_filepath(filename), mode_str) as f:
    return f.read()


def write_test_file(filename, obj_str, mode_str='wb'):
  with open(get_test_filepath(filename), mode_str) as f:
    return f.write(obj_str)


def is_existing_file(filename):
  return os.path.exists(get_test_filepath(filename))


def read_utf8_to_unicode(filename):
  utf8_path = get_test_filepath(filename)
  unicode_file = codecs.open(utf8_path, encoding='utf-8', mode='r')
  return unicode_file.read()


def read_xml_file_to_pyxb(filename, mode_str='r'):
  xml_str = read_test_file(filename, mode_str)
  return v2.CreateFromDocument(xml_str)


def deserialize_and_check(doc, shouldfail=False):
  try:
    d1_common.types.dataoneTypes.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')


def deserialize_exception_and_check(doc, shouldfail=False):
  try:
    obj = d1_common.types.dataoneErrors.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')
  return obj


def read_test_pyxb(filename, mode_str='r'):
  xml_str = read_test_file(filename, mode_str)
  return d1_common.types.dataoneTypes.CreateFromDocument(xml_str)


def get_total_number_of_objects(client):
  object_list = client.listObjects(
    count=1
  ) # TODO: Should be count=0 but there's currently a bug in CN.
  return object_list.total


def get_pid_by_index(client, idx):
  object_list = client.listObjects(start=idx, count=1)
  try:
    return object_list.objectInfo[0].identifier.value()
  except IndexError:
    raise Exception('No objects')


def get_random_valid_pid(client):
  total = get_total_number_of_objects(client)
  return get_pid_by_index(client, random.randint(0, total - 1))


def kdiff_pyxb(a_pyxb, b_pyxb):
  return kdiff_str(
    d1_common.pyxb.pretty_pyxb(a_pyxb),
    d1_common.pyxb.pretty_pyxb(b_pyxb),
  )


def kdiff_xml(a_xml, b_xml):
  return kdiff_str(
    d1_common.xml.pretty_xml(a_xml),
    d1_common.xml.pretty_xml(b_xml),
  )


def kdiff_str(a_str, b_str):
  with tempfile.NamedTemporaryFile() as a_f:
    with tempfile.NamedTemporaryFile() as b_f:
      a_f.write(a_str)
      b_f.write(b_str)
      a_f.seek(0)
      b_f.seek(0)
      subprocess.call(['kdiff3', a_f.name, b_f.name])
