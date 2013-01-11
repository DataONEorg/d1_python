#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`resolver.d1_object`
============================

:Synopsis:
 - Determine what type of DataONE object a given PID references and branch out
   to a resolver that is specialized for that type.

:Author: DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys

# D1.
import d1_client.data_package
import d1_client.object_format_info

# App.
#sys.path.append('.')
from impl import attributes
from impl import cache
from impl import command_processor
from impl import directory
from impl import directory_item
from impl import facet_path_formatter
from impl import facet_path_parser
from impl import path_exception
from . import resolver_abc
from impl import settings
from impl import util

# Set up logger for this module.
log = logging.getLogger(__name__)


class Resolver(resolver_abc.Resolver):
  def __init__(self):
    self.command_processor = command_processor.CommandProcessor()
    self.object_format_info = d1_client.object_format_info.ObjectFormatInfo()

  def get_attributes(self, path):
    log.debug('get_attributes: {0}'.format(util.string_from_path_elements(path)))

    return self._get_attribute(path)

  def get_directory(self, path):
    log.debug('get_directory: {0}'.format(util.string_from_path_elements(path)))

    return self._get_directory(path)

  def read_file(self, path, size, offset):
    log.debug(
      'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )

    return self._read_file(path, size, offset)

  # Private.

  def _get_attribute(self, path):
    # d1_object handles two levels:
    # /pid
    # /pid/pid.ext
    # /pid/system.xml

    # The parent resolver must not strip the PID off the path.
    assert (len(path))

    pid = path[0]

    description = self.command_processor.get_object_info_through_cache(pid)

    # This resolver does not call out to any other resolves. Any path that
    # is deeper than two levels, and any path that is one level, but does
    # not reference "pid.ext" or "system.xml" is invalid.

    if len(path) == 1:
      return attributes.Attributes(
        is_dir=True, size=description['size'],
        date=description['date']
      )

    if len(path) == 2:
      if path[1] == self._get_pid_filename(pid, description):
        return attributes.Attributes(size=description['size'], date=description['date'])

      if path[1] == 'system.xml':
        sys_meta_xml = self.command_processor.get_system_metadata_through_cache(pid)[1]
        return attributes.Attributes(size=len(sys_meta_xml), date=description['date'])

    self._raise_invalid_path()

  def _get_directory(self, path):
    pid = path[0]
    description = self.command_processor.get_object_info_through_cache(pid)
    return [
      directory_item.DirectoryItem(self._get_pid_filename(pid, description)),
      directory_item.DirectoryItem('system.xml'),
    ]

  def _read_file(self, path, size, offset):
    pid = path[0]
    filename = path[1]

    if filename == 'system.xml':
      sys_meta_xml = self.command_processor.get_system_metadata_through_cache(pid)[1]
      return sys_meta_xml[offset:offset + size]

    description = self.command_processor.get_object_info_through_cache(pid)

    if filename == self._get_pid_filename(pid, description):
      sci_obj = self.command_processor.get_science_object_through_cache(pid)
      return sci_obj[offset:offset + size]

    self._raise_invalid_path()

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException('Invalid PID: {0}'.format(pid))

  def _raise_invalid_path(self):
    raise path_exception.PathException('Invalid path')

  def _get_pid_filename(self, pid, description):
    return pid + self.object_format_info.filename_extension_from_format_id(
      description['format_id']
    )
