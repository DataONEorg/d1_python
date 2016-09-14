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
"""Utilities for manipulating System Metadata PyXB objects.
"""
# DataONE APIs.
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v1_1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions


def deserialize(sysmeta_xml):
  if not isinstance(sysmeta_xml, unicode):
    try:
      sysmeta_xml = sysmeta_xml.decode('utf8')
    except UnicodeDecodeError as e:
      raise d1_common.types.exceptions.InvalidRequest(
        0,
        u'The System Metadata XML doc is not valid UTF-8 encoded Unicode. '
        u'error="{}", xml="{}"'.format(str(e), sysmeta_xml)
      )
  try:
    return d1_common.types.dataoneTypes_v2_0.CreateFromDocument(sysmeta_xml)
  except pyxb.ValidationError as e:
    err_str = e.details()
  except pyxb.PyXBException as e:
    err_str = str(e)
  raise d1_common.types.exceptions.InvalidSystemMetadata(
    0,
    u'System Metadata XML doc validation failed. error="{}", xml="{}"'
      .format(err_str, sysmeta_xml)
  )


def serialize(sysmeta_obj):
  return sysmeta_obj.toxml().encode('utf-8')


def get_value(sysmeta_obj, sysmeta_attr):
  try:
    return getattr(sysmeta_obj, sysmeta_attr).value()
  except (ValueError, AttributeError):
    return None

