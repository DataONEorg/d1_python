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
"""Utilities for manipulating revision chains in the database
"""

from __future__ import absolute_import

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.models
import d1_gmn.app.util

import d1_common.xml

# PyXB


def has_sid(sysmeta_pyxb):
  return get_sid(sysmeta_pyxb) is not None


def get_sid(sysmeta_pyxb):
  return d1_common.xml.get_value(sysmeta_pyxb, 'seriesId')


# DB updates


def create_chain(sid, pid):
  """Create the initial chain structure for a new standalone object. Intended to
  be called in MNStorage.create().

  Preconditions:
  - {sid} must either be None or be previously unused.
    d1_gmn.app.views.asserts.is_unused()
  - {pid} must exist and be verified to be a PID.
    d1_gmn.app.views.asserts.is_pid()
  """
  sid_model = d1_gmn.app.models.did(sid) if sid else None
  pid_model = d1_gmn.app.models.did(pid)
  chain_model = d1_gmn.app.models.ChainIdToSeriesID(
    sid=sid_model, head_pid=pid_model
  )
  chain_model.save()
  pid_to_chain_model = d1_gmn.app.models.PersistentIdToChainID(
    chain=chain_model, pid=pid_model
  )
  pid_to_chain_model.save()


def add_pid_to_chain(sid, old_pid, new_pid):
  """Add a new revision {new_pid} to the chain that {old_pid} belongs to and
  update any SID to resolve to the new PID. Intended to be called in
  MNStorage.update().

  Preconditions:
  - {sid} must either be None or match the SID already assigned to the chain.
  - Both {old_pid} and {new_pid} must exist and be verified to be PIDs
    d1_gmn.app.views.asserts.is_pid()
  """
  old_pid_to_chain_model = d1_gmn.app.models.PersistentIdToChainID.objects.get(
    pid__did=old_pid
  )
  new_pid_to_chain_model = d1_gmn.app.models.PersistentIdToChainID(
    chain=old_pid_to_chain_model.chain,
    pid=d1_gmn.app.models.IdNamespace.objects.get(did=new_pid)
  )
  new_pid_to_chain_model.save()

  if sid:
    chain_model = d1_gmn.app.models.ChainIdToSeriesID.objects.get(sid__did=sid)
    assert chain_model.sid is None or chain_model.sid.did == sid, \
      'Cannot change SID for existing chain'
    chain_model.sid = d1_gmn.app.models.did(sid)
    chain_model.save()


def update_sid_to_head_pid_map(pid):
  """Set SID to resolve to the head of the chain to which {pid} belongs. If SID
  has not been set for chain, does nothing. Intended to be called in
  MNStorage.delete().

  Preconditions:
  - {pid} must exist and be verified to be a PID.
    d1_gmn.app.views.asserts.is_pid()
  """
  sci_model = d1_gmn.app.util.get_sci_model(pid)
  while sci_model.obsoleted_by is not None:
    sci_model = d1_gmn.app.util.get_sci_model(sci_model.obsoleted_by.did)
  chain_model = d1_gmn.app.models.PersistentIdToChainID.objects.get(
    pid__did=pid
  ).chain
  chain_model.head_pid = sci_model.pid
  chain_model.save()


def delete_chain(pid):
  """"""
  pid_to_chain_model = d1_gmn.app.models.PersistentIdToChainID.objects.get(
    pid__did=pid
  )
  chain_model = pid_to_chain_model.chain
  pid_to_chain_model.delete()
  if not d1_gmn.app.models.PersistentIdToChainID.objects.filter(
      chain=chain_model,
  ).exists():
    if chain_model.sid:
      # Cascades back to chain_model.
      d1_gmn.app.models.IdNamespace.objects.filter(did=chain_model.sid.did
                                                   ).delete()
    else:
      chain_model.delete()


def set_revision(pid, obsoletes_pid=None, obsoleted_by_pid=None):
  sciobj_model = d1_gmn.app.util.get_sci_model(pid)
  set_revision_by_model(sciobj_model, obsoletes_pid, obsoleted_by_pid)
  sciobj_model.save()


def set_revision_by_model(sciobj_model, obsoletes_pid, obsoleted_by_pid):
  if obsoletes_pid:
    sciobj_model.obsoletes = d1_gmn.app.models.did(obsoletes_pid)
  if obsoleted_by_pid:
    sciobj_model.obsoleted_by = d1_gmn.app.models.did(obsoleted_by_pid)


# Cut


def cut_from_chain(sciobj_model):
  """Remove an object from a revision chain.

  Preconditions:
  - The object with the pid is verified to exist and to be a member of an
  revision chain. E.g., with:

  d1_gmn.app.views.asserts.is_pid(pid)
  d1_gmn.app.views.asserts.is_in_revision_chain(pid)

  - The object can be at any location in the chain, including the head or tail.

  Postconditions:
  - The given object is a standalone object with empty obsoletes, obsoletedBy
  and seriesId fields.
  - The previously adjacent objects in the chain are adjusted to close any gap
  that was created or remove dangling reference at the head or tail.
  - If the object was the last object in the chain and the chain has a SID, the
  SID reference is shifted over to the new last object in the chain.
  """
  if is_head(sciobj_model):
    old_pid = sciobj_model.obsoletes.did
    _cut_head_from_chain(sciobj_model)
  elif is_tail(sciobj_model):
    old_pid = sciobj_model.obsoleted_by.did
    _cut_tail_from_chain(sciobj_model)
  else:
    old_pid = sciobj_model.obsoleted_by.did
    _cut_embedded_from_chain(sciobj_model)
  update_sid_to_head_pid_map(old_pid)


def _cut_head_from_chain(sciobj_model):
  new_head_model = d1_gmn.app.util.get_sci_model(sciobj_model.obsoletes.did)
  new_head_model.obsoleted_by = None
  sciobj_model.obsoletes = None
  sciobj_model.save()
  new_head_model.save()


def _cut_tail_from_chain(sciobj_model):
  new_tail_model = d1_gmn.app.util.get_sci_model(sciobj_model.obsoleted_by.did)
  new_tail_model.obsoletes = None
  sciobj_model.obsoleted_by = None
  sciobj_model.save()
  new_tail_model.save()


def _cut_embedded_from_chain(sciobj_model):
  prev_model = d1_gmn.app.util.get_sci_model(sciobj_model.obsoletes.did)
  next_model = d1_gmn.app.util.get_sci_model(sciobj_model.obsoleted_by.did)
  prev_model.obsoleted_by = next_model.pid
  next_model.obsoletes = prev_model.pid
  sciobj_model.obsoletes = None
  sciobj_model.obsoleted_by = None
  sciobj_model.save()
  prev_model.save()
  next_model.save()


# DB queries


def resolve_sid(sid):
  """Get the PID to which the {sid} currently maps.

  Preconditions:
  - {sid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_sid().
  """
  return d1_gmn.app.models.ChainIdToSeriesID.objects.get(
    sid__did=sid
  ).head_pid.did


def get_sid_by_pid(pid):
  """Given the {pid} of the object in a chain, return the SID for the chain.
  Return None if there is no SID for the chain. This operation is also valid
  for standalone objects which may or may not have SID.

  This is the reverse of resolve.

  Preconditions:
  - {pid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_pid().
  """
  sid_model = d1_gmn.app.models.PersistentIdToChainID.objects.get(
    pid__did=pid
  ).chain.sid
  if sid_model:
    return sid_model.did


# def get_pids_in_revision_chain(pid):
#   """Given the PID of any object in a chain, return a list of all PIDs in the
#   chain. The returned list is in the same order as the chain. The initial PID is
#   typically obtained by resolving a SID. If the given PID is not in a chain, a
#   list containing the single object is returned.
#   """
#   sci_model = d1_gmn.app.util.get_sci_model(pid)
#   while sci_model.obsoletes:
#     sci_model = d1_gmn.app.util.get_sci_model(sci_model.obsoletes.pid.did)
#   chain_pid_list = [sci_model.pid.did]
#   while sci_model.obsoleted_by:
#     sci_model = d1_gmn.app.util.get_sci_model(
#       sci_model.obsoleted_by.pid.did
#     )
#     chain_pid_list.append(sci_model.pid.did)
#   return chain_pid_list


def is_sid(did):
  return d1_gmn.app.models.ChainIdToSeriesID.objects.filter(sid__did=did
                                                            ).exists()


def is_obsoleted(pid):
  return d1_gmn.app.util.get_sci_model(pid).obsoleted_by is not None


def is_in_revision_chain(sciobj_model):
  return bool(sciobj_model.obsoleted_by or sciobj_model.obsoletes)


def is_head(sciobj_model):
  return sciobj_model.obsoletes and not sciobj_model.obsoleted_by


def is_tail(sciobj_model):
  return sciobj_model.obsoleted_by and not sciobj_model.obsoletes


# def is_sid_in_revision_chain(sid, pid):
#   """Determine if {sid} resolves to an object in the revision chain to which
#   {pid} belongs.
#
#   Preconditions:
#   - {sid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_sid().
#   """
#   chain_pid_list = get_pids_in_revision_chain(pid)
#   resolved_pid = resolve_sid(sid)
#   return resolved_pid in chain_pid_list

# def update_or_create_sid_to_pid_map(sid, pid):
#   """Update existing or create a new {sid} to {pid} association. Then create
#   or update the {sid} to resolve to the {pid}.
#
#   Preconditions:
#   - {sid} is verified to be unused if creating a standalone object (that may later become
#   the first object in a chain).
#   - {sid} is verified to belong to the given chain updating.
#   - {pid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_pid().
#   """
#   d1_gmn.app.models.sid_to_pid(sid, pid)
#   d1_gmn.app.models.sid_to_head_pid(sid, pid)

# def get_sid_by_pid(pid):
#   """Get the SID to which the {pid} maps.
#   Return None if there is no SID maps to {pid}.
#   """
#   try:
#     return d1_gmn.app.models.SeriesIdToPersistentId.objects.get(
#       pid__did=pid
#     ).sid.did
#   except d1_gmn.app.models.SeriesIdToPersistentId.DoesNotExist:
#     return None

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
#   - PID is verified to exist. E.g., with d1_gmn.app.views.asserts.is_pid().
#
#   Postconditions:
#   - The SID maps to the last object in the chain.
#   """
#   sid = sysmeta_db.get_sid_by_pid(pid)
#   if sid:
#     chain_pid_list = sysmeta_db.get_pids_in_revision_chain(pid)
#     update_sid(sid, chain_pid_list[-1])

# def update_revision_chain(pid, obsoletes_pid, obsoleted_by_pid, sid):
#   with sysmeta_file.SysMetaFile(pid) as sysmeta_pyxb:
#     sysmeta_file.update_revision_chain(
#       sysmeta_pyxb, obsoletes_pid, obsoleted_by_pid, sid
#     )
#   sysmeta_db.update_revision_chain(sysmeta_pyxb)

#    if sysmeta.obsoletes is not None:
# chain_pid_list = [pid]
#  sci_obj = mn.models.ScienceObject.objects.get(pid__did=pid)
#  while sci_obj.obsoletes:
#    obsoletes_pid = sysmeta_pyxb.obsoletes.value()
#    chain_pid_list.append(obsoletes_pid)
#    sci_obj = mn.models.ScienceObject.objects.get(pid__did=obsoletes_pid)
#  sci_obj = mn.models.ScienceObject.objects.get(pid__did=pid)
#  while sci_obj.obsoleted_by:
#    obsoleted_by_pid = sysmeta_pyxb.obsoleted_by.value()
#    chain_pid_list.append(obsoleted_by_pid)
#    sci_obj = mn.models.ScienceObject.objects.get(pid__did=obsoleted_by_pid)
#  return chain_pid_list
