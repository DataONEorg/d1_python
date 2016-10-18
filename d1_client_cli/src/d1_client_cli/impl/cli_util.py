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
import urlparse

# DataONE
import d1_common.const
import cli_exceptions


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


def clear_None_from_list(obj_list):
  result_list = []
  for q in obj_list:
    if q is not None:
      result_list.append(q)
    else:
      break
  return result_list


def confirm(prompt, default=u'no', allow_blank=False):
  def_response = None
  if default == u'no':
    p = u' [yes/NO] '
    def_response = False
  elif default == u'yes':
    p = u' [YES/no] '
    def_response = True
  else:
    default = u''
    p = u''
    def_response = None

  while True:
    response = None
    try:
      response = raw_input('{0:<9s}{1}{2}'.format('WARN', prompt, p))
    except (KeyboardInterrupt, EOFError) as e:
      pass
    if ((response is None) or (len(response) == 0)):
      response = string.lower(default)
    else:
      response = string.lower(response)
    if response == u'yes':
      return True
    elif response == u'no':
      return False
    elif allow_blank:
      return def_response
    else:
      print_error(u'Please type, "yes", "no" or press Enter to select the default')


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
      object_file = open(os.path.expanduser(path), u'wb')
      shutil.copyfileobj(file_like_object, object_file)
      object_file.close()
    except EnvironmentError as (errno, strerror):
      error_message_lines = []
      error_message_lines.append(u'Could not write to object_file: {0}'.format(path))
      error_message_lines.append(u'I/O error({0}): {1}'.format(errno, strerror))
      error_message = u'\n'.join(error_message_lines)
      raise cli_exceptions.CLIError(error_message)


def assert_file_exists(path):
  if not os.path.isfile(os.path.expanduser(path)):
    msg = u'Invalid file: {0}'.format(path)
    raise cli_exceptions.InvalidArguments(msg)

#def create_sys_meta(session, pid, path, formatId=None):
#  ''' Create a system meta data object.
#  '''
#  if session is None:
#    raise cli_exceptions.InvalidArguments(u'Missing session')
#  if pid is None:
#    raise cli_exceptions.InvalidArguments(u'Missing pid')
#  if path is None:
#    raise cli_exceptions.InvalidArguments(u'Missing filename')
#  algorithm = session.get(CHECKSUM_NAME)
#  if algorithm is None:
#    raise cli_exceptions.InvalidArguments(u'Checksum algorithm is not defined.')
#
#  path = os.path.expanduser(path)
#  checksum = get_file_checksum(path, algorithm)
#  size = get_file_size(path)
#  return session.create_system_metadata(pid, checksum, size, formatId)


def copy_file_like_object_to_file(file_like_object, path):
  try:
    fsrc = sys.stdin
    if file_like_object:
      fsrc = file_like_object

    if path:
      fdst = open(os.path.expanduser(path), u'wb')
      shutil.copyfileobj(fsrc, fdst)
      fdst.close()
    else:
      shutil.copyfileobj(fsrc, sys.stdout)

  except EnvironmentError as (errno, strerror):
    error_message_lines = []
    error_message_lines.append(u'Could not write to object_file: {0}'.format(path))
    error_message_lines.append(u'I/O error({0}): {1}'.format(errno, strerror))
    error_message = u'\n'.join(error_message_lines)
    raise cli_exceptions.CLIError(error_message)


def get_pid_from_url(url, action="object"):
  if url:
    ndx = url.find(u'/' + action + '/')
    if ndx != -1:
      return url[(ndx + 2 + len(action)):]
  return None


def create_complex_path(path):
  return ComplexPath(path)

# Print functions.


def print_debug(msg):
  _print_level(u'DEBUG', unicode(msg))


def print_error(msg):
  _print_level(u'ERROR', unicode(msg))


def print_warn(msg):
  _print_level(u'WARN', unicode(msg))


def print_info(msg):
  _print_level(u'', unicode(msg))


def _print_level(level, msg):
  '''Print the information in Unicode safe manner.
  '''
  for l in unicode(msg.rstrip()).split(u'\n'):
    print u'{0:<9s}{1}'.format(level, unicode(l)).encode(u'utf-8')

#===============================================================================


class ComplexPath(object):
  def __init__(self, path):
    self.path = None
    self.format_id = None
    #
    if not path:
      return
    parts = string.split(strip(path), u';')
    for part in parts:
      keyval = string.split(part, u'=', 1)
      if len(keyval) == 1:
        if keyval[0] != u'':
          self.path = keyval[0]
      else:
        key = strip(keyval[0]).lower()
        if key.find(u'format') == 0:
          self.format_id = strip(keyval[1])
        else:
          print_warn(u'Unknown keyword: "%s"' % strip(keyval[0]))
