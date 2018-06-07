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
"""Utilities for working with SIDs and PIDs
"""

import logging

import d1_gmn.app
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.resource_map
import d1_gmn.app.revision
import d1_gmn.app.util


def is_valid_pid_for_create(did):
  """Return True if {did} is the PID of an object that can be created with
  MNStorage.create() or MNStorage.update().

  To be valid for create() and update(), the DID:

  - Must not be the PID of an object that exists on this MN
  - Must not be a known SID known to this MN
  - Must not have been accepted for replication by this MN.
  - Must not be referenced as obsoletes or obsoletedBy in an object that exists on this MN

  In addition, if the DID exists in a resource map:

  - If RESOURCE_MAP_CREATE = 'reserve':

    - The DataONE subject that is making the call must have write or
    changePermission on the resource map.
  """
  # logging.debug('existing: {}'.format(is_existing_object(did)))
  # logging.debug('sid: {}'.format(is_sid(did)))
  # logging.debug('local_replica: {}'.format(is_local_replica(did)))
  # logging.debug('revision: {}'.format(d1_gmn.app.revision.is_revision(did)))
  return (
    not is_existing_object(did) and not is_sid(did) and
    not is_local_replica(did) and not d1_gmn.app.revision.is_revision(did) and
    d1_gmn.app.resource_map.is_sciobj_valid_for_create()
  )


def is_valid_pid_to_be_updated(did):
  """Return True if {did} is the PID of an object that can be updated
  (obsoleted) with MNStorage.update()
  """
  return (
    is_existing_object(did) and not is_local_replica(did) and
    not is_archived(did) and not is_obsoleted(did)
  )


def is_valid_sid_for_new_standalone(did):
  """Return True if {did} can be assigned to a new standalone object
  """
  return _is_unused_did(did)


def is_valid_sid_for_chain(pid, sid):
  """Return True if {sid} can be assigned to the single object {pid} or to the
  chain to which {pid} belongs.

  - If the chain does not have a SID, the new SID must be previously unused.
  - If the chain already has a SID, the new SID must match the existing SID.

  All known PIDs are associated with a chain.

  Preconditions:
  - {pid} is verified to exist. E.g., with d1_gmn.app.views.asserts.is_existing_object().
  - {sid} is None or verified to be a SID
  """
  if _is_unused_did(sid):
    return True
  existing_sid = d1_gmn.app.revision.get_sid_by_pid(pid)
  if existing_sid is None:
    return False
  return existing_sid == sid


def get_did_by_foreign_key(did_foreign_key):
  """Return the DID referenced by a ForeignKey or OneToOneField to IdNamespace

  Return None if ForeignKey or OneToOneField is NULL.

  This is used instead of "did_foreign_key.*.did" on ForeignKeys and
  OneToOneFields that allow NULL (null=True in the model).
  """
  return getattr(did_foreign_key, 'did', None)


def is_existing_object(did):
  """Return True if PID is for an object for which science bytes are stored
  locally

  This excludes SIDs and PIDs for unprocessed replica requests, remote or
  non-existing revisions of local replicas and objects aggregated in Resource
  Maps.
  """
  return d1_gmn.app.models.ScienceObject.objects.filter(pid__did=did).exists()


def is_sid(did):
  return d1_gmn.app.models.Chain.objects.filter(sid__did=did).exists()


def is_obsoleted(did):
  """Return True if {did} is the PID of an object that has been obsoleted"""
  return d1_gmn.app.model_util.get_sci_model(did).obsoleted_by is not None


def is_resource_map_db(pid):
  return d1_gmn.app.models.ResourceMap.objects.filter(pid__did=pid).exists()


def is_resource_map_member(pid):
  return d1_gmn.app.models.ResourceMapMember.objects.filter(did__did=pid
                                                            ).exists()


def classify_identifier(did):
  """Return a text fragment classifying the {did}

  Return <UNKNOWN> if the DID could not be classified. This should not
  normally happen and may indicate that the DID was orphaned in the database.
  """
  if _is_unused_did(did):
    return 'unused on this Member Node'
  elif is_sid(did):
    return 'a Series ID (SID) of a revision chain'
  elif is_local_replica(did):
    return 'a Persistent ID (PID) of a local replica'
  elif is_resource_map_db(did):
    return 'a Persistent ID (PID) of a local resource map'
  elif is_existing_object(did):
    return 'a Persistent ID (PID) of an existing local object'
  elif is_revision_chain_placeholder(did):
    return (
      'a Persistent ID (PID) of a remote or non-existing revision of a local '
      'replica'
    )
  elif is_resource_map_member(did):
    return (
      'a Persistent ID (PID) of a remote or non-existing object aggregated in '
      'a local Resource Map'
    )
  logging.warning('Unable to classify known identifier. did="{}"'.format(did))
  return '<UNKNOWN>'


def get_or_create_did(id_str):
  return d1_gmn.app.models.IdNamespace.objects.get_or_create(did=id_str)[0]


def is_in_revision_chain(sciobj_model):
  return bool(sciobj_model.obsoleted_by or sciobj_model.obsoletes)


def is_archived(pid):
  return (
    is_existing_object(pid) and
    d1_gmn.app.model_util.get_sci_model(pid).is_archived
  )


def is_local_replica(pid):
  """Includes unprocessed replication requests."""
  return d1_gmn.app.models.LocalReplica.objects.filter(pid__did=pid).exists()


def is_unprocessed_local_replica(pid):
  """Is local replica with status "queued"."""
  return d1_gmn.app.models.LocalReplica.objects.filter(
    pid__did=pid,
    info__status__status='queued',
  ).exists()


def is_revision_chain_placeholder(pid):
  """For replicas, the PIDs referenced in revision chains are reserved for
  use by other replicas."""
  return d1_gmn.app.models.ReplicaRevisionChainReference.objects.filter(
    pid__did=pid
  ).exists()


# These are private methods because decisions cannot typically be based only on
# the existence or non-existence of an identifier. Instead, use or make a
# "is_valid_for_*" method.


def _is_unused_did(did):
  """Return True if {did} is not recorded in any local context

  {did}=None is supported and returns True.

  A DID can be classified with classify_identifier().
  """
  return not _is_did(did)


def _is_did(did):
  """Return True if {did} is recorded in a local context

  {did}=None is supported and returns False.

  A DID can be classified with classify_identifier().
  """
  return d1_gmn.app.models.IdNamespace.objects.filter(did=did).exists()


def _is_pid(did):
  """Return True if {did} exists in IdNamespace and is not a SID.

  {did}=None is supported and returns False.

  Note: Non-existing and remote DIDs may not be known to be SIDs or PIDs, and
  are assumed to be PIDs by this function.
  """
  return _is_did(did) and not is_sid(did)
