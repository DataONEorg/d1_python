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
import d1_workspace.workspace_exception

# App.
from d1_client_onedrive.impl import attributes
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import directory
from d1_client_onedrive.impl import directory_item
from d1_client_onedrive.impl import path_exception
from d1_client_onedrive.impl import util
import resolver_base

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Resolver(resolver_base.Resolver):
  def __init__(self, options, workspace):
    super(Resolver, self).__init__(options, workspace)

    self.object_format_info = d1_client.object_format_info.ObjectFormatInfo(
      csv_file=pkg_resources.resource_stream(d1_client.__name__, 'mime_mappings.csv')
    )

  def get_attributes(self, workspace_root, path):
    log.debug(u'get_attributes: {0}'.format(util.string_from_path_elements(path)))
    return self._get_attributes(workspace_root, path)

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
    return self._read_file(workspace_root, path, size, offset)

  # Private.

  def _get_attributes(self, workspace_root, path):
    # d1_object handles two levels:
    # /pid
    # /pid/pid.ext
    # /pid/system.xml
    # /pid/search_fields.txt

    # The parent resolver must not strip the PID off the path.
    assert (len(path))

    pid = path[0]

    try:
      record = self._workspace.get_object_record(pid)
    except d1_workspace.workspace_exception.WorkspaceException:
      self._raise_invalid_path()

    # This resolver does not call out to any other resolvers.

    # Any path that is deeper than two levels, and any path that is one level,
    # but does not reference one of the fixed filenames is invalid.

    # Any path that is 1 level is a pid folder. We return the size of the
    # science object as the size of this folder. This is only indicative of the
    # actual size of the folder since the folder contains other objects as well.
    # But the filesystem drivers and clients do not seem to mind. On Linux, the
    # size of a folder is rarely taken into account since it indicates the
    # amount of disk space used for storing the folder record (an entirely
    # filesystem dependent size).
    if len(path) == 1:
      return attributes.Attributes(
        is_dir=True, size=record['size'],
        date=record['dateUploaded']
      )
    elif len(path) == 2:
      filename = path[1]
      if filename == self._get_search_fields_filename():
        return self._get_search_fields_file_attributes(record)
      elif filename == self._get_pid_filename(pid, record):
        return attributes.Attributes(size=record['size'], date=record['dateUploaded'])
      elif filename == u"system.xml":
        sys_meta_xml = self._workspace.get_system_metadata(pid)
        return attributes.Attributes(size=len(sys_meta_xml), date=record['dateUploaded'])

    self._raise_invalid_path()

  def _get_directory(self, workspace_root, path):
    #if len(path) > 1:
    #  self._raise_invalid_path()
    pid = path[0]
    record = self._workspace.get_object_record(pid)
    return [
      self._make_directory_item_for_solr_record(record),
      directory_item.DirectoryItem(u"system.xml"),
      directory_item.DirectoryItem(self._get_search_fields_filename(),
                                   is_dir=False)
    ]

  def _make_directory_item_for_solr_record(self, record):
    return directory_item.DirectoryItem(
      self._get_pid_filename(record['id'], record), record['size']
    )

  def _read_file(self, workspace_root, path, size, offset):
    pid, filename = path[0:2]

    if filename == u"system.xml":
      sys_meta_xml = self._workspace.get_system_metadata(pid)
      return sys_meta_xml[offset:offset + size]

    record = self._workspace.get_object_record(pid)

    if filename == self._get_pid_filename(pid, record):
      sci_obj = self._workspace.get_science_object(pid)
      return sci_obj[offset:offset + size]

    elif filename == self._get_search_fields_filename():
      return self._generate_search_fields_text(record)[offset:offset + size]

    self._raise_invalid_path()

  def _raise_invalid_pid(self, pid):
    raise path_exception.PathException(u'Invalid PID: {0}'.format(pid))

  def _raise_invalid_path(self):
    raise path_exception.PathException(u'Invalid path')

  def _get_pid_filename(self, pid, record):
    try:
      ext = self.object_format_info.filename_extension_from_format_id(record['formatId'])
    except KeyError:
      return pid
    if ext == os.path.splitext(pid)[1]:
      return pid
    else:
      return pid + ext

  # Search fields.

  def _get_search_fields_filename(self):
    return 'search_fields.txt'

  def _get_search_fields_file_attributes(self, record):
    return attributes.Attributes(
      size=len(self._generate_search_fields_text(record)),
      is_dir=False
    )

  def _generate_search_fields_text(self, record):
    return util.os_format(
      '\n'.join(
        sorted([u'{0}: {1}'.format(k, v) for k, v in record.items()])
      )
    )
