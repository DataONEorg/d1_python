"""
Module d1_dokan.py
==================

A read only Dokan filesystem driver for DataONE.

:Created:
:Author: Ryan Kroiss
:Dependencies:
  - python 2.7.2

This driver provides access to objects in the DataONE infrastructure through
DataONE's Apache Solr interface. Faceted search is provided through Solr.

http://lucene.apache.org/solr/

How to use:

- Install Dokan
- Set PYTHONPATH to include d1_common_python/src and d1_libclient_python/src

Run as::

  python d1_dokan.py <mount point>

"""

# standard library
import os
import ctypes
from ctypes.wintypes import FILETIME
from ctypes.wintypes import WIN32_FIND_DATAW
import optparse
import pdb
import sys
import time
import urllib
import logging

# Dokan imports
import dokan
from const import DOKAN_SUCCESS
from const import DOKAN_ERROR
from const import DOKAN_OPTION_DEBUG
from const import DOKAN_OPTION_STDERR
from const import DOKAN_OPTION_KEEP_ALIVE
from const import DOKAN_OPTION_NETWORK
from const import DOKAN_OPTION_REMOVABLE
from const import FILE_ATTRIBUTE_READONLY
from const import FILE_ATTRIBUTE_DEVICE
from const import FILE_ATTRIBUTE_NORMAL
from const import ERROR_FILE_NOT_FOUND
from const import FILE_ATTRIBUTE_DIRECTORY
from const import FILE_READ_ONLY_VOLUME
from const import FILE_CASE_SENSITIVE_SEARCH
from const import FILE_CASE_PRESERVED_NAMES

# DataONE imports
import d1_common.const
from fs_util import D1FS

# debugging flags
debug = False



class DataONEFS(dokan.Operations, D1FS):
  """
  Read-only user-mode file system for DataONE using Dokan
  """

  def __init__(self, baseurl=d1_common.const.URL_DATAONE_ROOT,
               filter_query=None):
    logging.debug('Initializing Dokan drive')
    D1FS.__init__(self, baseurl, filter_query)
    
  def getFileAttributes(self, fileName):
    if fileName == "\\":
      return (FILE_ATTRIBUTE_DEVICE | FILE_ATTRIBUTE_DIRECTORY 
              | FILE_ATTRIBUTE_READONLY)
    
    tokens = fileName[1:].split('\\')
    lastToken = tokens[len(tokens)-1]

    if (len(tokens)==4 and tokens[3]!='describes') or len(tokens)==5:
      return FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_READONLY
    else:
      return FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_READONLY
      

  def getFileInformation(self, fileName):
    # constuct filetime structure from current time
    now = time.time()
    
    # get file attributes
    attrs = self.getFileAttributes(fileName)
    
    # get info at the root level
    if fileName == "\\":
      return dict(attr=attrs, ctime=now, atime=now, wtime=now, size=0, nlinks=1)
    
    # split the path
    tokens = fileName[1:].split('\\')

    # check to see if file is junk Windows file
    last = tokens[len(tokens)-1]
    if last=='desktop.ini' or last=='folder.jpg' or last=='folder.gif':
      return None
    
    # facet level of file system, subdirs are facet values
    if len(tokens) == 1:
      if tokens[0] in [''] + self.facets.keys():
        if tokens[0] in self.facets.keys():
          facet_values = self.getFacetValues(tokens[0])
        return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                    size=0, nlinks=1)
      else:
        #raise IOError('specified facet does not exist')
        return None
    
    # identifier level, subdirs of the facet = identifier
    elif len(tokens) == 2:
      return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                  size=0, nlinks=1)
    
    # data package level
    elif len(tokens) == 3:
      return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                  size=0, nlinks=1)
    
    # related items
    elif len(tokens) == 4:
      pid = urllib.unquote(tokens[2]).decode('utf-8')
      mfname = urllib.unquote(tokens[3]).decode('utf-8')
      mfid = self.getObjectPid(mfname)

      # system metadata
      if tokens[3] == 'systemmetadata.xml':
        sysm = self.getSystemMetadata(pid)
        ctime1 = time.mktime(sysm.dateUploaded.timetuple())
        mtime1 = time.mktime(sysm.dateSysMetadataModified.timetuple())
        xml = sysm.toxml()
        return dict(attr=attrs, ctime=ctime1, atime=now, wtime=mtime1,
                    size=len(xml), nlinks=1)
      if mfid == pid:
        sysm = self.getSystemMetadata(pid)
        return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                    size=sysm.size, nlinks=1)
      # describes
      elif tokens[3] == 'describes':
        obj = self.getObject(pid)
        relations = obj.getRelatedObjects()
        return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                    size=0, nlinks=1)
      # abstract.txt
      elif tokens[3] == 'abstract.txt':
        abstxt = self.getAbstract(pid)
        return dict(attr=attrs, ctime=now, atime=now, wtime=now,
                    size=len(abstxt), nlinks=1)

    if len(tokens)==5:
      fname = urllib.unquote(tokens[4]).decode('utf-8')
      pid = self.getObjectPid(fname)
      if tokens[3]=='describes':
        try:
          sysm = self.getSystemMetadata(pid)
          ctime1 = time.mktime(sysm.dateUploaded.timetuple())
          mtime1 = time.mktime(sysm.dateSysMetadataModified.timetuple())
          return dict(attr=attrs, ctime=ctime1, atime=now, wtime=mtime1,
                      size=sysm.size, nlink=1)
        except:
          raise IOError('Unable to retrieve related object')
    raise IOError('Invalid path: %s', fileName)


  def findFilesWithPattern(self, fileName, searchPattern):
    #logging.error(fileName)
    # grab current time
    now = int(time.time())
    # array of search results
    result = []

    # device level - contains facets
    if fileName == '\\':
      for facet in self.facets.keys():
        result.append(dict(name=facet, attr=(FILE_ATTRIBUTE_DIRECTORY
                                             |FILE_ATTRIBUTE_READONLY),
                           ctime=now, atime=now, wtime=now, size=0))
      return result
      
    # split up the path to determine what level we're at
    pathTokens = fileName[1:].split('\\')
      
    # facet level - contains facet values
    if (len(pathTokens) == 1):
      #logging.error('lower => '+fileName.lower())
      if pathTokens[0].lower() in self.facets.keys():
        facet_values = self.getFacetValues(pathTokens[0].lower())
        for v in facet_values:
          result.append(dict(name=v, attr=(FILE_ATTRIBUTE_DIRECTORY
                                           |FILE_ATTRIBUTE_READONLY),
                             ctime=now, atime=now, wtime=now, size=0))
        return result
      else:
        raise IOError('facet does not exist')
          
    # identifier level - contains data packages
    elif (len(pathTokens) == 2):
      facetkey = urllib.unquote(pathTokens[0]).decode('utf-8')
      facetval = urllib.unquote(pathTokens[1]).decode('utf-8')
      entries = self.getIdentifiers(facetkey, facetval)
      for entry in entries:
        result.append(dict(name=self.encodePathName(entry),
                           attr=(FILE_ATTRIBUTE_DIRECTORY
                                 |FILE_ATTRIBUTE_READONLY),
                           ctime=now, atime=now, wtime=now, size=0))
      return result
      
    # data package level
    elif (len(pathTokens) == 3):
      pid = urllib.unquote(pathTokens[2]).decode('utf-8')
      obj = self.getObject(pid)
      fname = self.getObjectFileName(pid)
      #res = ['systemmetadata.xml', self.encodePathName(fname)]
      # describes
      related = obj.getRelatedObjects()
      if len(related['describes']) > 0:
        result.append(dict(name='describes',
                           attr=(FILE_ATTRIBUTE_DIRECTORY
                                 |FILE_ATTRIBUTE_READONLY),
                           ctime=now, atime=now, wtime=now, 
                           size=0))
      # abstract
      abstxt = self.getAbstract(pid)
      if len(abstxt) > 0:
        result.append(dict(name='abstract.txt',
                           attr=(FILE_ATTRIBUTE_NORMAL
                                 |FILE_ATTRIBUTE_READONLY),
                           ctime=now, atime=now, wtime=now, 
                           size=len(abstxt)))
      # system metadata 
      sysm = self.getSystemMetadata(pid)
      ctime1 = time.mktime(sysm.dateUploaded.timetuple())
      mtime1 = time.mktime(sysm.dateSysMetadataModified.timetuple())
      xml = sysm.toxml()
      result.append(dict(name='systemmetadata.xml',
                         attr=(FILE_ATTRIBUTE_NORMAL
                               |FILE_ATTRIBUTE_READONLY),
                         ctime=ctime1, atime=now, wtime=mtime1, 
                         size=len(xml)))
      # science metadata
      result.append(dict(name=self.encodePathName(fname), 
                         attr=(FILE_ATTRIBUTE_NORMAL
                               |FILE_ATTRIBUTE_READONLY),
                         ctime=now, atime=now, wtime=now, 
                         size=sysm.size))
      return result

    # related objects
    elif (len(pathTokens) == 4):
      pid = urllib.unquote(pathTokens[2]).decode('utf-8')
      if (pathTokens[3] == 'describes'):
        obj = self.getObject(pid)
        relations = obj.getRelatedObjects()
        for rel in relations['describes']:
          fname = self.getObjectFileName(rel)
          pid = self.getObjectPid(fname)
          sysm = self.getSystemMetadata(pid)
          ctime1 = time.mktime(sysm.dateUploaded.timetuple())
          mtime1 = time.mktime(sysm.dateSysMetadataModified.timetuple())
          result.append(dict(name=self.encodePathName(fname), 
                             attr=(FILE_ATTRIBUTE_NORMAL
                                   |FILE_ATTRIBUTE_READONLY),
                             ctime=ctime1, atime=now, wtime=mtime1, 
                             size=sysm.size))
        return result

    raise IOError('file not found')
  
  def readFile(self, fileName, numberOfBytesToRead, offset):
    logging.debug('%s %s %s', fileName, numberOfBytesToRead, offset)

    # tokenize path
    tokens = fileName[1:].split('\\')

    # related items
    if len(tokens)==4:
      pid = urllib.unquote(tokens[2]).decode('utf-8')
      mfname = urllib.unquote(tokens[3]).decode('utf-8')
      mpid = self.getObjectPid(mfname)

      if mfname == 'systemmetadata.xml':
        obj = self.getSystemMetadata(pid)
        xml = obj.toxml()
        if offset+numberOfBytesToRead>len(xml):
          numberOfBytesToRead = len(xml) - offset
        return xml[offset:offset+numberOfBytesToRead]

      if mfname == 'abstract.txt':
        abstxt = self.getAbstract(pid)
        if offset+numberOfBytesToRead>len(abstxt):
          numberOfBytesToRead = len(abstxt) - offset
        return abstxt[offset:offset+numberOfBytesToRead]

      if mpid==pid:
        sysm = self.getSystemMetadata(pid)
        if offset + numberOfBytesToRead > sysm.size:
          numberOfBytesToRead = sysm.size - offset
        data = self.get(pid)
        return data[offset:offset+numberOfBytesToRead]

    if len(tokens)==5:
      mfname = urllib.unquote(tokens[3]).decode('utf-8')
      if mfname=='describes':
        dfname = urllib.unquote(tokens[4]).decode('utf-8')
        dpid = self.getObjectPid(dfname)
        sysm = self.getSystemMetadata(dpid)
        if offset+numberOfBytesToRead>sysm.size:
          numberOfBytesToRead = sysm.size-offset
        data = self.get(dpid)
        return data[offset:offset+numberOfBytesToRead]

    raise IOError('Could not read specified file: %s', fileName)


  #TODO Not really sure what to do here...at the moment everything is virtual.
  # Everything is hard-coded right now just to get the idea across.  Mounting
  # as a network drive would solve this problem I think.
  def getDiskFreeSpace(self):
    return dict(freeBytesAvailable = 0x100000000L - 2048,
                totalNumberOfBytes = 0x100000000L,
                totalNumberOfFreeBytes = 0x100000000L - 2048)
  
  
  def getVolumeInformation(self):
    #logging.error('')
    fsFlags = (FILE_READ_ONLY_VOLUME
               | FILE_CASE_SENSITIVE_SEARCH 
               | FILE_CASE_PRESERVED_NAMES)
    return dict(volumeNameBuffer=u'DataONE Disk',
                maximumComponentLength=260,
                fileSystemFlags=fsFlags,
                fileSystemNameBuffer=u'DataONE File System')
                
  

def main():
  # set up argument parser
  parser = optparse.OptionParser('%prog [options] <mountPoint>')
  parser.add_option('-b', '--baseurl', dest='baseurl',
                    default=d1_common.const.URL_DATAONE_ROOT,
                    help='Base URL for dataONE services')
  parser.add_option('-f', '--filter', dest='filter', action='store',
                    type='string', default=None,
                    help='Filter for limiting view')
  parser.add_option('-l', '--loglevel', dest='llevel', default=20, type='int',
                    help='Reporting level: 10=Debug, 20=Info, 30=Warning, ' + \
                          '40=Error, 50=Fatal')
  parser.add_option('-d', '--debug', dest='debug', action='store_true',
                    default=False, help='Start pdb for debugging purposes')
  parser.add_option('-s', '--stderr', dest='stderr', action='store_true',
                    default=False, help='Display messages to stderr')
  parser.add_option('-t', '--threads', dest='threads', default=5,
                    type='int', help='Number of threads to use')
  parser.add_option('-u', '--unmount', dest='unmount', action='store_true',
                    default=False, help='Unmount the specified drive')
  #TODO add version option (see d1_fuse2.py)
  """parser.add_option('-v', '--version', dest='version', action='store_true',
                    help='Report current versions and exit.')"""
  #foreground vs background - running this as "pythonw d1_dokan.pyw" should 
  # take care of this problem
  
  # parse arguments
  (opts, args) = parser.parse_args()
  debug = opts.debug
  if opts.llevel not in [10, 20, 30, 40, 50]:
    opts.llevel = 20

  # format logging output
  format = '<%(levelname)s> %(module)s->%(funcName)s %(lineno)s: %(message)s '
  logging.basicConfig(format=format, level=opts.llevel)
  
  # check for proper thread count input
  if opts.threads < 0:
    opts.threads = 5
    
  # check for proper command syntax
  if len(args) < 1:
    logging.info('mountpoint argument is required')
    parser.print_help()
    sys.exit()

  #NOTE: mounts anywhere other than root level don't work
  #UPDATE: this seems to be a Windows issue since you can only specify volume
  # properties for a drive not a volume mounted to a mountpoint
  mountpoint = args[0]
  #directory = args[0]
  logging.debug('Starting Dokan driver')
  logging.debug('baseurl = %s' % opts.baseurl)
  logging.debug('filter = %s' % str(opts.filter))
  logging.debug('mountpoint = %s' % mountpoint)
        
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
  DriverOption = DOKAN_OPTION_KEEP_ALIVE #| DOKAN_OPTION_NETWORK
  if (opts.stderr):
    DriverOption |= DOKAN_OPTION_DEBUG | DOKAN_OPTION_STDERR 
  d1fs = dokan.Dokan(DataONEFS(baseurl=opts.baseurl,
                               filter_query=opts.filter),
                     mountpoint,
                     DriverOption,
                     0x19831116L,
                     opts.threads)
  
  if opts.unmount:
    # unmount the specified drive
    if not d1fs.dokanUnmount(mountpoint):
      logging.error("Failed to unmount DataONE drive")
  else:
    # start DataONE drive
    ret = d1fs.main()
    if (ret == -6):
      logging.error("Failed to mount DataONE drive: Bad mount point")
    elif (ret < 0):
      logging.error("Failed to mount DataONE drive")


if __name__ == '__main__':
  main()
