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
"""Create Dokan drive

Handle callbacks from Dokan.

The callbacks are called by Dokan when actions are performed on the filesystem.
"""

import errno
import fnmatch
import logging
import os
import time

import d1_onedrive.impl
import d1_onedrive.impl.drivers.dokan.const
import d1_onedrive.impl.drivers.dokan.dokan
import d1_onedrive.impl.onedrive_exceptions

import d1_common.const
import d1_common.date_time

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(
    logging.getLevelName(getattr(logging, 'ONEDRIVE_MODULES')[__name__])
  )
except KeyError:
  pass

THREADS = 5


def run(options, root_resolver):
  #NOTE: mounts anywhere other than root level don't work
  #UPDATE: this seems to be a Windows issue since you can only specify volume
  # properties for a drive not a volume mounted to a mountpoint
  #mountpoint = args[0]
  #directory = args[0]

  # set up Dokan
  #NOTE: DriverOption should either contain DOKAN_OPTION_REMOVABLE or
  # DOKAN_OPTION_NETWORK.  This will make the drive appear as a mounted drive
  # like it should.  There are a few problems with this though.  The network
  # approach gives an ugly icon in Windows Explorer and says that the drive is
  # disconnected.  The removable approach gives an error when I try to eject
  # the drive.  There may be solutions to both of these problems, but I
  # haven't figure it out yet.  I'm not sure what makes the most sense.
  #UPDATE: I was able to get rid of the ugly disconnected network icon in
  # a number of ways.  First, by editing the registry you can indicate an
  # icon that you want to be used for a particular drive letter.  Second,
  # I was able to register the network drive so that it appears connected.
  # There is a bug in this code though.  When you try to access the drive using
  # Windows Explorer, the first time it will always crash Explorer.  After that
  # first crash it appears to be fine.  I need to figure out how to fix this.

  DriverOption = (
    d1_onedrive.impl.drivers.dokan.const.DOKAN_OPTION_KEEP_ALIVE
    # | DOKAN_OPTION_NETWORK
  )
  if options.stderr:
    DriverOption |= (
      d1_onedrive.impl.drivers.dokan.const.DOKAN_OPTION_DEBUG |
      d1_onedrive.impl.drivers.dokan.const.DOKAN_OPTION_STDERR
    )

  d1fs = d1_onedrive.impl.drivers.dokan.dokan.Dokan(
    DataONEFS(options, root_resolver), options.mount_drive_letter, DriverOption,
    0x19831116, THREADS
  )

  #if options.unmount:
  #  # unmount the specified drive
  #  if not d1fs.dokanUnmount(mountpoint):
  #    logging.error("Failed to unmount DataONE drive")
  #else:
  # start DataONE drive
  ret = d1fs.main()
  if (ret == -6):
    logging.error("Failed to mount DataONE drive: Bad mount point")
  elif (ret < 0):
    logging.error("Failed to mount DataONE drive")


class DataONEFS(d1_onedrive.impl.drivers.dokan.dokan.Operations):
  """
  Read-only user-mode file system for DataONE using Dokan
  """

  def __init__(self, options, root_resolver):
    self._options = options
    self.READ_ONLY_ACCESS_MODE = 3
    self.root_resolver = root_resolver
    self.start_time = time.time()

    self.attribute_cache = options.attribute_cache
    self.directory_cache = options.directory_cache

  def getFileInformation(self, fileName):
    log.debug('getFileInformation(): fileName={}'.format(fileName))
    if self._is_os_special_file(fileName):
      return None
    attributes = self._get_attributes_through_cache(fileName)
    stat = self._stat_from_attributes(attributes)
    if fileName == "\\":
      stat['attr'] |= d1_onedrive.impl.drivers.dokan.const.FILE_ATTRIBUTE_DEVICE
    return stat

  def findFilesWithPattern(self, path, searchPattern):
    log.debug(
      'findFilesWithPattern(): path={} searchPattern={}'.
      format(path, searchPattern)
    )

    if self._is_os_special_file(searchPattern):
      return None

    try:
      dir = self.directory_cache[path]
    except KeyError:
      dir = self.root_resolver.get_directory(path)
      self.directory_cache[path] = dir

    files = []
    for file_name in dir.names():
      if not fnmatch.fnmatch(file_name, searchPattern):
        continue
      file_path = os.path.join(path, file_name)
      attribute = self._get_attributes_through_cache(file_path)
      stat = self._stat_from_attributes(attribute)
      stat['name'] = file_name
      files.append(stat)
    return files

    # example:
  #result.append(dict(name='systemmetadata.xml',
  #                   attr=(FILE_ATTRIBUTE_NORMAL
  #                         |FILE_ATTRIBUTE_READONLY),
  #                   ctime=ctime1, atime=now, wtime=mtime1,
  #                   size=len(xml)))
  # science metadata

  def readFile(self, path, size, offset):
    log.debug('read(): {}'.format(path))
    try:
      return self.root_resolver.read_file(path, size, offset)
    except d1_onedrive.impl.onedrive_exceptions.PathException:
      #raise OSError(errno.ENOENT, e) FUSE
      raise IOError('Could not read specified file: %s', path)

    #logging.debug('%s %s %s', fileName, numberOfBytesToRead, offset)
    #
    ## tokenize path
    #tokens = fileName[1:].split('\\')

    # example
    #if mfname == 'systemmetadata.xml':
    #  obj = self.getSystemMetadata(pid)
    #  xml = obj.toxml('utf-8')
    #  if offset+numberOfBytesToRead>len(xml):
    #    numberOfBytesToRead = len(xml) - offset
    #  return xml[offset:offset+numberOfBytesToRead]

    raise IOError('Could not read specified file: %s', path)

  #TODO Not really sure what to do here...at the moment everything is virtual.
  # Everything is hard-coded right now just to get the idea across.  Mounting
  # as a network drive would solve this problem I think.

  def getDiskFreeSpace(self):
    return dict(
      freeBytesAvailable=0x100000000 - 2048, totalNumberOfBytes=0x100000000,
      totalNumberOfFreeBytes=0x100000000 - 2048
    )

  def getVolumeInformation(self):
    #logging.error('')
    fsFlags = (
      d1_onedrive.impl.drivers.dokan.const.FILE_READ_ONLY_VOLUME |
      d1_onedrive.impl.drivers.dokan.const.FILE_CASE_SENSITIVE_SEARCH |
      d1_onedrive.impl.drivers.dokan.const.FILE_CASE_PRESERVED_NAMES
    )
    return dict(
      volumeNameBuffer='DataONE Disk', maximumComponentLength=260,
      fileSystemFlags=fsFlags, fileSystemNameBuffer='DataONE File System'
    )

  def _get_attributes_through_cache(self, path):
    try:
      return self.attribute_cache[path]
    except KeyError:
      attribute = self.root_resolver.get_attributes(path)
      self.attribute_cache[path] = attribute
      return attribute

  def _stat_from_attributes(self, attributes):
    #log.debug(u'_stat_from_attributes(): attributes={0}'.format(attributes))

    date_time = d1_common.date_time.ts_from_dt(
      attributes.date()
    ) if attributes.date() is not None else self.start_time

    attrs = d1_onedrive.impl.drivers.dokan.const.FILE_ATTRIBUTE_DIRECTORY if attributes.is_dir(
    ) else d1_onedrive.impl.drivers.dokan.const.FILE_ATTRIBUTE_NORMAL
    attrs |= d1_onedrive.impl.drivers.dokan.const.FILE_ATTRIBUTE_READONLY

    stat = dict(
      attr=attrs,
      nlinks=2, # TODO
      size=attributes.size(),
      atime=date_time,
      mtime=date_time, # in use?
      ctime=date_time,
      wtime=date_time,
    )

    #log.debug(u'_stat_from_attributes(): stat={0}'.format(stat))
    return stat

  def _is_os_special_file(self, path):
    return len(set(path.split(os.path.sep)) & self._options.ignore_special)

  def _raise_error_no_such_file_or_directory(self, path):
    log.debug('Error: No such file or directory: {}'.format(path))
    raise OSError(errno.ENOENT, '')


#  def _raise_error_permission_denied(self, path):
#    log.debug('Error: Permission denied: {0}'.format(path))
#    raise OSError(errno.EACCES, '')

################################################################################
#
#class FUSECallbacks():
#  def __init__(self, options, root_resolver):
#    self._options = options
#    self.READ_ONLY_ACCESS_MODE = 3
#    self.root_resolver = root_resolver
#    self.start_time = time.time()
#    self.gid = os.getgid()
#    self.uid = os.getuid()
#
#    self.attribute_cache = options.attribute_cache
#    self.directory_cache = options.directory_cache
#
#
#  def getattr(self, path, fh):
#    """Called by FUSE when the attributes for a file or directory are required.
#
#    Returns a dictionary with keys identical to the stat C structure of stat(2).
#    st_atime, st_mtime and st_ctime should be floats. On OSX, st_nlink should
#    count all files inside the directory. On Linux, only the subdirectories are
#    counted. The 'st_dev' and 'st_blksize' fields are ignored. The 'st_ino'
#    field is ignored except if the 'use_ino' mount option is given.
#
#    This method gets very heavy traffic.
#    """
#    self._raise_error_for_os_special_file(path)
#    #log.debug(u'getattr(): {0}'.format(path))
#    attribute = self._get_attributes_through_cache(path)
#    #log.debug('getattr() returned attribute: {0}'.format(attribute))
#    return self._stat_from_attributes(attribute)
#
#
#  def readdir(self, path, fh):
#    """Called by FUSE when a directory is opened.
#    Returns a list of file and directory names for the directory.
#    """
#    log.debug(u'readdir(): {0}'.format(path))
#    try:
#      dir = self.directory_cache[path]
#    except KeyError:
#      dir = self.root_resolver.get_directory(path)
#      self.directory_cache[path] = dir
#    return dir.names()
#
#
#  def open(self, path, flags):
#    """Called by FUSE when a file is opened.
#    Determines if the provided path and open flags are valid.
#    """
#    log.debug(u'open(): {0}'.format(path))
#    # ONEDrive is currently read only. Anything but read access is denied.
#    if (flags & self.READ_ONLY_ACCESS_MODE) != os.O_RDONLY:
#      self._raise_error_permission_denied(path)
#    # Any file in the filesystem can be opened.
#    attribute = self._get_attributes_through_cache(path)
#    return attribute.is_dir()
#
#
#  def read(self, path, size, offset, fh):
#    log.debug(u'read(): {0}'.format(path))
#    try:
#      return self.root_resolver.read_file(path, size, offset)
#    except onedrive_exceptions.PathException as e:
#      raise OSError(errno.ENOENT, e)
#
#  # Private.
#
#  def _get_attributes_through_cache(self, path):
#    try:
#      return self.attribute_cache[path]
#    except KeyError:
#      attribute = self.root_resolver.get_attributes(path)
#      self.attribute_cache[path] = attribute
#      return attribute
#
#
#  def _stat_from_attributes(self, attributes):
#    date_time = d1_common.date_time.to_seconds_since_epoch(
#      attributes.date()) if attributes.date() is not None else self.start_time
#    return dict(
#      st_mode = stat.S_IFDIR | 0555 if attributes.is_dir() else \
#        stat.S_IFREG | 0444,
#      st_ino = 0,
#      st_dev = 0,
#      st_nlink = 2, # TODO
#      st_uid = self.uid,
#      st_gid = self.gid,
#      st_size = attributes.size(),
#      st_atime = date_time,
#      st_mtime = date_time,
#      st_ctime = date_time,
#    )
#
#
#  def _raise_error_for_os_special_file(self, path):
#    if len(set(path.split(os.path.sep)) & settings.IGNORE_SPECIAL):
#      self._raise_error_no_such_file_or_directory(path)
#
#
#  def _raise_error_no_such_file_or_directory(self, path):
#    log.debug(u'Error: No such file or directory: {0}'.format(path))
#    raise OSError(errno.ENOENT, '')
#
#
##  def _raise_error_permission_denied(self, path):
##    log.debug('Error: Permission denied: {0}'.format(path))
##    raise OSError(errno.EACCES, '')
