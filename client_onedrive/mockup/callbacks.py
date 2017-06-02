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
"""FUSE callback handlers.
"""

import os
import stat
import time
import errno
import datetime

import fs
import fuse


def dbg(func):
  def debug_print(*args, **kwargs):
    #logging.debug('DBG CALL: {0}({1} {2})'.format(func.__name__, args, kwargs))
    fun = func(*args, **kwargs)
    #logging.debug('DBG RET: {0}: {1}'.format(func.__name__, fun))
    return fun

  return debug_print


class FUSECallbacks(fuse.Operations):
  def __init__(self):
    self.start_time = datetime.datetime.now() # time.time()
    self.fs = self._flatten(fs.fs)
    self.file_paths = set([p[0] for p in self.fs])

    print 'Generated files: {0}'.format(len(self.fs))

  # noinspection PyMethodOverriding
  @dbg
  def getattr(self, path, fh):
    """Called by FUSE when the attributes for a file or directory are required.

    Returns a dictionary with keys identical to the stat C structure of stat(2).
    st_atime, st_mtime and st_ctime should be floats. On OSX, st_nlink should
    count all files inside the directory. On Linux, only the subdirectories are
    counted. The 'st_dev' and 'st_blksize' fields are ignored. The 'st_ino'
    field is ignored except if the 'use_ino' mount option is given.

    This method gets very heavy traffic.
    """
    path = self._mk_relative(path)

    if self._is_dir(path):
      size, dt = self._get_meta_dir(path)
      return self._mk_stat(size, date_time=dt, is_dir=True)
    if self._is_file(path):
      size, dt = self._get_meta_file(path)
      return self._mk_stat(size, date_time=dt, is_dir=False)
    raise OSError(errno.ENOENT, '')

  @dbg
  def readdir(self, path, fh):
    """Called by FUSE when a directory is opened.
    Returns a list of file and directory names for the directory.
    """
    path = self._mk_relative(path)
    c = self._get_direct_children(path)
    if not len(c):
      raise OSError(errno.ENOENT, '')
    return c

  def open(self, path, flags):
    raise OSError(errno.ENOENT)

  def read(self, path, size, offset, fh):
    raise OSError(errno.ENOENT)

  def _mk_stat(self, size, date_time=None, is_dir=False):
    if date_time is None:
      date_time = self.start_time

    seconds_since_epoch = time.mktime(date_time.timetuple())

    #date_time = time.mktime(date_time.timetuple()) + date_time.microsecond / 1000000.0
    #date_time = int(time.time(date_time))

    return dict(
      st_mode=stat.S_IFDIR | 0555 if is_dir else stat.S_IFREG | 0444,
      st_ino=0,
      st_dev=0,
      st_nlink=2,
      st_uid=0, # self.uid,
      st_gid=0, # self.gid,
      st_size=size,
      st_atime=seconds_since_epoch,
      st_mtime=seconds_since_epoch,
      st_ctime=seconds_since_epoch,
    )

  #@dbg
  #def _get_direct_children(self, path):
  #  a = self._get_all_children(path)
  #  c = set()
  #  for aa in a:
  #    if self._is_direct_child(path, aa[0]):
  #      c.add(aa)
  #  return sorted(list(c))

  @dbg
  def _get_direct_children(self, path):
    a = self._get_all_children(path)
    n = self._count_path_elements(path)
    c = set()
    for aa in a:
      c.add(self._get_path_element(aa[0], n))
    return sorted(list(c))

  @dbg
  def _get_all_children(self, path):
    c = []
    for p in self.fs:
      if p[0].startswith(path):
        c.append(p)
    return c

  @dbg
  def _count_path_elements(self, path):
    if path == '':
      return 0
    return path.count('/') + 1

  @dbg
  def _get_paths(self, d):
    return [v[0] for v in d]

  @dbg
  def _get_first_path_elements(self, path, n):
    return '/'.join(path.split('/')[:n])

  @dbg
  def _get_path_element(self, path, n):
    return path.split('/')[n]

  @dbg
  def _get_meta(self, path):
    if self._is_dir(path):
      return self._get_meta_dir(path)
    else:
      return self._get_meta_file(path)

  @dbg
  def _get_meta_dir(self, path):
    self._get_direct_children(path)
    size = 0
    date = datetime.datetime.now()
    #for f in c:
    #  print f
    #  size += f[1]
    #  date = f[2]
    return size, date

  @dbg
  def _get_meta_file(self, path):
    for p in self.fs:
      if p[0] == path:
        return p[1], p[2]

  @dbg
  def _is_dir(self, path):
    if path == '':
      return True
    for p in self.fs:
      if (
        p[0].startswith(path) and (
          self._count_path_elements(p[0]) > self._count_path_elements(path)
        )
      ): # yapf: disable
        return True
    return False

  @dbg
  def _is_file(self, path):
    return path in self.file_paths

  @dbg
  def _is_direct_child(self, base, child):
    return child.startswith(base) and self._count_path_elements(
      child
    ) == self._count_path_elements(base) + 1

  @dbg
  def _mk_relative(self, path):
    assert (path[0] == '/')
    return path[1:]

  def _flatten(self, filesys):
    paths = []
    self._flatten_r(paths, '', filesys)
    return sorted(paths)

  def _flatten_r(self, paths, p, filesys):
    for v in filesys:
      try:
        iter(v[1])
      except TypeError:
        paths.append((os.path.join(p, v[0]), v[1], v[2]))
      else:
        self._flatten_r(paths, os.path.join(p, v[0]), v[1])


if __name__ == '__main__':
  f = FUSECallbacks()
