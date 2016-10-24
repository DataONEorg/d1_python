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

"""Utilities for manipulating obsolescence chains.
"""

# App.
import mn.auth
import mn.models
import mn.util
import sysmeta_util


def is_obsoleted(pid):
  return sysmeta_util.get_sci_row(pid).obsoleted_by is not None


def set_obsolescence(pid, obsoletes_pid=None, obsoleted_by_pid=None):
  sciobj_row = sysmeta_util.get_sci_row(pid)
  _set_obsolescence(sciobj_row, obsoletes_pid, obsoleted_by_pid)
  sciobj_row.save()


def cut_from_chain(pid):
  """Remove an object from an obsolescence chain.

  Preconditions:
  - The object with the pid is verified to exist and to be a member of an
  obsolescence chain. E.g., with:

  view_asserts.is_pid(pid)
  view_asserts.is_in_obsolescence_chain(pid)

  - The object can be at any location in the chain, including the head or tail.

  Postconditions:
  - The given object is a standalone object with empty obsoletes, obsoletedBy
  and seriesId fields.
  - The previously adjacent objects in the chain are adjusted to close any gap
  that was created or remove dangling reference at the head or tail.
  - If the object was the last object in the chain and the chain has a SID, the
  SID reference is shifted over to the new last object in the chain.
  """
  sciobj_row = sysmeta_util.get_sci_row(pid)
  if is_head(sciobj_row):
    _cut_head_from_chain(sciobj_row)
  elif is_tail(sciobj_row):
    _cut_tail_from_chain(sciobj_row)
  else:
    _cut_embedded_from_chain(sciobj_row)
  sciobj_row.obsoletes = None
  sciobj_row.obsoleted_by = None
  sciobj_row.save()

#
# Private
#

def _cut_head_from_chain(sciobj_row):
  new_head_row = sysmeta_util.get_sci_row(sciobj_row.obsoletes.pid_or_sid)
  new_head_row.obsoletedBy = None
  new_head_row.save()


def _cut_tail_from_chain(sciobj_row):
  new_tail_row = sysmeta_util.get_sci_row(sciobj_row.obsoleted_by.pid_or_sid)
  new_tail_row.obsoletes = None
  new_tail_row.save()


def _cut_embedded_from_chain(sciobj_row):
  prev_row = sysmeta_util.get_sci_row(sciobj_row.obsoletes)
  next_row = sysmeta_util.get_sci_row(sciobj_row.obsoleted_by)
  prev_row.obsoleted_by = next_row.pid.pid_or_sid
  next_row.obsoletes = prev_row.pid.pid_or_sid
  prev_row.save()
  next_row.save()


def _set_obsolescence(sciobj_row, obsoletes_pid, obsoleted_by_pid):
  sciobj_row.obsoletes = mn.models.did(obsoletes_pid) if obsoletes_pid else None
  sciobj_row.obsoleted_by = mn.models.did(obsoleted_by_pid) if obsoleted_by_pid else None



# def update_obsolescence_chain(pid, obsoletes_pid, obsoleted_by_pid, sid):
#   with sysmeta_file.SysMetaFile(pid) as sysmeta_obj:
#     sysmeta_file.update_obsolescence_chain(
#       sysmeta_obj, obsoletes_pid, obsoleted_by_pid, sid
#     )
#   sysmeta_db.update_obsolescence_chain(sysmeta_obj)

 #    if sysmeta.obsoletes is not None:
 # chain_pid_list = [pid]
 #  sci_obj = mn.models.ScienceObject.objects.get(pid__did=pid)
 #  while sci_obj.obsoletes:
 #    obsoletes_pid = sysmeta_obj.obsoletes.value()
 #    chain_pid_list.append(obsoletes_pid)
 #    sci_obj = mn.models.ScienceObject.objects.get(pid__did=obsoletes_pid)
 #  sci_obj = mn.models.ScienceObject.objects.get(pid__did=pid)
 #  while sci_obj.obsoleted_by:
 #    obsoleted_by_pid = sysmeta_obj.obsoleted_by.value()
 #    chain_pid_list.append(obsoleted_by_pid)
 #    sci_obj = mn.models.ScienceObject.objects.get(pid__did=obsoleted_by_pid)
 #  return chain_pid_list


def is_head(sciobj_row):
  return sciobj_row.obsoletes and not sciobj_row.obsoleted_by


def is_tail(sciobj_row):
  return sciobj_row.obsoleted_by and not sciobj_row.obsoletes


def get_pids_in_obsolescence_chain(pid):
  """Given the PID of any object in a chain, return a list of all PIDs in the
  chain. The returned list is in the same order as the chain. The initial PID is
  typically obtained by resolving a SID. If the given PID is not in a chain, a
  list containing the single object is returned.
  """
  sci_row = sysmeta_util.get_sci_row(pid)
  while sci_row.obsoletes:
    sci_row = sysmeta_util.get_sci_row(sci_row.obsoletes.pid.did)
  chain_pid_list = [sci_row.pid.did]
  while sci_row.obsoleted_by:
    sci_row = sysmeta_util.get_sci_row(sci_row.obsoleted_by.pid.did)
    chain_pid_list.append(sci_row.pid.did)
  return chain_pid_list


def is_sid_in_obsolescence_chain(sid, pid):
  """Determine if {sid} resolves to an object in the obsolescence chain to which
  {pid} belongs.

  Preconditions:
  - {sid} is verified to exist. E.g., with view_asserts.is_sid().
  """
  chain_pid_list = get_pids_in_obsolescence_chain(pid)
  resolved_pid = resolve_sid(sid)
  return resolved_pid in chain_pid_list


def get_sid_by_pid(pid):
  """Given the {pid} of the object in a chain, return the SID for the chain.
  Return None if there is no SID for the chain.

  Preconditions:
  - {pid} is verified to exist. E.g., with view_asserts.is_pid().
  """
  chain_pid_list = get_pids_in_obsolescence_chain(pid)
  for chain_pid in chain_pid_list:
    try:
      return mn.models.SeriesIdToScienceObject.objects.get(
        sciobj__pid__did=chain_pid
      ).sid.did
    except mn.models.SeriesIdToScienceObject.DoesNotExist:
      pass

# def update_chaining_info(pid, obsoletes_pid=None, obsoleted_by_pid=None, sid=None):
#   """Update the chain related fields.
#   """
#   sci_obj = mn.models.ScienceObject.objects.get(pid__did=pid)
#   if obsoletes_pid:
#     sci_obj.obsoletes = obsoletes_pid
#   if obsoleted_by_pid:
#     sci_obj.obsoleted_by = obsoleted_by_pid
#
#   update_chaining_info
#   except mn.models.ScienceObject.DoesNotExist:
#     raise d1_common.types.exceptions.ServiceFailure(
#       0, "Attempted to access non-existing object", pid
#     )
#

# def update_obsolescence_chain(sysmeta_obj):
#   pid = sysmeta_obj.identifier.value()
#   sci_row = sysmeta_util.get_sci_row(pid)
#   _update_obsolescence_chain(sci_row, sysmeta_obj)
#   _update_modified_timestamp(sci_row, sysmeta_obj)
#   sci_row.save()
