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

''':mod:`callbacks`
========================

:Synopsis:
 - Handle callbacks from FUSE. The callbacks are called by FUSE when actions
   are performed on the filesystem.
:Author: DataONE (Dahl)
'''

# Std.
import errno
import fuse
import logging
import os
import stat
import sys
import time
import urllib
import urlparse

# 3rd party.

# D1.
import d1_common.date_time

# App.
import directory
import directory_item
import cache
import root
import settings


# Set up logger for this module.
log = logging.getLogger(__name__)


class FUSECallbacks(fuse.Operations):
  def __init__(self):
    self.root = root.RootResolver()
    self.start_time = time.time()
    self.attribute_cache = cache.Cache(settings.MAX_ATTRIBUTE_CACHE_SIZE)
    self.directory_cache = cache.Cache(settings.MAX_DIRECTORY_CACHE_SIZE)


  def getattr(self, path, fh):
    '''Called by FUSE when the attributes for a file or directory are required.

    Returns a dictionary with keys identical to the stat C structure of stat(2).
    st_atime, st_mtime and st_ctime should be floats. On OSX, st_nlink should
    count all files inside the directory. On Linux, only the subdirectories are
    counted. The 'st_dev' and 'st_blksize' fields are ignored. The 'st_ino'
    field is ignored except if the 'use_ino' mount option is given.

    This method gets very heavy traffic.
    '''
    log.debug('getattr(): {0}'.format(path))
    try:
      attr = self.attribute_cache[path]
    except KeyError:
      attr = self.root.get_attributes(path)
      #self.attribute_cache[path] = attr //////////////////////////////////////// for debugging, disable cache
    log.debug('getattr() returned attribute: {0}'.format(attr))
    return self._stat_from_attributes(attr)
  

  def readdir(self, path, fh):
    '''Called by FUSE when a directory is opened.
    Returns a list of file and directory names for the directory.
    '''
    log.debug('readdir(): {0}'.format(path))
    try:
      dir = self.directory_cache[path]
    except KeyError:
      dir = self.root.get_directory(path)
      self.directory_cache[path] = dir
    return dir.names()
      

  def open(self, path, flags):
    '''Called by FUSE when a file is opened.
    Determines if the provided path and open flags are valid.
    '''
    log.debug('open(): {0}'.format(path))
    self._raise_error_no_such_file_or_directory(path)
#    split0 = os.path.split(path)
#    if split0[0] in ['/object', '/meta']:
#      if split0[1] not in self.objects.keys():
#    if (flags & O_ACCMODE) != os.O_RDONLY:
#      self._raise_error_permission_denied(path)
#    return 0

  
  def read(self, path, size, offset, fh):
    log.debug('read(): {0}'.format(path))
    self._raise_error_no_such_file_or_directory(path)


#  def _get_and_cache_directory(self, path):
#    #self.directory_cache.log_dump()
#    try:
#      directory, file_to_attributes_map = self.directory_cache[path]
#      log.debug('Found in cache: {0}'.format(path))
#    except KeyError:
#      log.debug('Not found in cache. {0}'.format(path))
#      directory = self.root.resolve(path)
#      file_to_attributes_map = self._create_file_to_attributes_map(directory)
#      self.directory_cache[path] = directory, file_to_attributes_map
#    return directory, file_to_attributes_map


#  def _create_file_to_attributes_map(self, directory):
#    return dict((d.name(), (d.size(), d.is_dir())) for d in directory)


  def _stat_from_attributes(self, attributes):
    date_time = d1_common.date_time.to_seconds_since_epoch(
      attributes.date()) if attributes.date() is not None else self.start_time 
    return dict(
      st_mode = stat.S_IFDIR | 0755 if attributes.is_dir() else \
        stat.S_IFREG | 0644,
      st_ino = 0,
      st_dev = 0,
      st_nlink = 2, # TODO
      st_uid = 0,
      st_gid = 0,
      st_size = attributes.size(),
      st_atime = date_time,
      st_mtime = date_time,
      st_ctime = date_time,
    )


  def _raise_error_no_such_file_or_directory(self, path):
    log.debug('Error: No such file or directory: {0}'.format(path))
    raise OSError(errno.ENOENT, '')


#  def _raise_error_permission_denied(self, path):
#    log.debug('Error: Permission denied: {0}'.format(path))
#    raise OSError(errno.EACCES, '')


  def _osx_special():
    for prefix in OSX_SPECIAL:
      if parts[len(parts)-1].startswith(prefix):
        self._raise_error_no_such_file_or_directory('todo')

