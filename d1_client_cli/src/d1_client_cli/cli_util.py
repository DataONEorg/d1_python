#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`cli_util`
===============

:Synopsis: Utilities shared between components of the DataONE Command Line
  Interface
:Created: 2012-03-07
:Author: DataONE (Dahl)
'''

# Stdlib.
import os
import shutil
import string
from string import strip
import sys
import traceback
import urlparse

# DataONE
# common
try:
  import d1_common.const
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_common.\n')
  raise

# client
import cli_exceptions
from const import CHECKSUM_sect, CHECKSUM_name
from print_level import * #@UnusedWildImport


def _handle_unexpected_exception(max_traceback_levels=5):
  exc_type, exc_msgs = sys.exc_info()[:2] # ignore the traceback.
  #
  if exc_type.__name__ == 'SSLError':
    print_error('There was a problem with SSL, did you update your key?')
  elif exc_type.__name__ == 'MissingSysmetaParameters':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'InvalidArguments':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'NotFound':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'ServiceFailure':
    print_error(
      'There was a problem with the response from the DataONE node. (error %d:%d)' %
      (exc_msgs.__dict__['errorCode'], exc_msgs.__dict__['detailCode'])
    )
  else:
    _print_unexpected_exception(max_traceback_levels)


def _print_unexpected_exception(max_traceback_levels=5):
  exc_class, exc_msgs, exc_traceback = sys.exc_info()
  print_error(u'Unexpected error:')
  print_error(u'  Name: {0}'.format(exc_class.__name__))
  print_error(u'  Value: {0}'.format(exc_msgs))
  try:
    exc_args = exc_msgs.__dict__["args"]
  except KeyError:
    exc_args = "<no args>"
  print_error('  Args: {0}'.format(exc_args))
  print_error('  Traceback:')
  for tb in traceback.format_tb(exc_traceback, max_traceback_levels):
    print_error('    {0}'.format(tb))


def _expand_path(filename):
  if filename:
    return os.path.expanduser(filename)
  return None


def get_host(url):
  '''Get the host component without the port number.
  '''
  url_dict = urlparse.urlparse(url)
  if url_dict.netloc is not None:
    host = url_dict.netloc
    ndx = host.find(":")
    if ndx > 0:
      host = host[:ndx]
    return host


def get_mn_url_from_host(host):
  return ''.join(
    (
      d1_common.const.DEFAULT_MN_PROTOCOL, '://', host, d1_common.const.DEFAULT_MN_PATH
    )
  )


def get_cn_url_from_host(host):
  return ''.join(
    (
      d1_common.const.DEFAULT_CN_PROTOCOL, '://', host, d1_common.const.DEFAULT_CN_PATH
    )
  )


def clear_None_from_list(obj_list):
  result_list = []
  for q in obj_list:
    if q is not None:
      result_list.append(q)
    else:
      break
  return result_list


def confirm(prompt, default='no', allow_blank=False):
  def_response = None
  if default == 'no':
    p = ' [yes,NO] '
    def_response = False
  elif default == 'yes':
    p = ' [YES,no] '
    def_response = True
  else:
    default = ''
    p = ''
    def_response = None

  while True:
    response = None
    try:
      response = raw_input(prompt + p)
    except KeyboardInterrupt as e:
      pass

    if ((response is None) or (len(response) == 0)):
      response = string.lower(default)
    else:
      response = string.lower(response)

    if response == 'yes':
      return True
    elif response == 'no':
      return False
    elif allow_blank:
      return def_response
    else:
      print_warn('Answer must be "yes" or "no" (or nothing)')


def output(file_like_object, path, verbose=False):
  '''Display or save file like object'''
  if not path:
    for line in file_like_object:
      if verbose:
        print_info(line.rstrip())
      else:
        print line.rstrip()
  else:
    try:
      object_file = open(_expand_path(path), 'wb')
      shutil.copyfileobj(file_like_object, object_file)
      object_file.close()
    except EnvironmentError as (errno, strerror):
      error_message_lines = []
      error_message_lines.append('Could not write to object_file: {0}'.format(path))
      error_message_lines.append('I/O error({0}): {1}'.format(errno, strerror))
      error_message = '\n'.join(error_message_lines)
      raise cli_exceptions.CLIError(error_message)


def get_file_size(self, path):
  with open(_expand_path(path), 'r') as f:
    f.seek(0, os.SEEK_END)
    size = f.tell()
  return size


def get_file_checksum(self, path, algorithm='SHA-1', block_size=1024 * 1024):
  h = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
  with open(_expand_path(path), 'r') as f:
    while True:
      data = f.read(block_size)
      if not data:
        break
      h.update(data)
  return h.hexdigest()


def assert_file_exists(self, path):
  if not os.path.isfile(_expand_path(path)):
    msg = 'Invalid file: {0}'.format(path)
    raise cli_exceptions.InvalidArguments(msg)


def create_sysmeta(session, pid, path, formatId=None):
  ''' Create a system meta data object.
  '''
  if session is None:
    raise cli_exceptions.InvalidArguments('Missing session')
  if pid is None:
    raise cli_exceptions.InvalidArguments('Missing pid')
  if path is None:
    raise cli_exceptions.InvalidArguments('Missing filename')
  algorithm = session.get(CHECKSUM_sect, CHECKSUM_name)
  if algorithm is None:
    raise cli_exceptions.InvalidArguments('Checksum algorithm is not defined.')

  path = _expand_path(path)
  checksum = get_file_checksum(path, algorithm)
  size = get_file_size(path)
  return session.create_system_metadata(pid, checksum, size, formatId)


def create_complex_path(path):
  return ComplexPath(path)


class ComplexPath(object):
  def __init__(self, path):
    self.path = None
    self.formatId = None
    #
    if not path:
      return
    parts = string.split(strip(path), ';')
    for part in parts:
      keyval = string.split(part, '=', 1)
      if len(keyval) == 1:
        path = keyval[0]
      else:
        key = strip(keyval[0]).lower()
        if key == 'formatid' or key == 'format-id':
          self.formatId = strip(keyval[1])
        else:
          print_warn('Unknown keyword: "%s"' % strip(keyval[0]))
