#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
:mod:`system_metadata`
======================

:Synopsis: Create System Meta documents based on session parameters.
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import logging

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# 3rd party.
import pyxb

# App.
from print_level import *
import cli_exceptions


class MissingSysmetaParameters(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class system_metadata():
  def __init__(self):
    pass

  def __repr__(self):
    return self.to_xml()

  def _get_missing_sysmeta_session_parameters(self, sysmeta):
    missing_values = []
    for k in sorted(sysmeta.keys()):
      if sysmeta[k][0] is None:
        missing_values.append(k)
    return missing_values

  def _assert_no_missing_sysmeta_session_parameters(self, sysmeta):
    missing_values = self._get_missing_sysmeta_session_parameters(sysmeta)
    if len(missing_values):
      msg = 'Missing system metadata parameters: {0}'.format(', '.join(missing_values))
      raise MissingSysmetaParameters(msg)

  def _create_pyxb_object(
    self, session, pid, size, checksum, access_policy, replication_policy
  ):
    sysmeta = dataoneTypes.systemMetadata()
    sysmeta.serialVersion = 1
    sysmeta.identifier = pid
    sysmeta.formatId = session.get('sysmeta', 'objectformat')
    sysmeta.size = size
    sysmeta.submitter = session.get('sysmeta', 'submitter')
    sysmeta.rightsHolder = session.get('sysmeta', 'rightsholder')
    sysmeta.checksum = dataoneTypes.checksum(checksum)
    sysmeta.checksum.algorithm = session.get('sysmeta', 'algorithm')
    sysmeta.dateUploaded = datetime.datetime.now()
    sysmeta.dateSysMetadataModified = datetime.datetime.now()
    sysmeta.originmn = session.get('sysmeta', 'originmn')
    sysmeta.authoritativemn = session.get('sysmeta', 'authoritativemn')
    sysmeta.accessPolicy = access_policy
    sysmeta.replicationPolicy = replication_policy
    #pyxb.RequireValidWhenGenerating(False)
    #print sysmeta.toxml()
    return sysmeta

  def create_pyxb_object(
    self, session, pid, size, checksum, access_policy, replication_policy
  ):
    self._assert_no_missing_sysmeta_session_parameters(session.session['sysmeta'])
    return self._create_pyxb_object(
      session, pid, size, checksum, access_policy, replication_policy
    )

  def to_xml(self):
    return self.to_pyxb().toxml()
