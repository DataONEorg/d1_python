#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
#
# Licensed under the Apache License, Version 2.0 (the "License"};
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
:mod:`const`
==============

:Synopsis: Constants (mostly names of things}.
:Created: 2012-04-03
:Author: DataONE (Pippin}
'''


class SessionVariable(object):
  def __init__(self, sect, name):
    self.sect = sect
    self.name = name

# Identifiers for names, in case they change again (i.e. object-format to format-id}.
SECTION_cli = 'cli'
SECTION_node = 'node'
SECTION_slice = 'slice'
SECTION_auth = 'auth'
SECTION_sysmeta = 'sysmeta'
SECTION_search = 'search'

PRETTY_sect = SECTION_cli
PRETTY_name = 'pretty'
VERBOSE_sect = SECTION_cli
VERBOSE_name = 'verbose'
CN_URL_sect = SECTION_node
CN_URL_name = 'dataone-url'
MN_URL_sect = SECTION_node
MN_URL_name = 'mn-url'
START_sect = SECTION_slice
START_name = 'start'
COUNT_sect = SECTION_slice
COUNT_name = 'count'
ANONYMOUS_sect = SECTION_auth
ANONYMOUS_name = 'anonymous'
CERT_FILENAME_sect = SECTION_auth
CERT_FILENAME_name = 'cert-file'
KEY_FILENAME_sect = SECTION_auth
KEY_FILENAME_name = 'key-file'
FORMAT_sect = SECTION_sysmeta
FORMAT_name = 'format-id'
SUBMITTER_sect = SECTION_sysmeta
SUBMITTER_name = 'submitter'
OWNER_sect = SECTION_sysmeta
OWNER_name = 'rights-holder'
ORIG_MN_sect = SECTION_sysmeta
ORIG_MN_name = 'origin-mn'
AUTH_MN_sect = SECTION_sysmeta
AUTH_MN_name = 'authoritative-mn'
CHECKSUM_sect = SECTION_sysmeta
CHECKSUM_name = 'algorithm'
FROM_DATE_sect = SECTION_search
FROM_DATE_name = 'from-date'
TO_DATE_sect = SECTION_search
TO_DATE_name = 'to-date'
SEARCH_FORMAT_sect = SECTION_search
SEARCH_FORMAT_name = 'search-format-id'
QUERY_ENGINE_sect = SECTION_search
QUERY_ENGINE_name = 'query-type'
QUERY_STRING_sect = SECTION_search
QUERY_STRING_name = 'query'

ALLOWABLE_SCIMETA_TYPES = (
  'eml://ecoinformatics.org/eml-2.0.0',
  'eml://ecoinformatics.org/eml-2.0.1',
  'eml://ecoinformatics.org/eml-2.1.0',
  'eml://ecoinformatics.org/eml-2.1.1',
  'FGDC-STD-001-1998',
  'FGDC-STD-001.1-1999',
  'FGDC-STD-001.2-1999',
)
