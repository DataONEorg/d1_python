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
"""Utilities for manipulating Series ID (SID)
"""

from __future__ import absolute_import

import gmn.app.auth
import gmn.app.util
import gmn.app.models
import gmn.app.sysmeta_util

# PyXB


def has_sid(sysmeta_pyxb):
  return get_sid(sysmeta_pyxb) is not None


def get_sid(sysmeta_pyxb):
  return gmn.app.sysmeta_util.get_value(sysmeta_pyxb, 'seriesId')


# Model


def is_sid(did):
  return gmn.app.models.SeriesIdToPersistentId.objects.filter(sid__did=did
                                                              ).exists()


def update_or_create_sid_to_pid_map(sid, pid):
  """Update existing or create a new {sid} to {pid} association. Then create
  or update the {sid} to resolve to the {pid}.

  Preconditions:
  - {sid} is verified to be unused if creating a standalone object (that may later become
  the first object in a chain).
  - {sid} is verified to belong to the given chain updating.
  - {pid} is verified to exist. E.g., with gmn.app.views.asserts.is_pid().
  """
  gmn.app.models.sid_to_pid(sid, pid)
  gmn.app.models.sid_to_head_pid(sid, pid)


def resolve_sid(sid):
  """Get the PID to which the {sid} currently maps.

  Preconditions:
  - {sid} is verified to exist. E.g., with gmn.app.views.asserts.is_sid().
  """
  return gmn.app.models.SeriesIdToHeadPersistentId.objects.get(
    sid__did=sid
  ).pid.did


def get_sid_by_pid(pid):
  """Get the SID to which the {pid} maps.
  This is the reverse of resolve.
  Return None if there is no SID maps to {pid}.
  """
  try:
    return gmn.app.models.SeriesIdToPersistentId.objects.get(
      pid__did=pid
    ).sid.did
  except gmn.app.models.SeriesIdToPersistentId.DoesNotExist:
    return None


#
# Private
#

# def move_sid_to_last_object_in_chain(pid):
#   """Move SID to the last object in a chain to which {pid} belongs.
#
#   - If the chain does not have a SID, do nothing.
#   - If the SID already maps to the last object in the chain, do nothing.
#
#   A SID always resolves to the last object in its chain. So System Metadata XML
#   docs are used for introducing SIDs and setting initial mappings, but the
#   database maintains the current mapping going forward.
#
#   Preconditions:
#   - PID is verified to exist. E.g., with gmn.app.views.asserts.is_pid().
#
#   Postconditions:
#   - The SID maps to the last object in the chain.
#   """
#   sid = sysmeta_db.get_sid_by_pid(pid)
#   if sid:
#     chain_pid_list = sysmeta_db.get_pids_in_revision_chain(pid)
#     update_sid(sid, chain_pid_list[-1])
