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

# Stdlib
import d1_common.xml
import datetime

# 3rd party
import pyxb

# D1
import d1_common.date_time
import d1_common.types.dataoneTypes
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions
import d1_common.util

# App
import app.auth
import app.models
import app.sysmeta_obsolescence
import app.sysmeta_replica
import app.sysmeta_sid
import app.sysmeta_util
import app.util


def archive_object(pid):
  """Set the status of an object as archived.

  Preconditions:
  - The object with the pid is verified to exist.
  - The object is not a replica.
  - The object is not archived.
  """
  sciobj_model = app.sysmeta_util.get_sci_model(pid)
  sciobj_model.is_archived = True
  sciobj_model.save()
  _update_modified_timestamp(sciobj_model)


# ------------------------------------------------------------------------------
# XML
# ------------------------------------------------------------------------------


def deserialize(sysmeta_xml):
  if not isinstance(sysmeta_xml, unicode):
    try:
      sysmeta_xml = sysmeta_xml.decode('utf8')
    except UnicodeDecodeError as e:
      raise d1_common.types.exceptions.InvalidRequest(
        0, u'The System Metadata XML doc is not valid UTF-8 encoded Unicode. '
        u'error="{}", xml="{}"'.format(str(e), sysmeta_xml)
      )
  try:
    return d1_common.types.dataoneTypes_v2_0.CreateFromDocument(sysmeta_xml)
  except pyxb.ValidationError as e:
    err_str = e.details()
  except pyxb.PyXBException as e:
    err_str = str(e)
  raise d1_common.types.exceptions.InvalidSystemMetadata(
    0, u'System Metadata XML doc validation failed. error="{}", xml="{}"'
    .format(err_str, sysmeta_xml)
  )


def serialize(sysmeta_pyxb):
  try:
    return sysmeta_pyxb.toxml().encode('utf-8')
  except pyxb.IncompleteElementContentError as e:
    raise d1_common.types.exceptions.ServiceFailure(
      0, u'Unable to serialize PyXB to XML. error="{}"'.format(e.details())
    )


def serialize_pretty(sysmeta_pyxb):
  return d1_common.xml.pretty_xml(serialize(sysmeta_pyxb))


# ------------------------------------------------------------------------------


def create(sysmeta_pyxb, url):
  """Create database representation of a System Metadata object and closely
  related internal state.

  Preconditions:
  - PID is verified not to exist. E.g., with app.views.asserts.is_unused(pid).
  - Any supplied SID is verified to be valid for the given operation. E.g., with
  app.views.asserts.is_valid_sid_for_chain_if_specified().
  """
  pid = sysmeta_pyxb.identifier.value()
  sci_model = app.models.ScienceObject()
  sci_model.pid = app.models.did(pid)
  _base_pyxb_to_model(sci_model, sysmeta_pyxb, url)
  sci_model.save()
  if _has_access_policy_pyxb(sysmeta_pyxb):
    _access_policy_pyxb_to_model(sci_model, sysmeta_pyxb)
  if _has_replication_policy_pyxb(sysmeta_pyxb):
    _replication_policy_pyxb_to_model(sci_model, sysmeta_pyxb)
  return sci_model


def update(sysmeta_pyxb, url=None, skip_immutable=False):
  """Update database representation of a System Metadata object. The System
  Metadata must already be verified to be correct and suitable for the
  operation which is being performed.

  {skip_immutable} is False for create() and update()
  """
  pid = sysmeta_pyxb.identifier.value()
  sci_model = app.sysmeta_util.get_sci_model(pid)
  _base_pyxb_to_model(
    sci_model, sysmeta_pyxb, url=url, skip_immutable=skip_immutable
  )
  sci_model.save()
  if _has_access_policy_pyxb(sysmeta_pyxb):
    _access_policy_pyxb_to_model(sci_model, sysmeta_pyxb)
  if _has_replication_policy_pyxb(sysmeta_pyxb):
    _replication_policy_pyxb_to_model(sci_model, sysmeta_pyxb)


def is_did(did):
  return app.models.IdNamespace.objects.filter(did=did).exists()


def is_pid(did):
  """An identifier is a PID if it exists in IdNamespace and is not a SID.
  Includes unprocessed replicas and obsolescence chain placeholders for remote
  objects.
  """
  return is_did(did) and not app.sysmeta_sid.is_sid(did)


def is_pid_of_existing_object(pid):
  """Excludes SIDs, unprocessed replicas and obsolescence chain placeholders for
  remote objects.
  """
  return app.models.ScienceObject.objects.filter(pid__did=pid).exists()


def is_archived(pid):
  return is_pid_of_existing_object(pid) \
         and app.sysmeta_util.get_sci_model(pid).is_archived


def update_modified_timestamp(pid):
  sci_model = app.sysmeta_util.get_sci_model(pid)
  _update_modified_timestamp(sci_model)


def model_to_pyxb(pid):
  return _model_to_pyxb(pid)


def get_identifier_type(did):
  if not is_did(did):
    return u'unused on this Member Node'
  elif app.sysmeta_sid.is_sid(did):
    return u'a Series ID (SID)'
  elif is_pid_of_existing_object(did):
    return u'a Persistent ID (PID) of an existing local object'
  elif app.sysmeta_replica.is_local_replica(did):
    return u'a Persistent ID (PID) of a local replica'
  elif app.sysmeta_replica.is_obsolescence_chain_placeholder(did):
    return \
      u'a Persistent ID (PID) that is reserved due to being referenced in ' \
      u'the obsolescence chain of a local replica'
  else:
    assert False, u'Unable to classify identifier'


#
# Private
#


def _model_to_pyxb(pid):
  sciobj_model = app.sysmeta_util.get_sci_model(pid)
  sysmeta_pyxb = _base_model_to_pyxb(sciobj_model)
  if _has_access_policy_db(sciobj_model):
    sysmeta_pyxb.accessPolicy = _access_policy_model_to_pyxb(sciobj_model)
  if _has_replication_policy_db(sciobj_model):
    sysmeta_pyxb.replicationPolicy = _replication_policy_model_to_pyxb(
      sciobj_model
    )
  sysmeta_pyxb.replica = app.sysmeta_replica.replica_model_to_pyxb(sciobj_model)
  return sysmeta_pyxb


def _base_pyxb_to_model(
    sci_model, sysmeta_pyxb, url=None, skip_immutable=False
):
  # The PID is used for looking up the sci_model so will always match and does
  # need to be updated.
  #
  # Any SID in the sysmeta is not updated in the DB here because the DB version
  # of the SID is used for mapping directly to the last PID in the chain. Since
  # any number of objects in a chain may specify (the same) SID for the chain,
  # updating the SID here would cause it to map to the object with the most
  # recently modified sysmeta in the chain.
  #
  # System Metadata fields
  sci_model.modified_timestamp = sysmeta_pyxb.dateSysMetadataModified
  if not skip_immutable:
    sci_model.serial_version = sysmeta_pyxb.serialVersion
    sci_model.uploaded_timestamp = sysmeta_pyxb.dateUploaded
  sci_model.format = app.models.format(sysmeta_pyxb.formatId)
  sci_model.checksum = sysmeta_pyxb.checksum.value()
  sci_model.checksum_algorithm = app.models.checksum_algorithm(
    sysmeta_pyxb.checksum.algorithm
  )
  sci_model.size = sysmeta_pyxb.size
  sci_model.submitter = app.models.subject(sysmeta_pyxb.submitter.value())
  sci_model.rights_holder = app.models.subject(
    sysmeta_pyxb.rightsHolder.value()
  )
  sci_model.origin_member_node = app.models.node(
    sysmeta_pyxb.originMemberNode.value()
  )
  sci_model.authoritative_member_node = app.models.node(
    sysmeta_pyxb.authoritativeMemberNode.value()
  )
  app.sysmeta_obsolescence.set_obsolescence_by_model(
    sci_model,
    app.sysmeta_util.get_value(sysmeta_pyxb, 'obsoletes'),
    app.sysmeta_util.get_value(sysmeta_pyxb, 'obsoletedBy'),
  )
  sci_model.is_archived = sysmeta_pyxb.archived or False
  # Internal fields
  if url is not None:
    sci_model.url = url


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
  base_pyxb.seriesId = app.sysmeta_sid.get_sid_by_pid(sciobj_model.pid.did)

  return base_pyxb


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
    app.auth.CHANGEPERMISSION_STR
  )
  allow_rights_holder.permission.append(permission)
  allow_rights_holder.subject.append(sysmeta_pyxb.rightsHolder.value())
  top_level = _get_highest_level_action_for_rule(allow_rights_holder)
  _insert_permission_rows(sci_model, allow_rights_holder, top_level)
  # Create db entries for all subjects for which permissions have been granted.
  for allow_rule in sysmeta_pyxb.accessPolicy.allow:
    top_level = _get_highest_level_action_for_rule(allow_rule)
    _insert_permission_rows(sci_model, allow_rule, top_level)


def _has_access_policy_db(sciobj_model):
  return app.models.Permission.objects.filter(sciobj=sciobj_model).exists()


def _has_access_policy_pyxb(sysmeta_pyxb):
  return hasattr(
    sysmeta_pyxb, 'accessPolicy'
  ) and sysmeta_pyxb.accessPolicy is not None


def _delete_existing_access_policy(sysmeta_pyxb):
  app.models.Permission.objects.filter(
    sciobj__pid__did=sysmeta_pyxb.identifier.value()
  ).delete()


def _get_highest_level_action_for_rule(allow_rule):
  top_level = 0
  for permission in allow_rule.permission:
    level = app.auth.action_to_level(permission)
    if level > top_level:
      top_level = level
  return top_level


def _insert_permission_rows(sci_model, allow_rule, top_level):
  for s in allow_rule.subject:
    permission_model = app.models.Permission(
      sciobj=sci_model, subject=app.models.subject(s.value()), level=top_level
    )
    permission_model.save()


def _access_policy_model_to_pyxb(sciobj_model):
  access_policy_pyxb = d1_common.types.dataoneTypes.AccessPolicy()
  for permission_model in app.models.Permission.objects.filter(
      sciobj=sciobj_model
  ):
    # Skip implicit permissions for rightsHolder.
    if permission_model.subject.subject == sciobj_model.rights_holder.subject:
      continue
    access_rule_pyxb = d1_common.types.dataoneTypes.AccessRule()
    permission_pyxb = d1_common.types.dataoneTypes.Permission(
      app.auth.level_to_action(permission_model.level)
    )
    access_rule_pyxb.permission.append(permission_pyxb)
    access_rule_pyxb.subject.append(permission_model.subject.subject)
    access_policy_pyxb.allow.append(access_rule_pyxb)
  if len(access_policy_pyxb.allow):
    return access_policy_pyxb


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

  replication_policy_model = app.models.ReplicationPolicy()
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
      node_urn_model = app.models.Node.objects.get_or_create(
        urn=rep_node_urn.value()
      )[0]
      rep_node_obj = rep_node_model()
      rep_node_obj.node = node_urn_model
      rep_node_obj.replication_policy = replication_policy_model
      rep_node_obj.save()

  add(
    sysmeta_pyxb.replicationPolicy.preferredMemberNode,
    app.models.PreferredMemberNode
  )
  add(
    sysmeta_pyxb.replicationPolicy.blockedMemberNode,
    app.models.BlockedMemberNode
  )

  return replication_policy_model


def _has_replication_policy_db(sciobj_model):
  return app.models.ReplicationPolicy.objects.filter(sciobj=sciobj_model
                                                     ).exists()


def _delete_existing_replication_policy(sciobj_model):
  app.models.ReplicationPolicy.objects.filter(sciobj=sciobj_model).delete()


def _has_replication_policy_pyxb(sysmeta_pyxb):
  return hasattr(
    sysmeta_pyxb, 'replicationPolicy'
  ) and sysmeta_pyxb.replicationPolicy is not None


def _replication_policy_model_to_pyxb(sciobj_model):
  replication_policy_model = app.models.ReplicationPolicy.objects.get(
    sciobj=sciobj_model
  )
  replication_policy_pyxb = d1_common.types.dataoneTypes.ReplicationPolicy()
  replication_policy_pyxb.replicationAllowed = replication_policy_model.replication_is_allowed
  replication_policy_pyxb.numberReplicas = replication_policy_model.desired_number_of_replicas

  def add(rep_pyxb, rep_node_model):
    for rep_node in rep_node_model.objects.filter(
        replication_policy=replication_policy_model
    ):
      rep_pyxb.append(rep_node.node.urn)

  add(
    replication_policy_pyxb.preferredMemberNode, app.models.PreferredMemberNode
  )
  add(replication_policy_pyxb.blockedMemberNode, app.models.BlockedMemberNode)

  return replication_policy_pyxb


def _update_modified_timestamp(sci_model):
  sci_model.modified_timestamp = datetime.datetime.utcnow()
  sci_model.save()
