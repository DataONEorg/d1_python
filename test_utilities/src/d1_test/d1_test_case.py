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
from __future__ import absolute_import

import codecs
import contextlib
import hashlib
import inspect
import json
import logging
import os
import random
import re
import StringIO
import subprocess
import sys
import tempfile
import traceback
import xml

import decorator
import mock
import pytest
import pyxb
import pyxb.binding.basis

import d1_common.const
import d1_common.types
import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes
import d1_common.util
import d1_common.xml

import d1_client.util

# Settings

CN_URL = d1_common.const.URL_DATAONE_ROOT

MOCK_BASE_URL = 'http://mock/node'
MOCK_REMOTE_BASE_URL = 'http://mock/remote'
MOCK_INVALID_BASE_URL = 'http://mock/invalid'

SOLR_QUERY_ENDPOINT = '/cn/v1/query/solr/'


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
  def _log(prompt_str):
    sys.stdout.write(prompt_str)
    return mock.DEFAULT

  with mock.patch(
      '__builtin__.raw_input',
      side_effect=_log,
      return_value=answer_str,
  ):
    yield


@contextlib.contextmanager
def ignore_exceptions(*exception_list):
  exception_list = exception_list or (Exception,)
  try:
    yield
  except exception_list:
    pass


# reproducible_random

# TODO: When we move to Py3, move this over to the simple wrapper supported
# there. For now, this works, and it's probably not worth simplifying it with
# any decorator/context/class/function/parameterized wrappers.


def reproducible_random_decorator(seed):
  def reproducible_random_decorator_real(cls_or_func):
    if inspect.isclass(cls_or_func):
      return _reproducible_random_class_decorator(cls_or_func, seed)
    elif callable(cls_or_func):
      return _reproducible_random_func_decorator(cls_or_func, seed)
    else:
      raise ValueError(
        'Decorated object must be a class or callable (function)'
      )

  return reproducible_random_decorator_real


def _reproducible_random_class_decorator(cls, seed):
  for test_name, test_func in cls.__dict__.items():
    if test_name.startswith('test_'):
      logging.debug(
        'Decorating: {}.{}: reproducible_random()'.
        format(cls.__name__, test_name)
      )
      setattr(
        cls, test_name, _reproducible_random_func_decorator(test_func, seed)
      )
  return cls


def _reproducible_random_func_decorator(func, seed):
  def wrapper(func2, *args, **kwargs):
    logging.debug(
      'Decorating: {}: reproducible_random()'.format(func2.__name__)
    )
    with reproducible_random_context(seed):
      return func2(*args, **kwargs)

  return decorator.decorator(wrapper, func)


@contextlib.contextmanager
def reproducible_random_context(seed):
  """Start the PRNG at a fixed seed"""
  state = random.getstate()
  random.seed(seed)
  yield
  random.setstate(state)


#


def generate_reproducible_sciobj_str(pid):
  """Return a science object byte string that is always the same for a given PID
  """
  # Ignore any decoration.
  pid = re.sub(r'^<.*?>', '', pid)
  pid_hash_int = int(hashlib.md5(pid.encode('utf-8')).hexdigest(), 16)
  with reproducible_random_context(pid_hash_int):
    return (
      'These are the reproducible Science Object bytes for pid="{}". '
      'What follows is 100 to 200 random bytes: '.format(pid.encode('utf-8')) +
      str(
        bytearray(
          random.getrandbits(8) for _ in range(random.randint(100, 200))
        )
      )
    )


def get_test_module_name():
  for module_path, line_num, func_name, line_str in traceback.extract_stack():
    module_name = os.path.splitext(os.path.split(module_path)[1])[0]
    if module_name.startswith('test_') and func_name.startswith('test_'):
      return module_name


def format_sample_file_name(client, name_postfix_str, extension_str):
  return '{}.{}'.format(
    '_'.join([
      get_test_module_name(),
      name_postfix_str,
      d1_client.util.get_client_type(client),
      d1_client.util.get_version_tag_by_d1_client(client),
    ]), extension_str
  )


#===============================================================================


class D1TestCase(object): # unittest.TestCase
  @staticmethod
  def get_sample_filepath(filename):
    return os.path.join(d1_common.util.abs_path('test_docs'), filename)

  @staticmethod
  def read_sample_file(filename, mode_str='rb'):
    with open(D1TestCase.get_sample_filepath(filename), mode_str) as f:
      return f.read()

  @staticmethod
  def read_utf8_to_unicode(filename):
    utf8_path = D1TestCase.get_sample_filepath(filename)
    unicode_file = codecs.open(utf8_path, encoding='utf-8', mode='r')
    return unicode_file.read()

  @staticmethod
  def read_xml_file_to_pyxb(filename, mode_str='r'):
    logging.debug('Reading sample XML file. filename="{}"'.format(filename))
    xml_str = D1TestCase.read_sample_file(filename, mode_str)
    return d1_common.types.dataoneTypes.CreateFromDocument(xml_str)

  @staticmethod
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

  @staticmethod
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

  @staticmethod
  def read_test_pyxb(filename, mode_str='r'):
    xml_str = D1TestCase.read_sample_file(filename, mode_str)
    return d1_common.types.dataoneTypes.CreateFromDocument(xml_str)

  @staticmethod
  def get_total_number_of_objects(client):
    object_list = client.listObjects(
      count=1
    ) # TODO: Should be count=0 but there's currently a bug in CN.
    return object_list.total

  @staticmethod
  def get_pid_by_index(client, idx):
    object_list = client.listObjects(start=idx, count=1)
    try:
      return object_list.objectInfo[0].identifier.value()
    except IndexError:
      raise Exception('No objects')

  @staticmethod
  def get_random_valid_pid(client):
    total = D1TestCase.get_total_number_of_objects(client)
    return D1TestCase.get_pid_by_index(client, random.randint(0, total - 1))

  @staticmethod
  def display_diff_pyxb(got_pyxb, exp_pyxb):
    return D1TestCase.display_diff_str(
      d1_common.xml.pretty_pyxb(got_pyxb),
      d1_common.xml.pretty_pyxb(exp_pyxb),
    )

  @staticmethod
  def display_diff_xml(got_xml, exp_xml):
    return D1TestCase.display_diff_str(
      d1_common.xml.pretty_xml(got_xml),
      d1_common.xml.pretty_xml(exp_xml),
    )

  @staticmethod
  def display_diff_str(got_str, exp_str):
    with tempfile.NamedTemporaryFile(prefix='GOT__', suffix='txt') as got_f:
      with tempfile.NamedTemporaryFile(prefix='EXP__', suffix='txt') as exp_f:
        got_f.write(got_str)
        exp_f.write(exp_str)
        got_f.seek(0)
        exp_f.seek(0)
        subprocess.call(['kdiff3', got_f.name, exp_f.name])

  @staticmethod
  def assert_equals_sample(
      got_obj, name_postfix_str, client, extension_str='sample'
  ):
    filename = format_sample_file_name(client, name_postfix_str, extension_str)
    logging.info('Using sample file. filename="{}"'.format(filename))
    got_str = D1TestCase.obj_to_pretty_str(got_obj)
    try:
      exp_str = D1TestCase.read_sample_file(filename)
    except EnvironmentError as e:
      logging.error(
        'Could not read sample file. filename="{}" error="{}"'.
        format(filename, str(e))
      )
      exp_str = ''

    try:
      assert got_str == exp_str
    except AssertionError:
      # noinspection PyUnresolvedReferences
      if not pytest.config.getoption("--update-samples"):
        raise
    else:
      return
    D1TestCase.write_sample_file_interactive(got_str, exp_str, filename)

  @staticmethod
  def write_sample_file_interactive(got_str, exp_str, filename):
    D1TestCase.display_diff_str(got_str, exp_str)
    answer_str = None
    while answer_str not in ('y', 'n'):
      answer_str = raw_input('Update sample file "{}"? [y/n] '.format(filename))
    if answer_str == 'y':
      D1TestCase.write_sample_file(filename, got_str)

  # noinspection PyUnreachableCode
  @staticmethod
  def obj_to_pretty_str(o):
    logging.debug('Serializing object. type="{}"'.format(type(o)))
    with ignore_exceptions():
      if isinstance(o, unicode):
        o = o.encode('utf-8')
    with ignore_exceptions():
      return d1_common.xml.pretty_xml(o)
    with ignore_exceptions():
      return d1_common.xml.pretty_pyxb(o)
    with ignore_exceptions():
      return '\n'.join(sorted(o.serialize(doc_format='nt').splitlines()))
    with ignore_exceptions():
      if 'digraph' in o:
        return '\n'.join(
          sorted(
            str(re.sub('node\d+', 'nodeX', o)).splitlines(),
          )
        )
    with ignore_exceptions():
      if '\n' in str(o):
        return str(o)
    with ignore_exceptions():
      return json.dumps(o, sort_keys=True, indent=2)
    with ignore_exceptions():
      return str(o)
    with ignore_exceptions():
      return repr(o)

  @staticmethod
  def write_sample_file(filename, obj_str, mode_str='wb'):
    logging.info('Writing sample file. filename="{}"'.format(filename))
    with open(D1TestCase.get_sample_filepath(filename), mode_str) as f:
      return f.write(obj_str)
