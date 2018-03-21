# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""
Module to interface with Dokan

:author: Ryan Kroiss

Exported classes:

Dokan -- "no-op" Dokan implementation
"""

import ctypes
import ctypes.wintypes as wintypes
import functools
import logging

import d1_onedrive.impl.drivers.dokan.const


class Dokan(object):
  """
  "No-op" implementation of Dokan user-mode file system interface
  """

  def __init__(
      self, operations, mountPoint, driverOptions, serialNumber, num_threads
  ):
    """
    Initialize Dokan instance.
    :param operations: implementations of callbacks to dokan operations
    :type operations: dokan_operations
    :param DriverLetterOrMountPoint: mount point
    :type DriverLetterOrMountPoint: str
    :param DriverOption: dokan options
    :type DriverOption: long
    :param num_threads: number of threads to launch Dokan with
    :type num_threads: int
    """
    self.mountPoint = mountPoint
    self.driverOptions = driverOptions
    self.serialNumber = serialNumber
    self.dokanDLL = ctypes.windll.dokan

    # set up preferences for Dokan drive
    self.options = DOKAN_OPTIONS(
      600, # Dokan version number
      num_threads, # number of threads
      self.driverOptions, # drive options
      0, # global context
      self.mountPoint
    ) # mount point

    self.operations = operations

    # use reflection to populate operations
    self.dokan_ops = dokan_operations()
    for name, prototype in dokan_operations._fields_:
      if prototype != ctypes.c_voidp and getattr(operations, name, None):
        op = functools.partial(self._wrapper_, getattr(self, name))
        setattr(self.dokan_ops, name, prototype(op))

  def _wrapper_(self, func, *args, **kwargs):
    # RD
    #try:
    return func(*args, **kwargs) or 0

  #except Exception,e:
  #logging.error('error in wrapper: %s %s', func, e)
  #return const.DOKAN_ERROR

  def dokanMain(self, dokanOptions, dokanOperations):
    """
    Issue callback to start dokan drive.
    :param DokanOptions: drive options
    :type DokanOptions: DOKAN_OPTIONS
    :param DokanOperations: pointers implemented file system calls
    :type DokanOperations: DokanOperations
    :return: error code
    :rtype: int
    """
    return int(
      self.dokanDLL.DokanMain(
        PDOKAN_OPTIONS(dokanOptions), PDOKAN_OPERATIONS(dokanOperations)
      )
    )

  def dokanUnmount(self, driveLetter):
    return bool(
      self.dokanDLL.DokanRemoveMountPoint(ctypes.c_wchar_p(driveLetter))
    )

  """
  # DokanIsNameInExpression
  #   check whether Name can match Expression
  #   Expression can contain wildcard characters (? and *)
  def DokanIsNameInExpression(self, Expression, Name, IgnoreCase):
      return bool(self.DokanDLL.DokanIsNameInExpression(
          ctypes.c_wchar_p(Expression),                # matching pattern
          ctypes.c_wchar_p(Name),                        # file name
          ctypes.c_bool(IgnoreCase)
      ))

  def DokanVersion(self):
      return long(self.DokanDLL.DokanVersion())

  def DokanDriverVersion(self):
      return long(self.DokanDLL.DokanDriverVersion())

  # DokanResetTimeout
  # extends the time out of the current IO operation in driver.
  def DokanResetTimeout(self, Timeout, DokanFileInfo):
      return bool(self.DokanDLL.DokanResetTimeout(
          ctypes.c_ulong(Timeout),                        # timeout in millisecond
          PDOKAN_FILE_INFO(DokanFileInfo)
      ))

  # Get the handle to Access Token
  # This method needs be called in CreateFile, OpenDirectory or CreateDirectly callback.
  # The caller must call CloseHandle for the returned handle.
  def DokanOpenRequestorToken(self, DokanFileInfo):
      return wintypes.HANDLE(self.DokanDLL.DokanOpenRequestorToken(
          PDOKAN_FILE_INFO(DokanFileInfo)
      ))
  """

  def createFile(
      self, fileName, desiredAccess, shareMode, creationDisposition,
      flagsAndAttributes, dokanFileInfo
  ):
    """
    Creates a file.
    :param fileName: name of file to create
    :type fileName: ctypes.c_wchar_p
    :param desiredAccess: desired access flags
    :type desiredAccess: ctypes.c_ulong
    :param shareMode: share mode flags
    :type shareMode: ctypes.c_ulong
    :param creationDisposition: creation disposition flags
    :type creationDisposition: ctypes.c_ulong
    :param flagsAndAttributes: creation flags and attributes
    :type flagsAndAttributes: ctypes.c_ulong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('createFile', fileName)

  def openDirectory(self, fileName, dokanFileInfo):
    """
    Opens a directory.
    :param fileName: name of directory to open
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('openDirectory', fileName)

  def createDirectory(self, fileName, dokanFileInfo):
    """
    Create a directory.
    :param fileName: name of directory to create
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('createDirectory', fileName)

  def cleanup(self, fileName, dokanFileInfo):
    """
    Cleanup when deleting a file or directory.
    :param fileName: name of file or directory to cleanup
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('cleanup', fileName)

  def closeFile(self, fileName, dokanFileInfo):
    """
    Close a file.
    :param fileName: name of file to close
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('closeFile', fileName)

  def readFile(
      self, fileName, buffer, numberOfBytesToRead, numberOfBytesRead, offset,
      dokanFileInfo
  ):
    """
    Read a file.
    :param fileName: name of file to read
    :type fileName: ctypes.c_wchar_p
    :param buffer: buffer for content read
    :type buffer: ctypes.c_void_p
    :param numberOfBytesToRead: number of bytes to read
    :type numberOfBytesToRead: ctypes.c_ulong
    :param numberOfBytesRead: number of bytes read
    :type numberOfBytesRead: ctypes.POINTER(ctypes.c_ulong)
    :param offset: byte offset
    :type offset: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    try:
      ret = self.operations('readFile', fileName, numberOfBytesToRead, offset)
      data = ctypes.create_string_buffer(
        ret[:numberOfBytesToRead], numberOfBytesToRead
      )
      ctypes.memmove(buffer, data, numberOfBytesToRead)
      sizeRead = ctypes.c_ulong(len(ret))
      ctypes.memmove(
        numberOfBytesRead, ctypes.byref(sizeRead),
        ctypes.sizeof(ctypes.c_ulong)
      )
      return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS
    except Exception:
      #logging.error('%s', e)
      return d1_onedrive.impl.drivers.dokan.const.DOKAN_ERROR

  def writeFile(
      self, fileName, buffer, numberOfBytesToWrite, numberOfBytesWritten,
      offset, dokanFileInfo
  ):
    """
    Read a file.
    :param fileName: name of file to write
    :type fileName: ctypes.c_wchar_p
    :param buffer: buffer to write
    :type buffer: ctypes.c_void_p
    :param numberOfBytesToWrite: number of bytes to write
    :type numberOfBytesToWrite: ctypes.c_ulong
    :param numberOfBytesWritten: number of bytes written
    :type numberOfBytesWritten: ctypes.POINTER(ctypes.c_ulong)
    :param offset: byte offset
    :type offset: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations(
      'writeFile', fileName, buffer, numberOfBytesToWrite, offset
    )

  def flushFileBuffers(self, fileName, dokanFileInfo):
    """
    Flush a file's buffer.
    :param fileName: name of file to flush
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('flushFileBuffers', fileName)

  def getFileInformation(self, fileName, buffer, dokanFileInfo):
    #"""
    #Get information about a file.
    #:param fileName: name of file fetch information for
    #:type fileName: ctypes.c_wchar_p
    #:param buffer: buffer to fill with file information
    #:type buffer: PBY_HANDLE_FILE_INFORMATION
    #:param dokanFileInfo: used by Dokan
    #:type dokanFileInfo: PDOKAN_FILE_INFO
    #:return: error code
    #:rtype: ctypes.c_int
    #"""
    #    try:
    ret = self.operations('getFileInformation', fileName)
    if ret is None:
      return -d1_onedrive.impl.drivers.dokan.const.ERROR_FILE_NOT_FOUND
    create_ft = self.python_timestamp_to_win32_filetime(ret['ctime'])
    last_access_ft = self.python_timestamp_to_win32_filetime(ret['atime'])
    last_write_ft = self.python_timestamp_to_win32_filetime(ret['wtime'])
    cft = ctypes.wintypes.FILETIME(create_ft[0], create_ft[1])
    laft = ctypes.wintypes.FILETIME(last_access_ft[0], last_access_ft[1])
    lwft = ctypes.wintypes.FILETIME(last_write_ft[0], last_write_ft[1])
    size = self.pyint_to_double_dwords(ret['size'])
    _Buffer = BY_HANDLE_FILE_INFORMATION(
      ctypes.c_ulong(ret['attr']), # attributes
      cft, # creation time
      laft, # last access time
      lwft, # last write time
      ctypes.c_ulong(self.serialNumber), # serial number
      size[1], # size (upper bits)
      size[0], # size (lower bits)
      ctypes.c_ulong(1), # num links to this file
      ctypes.c_ulong(0), # index (upper)
      ctypes.c_ulong(0)
    ) # index (lower)
    ctypes.memmove(
      buffer, ctypes.byref(_Buffer), ctypes.sizeof(BY_HANDLE_FILE_INFORMATION)
    )
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  #except Exception,e:
  #  logging.error('%s', e)
  #  return -const.ERROR_FILE_NOT_FOUND

  def findFiles(self, fileName, fillFindData, dokanFileInfo):
    """
    Find files in a certain path.
    :param fileName: path to search
    :type fileName: ctypes.c_wchar_p
    :param fillFindData: function pointer for populating search results
    :type fillFindData: PFillFindData
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('findFiles', fileName)

  def findFilesWithPattern(
      self, fileName, searchPattern, fillFindData, dokanFileInfo
  ):
    """
    Find files in a certain path that match the search pattern.
    :param fileName: path to search
    :type fileName: ctypes.c_wchar_p
    :param searchPattern: pattern to search for
    :type searchPattern: ctypes.c_wchar_p
    :param fillFindData: function pointer for populating search results
    :type fillFindData: PFillFindData
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    try:
      ret = self.operations('findFilesWithPattern', fileName, searchPattern)
      if ret is None:
        return d1_onedrive.impl.drivers.dokan.const.DOKAN_ERROR
      for r in ret:
        create_ft = self.python_timestamp_to_win32_filetime(r['ctime'])
        last_access_ft = self.python_timestamp_to_win32_filetime(r['atime'])
        last_write_ft = self.python_timestamp_to_win32_filetime(r['wtime'])
        cft = ctypes.wintypes.FILETIME(create_ft[0], create_ft[1])
        laft = ctypes.wintypes.FILETIME(last_access_ft[0], last_access_ft[1])
        lwft = ctypes.wintypes.FILETIME(last_write_ft[0], last_write_ft[1])
        size = self.pyint_to_double_dwords(r['size'])
        File = ctypes.wintypes.WIN32_FIND_DATAW(
          ctypes.c_ulong(r['attr']), # attributes
          cft, # creation time
          laft, # last access time
          lwft, # last write time
          size[1], # upper bits of size
          size[0], # lower bits of size
          ctypes.c_ulong(0), # reserved for FS
          ctypes.c_ulong(0), # reserved for FS
          r['name'], # file name
          ''
        ) # alternate name
        pFile = ctypes.wintypes.PWIN32_FIND_DATAW(File)
        fillFindData(pFile, dokanFileInfo)
      return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS
    except Exception as e:
      logging.error('%s', e)
      return d1_onedrive.impl.drivers.dokan.const.DOKAN_ERROR

  def setFileAttributes(self, fileName, fileAttributes, dokanFileInfo):
    """
    Set attributes for a file.
    :param fileName: name of file to set attributes for
    :type fileName: ctypes.c_wchar_p
    :param fileAttributes: new file attributes
    :type fileAttrributes: ctypes.c_ulong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('setFileAttributes', fileName)

  def setFileTime(
      self, fileName, creationTime, lastAccessTime, lastWriteTime, dokanFileInfo
  ):
    """
    Set time values for a file.
    :param fileName: name of file to set time values for
    :type fileName: ctypes.c_wchar_p
    :param creationTime: creation time of file
    :type creationTime: ctypes.POINTER(ctypes.wintypes.FILETIME)
    :param lastAccessTime: last access time of file
    :type lastAccessTime: ctypes.POINTER(ctypes.wintypes.FILETIME)
    :param lastWriteTime: last write time of file
    :type lastWriteTime: ctypes.POINTER(ctypes.wintypes.FILETIME)
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('setFileTime', fileName)

  def deleteFile(self, fileName, dokanFileInfo):
    """
    Delete a file.
    :param fileName: name of file to delete
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('deleteFile', fileName)

  def deleteDirectory(self, fileName, dokanFileInfo):
    """
    Delete a directory.
    :param fileName: name of directory to delete
    :type fileName: ctypes.c_wchar_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('deleteDirectory', fileName)

  def moveFile(
      self, existingFileName, newFileName, replaceExisiting, dokanFileInfo
  ):
    """
    Move a file.
    :param existingFileName: name of file to move
    :type existingFileName: ctypes.c_wchar_p
    :param newFileName: new name of file
    :type newFileName: ctypes.c_wchar_p
    :param replaceExisting: flag to indicate replacement of existing file
    :type replaceExisting: ctypes.c_bool
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('moveFile', existingFileName, newFileName)

  def setEndOfFile(self, fileName, length, dokanFileInfo):
    """
    Set end of file indicator.
    :param fileName: name of file to set EOF for
    :type fileName: ctypes.c_wchar_p
    :param length: position of new EOF
    :type length: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('setEndOfFile', fileName)

  def setAllocationSize(self, fileName, length, dokanFileInfo):
    """
    Set allocation size for a file.
    :param fileName: name of file to set allocation size for
    :type fileName: ctypes.c_wchar_p
    :param length: new allocation size
    :type length: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('setAllocationSize', fileName)

  def lockFile(self, fileName, byteOffset, length, dokanFileInfo):
    """
    Lock a file.
    :param fileName: name of file to lock
    :type fileName: ctypes.c_wchar_p
    :param byteOffset: location to start lock
    :type byteOffset: ctypes.c_longlong
    :param length: number of bytes to lock
    :type length: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('lockFile', fileName, byteOffset, length)

  def unlockFile(self, fileName, byteOffset, length, dokanFileInfo):
    """
    Unlock a file.
    :param fileName: name of file to unlock
    :type fileName: ctypes.c_wchar_p
    :param byteOffset: location to start unlock
    :type byteOffset: ctypes.c_longlong
    :param length: number of bytes to unlock
    :type length: ctypes.c_longlong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('unlockFile', fileName, byteOffset, length)

  def getDiskFreeSpace(
      self, freeBytesAvailable, totalNumberOfBytes, totalNumberOfFreeBytes,
      dokanFileInfo
  ):
    """
    Get the amount of free space on this volume.
    :param freeBytesAvailable: pointer for free bytes available
    :type freeBytesAvailable: ctypes.c_void_p
    :param totalNumberOfBytes: pointer for total number of bytes
    :type totalNumberOfBytes: ctypes.c_void_p
    :param totalNumberOfFreeBytes: pointer for total number of free bytes
    :type totalNumberOfFreeBytes: ctypes.c_void_p
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    ret = self.operations('getDiskFreeSpace')
    ctypes.memmove(
      freeBytesAvailable,
      ctypes.byref(ctypes.c_longlong(ret['freeBytesAvailable'])),
      ctypes.sizeof(ctypes.c_longlong)
    )
    ctypes.memmove(
      totalNumberOfBytes,
      ctypes.byref(ctypes.c_longlong(ret['totalNumberOfBytes'])),
      ctypes.sizeof(ctypes.c_longlong)
    )
    ctypes.memmove(
      totalNumberOfFreeBytes,
      ctypes.byref(ctypes.c_longlong(ret['totalNumberOfFreeBytes'])),
      ctypes.sizeof(ctypes.c_longlong)
    )
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def getVolumeInformation(
      self, volumeNameBuffer, volumeNameSize, volumeSerialNumber,
      maximumComponentLength, fileSystemFlags, fileSystemNameBuffer,
      fileSystemNameSize, dokanFileInfo
  ):
    """
    Get information about the volume.
    :param volumeNameBuffer: buffer for volume name
    :type volumeNameBuffer: ctypes.c_void_p
    :param volumeNameSize: volume name buffer size
    :type volumeNameSize: ctypes.c_ulong
    :param volumeSerialNumber: buffer for volume serial number
    :type volumeSerialNumber: ctypes.c_void_p
    :param maximumComponentLength: buffer for maximum component length
    :type maximumComponentLength: ctypes.c_void_p
    :param fileSystemFlags: buffer for file system flags
    :type fileSystemFlags: ctypes.c_void_p
    :param fileSystemNameBuffer: buffer for file system name
    :type fileSystemNameBuffer: ctypes.c_void_p
    :param fileSystemNameSize: file system name buffer size
    :type fileSystemNameSize: ctypes.c_ulong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    ret = self.operations('getVolumeInformation')
    # populate volume name buffer
    ctypes.memmove(
      volumeNameBuffer, ret['volumeNameBuffer'],
      min(
        ctypes.sizeof(ctypes.c_wchar) * len(ret['volumeNameBuffer']),
        volumeNameSize
      )
    )
    # populate serial number buffer
    serialNum = ctypes.c_ulong(self.serialNumber)
    ctypes.memmove(
      volumeSerialNumber, ctypes.byref(serialNum),
      ctypes.sizeof(ctypes.c_ulong)
    )
    # populate max component length
    maxCompLen = ctypes.c_ulong(ret['maximumComponentLength'])
    ctypes.memmove(
      maximumComponentLength,
      ctypes.byref(maxCompLen), ctypes.sizeof(ctypes.c_ulong)
    )
    # populate filesystem flags buffer
    fsFlags = ctypes.c_ulong(ret['fileSystemFlags'])
    ctypes.memmove(
      fileSystemFlags, ctypes.byref(fsFlags), ctypes.sizeof(ctypes.c_ulong)
    )
    # populate filesystem name
    ctypes.memmove(
      fileSystemNameBuffer, ret['fileSystemNameBuffer'],
      min(
        ctypes.sizeof(ctypes.c_wchar) * len(ret['fileSystemNameBuffer']),
        fileSystemNameSize
      )
    )
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def unmount(self, dokanFileInfo):
    """
    Unmount the volume.
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('unmount', dokanFileInfo)

  def getFileSecurity(
      self, fileName, securityInformation, securityDescriptor,
      lengthSecurityDescriptorBuffer, lengthNeeded, dokanFileInfo
  ):
    """
    Get security attributes of a file.
    :param fileName: name of file to get security for
    :type fileName: ctypes.c_wchar_p
    :param securityInformation: buffer for security information
    :type securityInformation: PSECURITY_INFORMATION
    :param securityDescriptor: buffer for security descriptor
    :type securityDescriptor: PSECURITY_DESCRIPTOR
    :param lengthSecurityDescriptorBuffer: length of descriptor buffer
    :type lengthSecurityDescriptorBuffer: ctypes.c_ulong
    :param lengthNeeded: length needed for the buffer
    :type lengthNeeded: ctypes.POINTER(ctypes.c_ulong)
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('getFileSecurity', fileName)

  def setFileSecurity(
      self, fileName, securityInformation, securityDescriptor,
      lengthSecurityDescriptorBuffer, dokanFileInfo
  ):
    """
    Set security attributes of a file.
    :param fileName: name of file to set security for
    :type fileName: ctypes.c_wchar_p
    :param securityInformation: new security information
    :type securityInformation: PSECURITY_INFORMATION
    :param securityDescriptor: newsecurity descriptor
    :type securityDescriptor: PSECURITY_DESCRIPTOR
    :param lengthSecurityDescriptorBuffer: length of descriptor buffer
    :type lengthSecurityDescriptorBuffer: ctypes.c_ulong
    :param dokanFileInfo: used by Dokan
    :type dokanFileInfo: PDOKAN_FILE_INFO
    :return: error code
    :rtype: ctypes.c_int
    """
    return self.operations('setFileSecurity', fileName)

  # https://bitbucket.org/pchambon/python-rock-solid-tools/src/021bb37fedfe/rsbackends/_utilities.py
  def pyint_to_double_dwords(cls, mylong, dwordsize=32):
    if (mylong < 0):
      raise ValueError("Positive argument required")
    uloworder = mylong & (2**dwordsize - 1)
    uhighorder = (mylong >> dwordsize) & (2**dwordsize - 1)
    return (uloworder, uhighorder)

  def python_timestamp_to_win32_filetime(cls, pytimestamp):
    win32_timestamp = int((10000000 * pytimestamp) + 116444736000000000)
    (loworder, highorder) = cls.pyint_to_double_dwords(win32_timestamp)
    return (loworder, highorder)

  def main(self):
    """
    Starts Dokan drive which dispatches events to the appropriate
    handlers.
    """
    return self.dokanMain(self.options, self.dokan_ops)


class Operations(object):
  def __call__(self, op, *args):
    if not hasattr(self, op):
      raise AttributeError('Invalid operation')
    return getattr(self, op)(*args)

  def createFile(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def openDirectory(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def createDirectory(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def cleanup(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def closeFile(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def readFile(self, fileName, numberOfBytesToRead, offset):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def writeFile(self, fileName, buffer, numberOfBytesToWrite, offset):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def flushFileBuffers(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def getFileInformation(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def findFiles(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def findFilesWithPattern(self, fileName, searchPattern):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def setFileAttributes(self, fileName, fileAttributes):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def setFileTime(self, fileName, creationTime, lastAccessTime, lastWriteTime):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def deleteFile(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def deleteDirectory(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def moveFile(self, existingFileName, newFileName, replaceExisting):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def setEndOfFile(self, fileName, length):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def setAllocationSize(self, fileName, length):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def lockFile(self, fileName, offset, length):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def unlockFile(self, fileName, offset, length):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def getDiskFreeSpace(self):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def getVolumeInformation(self):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def unmount(self):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def getFileSecurity(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS

  def setFileSecurity(self, fileName):
    return d1_onedrive.impl.drivers.dokan.const.DOKAN_SUCCESS


class _DOKAN_OPTIONS(ctypes.Structure):
  _fields_ = [("Version", ctypes.c_ushort),
              ("ThreadCount", ctypes.c_ushort),
              ("Options", ctypes.c_ulong),
              ("GlobalContext", ctypes.c_ulonglong),
              ("MountPoint", ctypes.c_wchar_p)]


DOKAN_OPTIONS = _DOKAN_OPTIONS
PDOKAN_OPTIONS = ctypes.POINTER(_DOKAN_OPTIONS)


class _DOKAN_FILE_INFO(ctypes.Structure):
  _fields_ = [("Context", ctypes.c_ulonglong),
              ("DokanContext", ctypes.c_ulonglong),
              ("DokanOptions", PDOKAN_OPTIONS),
              ("ProcessId", ctypes.c_ulong),
              ("IsDirectory", ctypes.c_ubyte),
              ("DeleteOnClose", ctypes.c_ubyte),
              ("PagingIo", ctypes.c_ubyte),
              ("SynchronousIo", ctypes.c_ubyte),
              ("Nocache", ctypes.c_ubyte),
              ("WriteToEndOfFile", ctypes.c_ubyte)]


DOKAN_FILE_INFO = _DOKAN_FILE_INFO
PDOKAN_FILE_INFO = ctypes.POINTER(_DOKAN_FILE_INFO)

PWIN32_FIND_DATAW = ctypes.POINTER(wintypes.WIN32_FIND_DATAW)


class _BY_HANDLE_FILE_INFORMATION(ctypes.Structure):
  _fields_ = [("dwFileAttributes", ctypes.c_ulong),
              ("ftCreationTime", wintypes.FILETIME),
              ("ftLastAccessTime", wintypes.FILETIME),
              ("ftLastWriteTime", wintypes.FILETIME),
              ("dwVolumeSerialNumber", ctypes.c_ulong),
              ("nFileSizeHigh", ctypes.c_ulong),
              ("nFileSizeLow", ctypes.c_ulong),
              ("nNumberOfLinks", ctypes.c_ulong),
              ("nFileIndexHigh", ctypes.c_ulong),
              ("nFileIndexLow", ctypes.c_ulong)]


BY_HANDLE_FILE_INFORMATION = _BY_HANDLE_FILE_INFORMATION
PBY_HANDLE_FILE_INFORMATION = ctypes.POINTER(_BY_HANDLE_FILE_INFORMATION)

PSECURITY_INFORMATION = ctypes.POINTER(ctypes.c_ulong)
PSECURITY_DESCRIPTOR = ctypes.c_void_p

PFillFindData = ctypes.WINFUNCTYPE(
  ctypes.c_int, ctypes.POINTER(wintypes.WIN32_FIND_DATAW), PDOKAN_FILE_INFO
)


class dokan_operations(ctypes.Structure):
  _fields_ = [(
    "createFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_ulong,
      ctypes.c_ulong, ctypes.c_ulong, PDOKAN_FILE_INFO
    )
  ), (
    "openDirectory",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "createDirectory",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "cleanup",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "closeFile",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "readFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_ulong,
      ctypes.POINTER(ctypes.c_ulong), ctypes.c_longlong, PDOKAN_FILE_INFO
    )
  ), (
    "writeFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_ulong,
      ctypes.POINTER(ctypes.c_ulong), ctypes.c_longlong, PDOKAN_FILE_INFO
    )
  ), (
    "flushFileBuffers",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "getFileInformation", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, PBY_HANDLE_FILE_INFORMATION,
      PDOKAN_FILE_INFO
    )
  ), (
    "findFiles", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, PFillFindData, PDOKAN_FILE_INFO
    )
  ), (
    "findFilesWithPattern", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p, PFillFindData,
      PDOKAN_FILE_INFO
    )
  ), (
    "setFileAttributes", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_ulong, PDOKAN_FILE_INFO
    )
  ), (
    "setFileTime", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p,
      ctypes.POINTER(wintypes.FILETIME),
      ctypes.POINTER(wintypes.FILETIME),
      ctypes.POINTER(wintypes.FILETIME), PDOKAN_FILE_INFO
    )
  ), (
    "deleteFile",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "deleteDirectory",
    ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_wchar_p, PDOKAN_FILE_INFO)
  ), (
    "moveFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_bool,
      PDOKAN_FILE_INFO
    )
  ), (
    "setEndOfFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_longlong, PDOKAN_FILE_INFO
    )
  ), (
    "setAllocationSize", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_longlong, PDOKAN_FILE_INFO
    )
  ), (
    "lockFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_longlong, ctypes.c_longlong,
      PDOKAN_FILE_INFO
    )
  ), (
    "unlockFile", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, ctypes.c_longlong, ctypes.c_longlong,
      PDOKAN_FILE_INFO
    )
  ), (
    "getDiskFreeSpace", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
      PDOKAN_FILE_INFO
    )
  ), (
    "getVolumeInformation", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong,
      ctypes.POINTER(ctypes.c_ulong),
      ctypes.POINTER(ctypes.c_ulong),
      ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p, ctypes.c_ulong,
      PDOKAN_FILE_INFO
    )
  ), ("unmount", ctypes.WINFUNCTYPE(ctypes.c_int, PDOKAN_FILE_INFO)), (
    "getFileSecurity", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, PSECURITY_INFORMATION,
      PSECURITY_DESCRIPTOR, ctypes.c_ulong,
      ctypes.POINTER(ctypes.c_ulong), PDOKAN_FILE_INFO
    )
  ), (
    "setFileSecurity", ctypes.WINFUNCTYPE(
      ctypes.c_int, ctypes.c_wchar_p, PSECURITY_INFORMATION,
      PSECURITY_DESCRIPTOR, ctypes.c_ulong, PDOKAN_FILE_INFO
    )
  )]


DOKAN_OPERATIONS = dokan_operations
PDOKAN_OPERATIONS = ctypes.POINTER(dokan_operations)
