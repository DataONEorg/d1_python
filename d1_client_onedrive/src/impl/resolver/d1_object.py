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
from impl import cache_memory as cache
from impl import command_processor
from impl import directory
from impl import directory_item
from impl import path_exception
from . import resolver_abc
#from impl #import settings
from impl import util

# Set up logger for this module.
log = logging.getLogger(__name__)
try:
  if __name__ in logging.DEBUG_MODULES:
    __level = logging.getLevelName("DEBUG")
    log.setLevel(__level)
except:
  pass


class Resolver(resolver_abc.Resolver):
  def __init__(self, options, command_processor):
    self._options = options
    self.command_processor = command_processor
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

    record = self.command_processor.get_solr_record(pid)

    # This resolver does not call out to any other resolves. Any path that
    # is deeper than two levels, and any path that is one level, but does
    # not reference "pid.ext" or "system.xml" is invalid.

    if len(path) == 1:
      return attributes.Attributes(
        is_dir=True, size=record['size'],
        date=record['dateUploaded']
      )

    if len(path) == 2:
      if path[1] == self._get_pid_filename(pid, record):
        return attributes.Attributes(size=record['size'], date=record['dateUploaded'])

      if path[1] == 'system.xml':
        sys_meta_xml = self.command_processor.get_system_metadata_through_cache(pid)[1]
        return attributes.Attributes(size=len(sys_meta_xml), date=record['dateUploaded'])
      #DV
      #The subfolder "Packages" lists all the resource maps that reference the 
      #parent PID
      if path[1] == "Packages":
        #list package identifiers
        dirlen = 0
        if record.has_key("resourceMap"):
          dirlen += len(record['resourceMap'])

        return attributes.Attributes(
          is_dir=True, size=dirlen, date=record['dateUploaded']
        )
    self._raise_invalid_path()

  def _get_directory(self, path):
    pid = path[0]
    record = self.command_processor.get_solr_record(pid)
    res = [
      self._make_directory_item_for_solr_record(record),
      directory_item.DirectoryItem('system.xml'),
    ]
    #DV
    #if record.has_key("resourceMap"):
    #  res.append( directory_item.DirectoryItem("Packages") )
    return res

  def _make_directory_item_for_solr_record(self, record):
    return directory_item.DirectoryItem(
      self._get_pid_filename(record['id'], record), record['size']
    )

  def _read_file(self, path, size, offset):
    pid = path[0]
    filename = path[1]

    if filename == 'system.xml':
      sys_meta_xml = self.command_processor.get_system_metadata_through_cache(pid)[1]
      return sys_meta_xml[offset:offset + size]

    record = self.command_processor.get_solr_record(pid)

    if filename == self._get_pid_filename(pid, record):
      sci_obj = self.command_processor.get_science_object_through_cache(pid)
      return sci_obj[offset:offset + size]

    self._raise_invalid_path()

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException('Invalid PID: {0}'.format(pid))

  def _raise_invalid_path(self):
    raise path_exception.PathException('Invalid path')

  def _get_pid_filename(self, pid, record):
    lcpid = pid.lower()
    ENDINGS = {
      'DATA': ['.zip', '.csv', '.xls', '.xslx', '.xml', '.pdf'],
      'METADATA': ['.xml', ],
      'RESOURCE': ['.rdf', '.xml']
    }
    try:
      for ending in ENDINGS[record['formatType']]:
        if lcpid.endswith(ending):
          return pid
    except KeyError:
      pass
    return pid + self.object_format_info.filename_extension_from_format_id(
      record['formatId']
    )
