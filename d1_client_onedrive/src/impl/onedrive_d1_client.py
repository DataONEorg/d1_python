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
''':mod:`onedrive_d1_client`
============================

:Synopsis:
 - Interact with the DataONE infrastructure.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging

# D1.
import d1_common
import d1_client.cnclient_1_1
import d1_client.mnclient

# App.
import settings

# Set up logger for this module.
log = logging.getLogger(__name__)


class D1Client(object):
  def __init__(self, base_url=settings.DATAONE_ROOT):
    self.client = d1_client.cnclient_1_1.CoordinatingNodeClient(base_url=base_url)
    self.query_engine_description = None
    self.all_facet_names = None

  def get_all_searchable_facet_names(self):
    if self.all_facet_names is not None:
      return self.all_facet_names
    if self.query_engine_description is None:
      self.init_query_engine_description()
    self.all_facet_names = []
    for f in self.query_engine_description.queryField:
      if f.searchable == True:
        self.all_facet_names.append(f.name)
    return self.all_facet_names

  def get_unapplied_facet_names(self, applied_facets):
    all_facet_names = set(self.get_all_searchable_facet_names())
    applied_facets = self.facet_path_parser.undecorate_facets(path)
    applied_facet_names = set(
      [
        self.facet_path_parser.undecorate_facet_name(
          f[0]
        ) for f in applied_facets
      ]
    )
    #return [self.facet_path_parser.decorate_facet_name(n) for n in
    #        all_facet_names - applied_facet_names]
    return all_facet_names - applied_facet_names

  def init_query_engine_description(self):
    self.query_engine_description = self.client.getQueryEngineDescription('solr')

# USED
################################################################################
# UNUSED

  def get_science_object(self, pid):
    try:
      return self.objectcache[pid]
    except:
      logging.info('get_object: Cache miss on PID {0}'.format(pid))
    self.objectcache[pid] = d1_client.d1client.DataONEObject(pid, cnBaseUrl=self.base_url)
    return self.objectcache[pid]

  def get_system_metadata(self, pid):
    try:
      return self.sysmetacache[pid]
    except:
      logging.info('get_system_metadata: Cache miss on PID {0}'.format(pid))
    obj = self.get_object(pid)
    sysm = obj.get_system_metadata()
    self.sysmetacache[pid] = sysm
    return self.sysmetacache[pid]

  def get_object_filename(self, pid):
    '''Get filename for object. Filename format is pid.ext. Ext is looked up
    in object format map.
    '''
    sysm = self.get_system_metadata(pid)
    ofmt = sysm.formatId
    extension = getExtensionFromObjectFormat(ofmt)
    filename = pid + extension
    return filename

  def get_object_pid(self, filename):
    '''Get pid from filename. Filename format is pid.ext.
    :param filename: Name of file for which to get PID
    :type filename: str
    :return: object identifier
    :rtype: DataONE Persistent ID
    '''
    return filename[:filename.rfind('.')]

  def get(self, pid):
    '''Get object bytes.
    '''
    try:
      return self.datacache[pid]
    except:
      logging.info('get: Cache miss on PID {0}'.format(pid))
    obj = self.get_object(pid)
    self.datacache[pid] = obj.get().read()
    return self.datacache[pid]
