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
"""Utilities for manipulating System Metadata.

This module contains functions that act on system metadata both in the database
and the filesystem.

There is no validation done in this layer. Validation must be done before
calling this module.
"""

# Stdlib.
import datetime
# import os
# import time
#
# Django.
# import django.db
# import django.db.transaction
from django.conf import settings
#
# # D1.
# import d1_common.date_time
# import d1_common.types.dataoneTypes
# import d1_common.types.exceptions

# App.
import mn.models
import sysmeta_base
import sysmeta_db
import sysmeta_file


def update_sysmeta_with_mn_values(request, sysmeta_obj):
  sysmeta_obj.submitter = request.primary_subject
  sysmeta_obj.originMemberNode = settings.NODE_IDENTIFIER
  # If authoritativeMemberNode is not specified, set it to this MN.
  # TODO: What happens if authoritativeMemberNode is set to some other MN?
  if sysmeta_obj.authoritativeMemberNode is None:
    sysmeta_obj.authoritativeMemberNode = settings.NODE_IDENTIFIER
  now = datetime.datetime.utcnow()
  sysmeta_obj.dateUploaded = now
  sysmeta_obj.dateSysMetadataModified = now
  sysmeta_obj.serialVersion = 1


def create(sysmeta_obj, url, is_replica=False):
  sysmeta_file.write_sysmeta_to_file(sysmeta_obj)
  sysmeta_db.create(sysmeta_obj, url, is_replica)


def archive_object(pid):
  """Set the status of an object as archived.

  Preconditions:
  - The object with the pid is verified to exist.
  - The object is not a replica.
  - The object is not archived.
  """
  with mn.sysmeta_file.SysMetaFile(pid) as sysmeta_obj:
    sysmeta_obj.archived = True
    sysmeta_db.update_sci_row(sysmeta_obj)


def set_obsoleted_by(obsoleted_pid, obsoleted_by_pid):
  with mn.sysmeta_file.SysMetaFile(obsoleted_pid) as sysmeta_obj:
    sysmeta_obj.obsoletedBy = obsoleted_by_pid
    sysmeta_db.update_sci_row(sysmeta_obj)

# ------------------------------------------------------------------------------
# Obsolescence chain
# ------------------------------------------------------------------------------

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
  with sysmeta_file.SysMetaFile(pid) as sysmeta_obj:
    if is_head(sysmeta_obj):
      _cut_head_from_chain(sysmeta_obj)
    elif is_tail(sysmeta_obj):
      _cut_tail_from_chain(sysmeta_obj)
    else:
      _cut_embedded_from_chain(sysmeta_obj)
    sysmeta_obj.obsoletes = None
    sysmeta_obj.obsoletedBy = None
    sysmeta_db.update_sci_row(sysmeta_obj)


def _cut_head_from_chain(old_head_sysmeta_obj):
  with sysmeta_file.SysMetaFile(old_head_sysmeta_obj.obsoletes.value()) as new_head_sysmeta_obj:
    new_head_sysmeta_obj.obsoletedBy = None
    sysmeta_db.update_sci_row(new_head_sysmeta_obj)


def _cut_tail_from_chain(old_tail_sysmeta_obj):
  with sysmeta_file.SysMetaFile(old_tail_sysmeta_obj.obsoletedBy.value()) as new_tail_sysmeta_obj:
    new_tail_sysmeta_obj.obsoletes = None
    sysmeta_db.update_sci_row(new_tail_sysmeta_obj)


def _cut_embedded_from_chain(old_embedded_sysmeta_obj):
  with sysmeta_file.SysMetaFile(old_embedded_sysmeta_obj.obsoletes.value()) as prev_sysmeta_obj:
    with sysmeta_file.SysMetaFile(old_embedded_sysmeta_obj.obsoletedBy.value()) as next_sysmeta_obj:
      prev_sysmeta_obj.obsoletedBy = next_sysmeta_obj.identifier.value()
      next_sysmeta_obj.obsoletes = prev_sysmeta_obj.identifier.value()
      sysmeta_db.update_sci_row(prev_sysmeta_obj)
      sysmeta_db.update_sci_row(next_sysmeta_obj)


def update_sid(sid, pid):
  """Change the existing {sid} to resolve to {pid}.

  Preconditions:
  - SID is verified to exist. E.g., with view_asserts.is_sid().

  Postconditions:
  - The SID maps to the object specified by pid.
  """
  sci_row = sysmeta_db.get_sci_row(pid)
  sysmeta_db.update_sid(sid, sci_row)


def move_sid_to_last_object_in_chain(pid):
  """Move SID to the last object in a chain to which {pid} belongs.

  - If the chain does not have a SID, do nothing.
  - If the SID already maps to the last object in the chain, do nothing.

  A SID always resolves to the last object in its chain. So System Metadata XML
  docs are used for introducing SIDs and setting initial mappings, but the
  database maintains the current mapping going forward.

  Preconditions:
  - PID is verified to exist. E.g., with view_asserts.is_pid().

  Postconditions:
  - The SID maps to the last object in the chain.
  """
  sid = sysmeta_db.get_sid_by_pid(pid)
  if sid:
    chain_pid_list = sysmeta_db.get_pids_in_obsolescence_chain(pid)
    update_sid(sid, chain_pid_list[-1])


def update_sid(sid, pid):
  """Change the existing {sid} to resolve to {pid}.

  Preconditions:
  - SID is verified to exist. E.g., with view_asserts.is_sid().

  Postconditions:
  - The SID maps to the object specified by pid.
  """
  sci_row = sysmeta_db.get_sci_row(pid)
  sysmeta_db.update_sid(sid, sci_row)

# def update_obsolescence_chain(pid, obsoletes_pid, obsoleted_by_pid, sid):
#   with sysmeta_file.SysMetaFile(pid) as sysmeta_obj:
#     sysmeta_file.update_obsolescence_chain(
#       sysmeta_obj, obsoletes_pid, obsoleted_by_pid, sid
#     )
#   sysmeta_db.update_obsolescence_chain(sysmeta_obj)

 #    if sysmeta.obsoletes is not None:
 # chain_pid_list = [pid]
 #  sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
 #  while sci_obj.obsoletes:
 #    obsoletes_pid = sysmeta_obj.obsoletes.value()
 #    chain_pid_list.append(obsoletes_pid)
 #    sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=obsoletes_pid)
 #  sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
 #  while sci_obj.obsoleted_by:
 #    obsoleted_by_pid = sysmeta_obj.obsoleted_by.value()
 #    chain_pid_list.append(obsoleted_by_pid)
 #    sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=obsoleted_by_pid)
 #  return chain_pid_list


def is_head(sysmeta_obj):
  return sysmeta_obj.obsoletes and not sysmeta_obj.obsoletedBy


def is_tail(sysmeta_obj):
  return sysmeta_obj.obsoletedBy and not sysmeta_obj.obsoletes


# def update_chaining_info(pid, obsoletes_pid=None, obsoleted_by_pid=None, sid=None):
#   """Update the chain related fields.
#   """
#   sci_obj = mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)
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
