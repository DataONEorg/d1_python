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
"""Utilities for Science Metadata
"""

import d1_scimeta.xml_schema

import d1_common.const
import d1_common.date_time
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_common.wrap.access_policy
import d1_common.xml

import django.conf


def assert_valid(sysmeta_pyxb, sciobj_path):
  """Validate file at {sciobj_path} against schema selected via formatId and
  raise InvalidRequest if invalid

  Validation is only performed when:

  - SciMeta validation is enabled
  - and Object size is below size limit for validation
  - and formatId designates object as a Science Metadata object which is recognized
    and parsed by DataONE CNs
  - and XML Schema (XSD) files for formatId are present on local system
  """
  if not (
      _is_validation_enabled() and
      _is_installed_scimeta_format_id(sysmeta_pyxb)
  ):
    return

  if _is_above_size_limit(sysmeta_pyxb):
    if _is_action_accept():
      return
    else:
      raise d1_common.types.exceptions.InvalidRequest(
        0, 'Science Metadata file is above size limit for validation and this '
        'node has been configured to reject unvalidated Science Metadata '
        'files. For more information, see the SCIMETA_VALIDATE* settings. '
        'size={} size_limit={}'.format(
          sysmeta_pyxb.size, django.conf.settings.SCIMETA_VALIDATION_MAX_SIZE
        )
      )

  with open(sciobj_path, 'rb') as f:
    try:
      d1_scimeta.xml_schema.validate(sysmeta_pyxb.formatId, f.read())
    except d1_scimeta.xml_schema.SciMetaValidationError as e:
      raise d1_common.types.exceptions.InvalidRequest(0, str(e))


def _is_validation_enabled():
  return django.conf.settings.SCIMETA_VALIDATION_ENABLED


def _is_installed_scimeta_format_id(sysmeta_pyxb):
  return d1_scimeta.xml_schema.is_installed_scimeta_format_id(
    sysmeta_pyxb.formatId
  )


def _is_above_size_limit(sysmeta_pyxb):
  return (
    django.conf.settings.SCIMETA_VALIDATION_MAX_SIZE == -1 or
    sysmeta_pyxb.size > django.conf.settings.SCIMETA_VALIDATION_MAX_SIZE
  )


def _is_action_accept():
  return django.conf.settings.SCIMETA_VALIDATION_OVER_SIZE_ACTION == 'accept'
