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
"""Utilities for manipulating System Metadata
- Translate System Metadata between XML and PyXB.
- Translate System Metadata between PyXB and GMN database representations.
- Query the database for System Metadata properties.
"""

from __future__ import absolute_import

import datetime

import pyxb

import d1_gmn.app
import d1_gmn.app.auth
import d1_gmn.app.local_replica
import d1_gmn.app.models
import d1_gmn.app.revision
import d1_gmn.app.util

import d1_common.access_policy
import d1_common.date_time
import d1_common.types
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util
import d1_common.xml


def archive_object(pid):
  """Set the status of an object to archived.

  Preconditions:
  - The object with the pid is verified to exist.
  - The object is not a replica.
  - The object is not archived.
  """
  sciobj_model = d1_gmn.app.util.get_sci_model(pid)
  sciobj_model.is_archived = True
  sciobj_model.save()
  _update_modified_timestamp(sciobj_model)


def serialize(sysmeta_pyxb):
  try:
    return sysmeta_pyxb.toxml('utf-8')
  except pyxb.IncompleteElementContentError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unable to serialize PyXB to XML. error="{}"'.format(e.details())
    )


def serialize_pretty(sysmeta_pyxb):
  return d1_common.xml.pretty_xml(serialize(sysmeta_pyxb))


# ------------------------------------------------------------------------------


def create_or_update(sysmeta_pyxb, url=None):
  """Create or update database representation of a System Metadata object and
  closely related internal state.

  Preconditions:
  - For Create, PID is verified not to exist. E.g., with
  d1_gmn.app.views.asserts.is_unused(pid).
  - Any supplied SID is verified to be valid for the given operation. E.g., with
  d1_gmn.app.views.asserts.is_valid_sid_for_chain().
  """

  pid = d1_common.xml.uvalue(sysmeta_pyxb.identifier)

  try:
    sci_model = d1_gmn.app.util.get_sci_model(pid)
  except d1_gmn.app.models.ScienceObject.DoesNotExist:
    sci_model = d1_gmn.app.models.ScienceObject()
    sci_model.pid = d1_gmn.app.models.did(pid)
    sci_model.url = url
    sci_model.serial_version = sysmeta_pyxb.serialVersion
    sci_model.uploaded_timestamp = sysmeta_pyxb.dateUploaded

  _base_pyxb_to_model(sci_model, sysmeta_pyxb)
  sci_model.save()

  if _has_media_type_pyxb(sysmeta_pyxb):
    _media_type_pyxb_to_model(sci_model, sysmeta_pyxb)

  _access_policy_pyxb_to_model(sci_model, sysmeta_pyxb)

  if _has_replication_policy_pyxb(sysmeta_pyxb):
    _replication_policy_pyxb_to_model(sci_model, sysmeta_pyxb)

  replica_pyxb_to_model(sci_model, sysmeta_pyxb)

  return sci_model


def is_did(did):
  return d1_gmn.app.models.IdNamespace.objects.filter(did=did).exists()


def is_pid(did):
  """An identifier is a PID if it exists in IdNamespace and is not a SID.
  Includes unprocessed replicas and revision chain placeholders for remote
  objects.
  """
  return is_did(did) and not d1_gmn.app.revision.is_sid(did)


def is_pid_of_existing_object(pid):
  """Excludes SIDs, unprocessed replicas and revision chain placeholders for
  remote objects.
  """
  return d1_gmn.app.models.ScienceObject.objects.filter(pid__did=pid).exists()


def is_archived(pid):
  return is_pid_of_existing_object(pid) \
         and d1_gmn.app.util.get_sci_model(pid).is_archived


def update_modified_timestamp(pid):
  sci_model = d1_gmn.app.util.get_sci_model(pid)
  _update_modified_timestamp(sci_model)


def model_to_pyxb(pid):
  return _model_to_pyxb(pid)


def get_identifier_type(did):
  if not is_did(did):
    return u'unused on this Member Node'
  elif d1_gmn.app.revision.is_sid(did):
    return u'a Series ID (SID)'
  elif is_pid_of_existing_object(did):
    return u'a Persistent ID (PID) of an existing local object'
  elif d1_gmn.app.local_replica.is_local_replica(did):
    return u'a Persistent ID (PID) of a local replica'
  elif d1_gmn.app.local_replica.is_revision_chain_placeholder(did):
    return \
      u'a Persistent ID (PID) that is reserved due to being referenced in ' \
      u'the revision chain of a local replica'
  else:
    assert False, u'Unable to classify identifier'


def _model_to_pyxb(pid):
  sciobj_model = d1_gmn.app.util.get_sci_model(pid)
  sysmeta_pyxb = _base_model_to_pyxb(sciobj_model)
  if _has_media_type_db(sciobj_model):
    sysmeta_pyxb.mediaType = _media_type_model_to_pyxb(sciobj_model)
  if _has_access_policy_db(sciobj_model):
    sysmeta_pyxb.accessPolicy = _access_policy_model_to_pyxb(sciobj_model)
  if _has_replication_policy_db(sciobj_model):
    sysmeta_pyxb.replicationPolicy = _replication_policy_model_to_pyxb(
      sciobj_model
    )
  sysmeta_pyxb.replica = replica_model_to_pyxb(sciobj_model)
  return sysmeta_pyxb


def _base_pyxb_to_model(sci_model, sysmeta_pyxb):
  sci_model.modified_timestamp = sysmeta_pyxb.dateSysMetadataModified
  sci_model.format = d1_gmn.app.models.format(sysmeta_pyxb.formatId)
  sci_model.filename = getattr(sysmeta_pyxb, 'fileName', None)
  sci_model.checksum = d1_common.xml.uvalue(sysmeta_pyxb.checksum)
  sci_model.checksum_algorithm = d1_gmn.app.models.checksum_algorithm(
    sysmeta_pyxb.checksum.algorithm
  )
  sci_model.size = sysmeta_pyxb.size
  if sysmeta_pyxb.submitter:
    sci_model.submitter = d1_gmn.app.models.subject(
      d1_common.xml.uvalue(sysmeta_pyxb.submitter)
    )
  sci_model.rights_holder = d1_gmn.app.models.subject(
    d1_common.xml.uvalue(sysmeta_pyxb.rightsHolder)
  )
  sci_model.origin_member_node = d1_gmn.app.models.node(
    d1_common.xml.uvalue(sysmeta_pyxb.originMemberNode)
  )
  sci_model.authoritative_member_node = d1_gmn.app.models.node(
    d1_common.xml.uvalue(sysmeta_pyxb.authoritativeMemberNode)
  )
  d1_gmn.app.revision.set_revision_by_model(
    sci_model,
    d1_common.xml.get_value(sysmeta_pyxb, 'obsoletes'),
    d1_common.xml.get_value(sysmeta_pyxb, 'obsoletedBy'),
  )
  sci_model.is_archived = sysmeta_pyxb.archived or False
  # series_id = d1_gmn.app.util.get_value(sysmeta_pyxb, 'seriesId')
  # if series_id:
  #   d1_gmn.app.sysmeta_revision.update_or_create_sid_to_pid_map(
  #     series_id, d1_common.xml.uvalue(sysmeta_pyxb.identifier)
  #   )


def _base_model_to_pyxb(sciobj_model):
  def sub_sciobj(sub_sciobj_model):
    if sub_sciobj_model is None:
      return None
    return sub_sciobj_model.did

  base_pyxb = d1_common.types.dataoneTypes.systemMetadata()
  base_pyxb.identifier = d1_common.types.dataoneTypes.Identifier(
    sciobj_model.pid.did
  )
  base_pyxb.serialVersion = sciobj_model.serial_version
  base_pyxb.dateSysMetadataModified = sciobj_model.modified_timestamp
  base_pyxb.dateUploaded = sciobj_model.uploaded_timestamp
  base_pyxb.formatId = sciobj_model.format.format
  base_pyxb.fileName = sciobj_model.filename
  base_pyxb.checksum = d1_common.types.dataoneTypes.Checksum(
    sciobj_model.checksum
  )
  base_pyxb.checksum.algorithm = sciobj_model.checksum_algorithm.checksum_algorithm
  base_pyxb.size = sciobj_model.size
  base_pyxb.submitter = sciobj_model.submitter.subject
  base_pyxb.rightsHolder = sciobj_model.rights_holder.subject
  base_pyxb.originMemberNode = sciobj_model.origin_member_node.urn
  base_pyxb.authoritativeMemberNode = sciobj_model.authoritative_member_node.urn
  base_pyxb.obsoletes = sub_sciobj(sciobj_model.obsoletes)
  base_pyxb.obsoletedBy = sub_sciobj(sciobj_model.obsoleted_by)
  base_pyxb.archived = sciobj_model.is_archived
  base_pyxb.seriesId = d1_gmn.app.revision.get_sid_by_pid(sciobj_model.pid.did)
  return base_pyxb


def _update_modified_timestamp(sci_model):
  sci_model.modified_timestamp = datetime.datetime.utcnow()
  sci_model.save()


# ------------------------------------------------------------------------------
# Media Type
# ------------------------------------------------------------------------------

# <!--Optional:-->
# <mediaType name="string">
#   <!--Zero or more repetitions:-->
#   <property name="string">string1</property>
#   <property name="string">string3</property>
#   <property name="string">string4</property>
# </mediaType>


def _has_media_type_pyxb(sysmeta_pyxb):
  return hasattr(
    sysmeta_pyxb, 'mediaType'
  ) and sysmeta_pyxb.mediaType is not None


def _media_type_pyxb_to_model(sci_model, sysmeta_pyxb):
  _delete_existing_media_type(sysmeta_pyxb)
  media_type_model = _insert_media_type_name_row(
    sci_model, sysmeta_pyxb.mediaType
  )
  _insert_media_type_property_rows(media_type_model, sysmeta_pyxb.mediaType)


def _delete_existing_media_type(sysmeta_pyxb):
  d1_gmn.app.models.MediaType.objects.filter(
    sciobj__pid__did=d1_common.xml.uvalue(sysmeta_pyxb.identifier)
  ).delete()


def _insert_media_type_name_row(sci_model, media_type_pyxb):
  media_type_model = d1_gmn.app.models.MediaType(
    sciobj=sci_model, name=media_type_pyxb.name
  )
  media_type_model.save()
  return media_type_model


def _insert_media_type_property_rows(media_type_model, media_type_pyxb):
  for p in media_type_pyxb.property_:
    media_type_property_model = d1_gmn.app.models.MediaTypeProperty(
      media_type=media_type_model, name=p.name, value=d1_common.xml.uvalue(p)
    )
    media_type_property_model.save()


def _has_media_type_db(sciobj_model):
  return d1_gmn.app.models.MediaType.objects.filter(sciobj=sciobj_model).exists()


def _media_type_model_to_pyxb(sciobj_model):
  media_type_model = d1_gmn.app.models.MediaType.objects.get(
    sciobj=sciobj_model
  )
  media_type_pyxb = d1_common.types.dataoneTypes.MediaType()
  media_type_pyxb.name = media_type_model.name

  for media_type_property_model in d1_gmn.app.models.MediaTypeProperty.objects.filter(
      media_type=media_type_model
  ).order_by('name', 'value'):
    media_type_property_pyxb = d1_common.types.dataoneTypes.MediaTypeProperty(
      media_type_property_model.value, name=media_type_property_model.name
    )
    media_type_pyxb.property_.append(media_type_property_pyxb)

  return media_type_pyxb


# ------------------------------------------------------------------------------
# Access Policy
# ------------------------------------------------------------------------------


def _access_policy_pyxb_to_model(sci_model, sysmeta_pyxb):
  """Create or update the database representation of the sysmeta_pyxb access
  policy.

  If called without an access policy, any existing permissions on the object
  are removed and the access policy for the rights holder is recreated.

  Preconditions:
    - Each subject has been verified to a valid DataONE account.
    - Subject has changePermission for object.

  Postconditions:
    - The Permission and related tables contain the new access policy.

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
  _delete_existing_access_policy(sysmeta_pyxb)
  # Add an implicit allow rule with all permissions for the rights holder.
  allow_rights_holder = d1_common.types.dataoneTypes.AccessRule()
  permission = d1_common.types.dataoneTypes.Permission(
    d1_gmn.app.auth.CHANGEPERMISSION_STR
  )
  allow_rights_holder.permission.append(permission)
  allow_rights_holder.subject.append(
    d1_common.xml.uvalue(sysmeta_pyxb.rightsHolder)
  )
  top_level = _get_highest_level_action_for_rule(allow_rights_holder)
  _insert_permission_rows(sci_model, allow_rights_holder, top_level)
  # Create db entries for all subjects for which permissions have been granted.
  if _has_access_policy_pyxb(sysmeta_pyxb):
    for allow_rule in sysmeta_pyxb.accessPolicy.allow:
      top_level = _get_highest_level_action_for_rule(allow_rule)
      _insert_permission_rows(sci_model, allow_rule, top_level)


def _has_access_policy_db(sciobj_model):
  return d1_gmn.app.models.Permission.objects.filter(sciobj=sciobj_model
                                                     ).exists()


def _has_access_policy_pyxb(sysmeta_pyxb):
  return hasattr(
    sysmeta_pyxb, 'accessPolicy'
  ) and sysmeta_pyxb.accessPolicy is not None


def _delete_existing_access_policy(sysmeta_pyxb):
  d1_gmn.app.models.Permission.objects.filter(
    sciobj__pid__did=d1_common.xml.uvalue(sysmeta_pyxb.identifier)
  ).delete()


def _get_highest_level_action_for_rule(allow_rule):
  top_level = 0
  for permission in allow_rule.permission:
    level = d1_gmn.app.auth.action_to_level(permission)
    if level > top_level:
      top_level = level
  return top_level


def _insert_permission_rows(sci_model, allow_rule, top_level):
  for s in allow_rule.subject:
    permission_model = d1_gmn.app.models.Permission(
      sciobj=sci_model,
      subject=d1_gmn.app.models.subject(d1_common.xml.uvalue(s)),
      level=top_level
    )
    permission_model.save()


def _access_policy_model_to_pyxb(sciobj_model):
  access_policy_pyxb = d1_common.types.dataoneTypes.AccessPolicy()
  for permission_model in d1_gmn.app.models.Permission.objects.filter(
      sciobj=sciobj_model
  ).order_by('subject', 'level', 'sciobj__pid__did'):
    # Skip implicit permissions for rightsHolder.
    if permission_model.subject.subject == sciobj_model.rights_holder.subject:
      continue
    access_rule_pyxb = d1_common.types.dataoneTypes.AccessRule()
    permission_pyxb = d1_common.types.dataoneTypes.Permission(
      d1_gmn.app.auth.level_to_action(permission_model.level)
    )
    access_rule_pyxb.permission.append(permission_pyxb)
    access_rule_pyxb.subject.append(permission_model.subject.subject)
    access_policy_pyxb.allow.append(access_rule_pyxb)
  if len(access_policy_pyxb.allow):
    return d1_common.access_policy.normalize(access_policy_pyxb)


# ------------------------------------------------------------------------------
# Replication Policy
# ------------------------------------------------------------------------------

# <replicationPolicy xmlns="" replicationAllowed="false" numberReplicas="0">
#     <preferredMemberNode>preferredMemberNode0</preferredMemberNode>
#     <preferredMemberNode>preferredMemberNode1</preferredMemberNode>
#     <blockedMemberNode>blockedMemberNode0</blockedMemberNode>
#     <blockedMemberNode>blockedMemberNode1</blockedMemberNode>
# </replicationPolicy>


def _replication_policy_pyxb_to_model(sciobj_model, sysmeta_pyxb):
  _delete_existing_replication_policy(sciobj_model)

  replication_policy_model = d1_gmn.app.models.ReplicationPolicy()
  replication_policy_model.sciobj = sciobj_model
  replication_policy_model.replication_is_allowed = (
    sysmeta_pyxb.replicationPolicy.replicationAllowed
  )
  replication_policy_model.desired_number_of_replicas = (
    sysmeta_pyxb.replicationPolicy.numberReplicas
  )
  replication_policy_model.save()

  def add(node_ref_pyxb, rep_node_model):
    for rep_node_urn in node_ref_pyxb:
      # node_urn_model = d1_gmn.app.models.Node.objects.get_or_create(
      #   urn=rep_node_urn.value()
      # )[0]
      node_urn_model = d1_gmn.app.models.node(
        d1_common.xml.uvalue(rep_node_urn)
      )
      rep_node_obj = rep_node_model()
      rep_node_obj.node = node_urn_model
      rep_node_obj.replication_policy = replication_policy_model
      rep_node_obj.save()

  add(
    sysmeta_pyxb.replicationPolicy.preferredMemberNode,
    d1_gmn.app.models.PreferredMemberNode
  )
  add(
    sysmeta_pyxb.replicationPolicy.blockedMemberNode,
    d1_gmn.app.models.BlockedMemberNode
  )

  return replication_policy_model


def _has_replication_policy_db(sciobj_model):
  return d1_gmn.app.models.ReplicationPolicy.objects.filter(
    sciobj=sciobj_model
  ).exists()


def _delete_existing_replication_policy(sciobj_model):
  d1_gmn.app.models.ReplicationPolicy.objects.filter(sciobj=sciobj_model
                                                     ).delete()


def _has_replication_policy_pyxb(sysmeta_pyxb):
  return hasattr(
    sysmeta_pyxb, 'replicationPolicy'
  ) and sysmeta_pyxb.replicationPolicy is not None


def _replication_policy_model_to_pyxb(sciobj_model):
  replication_policy_model = d1_gmn.app.models.ReplicationPolicy.objects.get(
    sciobj=sciobj_model
  )
  replication_policy_pyxb = d1_common.types.dataoneTypes.ReplicationPolicy()
  replication_policy_pyxb.replicationAllowed = replication_policy_model.replication_is_allowed
  replication_policy_pyxb.numberReplicas = replication_policy_model.desired_number_of_replicas

  def add(rep_pyxb, rep_node_model):
    for rep_node in rep_node_model.objects.filter(
        replication_policy=replication_policy_model
    ).order_by('node__urn'):
      rep_pyxb.append(rep_node.node.urn)

  add(
    replication_policy_pyxb.preferredMemberNode,
    d1_gmn.app.models.PreferredMemberNode
  )
  add(
    replication_policy_pyxb.blockedMemberNode,
    d1_gmn.app.models.BlockedMemberNode
  )

  return replication_policy_pyxb


# ------------------------------------------------------------------------------
# Remote Replica
# ------------------------------------------------------------------------------

# <replica xmlns="">
#     <replicaMemberNode>replicaMemberNode0</replicaMemberNode>
#     <replicationStatus>queued</replicationStatus>
#     <replicaVerified>2006-05-04T18:13:51.0</replicaVerified>
# </replica>


def replica_pyxb_to_model(sciobj_model, sysmeta_pyxb):
  d1_gmn.app.models.RemoteReplica.objects.filter(sciobj=sciobj_model).delete()
  for replica_pyxb in sysmeta_pyxb.replica:
    _register_remote_replica(sciobj_model, replica_pyxb)


def _register_remote_replica(sciobj_model, replica_pyxb):
  replica_info_model = d1_gmn.app.models.replica_info(
    status_str=replica_pyxb.replicationStatus,
    source_node_urn=d1_common.xml.uvalue(replica_pyxb.replicaMemberNode),
    timestamp=replica_pyxb.replicaVerified,
  )
  d1_gmn.app.models.remote_replica(
    sciobj_model=sciobj_model,
    replica_info_model=replica_info_model,
  )


def replica_model_to_pyxb(sciobj_model):
  replica_pyxb_list = []
  for replica_model in d1_gmn.app.models.RemoteReplica.objects.filter(
      sciobj=sciobj_model
  ).order_by('info__timestamp', 'info__member_node__urn'):
    replica_pyxb = d1_common.types.dataoneTypes.Replica()
    replica_pyxb.replicaMemberNode = replica_model.info.member_node.urn
    replica_pyxb.replicationStatus = replica_model.info.status.status
    replica_pyxb.replicaVerified = d1_common.date_time.cast_datetime_to_utc(
      replica_model.info.timestamp
    )
    replica_pyxb_list.append(replica_pyxb)
  return replica_pyxb_list
