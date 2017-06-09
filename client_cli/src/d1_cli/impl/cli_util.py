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
"""Utilities shared between components of the DataONE Command Line
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import string
import sys

import d1_cli.impl.cli_exceptions as cli_exceptions


def confirm(prompt, default=u'no', allow_blank=False):
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
    except (KeyboardInterrupt, EOFError):
      pass
    if (response is None) or (len(response) == 0):
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
      print_error(
        u'Please type, "yes", "no" or press Enter to select the default'
      )


def output(file_like_object, path, verbose=False):
  """Display or save file like object"""
  if not path:
    for line in file_like_object:
      if verbose:
        print_info(line.rstrip())
      else:
        print(line.rstrip())
  else:
    try:
      object_file = open(os.path.expanduser(path), u'wb')
      shutil.copyfileobj(file_like_object, object_file)
      object_file.close()
    except EnvironmentError as xxx_todo_changeme:
      (errno, strerror) = xxx_todo_changeme.args
      error_line_list = [
        u'Could not write to object_file: {}'.format(path),
        u'I/O error({}): {}'.format(errno, strerror),
      ]
      error_message = u'\n'.join(error_line_list)
      raise cli_exceptions.CLIError(error_message)


def assert_file_exists(path):
  if not os.path.isfile(os.path.expanduser(path)):
    msg = u'Invalid file: {}'.format(path)
    raise cli_exceptions.InvalidArguments(msg)


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

  except EnvironmentError as xxx_todo_changeme1:
    (errno, strerror) = xxx_todo_changeme1.args
    error_line_list = [
      u'Could not write to object_file: {}'.format(path),
      u'I/O error({}): {}'.format(errno, strerror),
    ]
    error_message = u'\n'.join(error_line_list)
    raise cli_exceptions.CLIError(error_message)


def copy_requests_stream_to_file(response, path):
  try:
    with open(os.path.expanduser(path), u'wb') as f:
      for chunk_str in response.iter_content():
        f.write(chunk_str)
  except EnvironmentError as xxx_todo_changeme2:
    (errno, strerror) = xxx_todo_changeme2.args
    error_line_list = [
      u'Could not write to object_file: {}'.format(path),
      u'I/O error({}): {}'.format(errno, strerror),
    ]
    error_message = u'\n'.join(error_line_list)
    raise cli_exceptions.CLIError(error_message)


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
  """Print the information in Unicode safe manner.
  """
  for l in unicode(msg.rstrip()).split(u'\n'):
    print(u'{0:<9s}{1}'.format(level, unicode(l)).encode(u'utf-8'))
