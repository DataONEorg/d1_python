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
''':mod:`command_processor`
===========================

:Synopsis:
 - Interface to the backends.
:Author:
 - DataONE (Dahl)
'''

# Stdlib.
import logging
import os
import re

# App.
import onedrive_d1_client
import onedrive_solr_client
import settings

# Set up logger for this module.
log = logging.getLogger(__name__)


class CommandProcessor(object):
  def __init__(self):
    self.d1_client = onedrive_d1_client.D1Client()
    self.solr_client = onedrive_solr_client.SolrClient()
    self.fields_good_for_faceting = self.init_field_names_good_for_faceting()

  def solr_query(self, applied_facets=None):
    self.solr_client = onedrive_solr_client.SolrClient()
    if applied_facets is None:
      applied_facets = []
    #log.debug('Fields good for faceting: {0}'.format(self.fields_good_for_faceting))
    return self.solr_client.faceted_search(self.fields_good_for_faceting, applied_facets)

  def get_all_field_names_good_for_faceting(self):
    return self.fields_good_for_faceting

  def init_field_names_good_for_faceting(self):
    candidate_facet_names = \
      self.d1_client.get_all_searchable_and_returnable_facet_names()
    good = []
    for f in candidate_facet_names:
      if not self.facet_matches_filter(f):
        good.append(f)
    return good

  def facet_matches_filter(self, facet_name):
    for regex in settings.FACET_FILTER:
      if re.match(regex, facet_name):
        return True
    return False
