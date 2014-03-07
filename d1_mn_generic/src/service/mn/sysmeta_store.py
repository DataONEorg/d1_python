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
'''
:mod:`sysmeta`
==============

:Synopsis:
  Utilities for manipulating System Metadata documents.

:Created: 2011-04-20
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import datetime
import os

# D1.
import d1_common.date_time
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions

# App.
import settings
import mn.util


def write_sysmeta_to_store(sysmeta_pyxb):
  '''Write a PyXB System Metadata object to the System Metadata store.
  '''
  sysmeta_path = mn.util.store_path(
    settings.SYSMETA_STORE_PATH, sysmeta_pyxb.identifier.value(),
    sysmeta_pyxb.serialVersion
  )
  mn.util.create_missing_directories(sysmeta_path)
  sysmeta_xml = sysmeta_pyxb.toxml().encode('utf-8')
  with open(sysmeta_path, 'wb') as f:
    f.write(sysmeta_xml)


def read_sysmeta_from_store(pid, serial_version):
  # Return the raw bytes of the object in chunks.
  file_in_path = mn.util.store_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
  # Can't use "with".
  f = open(file_in_path, 'rb')
  return mn.util.fixed_chunk_size_iterator(f)


def delete_sysmeta_from_store(pid, serial_version):
  sysmeta_path = mn.util.store_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
  try:
    os.unlink(sysmeta_path)
  except EnvironmentError:
    pass


class sysmeta():
  '''Manipulate SysMeta files in the SysMeta store.

  When a SysMeta file is updated, the old file is left untouched and a new
  file is created. The new file is written with a serial version that has been
  increased by one, as compared to the old serial version.

  Preconditions:
    - Exclusive access to the given PID must be ensured by the caller.

  Example:
    with sysmeta('mypid') as m:
      m.accessPolicy = access_policy
  '''

  def __init__(self, pid, serial_version, read_only=False):
    sysmeta_path = mn.util.store_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
    self.read_only = read_only
    self.pid = pid
    with open(sysmeta_path, 'rb') as f:
      sysmeta_xml = f.read()
    # SysMeta is stored in UTF-8 and CreateFromDocument() does not handle
    # native Unicode objects, so the SysMeta is passed to CreateFromDocument()
    # as UTF-8.
    self.sysmeta_pyxb = dataoneTypes.CreateFromDocument(sysmeta_xml)
    if not read_only:
      self._increment_serial_version()

  def __enter__(self):
    return self.sysmeta_pyxb

  def __exit__(self, exc_type, exc_value, traceback):
    if not self.read_only:
      self._save_file_to_store()
    return False

  def _save_file_to_store(self):
    self._set_modified_datetime()
    sysmeta_path = mn.util.store_path(
      settings.SYSMETA_STORE_PATH, self.pid, self.sysmeta_pyxb.serialVersion
    )
    with open(sysmeta_path, 'wb') as f:
      f.write(self.sysmeta_pyxb.toxml().encode('utf-8'))

  def _set_modified_datetime(self):
    timestamp = d1_common.date_time.utc_now()
    self.sysmeta_pyxb.dateSysMetadataModified = \
      datetime.datetime.isoformat(timestamp)

  def _increment_serial_version(self):
    self.sysmeta_pyxb.serialVersion += 1
