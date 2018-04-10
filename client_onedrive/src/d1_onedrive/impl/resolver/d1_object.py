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
"""Resolve a DataONE object

Determine what type of DataONE object a given PID references and branch out to a
resolver that is specialized for that type.
"""

import logging
import os

import pkg_resources

import d1_onedrive.impl.resolver.resolver_base
from d1_onedrive.impl import attributes
from d1_onedrive.impl import util

from .. import onedrive_exceptions

import d1_client.object_format_info

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class Resolver(d1_onedrive.impl.resolver.resolver_base.Resolver):
  def __init__(self, options, object_tree):
    super().__init__(options, object_tree)

    self._object_format_info = d1_client.object_format_info.ObjectFormatInfo(
      csv_file=open(
        pkg_resources.
        resource_filename(d1_client.__name__, 'mime_mappings.csv')
      )
    )

  def get_attributes(self, object_tree_root, path):
    log.debug('get_attributes: {}'.format(util.string_from_path_elements(path)))
    return self._get_attributes(object_tree_root, path)

  def get_directory(self, object_tree_root, path):
    log.debug('get_directory: {}'.format(util.string_from_path_elements(path)))
    return self._get_directory(object_tree_root, path)

  def read_file(self, object_tree_root, path, size, offset):
    log.debug(
      'read_file: {}, {}, {}'.
      format(util.string_from_path_elements(path), size, offset)
    )
    return self._read_file(object_tree_root, path, size, offset)

  # Private.

  def _get_attributes(self, object_tree_root, path):
    # d1_object handles two levels:
    # /pid
    # /pid/pid.ext
    # /pid/system.xml
    # /pid/search_fields.txt

    # The parent resolver must not strip the PID off the path.
    assert (len(path))

    pid = path[0]

    try:
      record = self._object_tree.get_object_record(pid)
    except onedrive_exceptions.ONEDriveException:
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
        is_dir=True, size=record['size'], date=record['dateUploaded']
      )
    elif len(path) == 2:
      filename = path[1]
      if filename == self._get_search_fields_filename():
        return self._get_search_fields_file_attributes(record)
      elif filename == self._get_pid_filename(pid, record):
        return attributes.Attributes(
          size=record['size'], date=record['dateUploaded']
        )
      elif filename == "system.xml":
        sys_meta_xml = self._object_tree.get_system_metadata(pid)
        return attributes.Attributes(
          size=len(sys_meta_xml), date=record['dateUploaded']
        )

    self._raise_invalid_path()

  def _get_directory(self, object_tree_root, path):
    #if len(path) > 1:
    #  self._raise_invalid_path()
    pid = path[0]
    record = self._object_tree.get_object_record(pid)
    return [
      self._get_pid_filename(record['id'], record),
      'system.xml',
      self._get_search_fields_filename(),
    ]

  def _read_file(self, object_tree_root, path, size, offset):
    pid, filename = path[0:2]

    if filename == "system.xml":
      sys_meta_xml = self._object_tree.get_system_metadata(pid)
      return sys_meta_xml[offset:offset + size]

    record = self._object_tree.get_object_record(pid)

    if filename == self._get_pid_filename(pid, record):
      sci_obj = self._object_tree.get_science_object(pid)
      return sci_obj[offset:offset + size]

    elif filename == self._get_search_fields_filename():
      return self._generate_search_fields_text(record)[offset:offset + size]

    self._raise_invalid_path()

  def _raise_invalid_pid(self, pid):
    raise onedrive_exceptions.PathException('Invalid PID: {}'.format(pid))

  def _raise_invalid_path(self):
    raise onedrive_exceptions.PathException('Invalid path')

  def _get_pid_filename(self, pid, record):
    try:
      ext = self._object_format_info.filename_extension_from_format_id(
        record['formatId']
      )
    except KeyError:
      return pid
    if ext in (os.path.splitext(pid)[1], 'data'):
      return pid
    else:
      return pid + ext

  # Search fields.

  def _get_search_fields_filename(self):
    return 'search_fields.txt'

  def _get_search_fields_file_attributes(self, record):
    return attributes.Attributes(
      size=len(self._generate_search_fields_text(record)), is_dir=False
    )

  def _generate_search_fields_text(self, record):
    return util.os_format(
      '\n'.
      join(sorted(['{}: {}'.format(k, v) for k, v in list(record.items())]))
    )
