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
"""Handle callbacks from FUSE

The callbacks are called by FUSE when actions are performed on the filesystem.
"""

import errno
import logging
import os
import stat
import time

import d1_onedrive.impl
# App
import d1_onedrive.impl.onedrive_exceptions
import fuse

import d1_common.date_time

# 3rd party

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class FUSECallbacks(fuse.Operations):
  def __init__(self, options, root_resolver):
    self._options = options
    self._READ_ONLY_ACCESS_MODE = 3
    self._root_resolver = root_resolver
    self._start_time = time.time()
    self._gid = os.getgid()
    self._uid = os.getuid()
    self._attribute_cache = d1_onedrive.impl.cache_memory.Cache(
      self._options.attribute_max_cache_items
    )
    self._directory_cache = d1_onedrive.impl.cache_memory.Cache(
      self._options.directory_max_cache_items
    )

  def getattr(self, path, fh):
    """Called by FUSE when the attributes for a file or directory are required.

    Returns a dictionary with keys identical to the stat C structure of stat(2).
    st_atime, st_mtime and st_ctime should be floats. On OSX, st_nlink should
    count all files inside the directory. On Linux, only the subdirectories are
    counted. The 'st_dev' and 'st_blksize' fields are ignored. The 'st_ino'
    field is ignored except if the 'use_ino' mount option is given.

    This method gets very heavy traffic.
    """
    self._raise_error_if_os_special_file(path)
    #log.debug(u'getattr(): {0}'.format(path))
    attribute = self._get_attributes_through_cache(path)
    #log.debug('getattr() returned attribute: {0}'.format(attribute))
    return self._stat_from_attributes(attribute)

  def readdir(self, path, fh):
    """Called by FUSE when a directory is opened.
    Returns a list of file and directory names for the directory.
    """
    log.debug('readdir(): {}'.format(path))
    try:
      dir = self._directory_cache[path]
    except KeyError:
      dir = self._get_directory(path)
      self._directory_cache[path] = dir
    return dir

  def open(self, path, flags):
    """Called by FUSE when a file is opened.
    Determines if the provided path and open flags are valid.
    """
    log.debug('open(): {}'.format(path))
    # ONEDrive is currently read only. Anything but read access is denied.
    if (flags & self._READ_ONLY_ACCESS_MODE) != os.O_RDONLY:
      self._raise_error_permission_denied(path)
    # Any file in the filesystem can be opened.
    attribute = self._get_attributes_through_cache(path)
    return attribute.is_dir()

  def read(self, path, size, offset, fh):
    log.debug('read(): {}'.format(path))
    try:
      return self._root_resolver.read_file(path, size, offset)
    except d1_onedrive.impl.onedrive_exceptions.PathException:
      self._raise_error_no_such_file_or_directory(path)

  # Private.

  def _get_directory(self, path):
    try:
      d = self._root_resolver.get_directory(path)
      d.append('.')
      d.append('..')
      return d
    except d1_onedrive.impl.onedrive_exceptions.PathException:
      self._raise_error_no_such_file_or_directory(path)

  def _get_attributes_through_cache(self, path):
    try:
      return self._attribute_cache[path]
    except KeyError:
      attributes = self._get_attributes(path)
      self._attribute_cache[path] = attributes
      return attributes

  def _get_attributes(self, path):
    try:
      return self._root_resolver.get_attributes(path)
    except d1_onedrive.impl.onedrive_exceptions.PathException:
      self._raise_error_no_such_file_or_directory(path)

  def _stat_from_attributes(self, attributes):
    date_time = d1_common.date_time.ts_from_dt(
      attributes.date()
    ) if attributes.date() is not None else self._start_time
    return dict(
      st_mode=stat.S_IFDIR | 0o555 if attributes.is_dir() else stat.S_IFREG | 0o444,
      st_ino=0,
      st_dev=0,
      st_nlink=2, # TODO
      st_uid=self._uid,
      st_gid=self._gid,
      st_size=attributes.size(),
      st_atime=date_time,
      st_mtime=date_time,
      st_ctime=date_time,
    )

  def _raise_error_if_os_special_file(self, path):
    if len(set(path.split(os.path.sep)) & self._options.ignore_special):
      self._raise_error_no_such_file_or_directory(path)

  def _raise_error_no_such_file_or_directory(self, path):
    log.debug('Error: No such file or directory: {}'.format(path))
    raise fuse.FuseOSError(errno.ENOENT)

  def _raise_error_permission_denied(self, path):
    log.debug('Error: Permission denied: {}'.format(path))
    raise fuse.FuseOSError(errno.EACCES)
