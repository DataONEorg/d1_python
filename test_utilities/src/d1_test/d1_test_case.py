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

import contextlib
import datetime
import hashlib
import inspect
import logging
import os
import random
import re
import string
import StringIO
import sys
import xml

import decorator
import mock
import pyxb
import pyxb.binding.basis

import d1_common.cert.x509
import d1_common.const
import d1_common.types
import d1_common.types.dataoneErrors
import d1_common.types.dataoneTypes
import d1_common.util
import d1_common.xml

import d1_test.instance_generator.system_metadata
import d1_test.sample

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


#===============================================================================


class D1TestCase(object):
  @property
  def sample(self):
    return d1_test.sample

  @staticmethod
  def deserialize_and_check(doc, raises_pyxb_exc=False):
    try:
      d1_common.types.dataoneTypes.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if raises_pyxb_exc:
        return
      else:
        raise
    if raises_pyxb_exc:
      raise Exception('Did not receive expected exception')

  @staticmethod
  def deserialize_exception_and_check(doc, raises_pyxb_exc=False):
    try:
      obj = d1_common.types.dataoneErrors.CreateFromDocument(doc)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if raises_pyxb_exc:
        return
      else:
        raise
    if raises_pyxb_exc:
      raise Exception('Did not receive expected exception')
    return obj

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
  def touch(module_path, times=None):
    with open(module_path, 'a'):
      os.utime(module_path, times)

  @staticmethod
  @contextlib.contextmanager
  def mock_ssl_download(cert_obj):
    """Simulate successful cert download by catching call to
    ssl.SSLSocket.getpeercert() and returning {cert_obj} in DER format.
    """
    cert_der = d1_common.cert.x509.get_cert_der(cert_obj)
    with mock.patch(
        'd1_common.cert.x509.ssl.SSLSocket.connect'
    ) as mock_connect:
      with mock.patch(
          'd1_common.cert.x509.ssl.SSLSocket.getpeercert'
      ) as mock_getpeercert:
        mock_getpeercert.return_value = cert_der
        yield mock_connect, mock_getpeercert

  def create_random_sciobj(self, client, pid=True, sid=True):
    pid = self.random_pid() if pid is True else pid
    sid = self.random_sid() if sid is True else sid
    options = {
      # 'rightsHolder': 'fixture_rights_holder_subj',
      'identifier': client.bindings.Identifier(pid) if pid else None,
      'seriesId': client.bindings.Identifier(sid) if sid else None,
    }
    sciobj_str = generate_reproducible_sciobj_str(pid)
    sysmeta_pyxb = (
      d1_test.instance_generator.system_metadata.generate_from_file(
        client, StringIO.StringIO(sciobj_str), options
      )
    )
    return pid, sid, sciobj_str, sysmeta_pyxb

  def get_pyxb_value(self, inst_pyxb, inst_attr):
    try:
      return unicode(getattr(inst_pyxb, inst_attr).value())
    except (ValueError, AttributeError):
      return None

  def now_str(self):
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

  def random_str(self, num_chars=10):
    return ''.join([
      random.choice(string.ascii_lowercase) for _ in range(num_chars)
    ])

  def random_id(self):
    return '{}_{}'.format(self.random_str(), self.now_str())

  def random_pid(self):
    return 'PID_{}'.format(self.random_id())

  def random_sid(self):
    return 'SID_{}'.format(self.random_id())

  def random_tag(self, tag_str):
    return '{}_{}'.format(tag_str, self.random_str())
