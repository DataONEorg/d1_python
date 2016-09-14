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
"""
:mod:`sysmeta_file`
===================

:Synopsis:
  Utilities for manipulating System Metadata files.

:Created: 2011-04-20
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

# Stdlib.
import datetime
import os

# Django.
from django.conf import settings

# 3rd party.
import pyxb

# D1.
import d1_common.date_time

# App.
import mn.util
import sysmeta_db
import sysmeta_base


def write_sysmeta_to_file(sysmeta_obj):
  """Write a PyXB System Metadata object to the System Metadata directory tree.
  """
  sysmeta_path = mn.util.file_path(
    settings.SYSMETA_STORE_PATH, sysmeta_obj.identifier.value(
    ), sysmeta_obj.serialVersion
  )
  mn.util.create_missing_directories(sysmeta_path)
  sysmeta_xml = sysmeta_base.serialize(sysmeta_obj)
  with open(sysmeta_path, 'wb') as f:
    f.write(sysmeta_xml)


def read_sysmeta_from_file(pid, serial_version):
  sysmeta_path = mn.util.file_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
  sysmeta_xml_str = open(sysmeta_path, 'rb').read()
  return sysmeta_xml_str


def delete_sysmeta_file(pid, serial_version):
  sysmeta_path = mn.util.file_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
  try:
    os.unlink(sysmeta_path)
  except EnvironmentError:
    pass


class SysMetaFile(object):
  """Manipulate SysMeta files in the SysMeta directory tree

  When a SysMeta file is updated, the old file is left untouched and a new
  file is created. The new file is written with a serial version that has been
  increased by one.

  Preconditions:
    - Exclusive access to the given PID must be ensured by the caller.

  Example:
    with SysMetaFile('mypid') as m:
      m.accessPolicy = access_policy
  """

  def __init__(self, pid, read_only=False):
    serial_version = self._get_and_lock_serial_version(pid)
    sysmeta_path = mn.util.file_path(settings.SYSMETA_STORE_PATH, pid, serial_version)
    self._read_only = read_only
    self._pid = pid
    with open(sysmeta_path, 'rb') as f:
      sysmeta_xml = f.read()
    self._sysmeta_obj = sysmeta_base.deserialize(sysmeta_xml)
    if not read_only:
      self._increment_serial_version()
      self._set_modified_datetime()

  def __enter__(self):
    return self._sysmeta_obj

  def __exit__(self, exc_type, exc_value, traceback):
    if not self._read_only:
      self._save_file()
    return False

  def _get_and_lock_serial_version(self, pid):
    """Get the serial version and lock it for the entire reminder of the
    implicit transaction covering the view. This prevents concurrent views from
    basing sysmeta file modifications on files that are already being modified,
    and thereby overwriting each other's modifications.
    """
    # TODO: I think select_for_update() makes it unnecessary to track
    # serial_version. Investigate.
    sci_obj = mn.models.ScienceObject.objects.select_for_update().get(
      pid__sid_or_pid=pid
    )
    return sci_obj.serial_version

  def _save_file(self):
    sysmeta_path = mn.util.file_path(
      settings.SYSMETA_STORE_PATH, self._pid, self._sysmeta_obj.serialVersion
    )
    with open(sysmeta_path, 'wb') as f:
      f.write(sysmeta_base.serialize(self._sysmeta_obj))

  def _set_modified_datetime(self):
    self._sysmeta_obj.dateSysMetadataModified = datetime.datetime.utcnow()

  def _increment_serial_version(self):
    self._sysmeta_obj.serialVersion += 1
