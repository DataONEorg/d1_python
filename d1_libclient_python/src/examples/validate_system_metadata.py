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
"""
:mod:`validate_system_metadata`
===============================

:Synopsis:
  Check basic availability and correctness of the Science Objects and System
  Metadata available on a CN or MN.

  This is an example on how to use the DataONE Client Library for Python. It
  shows how to:

  - Iterate over all objects that are available on a CN or MN when
    authenticating with a specific certificate.
  - Work around System Metadata issues that cause validation errors.
  - Compare the size and checksum recorded in an object's System Metadata with
    the actual size and checksum of the object.

:Author:
  DataONE (Dahl, Servilla)

:Created:
  2014-08-14

:Requires:
  - Python 2.7.
  - DataONE Common Library for Python (automatically installed as a dependency)
  - DataONE Client Library for Python (sudo pip install dataone.libclient)
  - A client side certificate that is trusted by the target Member Node.
"""

# Future
from __future__ import print_function

# Stdlib
import csv
import sys

# 3rd party
import pyxb

# DataONE.
import d1_client.mnclient
import d1_client.objectlistiterator
import d1_common.checksum
import d1_common.types.generated.dataoneTypes as dataone_types
import d1_common.types.exceptions

CSV_FILE_PATH = './validation_results.csv'
BASE_URL = None # e.g., https://tropical.lternet.edu/knb/d1/mn/
CERTIFICATE_PATH = None
CERTIFICATE_KEY_PATH = None


def main():
  mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
    BASE_URL, cert_path=CERTIFICATE_PATH, key_path=CERTIFICATE_KEY_PATH
  )
  with DataONENodeObjectValidator(mn_client, CSV_FILE_PATH) as mn_validator:
    # Validate all PIDs that are accessible with certificate on MN or CN.
    mn_validator.validate()
    # Validating a single PID.
    # mn_validator.validate_pid('doi:10.6073/AA/cce.155.1')


class DataONENodeObjectValidator(object):
  def __init__(self, mn_client, csv_file_path):
    self._src_client = mn_client
    self._csv_file = csv.writer(open(csv_file_path, 'wb'))
    self._counts = {}

  def __enter__(self):
    self._csv_file.writerow([
      'status', 'pid', 'sys_meta_size', 'sys_meta_checksum', 'actual_size',
      'actual_checksum'
    ])
    return self

  def __exit__(self, type, value, traceback):
    self._print_status()

  def validate(self):
    for o in d1_client.objectlistiterator.ObjectListIterator(self._src_client):
      pid = o.identifier.value()
      self.validate_pid(pid)

  def validate_pid(self, pid):
    try:
      self._validate_pid(pid)
    except ValidationError:
      self._inc_count('Objects failed validation')
    else:
      self._inc_count('Objects passed validation')
    self._inc_count('Objects checked')

  def _validate_pid(self, pid):
    sys_meta = self._read_sys_meta_with_correction(pid)
    sci_obj = self._read_obj(pid)
    checksum = d1_common.checksum.calculate_checksum(
      sci_obj, sys_meta.checksum.algorithm
    )
    errors = []
    if checksum != sys_meta.checksum.value():
      self._inc_count('Checksum mismatches')
      errors.append('checksum_mismatch')
    if len(sci_obj) != sys_meta.size:
      self._inc_count('Size mismatches')
      errors.append('size_mismatch')
    if errors:
      self._write_csv_row(
        pid, '/'.join(errors), sys_meta.size,
        sys_meta.checksum.value(), len(sci_obj), checksum
      )
      raise ValidationError()
    else:
      self._write_csv_row(
        pid, 'ok', sys_meta.size,
        sys_meta.checksum.value(), len(sci_obj), checksum
      )

  def _read_obj(self, pid):
    try:
      return self._src_client.get(pid).read()
    except d1_common.types.exceptions.DataONEException:
      self._inc_count('Science Object Read errors')
      self._write_csv_row(pid, 'sci_obj_read_error')
      raise ValidationError()

  def _read_sys_meta(self, pid):
    try:
      return self._src_client.getSystemMetadata(pid)
    except (d1_common.types.exceptions.NotAuthorized):
      self._inc_count('System Metadata Not Authorized error')
      self._write_csv_row(pid, 'sys_meta_not_authorized_error')
      raise NotAuthorized()
    except (
        d1_common.types.exceptions.DataONEException,
        pyxb.UnrecognizedDOMRootNodeError
    ):
      self._inc_count('System Metadata Read errors (before correction)')
      raise ValidationError()

  def _read_sys_meta_with_correction(self, pid):
    try:
      return self._read_sys_meta(pid)
    except NotAuthorized:
      raise ValidationError()
    except ValidationError:
      sys_meta_str = self._src_client.getSystemMetadataResponse(pid).read()
      sys_meta_str = sys_meta_str.replace('<preferredMemberNode/>', '')
      sys_meta_str = sys_meta_str.replace(
        '<preferredMemberNode></preferredMemberNode>', ''
      )
      sys_meta_str = sys_meta_str.replace('<accessPolicy/>', '')
      sys_meta_str = sys_meta_str.replace('<blockedMemberNode/>', '')
      sys_meta_str = sys_meta_str.replace(
        '<blockedMemberNode></blockedMemberNode>', ''
      )
      try:
        return dataone_types.CreateFromDocument(sys_meta_str)
      except (d1_common.types.exceptions.DataONEException, pyxb.PyXBException):
        self._inc_count('System Metadata Read errors (after correction)')
        self._write_csv_row(pid, 'sys_meta_read_error')
        raise ValidationError()

  def _inc_count(self, name):
    try:
      self._counts[name] += 1
    except KeyError:
      self._counts[name] = 1

  def _write_csv_row(
      self, pid, status, sys_meta_size=None, sys_meta_checksum=None,
      actual_size=None, actual_checksum=None
  ):
    self._csv_file.writerow([
      status, pid, sys_meta_size, sys_meta_checksum, actual_size,
      actual_checksum
    ])

  def _print_status(self):
    for c in sorted(self._counts):
      print('{}: {}'.format(c, self._counts[c]), file=sys.stderr)


class ValidationError(Exception):
  pass


class NotAuthorized(Exception):
  pass


if __name__ == '__main__':
  main()
