'''FUSE driver for a DataONE node

:Author: vieglais
:Date: 20100720

Implements a simple read only file system for DataONE infrastructure.

Currently just a proof of concept - only 10 entries are listed.

Example::

  $ ls
  README.txt  d1fuse.py  d1fuse.pyc  fuse.py    fuse.pyc  test_mount
  $ python d1fuse.py test_mount
  $ ls test_mount
  log meta object 
  $ ls -la test_mount/object
  total 176
  drwxr-xr-x  3 root  wheel      0 Jul 24 14:02 .
  drwxr-xr-x  3 root  wheel      0 Jul 24 14:02 ..
  -r--r--r--  1 root  wheel   3449 Jul 22 19:19 hdl%3A10255%2Fdryad.105%2Fmets.xml
  -r--r--r--  1 root  wheel  27985 Jul 22 19:19 hdl%3A10255%2Fdryad.105%2Fmets.xml_data
  -r--r--r--  1 root  wheel   3783 Jul 22 19:19 hdl%3A10255%2Fdryad.107%2Fmets.xml
  -r--r--r--  1 root  wheel  22220 Jul 22 19:19 hdl%3A10255%2Fdryad.107%2Fmets.xml_data
  -r--r--r--  1 root  wheel   3605 Jul 22 19:19 hdl%3A10255%2Fdryad.109%2Fmets.xml
  -r--r--r--  1 root  wheel   2511 Jul 22 19:19 hdl%3A10255%2Fdryad.109%2Fmets.xml_data
  -r--r--r--  1 root  wheel   3516 Jul 22 19:19 hdl%3A10255%2Fdryad.31%2Fmets.xml
  -r--r--r--  1 root  wheel   1969 Jul 22 19:19 hdl%3A10255%2Fdryad.31%2Fmets.xml_data
  -r--r--r--  1 root  wheel   2854 Jul 22 19:19 hdl%3A10255%2Fdryad.721%2Fmets.xml
  -r--r--r--  1 root  wheel   7365 Jul 22 19:19 hdl%3A10255%2Fdryad.721%2Fmets.xml_data
  
  $ cat test_mount/object/hdl%3A10255%2Fdryad.105%2Fmets.xml
  <?xml version="1.0" encoding="UTF-8"?>
  <mets:METS xmlns:mets="http://www.loc.gov/METS/" xmlns:xlink="http://www.w3.org/TR/xlink/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dim="http://www.dspace.org/xmlns/dspace/dim" OBJEDIT="/admin/item?itemID=112" OBJID="/handle/10255/dryad.105" PROFILE="DSPACE METS SIP Profile 1.0" LABEL="DSpace Item" ID="hdl:10255/dryad.105">
  <mets:dmdSec GROUPID="group_dmd_0" ID="dmd_1">
  <mets:mdWrap MDTYPE="OTHER" OTHERMDTYPE="DIM">
  <mets:xmlData>
  <dim:dim dspaceType="ITEM">
  <dim:field element="contributor" qualifier="author" language="" mdschema="dc">Burk, Angela</dim:field>
  <dim:field element="contributor" qualifier="author" language="" mdschema="dc">Westerman, Michael</dim:field>
  <dim:field element="contributor" qualifier="author" language="" mdschema="dc">Springer, Mark S.</dim:field>
  <dim:field element="date" qualifier="accessioned" language="" mdschema="dc">2008-03-19T19:50:32Z</dim:field>
  ...

  $ umount test_mount
  $ ls test_mount
  $

If you get an exception on OSX that looks like this::

  OSError: dlopen(/opt/local/lib/libfuse.dylib, 6): Symbol not found: _iconv
    Referenced from: /opt/local/lib/libfuse.dylib

Run d1fuse with::

  export DYLD_LIBRARY_PATH=/usr/lib:$DYLD_LIBRARY_PATH
'''

from errno import ENOENT, EACCES
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time, mktime
import os
import urllib
import fuse

from d1pythonitk import client

#from fuse import FUSE, Operations, LoggingMixIn

O_ACCMODE = 3
TARGET_NODE = "http://dev-dryad-mn.dataone.org/mn"


class DataOneFS(fuse.Operations):
  def __init__(self):
    self.client = client.DataOneClient(TARGET_NODE)
    #get the first 100 objects from the target
    self._refresh()
    self._objectcache = {}
    #self.file_path = "/hello.txt"
    #self.file_contents = "Hello world!\n"

  def _refresh(self):
    self._objects = self.client.listObjects(count=10)
    self._logrecs = self.client.getLogRecords(count=10)
    self.objects = {}
    for obj in self._objects.objectInfo:
      self.objects[str(urllib.quote(obj.identifier, ''))] = [
        obj.size, obj.dateSysMetadataModified, obj.identifier
      ]

  def getattr(self, path, fh=None):
    """Returns a dictionary with keys identical to the stat C structure
    of stat(2). st_atime, st_mtime and st_ctime should be floats.
    On OSX, st_nlink should count all files inside the directory.
    On Linux, only the subdirectories are counted.
    /log
    /object
    /meta
    """
    now = time()
    if path in ["/", "/log", "/meta", "/object"]:
      return dict(
        st_mode=(
          S_IFDIR | 0755
        ), st_ctime=now,
        st_mtime=now,
        st_atime=now,
        st_nlink=3
      )
    split0 = os.path.split(path)
    if split0[1] == '':
      return dict(
        st_mode=(
          S_IFDIR | 0755
        ), st_ctime=now,
        st_mtime=now,
        st_atime=now,
        st_nlink=3
      )
    if split0[0] == "/object":
      identifier = split0[1]
      if identifier in self.objects.keys():
        return dict(
          st_mode=(S_IFREG | 0444),
          st_size=self.objects[identifier][0], st_ctime=now, st_mtime=mktime(
            self.objects[identifier][1].timetuple(
            )
          ), st_atime=now, st_nlink=1
        )
    else:
      raise OSError(ENOENT, "")

  def open(self, path, flags):
    split0 = os.path.split(path)
    if split0[0] in ["/object", "/meta"]:
      if split0[1] not in self.objects.keys():
        raise OSError(ENOENT, "")
    if (flags & O_ACCMODE) != os.O_RDONLY:
      raise OSError(EACCES, "")
    return 0

  def readdir(self, path, fh):
    """Can return either a list of names, or a list of (name, attrs, offset)
    tuples. attrs is a dict as in getattr.
    """
    if path == "/":
      return [".", "..", "log", "meta", "object"]
    if path in ["/object", "/object/", "/meta", "/meta/"]:
      res = [".", "..", ] + self.objects.keys()
      return res
    raise OSError(ENOENT, "")

  def read(self, path, size, offset, fh):
    split0 = os.path.split(path)
    if split0[0] == "/object":
      identifier = split0[1]
      if identifier not in self.objects.keys():
        raise OSError(EACCESS, "")
      if offset + size > self.objects[identifier][0]:
        size = self.objects[identifier][0] - offset
      if identifier not in self._objectcache.keys():
        self._objectcache[identifier] = self.client.get(self.objects[identifier][2]).read(
        )
      return self._objectcache[identifier][offset:offset + size]
    raise OSError(EACCESS, "")


if __name__ == "__main__":
  if len(argv) < 2:
    print 'usage: %s <node> <mountpoint>' % argv[0]
    exit(1)
  mountpoint = argv[1]
  if len(argv) > 2:
    TARGET_NODE = argv[1]
    mountpoint = argv[2]
  fusehandler = fuse.FUSE(DataOneFS(), mountpoint, foreground=False)
