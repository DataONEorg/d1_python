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
"""Create System Metadata documents based on session variables.
"""
import os

import d1_cli.impl.cli_util as cli_util

import d1_common.checksum
import d1_common.const
import d1_common.date_time
import d1_common.types.dataoneTypes as dataoneTypes

# 3rd party

RESOURCE_MAP_FORMAT_ID = 'http://www.openarchives.org/ore/terms'


class SystemMetadataCreator():
  def __init__(self):
    pass

  def create_system_metadata(self, operation):
    #import pyxb
    #pyxb.RequireValidWhenGenerating(False)
    cli_util.assert_file_exists(operation['parameters']['science-file'])
    pid = operation['parameters']['identifier']
    format_id = operation['parameters']['format-id']
    file_size = self._get_file_size(operation['parameters']['science-file'])
    checksum = dataoneTypes.checksum(
      self._get_file_checksum(operation['parameters']['science-file'])
    )
    return self._create_pyxb_object(
      operation, pid, format_id, file_size, checksum
    )

  def create_system_metadata_for_update(self, operation):
    #import pyxb
    #pyxb.RequireValidWhenGenerating(False)
    cli_util.assert_file_exists(operation['parameters']['science-file'])
    pid_new = operation['parameters']['identifier-new']
    format_id = operation['parameters']['format-id']
    file_size = self._get_file_size(operation['parameters']['science-file'])
    checksum = dataoneTypes.checksum(
      self._get_file_checksum(operation['parameters']['science-file'])
    )
    sys_meta = self._create_pyxb_object(
      operation, pid_new, format_id, file_size, checksum
    )
    sys_meta.obsoletes = operation['parameters']['identifier-old']
    return sys_meta

  def create_system_metadata_for_package(
      self, resource_map, create_package_operation
  ):
    pid = create_package_operation['parameters']['identifier-package']
    file_size = len(resource_map)
    checksum = self._get_string_checksum(resource_map)
    return self._create_pyxb_object(
      create_package_operation, pid, RESOURCE_MAP_FORMAT_ID, file_size, checksum
    )

  def create_access_policy(self, operation):
    return self._create_access_policy_pyxb_object(operation)

  def create_replication_policy(self, operation):
    return self._create_replication_policy_pyxb_object(operation)

  #
  # Private.
  #

  def _create_pyxb_object(self, operation, pid, format_id, file_size, checksum):
    now = d1_common.date_time.utc_now()
    sys_meta = dataoneTypes.systemMetadata()
    sys_meta.serialVersion = 1
    sys_meta.identifier = pid
    sys_meta.formatId = format_id
    sys_meta.size = file_size
    sys_meta.rightsHolder = operation['parameters']['rights-holder']
    sys_meta.checksum = checksum
    sys_meta.checksum.algorithm = operation['parameters']['algorithm']
    sys_meta.dateUploaded = now
    sys_meta.dateSysMetadataModified = now
    sys_meta.authoritativemn = operation['parameters']['authoritative-mn']
    sys_meta.accessPolicy = self._create_access_policy_pyxb_object(operation)
    sys_meta.replicationPolicy = self._create_replication_policy_pyxb_object(
      operation
    )
    #pyxb.RequireValidWhenGenerating(False)
    return sys_meta

  def _create_access_policy_pyxb_object(self, operation):
    acl = operation['parameters']['allow']
    if not len(acl):
      return None
    access_policy = dataoneTypes.accessPolicy()
    for s, p in acl:
      access_rule = dataoneTypes.AccessRule()
      access_rule.subject.append(s)
      permission = dataoneTypes.Permission(p)
      access_rule.permission.append(permission)
      access_policy.append(access_rule)
    return access_policy

  def _create_replication_policy_pyxb_object(self, operation):
    r = operation['parameters']['replication']
    access_policy = dataoneTypes.ReplicationPolicy()
    for preferred in r['preferred-nodes']:
      node_reference = dataoneTypes.NodeReference(preferred)
      access_policy.preferredMemberNode.append(node_reference)
    for blocked in r['blocked-nodes']:
      node_reference = dataoneTypes.NodeReference(blocked)
      access_policy.blockedMemberNode.append(node_reference)
    access_policy.replicationAllowed = r['replication-allowed']
    access_policy.numberReplicas = r['number-of-replicas']
    return access_policy

  def _get_file_size(self, path):
    return os.path.getsize(os.path.expanduser(path))

  def _get_file_checksum(self, path, algorithm='SHA-1', block_size=1024 * 1024):
    with open(os.path.expanduser(path), 'rb') as f:
      return d1_common.checksum.calculate_checksum_on_stream(
        f, algorithm, block_size
      )

  def _get_string_checksum(self, string, algorithm='SHA-1', block_size=None):
    return d1_common.checksum.calculate_checksum_on_string(string, algorithm)

  #def _create_system_metadata(self, pid, path, format_id=None):
  #  checksum = self._get_file_checksum(
  #    cli_util.os.path.expanduser(path), self.session.get(CHECKSUM_NAME)
  #  )
  #  size = cli_util.get_file_size(cli_util.os.path.expanduser(path))
  #  sys_meta = self.session.create_system_metadata(pid, checksum, size, format_id)
  #  return sys_meta

  #def _create_system_metadata_xml(self, pid, path):
  #  sys_meta = self._create_system_metadata(pid, cli_util.os.path.expanduser(path))
  #  return sys_meta.toxml('utf-8')

  #sys_meta_creator = system_metadata.system_metadata()
  #access_policy = self.access_control.to_pyxb()
  #replication_policy = self.replication_policy.to_pyxb()
  ##self._create_missing_sys_meta_session_parameters()
  #return sys_meta_creator.create_pyxb_object(self, pid, size, checksum,
  #  access_policy, replication_policy, formatId)

  #
  #def _create_access_policy(self, operation):
  #  pass
  #
  #
  #def _create_replication_policy(self, operation):
  #  pass
  #

  #def _create_missing_sys_meta_session_parameters(self):
  #  """ Make sure all the session values that are:
  #        necessary to create the sys_meta data
  #        can be determined from other values
  #      are there.
  #      * authoritative-mn, rights-holder
  #  """
  #  save_data = False
  #  if self.get(AUTH_MN_NAME) is None:
  #    mn = self.get(MN_URL_NAME)
  #    mn_host = self._get_host_from_url(mn)
  #    if mn_host is not None:
  #      self.set(AUTH_MN_NAME, mn_host)
  #      cli_util.print_info(u'Setting %s to "%s"' % (AUTH_MN_NAME, mn_host))
  #      save_data = True;

  #def _get_host_from_url(self, url):
  #  if url is not None:
  #    url_dict = urlparse.urlparse(url)
  #    if url_dict.netloc is not None:
  #      host = url_dict.netloc
  #      ndx = host.find(":")
  #      if ndx > 0:
  #        host = host[:ndx]
  #      return host
  #  return None

  #def assert_required_parameters_present(self, names):
  #  missing_parameters = []
  #  for name in names:
  #    value = self.get_with_implicit_section(name)
  #    if value is None:
  #      missing_parameters.append(name)
  #  if len(missing_parameters):
  #    msg_missing = u'Missing session variables: {0}'.format(
  #      u', '.join(missing_parameters))
  #    raise cli_exceptions.InvalidArguments(msg_missing)

  #def create_pyxb_object(self, session, pid, size, checksum, access_policy,
  #                       replication_policy, formatId=None, algorithm=None):
  #  #TODO: Instead of checking for missing parameters here, probably want to
  #  #check after the user has edited the queue and where the command is created.
  #  #self._assert_no_missing_sys_meta_session_parameters(
  #  #  session.session[u'sys-meta'], formatId, algorithm)
  #  return self._create_pyxb_object(session, pid, size, checksum, access_policy,
  #                                  replication_policy, formatId, algorithm)
  #
  #
  #def to_xml(self):
  #  return self.to_pyxb().toxml('utf-8')
  #
  ##
  ## Private.
  ##
  #
  #def _create_pyxb_object(self, session, pid, size, checksum, access_policy,
  #                        replication_policy, formatId, algorithm):
  #  # Fix arguments.
  #  _formatId = formatId
  #  if _formatId is None:
  #    _formatId = session.get(FORMAT_NAME)
  #  _algorithm = algorithm
  #  if _algorithm is None:
  #    _algorithm = session.get(CHECKSUM_NAME)
  #
  #  sys_meta = dataoneTypes.systemMetadata()
  #  sys_meta.serialVersion = 1
  #  sys_meta.identifier = pid
  #  sys_meta.formatId = _formatId
  #  sys_meta.size = size
  #  sys_meta.rightsHolder = session.get(OWNER_NAME)
  #  sys_meta.checksum = dataoneTypes.checksum(checksum)
  #  sys_meta.checksum.algorithm = _algorithm
  #  sys_meta.dateUploaded = d1_common.date_time.utc_now()
  #  sys_meta.dateSysMetadataModified = d1_common.date_time.utc_now()
  #  sys_meta.authoritativemn = session.get(AUTH_MN_NAME)
  #  sys_meta.accessPolicy = access_policy
  #  sys_meta.replicationPolicy = replication_policy
  #  #pyxb.RequireValidWhenGenerating(False)
  #  #print sys_meta.toxml('utf-8')
  #  return sys_meta
  #
  #
  #def to_pyxb(self):
  #  access_policy = self._list_to_pyxb()
  #  if self.public:
  #    access_policy = self._add_public_subject(access_policy)
  #  return access_policy
  #
  #
  #def to_xml(self):
  #  return self.to_pyxb().toxml('utf-8')
  #

  #def from_xml(self, xml):
  #  access_policy = dataoneTypes.CreateFromDocument(xml)
  #  for access_rule in access_policy.allow:
  #    subject = access_rule.subject[0].value()
  #    permission = access_rule.permission[0]
  #    self._add_allowed_subject(subject, permission)
