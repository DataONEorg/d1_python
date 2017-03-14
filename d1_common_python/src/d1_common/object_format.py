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
"""Utilities for handling the DataONE ObjectFormat and ObjectFormatList types
"""


def pyxb_to_dict(object_format_list_pyxb):
  """Return a dict representation of {object_format_list_pyxb}, keyed on
  formatId. E.g.:
  {
    u'-//ecoinformatics.org//eml-access-2.0.0beta4//EN': {
      'extension': u'xml',
      'format_name': u'Ecological Metadata Language, Access module, version 2.0.0beta4',
      'format_type': u'METADATA',
      'media_type': {
        'name': u'text/xml',
        'property_list': []
      }
    },
    u'-//ecoinformatics.org//eml-access-2.0.0beta6//EN': {
      'extension': u'xml',
      'format_name': u'Ecological Metadata Language, Access module, version 2.0.0beta6',
      'format_type': u'METADATA',
      'media_type': {
        'name': u'text/xml',
        'property_list': []}
      },
  }
  """
  f_dict = {}
  for f_pyxb in object_format_list_pyxb.objectFormat:
    d_dict = {
      'format_name': f_pyxb.formatName,
      'format_type': f_pyxb.formatType,
    }
    if getattr(f_pyxb, 'extension', False):
      d_dict['extension'] = f_pyxb.extension
    if getattr(f_pyxb, 'mediaType', False):
      d_dict['media_type'] = {
        'name': f_pyxb.mediaType.name,
        'property_list': [p for p in f_pyxb.mediaType.property_],
      }
    f_dict[f_pyxb.formatId] = d_dict

  return f_dict
