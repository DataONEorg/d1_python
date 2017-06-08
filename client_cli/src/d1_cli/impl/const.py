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
"""Constants (mostly names of things}.
"""


class SessionVariable(object):
  def __init__(self, sect, name):
    self.sect = sect
    self.name = name


# REST URLs
REST_Version = u'v1'
REST_URL_Get = u'object'

# Science Metadata types - this should be pulled from the list.
ALLOWABLE_SCIMETA_TYPES = (
  u'eml://ecoinformatics.org/eml-2.0.0', u'eml://ecoinformatics.org/eml-2.0.1',
  u'eml://ecoinformatics.org/eml-2.1.0', u'eml://ecoinformatics.org/eml-2.1.1',
  u'FGDC-STD-001-1998', u'FGDC-STD-001.1-1999', u'FGDC-STD-001.2-1999',
)
