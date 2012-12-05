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
sys.path.append('.')
import attributes
import cache
import command_processor
import directory
import directory_item
import facet_path_formatter
import facet_path_parser
import path_exception
import resolver_abc
import settings
import util

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

  # Private.

  def _get_attribute(self, path):
    # d1_object handles two levels. The first level is a folder named after the
    # pid. The second level is files for the data and system metadata.

    if len(path) > 2:
      self._raise_invalid_path()

    description = self._get_description(path[0])

    if len(path) == 1:
      return attributes.Attributes(
        is_dir=True,
        size=description['Content-Length'],
        date=description['last-modified']
      )

    #root, ext = os.path.splitext(path[1])

    if path[1] == 'system.xml':
      return attributes.Attributes(date=description['last-modified'])

    return attributes.Attributes(
      size=description['Content-Length'],
      date=description['last-modified']
    )

  def _get_directory(self, path):
    description = self._get_description(path[0])
    dir = []
    ext = self.object_format_info.filename_extension_from_format_id(
      description['dataone-objectformat']
    )
    dir.append(directory_item.DirectoryItem(path[0] + ext))

    dir.append(directory_item.DirectoryItem('system.xml'))

    return dir

  def _get_description(self, pid):
    try:
      return self.command_processor.get_and_cache_description(pid)
    except:
      self._raise_invalid_pid(pid)

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException('Invalid PID: {0}'.format(pid))

  def _raise_invalid_path(self):
    raise path_exception.PathException('Invalid path')
