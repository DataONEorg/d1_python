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
:mod:`sysmeta_validate`
=======================

:Synopsis:
  Validate that system metadata matches the corresponding science data object.
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime

# D1.
import d1_common.checksum
import d1_common.types.exceptions

# App.
import service.settings


def validate_sysmeta_against_uploaded(request, pid, sysmeta):
  _validate_sysmeta_identifier(pid, sysmeta)
  if not 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    _validate_sysmeta_filesize(request, sysmeta)
    _validate_sysmeta_checksum(request, sysmeta)


def _validate_sysmeta_identifier(pid, sysmeta):
  if sysmeta.identifier.value() != pid:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'PID in System Metadata does not match that of the URL'
    )


def _validate_sysmeta_filesize(request, sysmeta):
  if sysmeta.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Object size in System Metadata ({0} bytes) does not match that of the '
      'uploaded object ({1} bytes)'.format(sysmeta.size, request.FILES['object'].size)
    )


def _validate_sysmeta_checksum(request, sysmeta):
  h = _get_checksum_calculator(sysmeta)
  c = _calculate_object_checksum(request, h)
  if sysmeta.checksum.value().lower() != c.lower():
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Checksum in System Metadata does not match that of the uploaded object'
    )


def _get_checksum_calculator(sysmeta):
  try:
    return d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      sysmeta.checksum.algorithm
    )
  except LookupError:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, 'Checksum algorithm is unsupported: {0}'.format(sysmeta.checksum.algorithm)
    )


def _calculate_object_checksum(request, checksum_calculator):
  for chunk in request.FILES['object'].chunks():
    checksum_calculator.update(chunk)
  return checksum_calculator.hexdigest()


def update_sysmeta_with_mn_values(request, sysmeta):
  sysmeta.submitter = request.primary_subject
  sysmeta.originMemberNode = service.settings.NODE_IDENTIFIER
  # If authoritativeMemberNode is not specified, set it to this MN.
  if sysmeta.authoritativeMemberNode is None:
    sysmeta.authoritativeMemberNode = service.settings.NODE_IDENTIFIER
  now = datetime.datetime.utcnow()
  sysmeta.dateUploaded = now
  sysmeta.dateSysMetadataModified = now
  sysmeta.serialVersion = 1
