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

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.did
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.util

import d1_common.types.exceptions
import d1_common.xml


def create_or_update_chain(pid, sid, obsoletes_pid, obsoleted_by_pid):
  chain_model = _get_chain_by_pid(pid)
  if chain_model:
    _set_chain_sid(chain_model, sid)
  else:
    _add_sciobj(pid, sid, obsoletes_pid, obsoleted_by_pid)
  _update_sid_to_last_existing_pid_map(pid)


def delete_chain(pid):
  pid_to_chain_model = d1_gmn.app.models.ChainMember.objects.get(pid__did=pid)
  chain_model = pid_to_chain_model.chain
  pid_to_chain_model.delete()
  if not d1_gmn.app.models.ChainMember.objects.filter(chain=chain_model
                                                      ).exists():
    if chain_model.sid:
      # Cascades back to chain_model.
      d1_gmn.app.models.IdNamespace.objects.filter(did=chain_model.sid.did
                                                   ).delete()
    else:
      chain_model.delete()


def cut_from_chain(sciobj_model):
  """Remove an object from a revision chain.

  The object can be at any location in the chain, including the head or tail.

  Preconditions:
  - The object with the pid is verified to exist and to be a member of an
  revision chain. E.g., with:

  d1_gmn.app.views.asserts.is_existing_object(pid)
  d1_gmn.app.views.asserts.is_in_revision_chain(pid)

  Postconditions:
  - The given object is a standalone object with empty obsoletes, obsoletedBy
  and seriesId fields.
  - The previously adjacent objects in the chain are adjusted to close any gap
  that was created or remove dangling reference at the head or tail.
  - If the object was the last object in the chain and the chain has a SID, the
  SID reference is shifted over to the new last object in the chain.
  """
  if _is_head(sciobj_model):
    old_pid = sciobj_model.obsoletes.did
    _cut_head_from_chain(sciobj_model)
  elif _is_tail(sciobj_model):
    old_pid = sciobj_model.obsoleted_by.did
    _cut_tail_from_chain(sciobj_model)
  else:
    old_pid = sciobj_model.obsoleted_by.did
    _cut_embedded_from_chain(sciobj_model)
  _update_sid_to_last_existing_pid_map(old_pid)


def get_all_pid_by_sid(sid):
  return [c.pid.did for c in _get_all_chain_member_queryset_by_sid(sid)]


# def set_revision(pid, obsoletes_pid=None, obsoleted_by_pid=None):
#   sciobj_model = d1_gmn.app.util.get_sci_model(pid)
#   set_revision_links(sciobj_model, obsoletes_pid, obsoleted_by_pid)
#   sciobj_model.save()


def resolve_sid(sid):
  """Get the PID to which the {sid} currently maps.

  Preconditions:
  - {sid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_sid().
  """
  return d1_gmn.app.models.Chain.objects.get(sid__did=sid).head_pid.did


def get_sid_by_pid(pid):
  """Given the {pid} of the object in a chain, return the SID for the chain

  Return None if there is no SID for the chain. This operation is also valid
  for standalone objects which may or may not have a SID.

  This is the reverse of resolve.

  All known PIDs are associated with a chain.

  Preconditions:
  - {pid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_existing_object().
  """
  return d1_gmn.app.did.get_did_by_foreign_key(_get_chain_by_pid(pid).sid)


def set_revision_links(sciobj_model, obsoletes_pid=None, obsoleted_by_pid=None):
  if obsoletes_pid:
    sciobj_model.obsoletes = d1_gmn.app.did.get_or_create_did(obsoletes_pid)
    _set_revision_reverse(
      sciobj_model.pid.did, obsoletes_pid, is_obsoletes=False
    )
  if obsoleted_by_pid:
    sciobj_model.obsoleted_by = d1_gmn.app.did.get_or_create_did(
      obsoleted_by_pid
    )
    _set_revision_reverse(
      sciobj_model.pid.did, obsoleted_by_pid, is_obsoletes=True
    )
  sciobj_model.save()


def is_obsoletes_pid(pid):
  """Return True if {pid} is referenced in the obsoletes field of any object

  This will return True even if the PID is in the obsoletes field of an object
  that does not exist on the local MN, such as replica that is in an incomplete
  chain.
  """
  return d1_gmn.app.models.ScienceObject.objects.filter(obsoletes__did=pid
                                                        ).exists()


def is_obsoleted_by_pid(pid):
  """Return True if {pid} is referenced in the obsoletedBy field of any object

  This will return True even if the PID is in the obsoletes field of an object
  that does not exist on the local MN, such as replica that is in an incomplete
  chain.
  """
  return d1_gmn.app.models.ScienceObject.objects.filter(obsoleted_by__did=pid
                                                        ).exists()


def is_revision(pid):
  """Return True if {pid} is referenced in the obsoletes or obsoletedBy field of
  any object

  This will return True even if the PID is in the obsoletes field of an object
  that does not exist on the local MN, such as replica that is in an incomplete
  chain.
  """
  return is_obsoletes_pid(pid) or is_obsoleted_by_pid(pid)


def _add_sciobj(pid, sid, obsoletes_pid, obsoleted_by_pid):
  is_added = _add_to_chain(pid, sid, obsoletes_pid, obsoleted_by_pid)
  if not is_added:
    # if not obsoletes_pid and not obsoleted_by_pid:
    _add_standalone(pid, sid)
  # else:


def _add_standalone(pid, sid):
  # assert_sid_unused(sid)
  _create_chain(pid, sid)


def _add_to_chain(pid, sid, obsoletes_pid, obsoleted_by_pid):
  _assert_sid_is_in_chain(sid, obsoletes_pid)
  _assert_sid_is_in_chain(sid, obsoleted_by_pid)
  obsoletes_chain_model = _get_chain_by_pid(obsoletes_pid)
  obsoleted_by_chain_model = _get_chain_by_pid(obsoleted_by_pid)
  sid_chain_model = _get_chain_by_sid(sid) if sid else None
  chain_model = obsoletes_chain_model or obsoleted_by_chain_model or sid_chain_model
  if not chain_model:
    return False
  if obsoletes_chain_model and obsoletes_chain_model != chain_model:
    _merge_chains(chain_model, obsoletes_chain_model)
  if obsoleted_by_chain_model and obsoleted_by_chain_model != chain_model:
    _merge_chains(chain_model, obsoleted_by_chain_model)
  _add_pid_to_chain(chain_model, pid)
  _set_chain_sid(chain_model, sid)
  return True


def _merge_chains(chain_model_a, chain_model_b):
  """Merge two chains

  For use when it becomes known that two chains that were created separately
  actually are separate sections of the same chain

  E.g.:

  - A obsoleted by X is created. A has no SID. X does not exist
  yet. A chain is created for A.
  - B obsoleting Y is created. B has SID. Y does not exist yet. A
  chain is created for B.
  - C obsoleting X, obsoleted by Y is created. C tells us that X and Y
  are in the same chain, which means that A and B are in the same chain. At
  this point, the two chains need to be merged. Merging the chains causes A
  to take on the SID of B.
  """
  _set_chain_sid(
    chain_model_a, d1_gmn.app.did.get_did_by_foreign_key(chain_model_b.sid)
  )
  for member_model in _get_all_chain_member_queryset_by_chain(chain_model_b):
    member_model.chain = chain_model_a
    member_model.save()
  chain_model_b.delete()


def _add_pid_to_chain(chain_model, pid):
  chain_member_model = d1_gmn.app.models.ChainMember(
    chain=chain_model, pid=d1_gmn.app.did.get_or_create_did(pid)
  )
  chain_member_model.save()


def _set_chain_sid(chain_model, sid):
  """Set or update SID for chain

  If the chain already has a SID, {sid} must either be None or match the
  existing SID.
  """
  if not sid:
    return
  if chain_model.sid and chain_model.sid.did != sid:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Attempted to modify existing SID. '
      'existing_sid="{}", new_sid="{}"'.format(chain_model.sid.did, sid)
    )
  chain_model.sid = d1_gmn.app.did.get_or_create_did(sid)
  chain_model.save()


def _assert_sid_is_in_chain(sid, pid):
  if not sid or not pid:
    return
  chain_model = _get_chain_by_pid(pid)
  if not chain_model or not chain_model.sid:
    return
  if chain_model.sid.did != sid:
    raise d1_common.types.exceptions.ServiceFailure(
      0, 'Attempted to create object in chain with non-matching SID. '
      'existing_sid="{}", new_sid="{}"'.format(chain_model.sid.did, sid)
    )


def _find_head_or_latest_connected(pid, last_pid=None):
  """Find latest existing sciobj that can be reached by walking towards the head
  from {pid}

  If {pid} does not exist, return None.
  If chain is connected all the way to head and head exists, return the head.
  If chain ends in a dangling obsoletedBy, return the last existing object.
  """
  try:
    sci_model = d1_gmn.app.model_util.get_sci_model(pid)
  except d1_gmn.app.models.ScienceObject.DoesNotExist:
    return last_pid
  if sci_model.obsoleted_by is None:
    return pid
  return _find_head_or_latest_connected(sci_model.obsoleted_by.did, pid)


def _get_chain_by_pid(pid):
  """Find chain by pid

  Return None if not found.
  """
  try:
    return d1_gmn.app.models.ChainMember.objects.get(pid__did=pid).chain
  except d1_gmn.app.models.ChainMember.DoesNotExist:
    pass


def _get_chain_by_sid(sid):
  """Return None if not found
  """
  try:
    return d1_gmn.app.models.Chain.objects.get(sid__did=sid)
  except d1_gmn.app.models.Chain.DoesNotExist:
    pass


def _update_sid_to_last_existing_pid_map(pid):
  """Set chain head PID to the last existing object in the chain to which {pid}
  belongs. If SID has been set for chain, it resolves to chain head PID.

  Intended to be called in MNStorage.delete() and other chain manipulation.

  Preconditions:
  - {pid} must exist and be verified to be a PID.
    d1_gmn.app.views.asserts.is_existing_object()
  """
  last_pid = _find_head_or_latest_connected(pid)
  chain_model = _get_chain_by_pid(last_pid)
  if not chain_model:
    return
  chain_model.head_pid = d1_gmn.app.did.get_or_create_did(last_pid)
  chain_model.save()


def _create_chain(pid, sid):
  """Create the initial chain structure for a new standalone object. Intended to
  be called in MNStorage.create().

  Preconditions:
  - {sid} must be verified to be available to be assigned to a new standalone
  object. E.g., with is_valid_sid_for_new_standalone().
  """
  chain_model = d1_gmn.app.models.Chain(
    # sid=d1_gmn.app.models.did(sid) if sid else None,
    head_pid=d1_gmn.app.did.get_or_create_did(pid)
  )
  chain_model.save()
  _add_pid_to_chain(chain_model, pid)
  _set_chain_sid(chain_model, sid)
  return chain_model


# def _get_or_create_chain_for_pid(pid):
#   try:
#     return d1_gmn.app.models.ChainMember.objects.get(pid__did=pid).chain
#   except d1_gmn.app.models.ChainMember.DoesNotExist:
#     return _create_chain(pid, None)


def _map_sid_to_pid(chain_model, sid, pid):
  if sid is not None:
    chain_model.sid = d1_gmn.app.did.get_or_create_did(sid)
  chain_model.head_pid = d1_gmn.app.did.get_or_create_did(pid)
  chain_model.save()


def _get_all_chain_member_queryset_by_sid(sid):
  return d1_gmn.app.models.ChainMember.objects.filter(
    chain=d1_gmn.app.models.Chain.objects.get(sid__did=sid)
  )


def _get_all_chain_member_queryset_by_chain(chain_model):
  return d1_gmn.app.models.ChainMember.objects.filter(chain=chain_model)


def _cut_head_from_chain(sciobj_model):
  new_head_model = d1_gmn.app.model_util.get_sci_model(
    sciobj_model.obsoletes.did
  )
  new_head_model.obsoleted_by = None
  sciobj_model.obsoletes = None
  sciobj_model.save()
  new_head_model.save()


def _cut_tail_from_chain(sciobj_model):
  new_tail_model = d1_gmn.app.model_util.get_sci_model(
    sciobj_model.obsoleted_by.did
  )
  new_tail_model.obsoletes = None
  sciobj_model.obsoleted_by = None
  sciobj_model.save()
  new_tail_model.save()


def _cut_embedded_from_chain(sciobj_model):
  prev_model = d1_gmn.app.model_util.get_sci_model(sciobj_model.obsoletes.did)
  next_model = d1_gmn.app.model_util.get_sci_model(
    sciobj_model.obsoleted_by.did
  )
  prev_model.obsoleted_by = next_model.pid
  next_model.obsoletes = prev_model.pid
  sciobj_model.obsoletes = None
  sciobj_model.obsoleted_by = None
  sciobj_model.save()
  prev_model.save()
  next_model.save()


def _is_head(sciobj_model):
  return sciobj_model.obsoletes and not sciobj_model.obsoleted_by


def _is_tail(sciobj_model):
  return sciobj_model.obsoleted_by and not sciobj_model.obsoletes


def _set_revision_reverse(to_pid, from_pid, is_obsoletes):
  try:
    sciobj_model = d1_gmn.app.model_util.get_sci_model(from_pid)
  except d1_gmn.app.models.ScienceObject.DoesNotExist:
    return
  if not d1_gmn.app.did.is_existing_object(to_pid):
    return
  did_model = d1_gmn.app.did.get_or_create_did(to_pid)
  if is_obsoletes:
    sciobj_model.obsoletes = did_model
  else:
    sciobj_model.obsoleted_by = did_model
  sciobj_model.save()


# def assert_sid_unused(sid):
#   if not sid:
#     return
#   if find_chain_by_sid(sid):
#     raise d1_common.types.exceptions.ServiceFailure(
#       0, u'Attempted to create standalone object with SID already in use. '
#       'sid="{}"'.format(sid)
#     )

# def upd_sid_resolve(pid, sid=None, obsoletes_pid=None, obsoleted_by_pid=None):
#   """Set SID to resolve to the newest object that exists locally for a chain"""
#
#   last_pid = find_head_or_latest_connected(pid)

# def has_chain(pid):
#   return d1_gmn.app.models.ChainMember.objects.filter(pid__did=pid).exists()

# def create_chain(sid, pid):
#   """Create the initial chain structure for a new standalone object. Intended to
#   be called in MNStorage.create().
#
#   Preconditions:
#   - {sid} must either be None or be previously unused.
#     d1_gmn.app.views.asserts.is_unused()
#   - {pid} must exist and be verified to be a PID.
#     d1_gmn.app.views.asserts.is_pid()
#   """
#   chain_model = _get_or_create_chain_for_pid(pid)
#   _map_sid_to_pid(chain_model, sid, pid)

# def add_pid_to_chain(sid, old_pid, new_pid):
#   """Add a new revision {new_pid} to the chain that {old_pid} belongs to and
#   update any SID to resolve to the new PID. Intended to be called in
#   MNStorage.update().
#
#   Preconditions:
#   - {sid} must either be None or match the SID already assigned to the chain.
#   - Both {old_pid} and {new_pid} must exist and be verified to be PIDs
#     d1_gmn.app.views.asserts.is_pid()
#   """
#   chain_model = _get_or_create_chain_for_pid(old_pid)
#   _add_pid_to_chain(chain_model, new_pid)
#   _map_sid_to_pid(chain_model, sid, new_pid)

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
