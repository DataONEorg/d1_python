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
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import httplib
import logging
import os
import pprint
import sys
import pkg_resources

# D1.
import d1_client.data_package
import d1_client.object_format_info

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log.setLevel(logging.DEBUG)


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)

    self.object_format_info = d1_client.object_format_info.ObjectFormatInfo(
      csv_file=pkg_resources.resource_stream(d1_client.__name__, 'mime_mappings.csv')
    )

  def get_attributes(self, workspace_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))

    if self._is_readme_file(path):
      return self._get_readme_file_attributes()

    return self._get_attribute(workspace_root, path)

  def get_directory(self, workspace_root, path):
    log.debug(u'get_directory: {0}'.format(util.string_from_path_elements(path)))
    return self._get_directory(workspace_root, path)

  def read_file(self, workspace_root, path, size, offset):
    log.debug(
      u'read_file: {0}, {1}, {2}'.format(
        util.string_from_path_elements(
          path
        ), size, offset
      )
    )
    if self._is_readme_file(path):
      return self._get_readme_text(size, offset)
    return self._read_file(workspace_root, path, size, offset)

  # Private.

  def _get_attribute(self, workspace_root, path):
    # d1_object handles two levels:
    # /pid
    # /pid/pid.ext
    # /pid/system.xml

    # The parent resolver must not strip the PID off the path.
    assert (len(path))

    pid = path[0]

    record = self._workspace.get_object_record(pid)

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

      if path[1] == u"system.xml":
        sys_meta_xml = self._workspace.get_system_metadata(pid)
        return attributes.Attributes(size=len(sys_meta_xml), date=record['dateUploaded'])

    self._raise_invalid_path()

  def _get_directory(self, workspace_root, path):
    pid = path[0]
    record = self._workspace.get_object_record(pid)
    res = [
      self._make_directory_item_for_solr_record(record),
      directory_item.DirectoryItem(u"system.xml"),
    ]
    #if self._has_readme_entry(path):
    #  res.append(self.get_readme_directory_item())
    return res

  def _make_directory_item_for_solr_record(self, record):
    return directory_item.DirectoryItem(
      self._get_pid_filename(record['id'], record), record['size']
    )

  def _read_file(self, workspace_root, path, size, offset):
    pid = path[0]
    filename = path[1]

    if filename == u"system.xml":
      sys_meta_xml = self._workspace.get_system_metadata(pid)
      return sys_meta_xml[offset:offset + size]

    record = self._workspace.get_object_record(pid)

    if filename == self._get_pid_filename(pid, record):
      sci_obj = self._workspace.get_science_object(pid)
      return sci_obj[offset:offset + size]

    self._raise_invalid_path()

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException(u'Invalid PID: {0}'.format(pid))

  def _raise_invalid_path(self):
    raise path_exception.PathException(u'Invalid path')

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
