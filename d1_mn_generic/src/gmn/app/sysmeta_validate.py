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

"""Validate that System Metadata matches the corresponding science data object
"""

# D1.
import d1_common.checksum
import d1_common.types.exceptions


def validate_sysmeta_against_uploaded(request, sysmeta):
  if not 'HTTP_VENDOR_GMN_REMOTE_URL' in request.META:
    _validate_sysmeta_filesize(request, sysmeta)
    _validate_sysmeta_checksum(request, sysmeta)


def _validate_sysmeta_filesize(request, sysmeta):
  if sysmeta.size != request.FILES['object'].size:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0, u'Object size in System Metadata does not match that of the '
      u'uploaded object. sysmeta={} bytes, uploaded={} bytes'
        .format(sysmeta.size, request.FILES['object'].size)
    )


def _validate_sysmeta_checksum(request, sysmeta):
  h = _get_checksum_calculator(sysmeta)
  c = _calculate_object_checksum(request, h)
  if sysmeta.checksum.value().lower() != c.lower():
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'Checksum in System Metadata does not match that of the uploaded object. '
      u'sysmeta="{}", uploaded="{}"'
        .format(sysmeta.checksum.value().lower(), c.lower())
    )


def _get_checksum_calculator(sysmeta):
  try:
    return d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      sysmeta.checksum.algorithm
    )
  except LookupError:
    raise d1_common.types.exceptions.InvalidSystemMetadata(
      0,
      u'Checksum algorithm is unsupported. algorithm="{}"'
        .format(sysmeta.checksum.algorithm)
    )


def _calculate_object_checksum(request, checksum_calculator):
  for chunk in request.FILES['object'].chunks():
    checksum_calculator.update(chunk)
  return checksum_calculator.hexdigest()
