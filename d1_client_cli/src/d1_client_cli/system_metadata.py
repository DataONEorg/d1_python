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
:mod:`system_metadata`
======================

:Synopsis: Create System Meta documents based on session parameters.
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import datetime
import sys

# D1.
try:
  import d1_common.types.generated.dataoneTypes as dataoneTypes
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# 3rd party.

# App.
from print_level import * #@UnusedWildImport
from const import * #@UnusedWildImport


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

  def _get_missing_sysmeta_session_parameters(
    self, sysmeta, formatId=None, algorithm=None
  ):
    missing_values = []
    for k in sorted(sysmeta.keys()):
      if sysmeta[k][0] is None:
        if k == CHECKSUM_name and algorithm is not None:
          continue
        if k == FORMAT_name and formatId is not None:
          continue
        missing_values.append(k)
    return missing_values

  def _assert_no_missing_sysmeta_session_parameters(
    self, sysmeta, formatId=None, algorithm=None
  ):
    missing_values = self._get_missing_sysmeta_session_parameters(
      sysmeta, formatId, algorithm
    )
    if len(missing_values):
      msg = 'Missing system metadata parameters: {0}'.format(', '.join(missing_values))
      raise MissingSysmetaParameters(msg)

  def _create_pyxb_object(
    self, session, pid, size, checksum, access_policy, replication_policy, formatId,
    algorithm
  ):
    # Fix arguments.
    _formatId = formatId
    if _formatId is None:
      _formatId = session.get(FORMAT_sect, FORMAT_name)
    _algorithm = algorithm
    if _algorithm is None:
      _algorithm = session.get(CHECKSUM_sect, CHECKSUM_name)

    sysmeta = dataoneTypes.systemMetadata()
    sysmeta.serialVersion = 1
    sysmeta.identifier = pid
    sysmeta.formatId = _formatId
    sysmeta.size = size
    sysmeta.submitter = session.get(SUBMITTER_sect, SUBMITTER_name)
    sysmeta.rightsHolder = session.get(OWNER_sect, OWNER_name)
    sysmeta.checksum = dataoneTypes.checksum(checksum)
    sysmeta.checksum.algorithm = _algorithm
    sysmeta.dateUploaded = datetime.datetime.utcnow()
    sysmeta.dateSysMetadataModified = datetime.datetime.utcnow()
    sysmeta.originmn = session.get(ORIG_MN_sect, ORIG_MN_name)
    sysmeta.authoritativemn = session.get(AUTH_MN_sect, AUTH_MN_name)
    sysmeta.accessPolicy = access_policy
    sysmeta.replicationPolicy = replication_policy
    #pyxb.RequireValidWhenGenerating(False)
    #print sysmeta.toxml()
    return sysmeta

  def create_pyxb_object(
    self,
    session,
    pid,
    size,
    checksum,
    access_policy,
    replication_policy,
    formatId=None,
    algorithm=None
  ):
    self._assert_no_missing_sysmeta_session_parameters(
      session.session['sysmeta'], formatId, algorithm
    )
    return self._create_pyxb_object(
      session, pid, size, checksum, access_policy, replication_policy, formatId, algorithm
    )

  def to_xml(self):
    return self.to_pyxb().toxml()
