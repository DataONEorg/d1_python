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
"""Utilities for manipulating System Metadata in the database.
"""

# Stdlib.
import datetime
import os
import time

# Django.
import django.db
import django.db.transaction
from django.conf import settings

# D1.
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.exceptions

# App.
import mn.auth
import mn.models
import mn.util
import sysmeta_base

# def _has_sid(sysmeta):
#   return hasattr(sysmeta, 'seriesId')

# # Log this object creation.
# mn.event_log.create(pid, request)

# return sysmeta.seriesId

# # Open the sysmeta file on disk for read-write. This causes a new file with a
# # new serial version to be automatically written to disk when the sysmeta
# # context manager goes out of scope.
# with mn.sysmeta_file.sysmeta(pid, sci_row.serial_version, read_only=False) as sysmeta_obj:
# # Open the sysmeta file on disk for read only and get the access policy. Since the sysmeta is opened for read-only,
# # a new document is *not* created when the sysmeta context manager goes out of scope.
# with mn.sysmeta_file.sysmeta(pid, sci_row.serial_version, read_only=True) as sysmeta:


def create(sysmeta_obj, url, is_replica=False):
  """Create database representation of a System Metadata object and closely
  related internal state.

  Preconditions:
  - PID is verified not to exist as a PID, SID or object accepted for
  replication. E.g., with view_asserts.is_unused(pid).
  - Any supplied SID is verified to be valid for the given operation. E.g., with
  view_asserts.is_valid_sid_for_chain_if_specified() or
  view_asserts.is_unused().

  Postconditions:
  - New rows are created in ScienceObject, Permission and related tables as
  necessary to hold portions of the System Metadata XML document and
  internal values that are required for performance when processing requests.

  Notes:
  - The authoritative location for System Metadata is the XML files that are
  stored in the directory tree managed by the sysmeta_file module. The XML files
  are created and updated first, then the database is updated to match.
  - The System Metadata portions of the database are essentially a cache of the
  actual System Metadata that enables processing of requests without having to
  read and deserialize the XML files.
  """
  pid = sysmeta_obj.identifier.value()
  sci_row = mn.models.ScienceObject()
  sci_row.pid = create_id_row(pid)
  _update_sci_row(sci_row, sysmeta_obj, url, is_replica)
  _update_access_policy(sci_row, sysmeta_obj)
  # _update_obsolescence_chain(sci_row, sysmeta_obj)
  # _update_sid(sci_row, sysmeta_obj).
  # _update_mtime(sci_row, sysmeta_obj)


def create_sid_if_specified(sysmeta_obj):
  seriesId = sysmeta_base.get_value(sysmeta_obj, 'seriesId')
  if seriesId is not None:
    sid = sysmeta_obj.seriesId.value()
    pid = sysmeta_obj.identifier.value()
    _create_sid(sid, pid)


def update(sysmeta_obj, url=None, is_replica=None):
  """Update database representation of a System Metadata object. The System
  Metadata must already be verified to be correct and suitable for the
  operation which is being performed.
  """
  pid = sysmeta_obj.identifier.value()
  sci_row = get_sci_row(pid)
  _update_sci_row(sci_row, sysmeta_obj, url=url, is_replica=is_replica)
  _update_access_policy(sci_row, sysmeta_obj)


def update_sci_row(sysmeta_obj, url=None, is_replica=None):
  pid = sysmeta_obj.identifier.value()
  sci_row = get_sci_row(pid)
  _update_sci_row(sci_row, sysmeta_obj, url=url, is_replica=is_replica)


def update_access_policy(sysmeta_obj):
  pid = sysmeta_obj.identifier.value()
  sci_row = get_sci_row(pid)
  _update_access_policy(sci_row, sysmeta_obj)


def create_id_row(sid_or_pid):
  """Create a new SID or PID.

  Preconditions:
  - {sid_or_pid} is verified to be unused. E.g., with view_asserts.is_unused().
  """
  id_row = mn.models.IdNamespace()
  id_row.sid_or_pid = sid_or_pid
  id_row.save()
  return id_row


def _create_sid(sid, pid):
  """Create a new {sid} that resolves to {pid}.

  Preconditions:
  - {sid} is verified to be unused. E.g., with view_asserts.is_unused().
  - {pid} is verified to exist. E.g., with view_asserts.is_pid().
  """
  sid_row = mn.models.SeriesIdToScienceObject()
  sid_row.object = get_sci_row(pid)
  sid_row.sid = create_id_row(sid)
  sid_row.save()


def get_sci_row(pid):
  return mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)


def update_sid(sid, sci_row):
  """Change an existing {sid} to resolve to {sci_row}"""
  sid_row = mn.models.SeriesIdToScienceObject.objects.get(sid__sid_or_pid=sid)
  sid_row.object = sci_row
  sid_row.save()


def resolve_sid(sid):
  """Get the pid to which the {sid} currently maps.

  Preconditions:
  - {sid} is verified to exist. E.g., with view_asserts.is_sid().
  """
  return mn.models.SeriesIdToScienceObject.objects.get(
    sid__sid_or_pid=sid
  ).object.pid.sid_or_pid


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
        object__pid__sid_or_pid=chain_pid
      ).sid.sid_or_pid
    except mn.models.SeriesIdToScienceObject.DoesNotExist:
      pass

# def update_obsolescence_chain(sysmeta_obj):
#   pid = sysmeta_obj.identifier.value()
#   sci_row = get_sci_row(pid)
#   _update_obsolescence_chain(sci_row, sysmeta_obj)
#   _update_mtime(sci_row, sysmeta_obj)
#   sci_row.save()

#
# def update_sid(sysmeta_obj):
#   pid = sysmeta_obj.identifier.value()
#   sci_row = get_sci_row(pid)
#   _update_sid(sci_row, sysmeta_obj)
#   _update_mtime(sci_row, sysmeta_obj)
#   sci_row.save()

# def update_archived_flag(sysmeta_obj):
#   pid = sysmeta_obj.identifier.value()
#   sci_row = get_sci_row(pid)
#   sci_row.is_archived = archived_bool
#
#     sci_row.serial_version = m.serialVersion
#   sci_row.save()


def get_pids_in_obsolescence_chain(pid):
  """Given the PID of any object in a chain, return a list of all PIDs in the
  chain. The returned list is in the same order as the chain. The initial PID is
  typically obtained by resolving a SID. If the given PID is not in a chain, a
  list containing the single object is returned.
  """
  sci_row = _get_sci_row(pid)
  while sci_row.obsoletes:
    sci_row = _get_sci_row(sci_row.obsoletes.pid.sid_or_pid)
  chain_pid_list = [sci_row.pid.sid_or_pid]
  while sci_row.obsoleted_by:
    sci_row = _get_sci_row(sci_row.obsoleted_by.pid.sid_or_pid)
    chain_pid_list.append(sci_row.pid.sid_or_pid)
  return chain_pid_list


def is_sid_in_obsolescence_chain(sid, pid):
  """Determine if {sid} resolves to an object in the obsolescence chain to which
  {pid} belongs.

  Preconditions:
  - {sid} is verified to exist. E.g., with view_asserts.is_sid().
  """
  chain_pid_list = mn.sysmeta_db.get_pids_in_obsolescence_chain(pid)
  resolved_pid = resolve_sid(sid)
  return resolved_pid in chain_pid_list


def is_identifier(sid_or_pid):
  return mn.models.IdNamespace.objects.filter(sid_or_pid=sid_or_pid).exists()


def is_pid(sid_or_pid):
  return is_pid_of_existing_object(sid_or_pid) or is_pid_in_replication_queue(sid_or_pid)


def is_pid_of_existing_object(sid_or_pid):
  return mn.models.ScienceObject.objects.filter(
    pid__sid_or_pid=sid_or_pid).exists()


def is_pid_in_replication_queue(sid_or_pid):
  return mn.models.ReplicationQueue.objects.filter(
    pid__sid_or_pid=sid_or_pid).exists()


def is_sid(sid_or_pid):
  return mn.models.SeriesIdToScienceObject.objects.filter(
    sid__sid_or_pid=sid_or_pid
  ).exists()


def is_replica(pid):
  return _get_sci_row(pid).is_replica


def is_archived(pid):
  return _get_sci_row(pid).is_archived


def is_obsoleted(pid):
  return _get_sci_row(pid).obsoleted_by is not None

#
# Private
#


def _get_sci_row(pid):
  return mn.models.ScienceObject.objects.get(pid__sid_or_pid=pid)

# def _update_sid(sci_row, sysmeta_obj):
#   try:
#     sid = sysmeta_obj.seriesId.value()
#   except (ValueError, AttributeError):
#     return
#   sid_row = _get_or_create_sid(sid)
#   sid_row.object = sci_row
#   sid_row.save()


def _update_sci_row(sci_row, sysmeta_obj, url=None, is_replica=None):
  # The PID is used for looking up the sci_row so will always match and does
  # need to be updated.
  #
  # Any SID in the sysmeta is not updated in the DB here because the DB version
  # of the SID is used for mapping directly to the last PID in the chain. Since
  # any number of objects in a chain may specify (the same) SID for the chain,
  # updating the SID here would cause it to map to the object with the most
  # recently modified sysmeta in the chain.
  #
  # System Metadata fields
  sci_row.serial_version = sysmeta_obj.serialVersion
  sci_row.format = _get_or_create_format_row(sysmeta_obj.formatId)
  sci_row.checksum = sysmeta_obj.checksum.value()
  sci_row.checksum_algorithm = _get_or_create_checksum_algorithm_row(
    sysmeta_obj.checksum.algorithm
  )
  sci_row.size = sysmeta_obj.size
  sci_row.mtime = sysmeta_obj.dateSysMetadataModified
  obsoletes_pid = sysmeta_base.get_value(sysmeta_obj, 'obsoletes')
  sci_row.obsoletes = get_sci_row(obsoletes_pid) if obsoletes_pid else None
  obsoleted_by_pid = sysmeta_base.get_value(sysmeta_obj, 'obsoletedBy')
  sci_row.obsoleted_by = get_sci_row(
    obsoleted_by_pid
  ) if obsoleted_by_pid else None
  sci_row.is_archived = sysmeta_obj.archived or False
  # Internal fields
  if url is not None:
    sci_row.url = url
  sci_row.is_replica = is_replica or False
  sci_row.save()

  # pid = sysmeta_obj.identifier.value()
  # sci_row = get_sci_row(pid)
  # _update_sci_row(sci_row, sysmeta_obj, url, is_replica)
  # sci_row.save()
  # _update_access_policy(sci_row, sysmeta_obj)
  # _update_obsolescence_chain(sci_row, sysmeta_obj)
  # _update_sid(sci_row, sysmeta_obj)
  # _update_mtime(sci_row, sysmeta_obj)

  # .objects.get_or_create(pid=pid_row)
  # try:
  #   
  # except mn.models.ScienceObject.DoesNotExist:
  #   sci_row = mn.models.ScienceObject()
  #   sci_row.pid = pid_row

  # sid_row mn.models.IdNamespace.objects.get_or_create(sid_or_pid=sid_or_pid)[0]

  # def _id_exists(sid_or_pid):
  #   return mn.models.IdNamespace.objects.filter(sid_or_pid=sid_or_pid).exists()

  # def _get_or_create_sci_row(pid_row):
  #   return mn.models.ScienceObject.objects.get_or_create(pid=pid_row)
  #   # try:
  #   #   sci_row = mn.models.ScienceObject.objects.get(pid=pid_row)
  #   # except mn.models.ScienceObject.DoesNotExist:
  #   #   sci_row = mn.models.ScienceObject()
  #   #   sci_row.pid = pid_row
  # 
  # 
  # def _get_or_create_id(sid_or_pid):
  #   return mn.models.IdNamespace.objects.get_or_create(sid_or_pid=sid_or_pid)[0]
  # 
  # 
  # def _get_or_create_sid(sid):
  #   id_row = _get_or_create_id(sid)
  #   return mn.models.SeriesIdToScienceObject.objects.get_or_create(sid=id_row)


def _get_or_create_format_row(format_id):
  return mn.models.ScienceObjectFormat.objects.get_or_create(
    format_id=format_id
  )[0]


def _get_or_create_checksum_algorithm_row(checksum_algorithm_str):
  return mn.models.ScienceObjectChecksumAlgorithm.objects.get_or_create(
    checksum_algorithm=checksum_algorithm_str
  )[0]

# ------------------------------------------------------------------------------
# Access Policy
# ------------------------------------------------------------------------------


def _update_access_policy(sci_row, sysmeta_obj):
  """Create or update the database representation of the sysmeta_obj access
  policy.

  If called without an access policy, any existing permissions on the object
  are removed and the access policy for the rights holder is recreated.

  Preconditions:
    - Each subject has been verified to a valid DataONE account.
    - Subject has changePermission for object.

  Postconditions:
    - The Permission and related tables contain the new access policy.
    - The SysMeta object in the filesystem contains the new access policy.

  Notes:
    - There can be multiple rules in a policy and each rule can contain multiple
      subjects. So there are two ways that the same subject can be specified
      multiple times in a policy. If this happens, multiple, conflicting action
      levels may be provided for the subject. This is handled by checking for an
      existing row for the subject for this object and updating it if it
      contains a lower action level. The end result is that there is one row for
      each subject, for each object and this row contains the highest action
      level.
  """
  # Remove any existing permissions for this object. The temporary absence of
  # permissions is hidden in Django's implicit view transaction
  # (ATOMIC_REQUESTS).
  #
  # The models.CASCADE property is set on all ForeignKey fields, so most object
  # related info is deleted when deleting the IdNamespace "root".
  mn.models.Permission.objects.filter(
    object__pid__sid_or_pid=sysmeta_obj.identifier.value()
  ).delete()

  # Add an implicit allow rule with all permissions for the rights holder.
  allow_rights_holder = d1_common.types.dataoneTypes.AccessRule()
  permission = d1_common.types.dataoneTypes.Permission(
    mn.auth.CHANGEPERMISSION_STR
  )
  allow_rights_holder.permission.append(permission)
  allow_rights_holder.subject.append(sysmeta_obj.rightsHolder)
  top_level = _get_highest_level_action_for_rule(allow_rights_holder)
  _insert_permission_rows(sci_row, allow_rights_holder, top_level)

  # Create db entries for all subjects for which permissions have been granted.
  if sysmeta_obj.accessPolicy:
    for allow_rule in sysmeta_obj.accessPolicy.allow:
      top_level = _get_highest_level_action_for_rule(allow_rule)
      _insert_permission_rows(sci_row, allow_rule, top_level)


def _get_highest_level_action_for_rule(allow_rule):
  top_level = 0
  for permission in allow_rule.permission:
    level = mn.auth.action_to_level(permission)
    if level > top_level:
      top_level = level
  return top_level


def _insert_permission_rows(sci_row, allow_rule, top_level):
  for i in range(3):
    savepoint = django.db.transaction.savepoint()
    try:
      _insert_permission_rows_transaction(sci_row, allow_rule, top_level)
    except django.db.IntegrityError, django.db.DatabaseError:
      django.db.transaction.savepoint_rollback(savepoint)
      if i == 2:
        raise
      time.sleep(3)
    else:
      django.db.transaction.savepoint_commit(savepoint)
      break


def _insert_permission_rows_transaction(sci_row, allow_rule, top_level):
  subjects_required = set([s.value() for s in allow_rule.subject])
  permission_create_rows = []
  subjects_existing = set()
  for subject_existing_row in mn.models.PermissionSubject.objects.filter(
    subject__in=subjects_required
  ):
    subjects_existing.add(subject_existing_row.subject)
    permission_create_rows.append(
      mn.models.Permission(
        object=sci_row,
        subject=subject_existing_row,
        level=top_level
      )
    )

  subjects_missing = subjects_required - subjects_existing

  for s in subjects_missing:
    subject_row = mn.models.PermissionSubject(subject=s)
    subject_row.save()
    permission_create_rows.append(
      mn.models.Permission(
        object=sci_row, subject=subject_row,
        level=top_level
      )
    )

  mn.models.Permission.objects.bulk_create(permission_create_rows)
