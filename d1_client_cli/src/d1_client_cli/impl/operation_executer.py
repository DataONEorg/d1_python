#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2013 DataONE
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
'''
:mod:`operation_executer`
=========================

:Synopsis: Execute queued write operations.
:Created: 2013-07-17
:Author: DataONE (Dahl)
'''

# Stdlib.
import StringIO

# D1.
import d1_common
import d1_client.data_package

# App.
import cli_client
import cli_util
import system_metadata
import operation_validator

# Example operation:
#
#[
#    {
#        "comment": "create(a, t)",
#        "arguments": {
#            "format-id": null,
#            "path": "t",
#            "pid": "a"
#        },
#        "authentication": {
#            "anonymous": true,
#            "cert-file": null,
#            "key-file": null
#        },
#        "operation": "create",
#        "parameters": {
#            "access-control": [],
#            "algorithm": "SHA-1",
#            "authoritative-mn": null,
#            "format-id": null,
#            "member-node": "https://localhost/mn/",
#            "origin-mn": null,
#            "replication": {
#                "blocked-nodes": [],
#                "number-of-replicas": 3,
#                "preferred-nodes": [],
#                "replication-allowed": true
#            },
#            "rights-holder": null,
#            "submitter": null
#        }
#    }
#]


class OperationExecuter(object):
  def __init__(self):
    self._operation_validator = operation_validator.OperationValidator()

  def execute(self, operation):
    self._operation_validator.assert_valid(operation)
    if operation[u'operation'] == 'create':
      self.execute_create(operation)
    elif operation[u'operation'] == 'update':
      self.execute_update(operation)
    elif operation[u'operation'] == 'create_package':
      self.execute_create_package(operation)
    elif operation[u'operation'] == 'archive':
      self.execute_archive(operation)
    elif operation[u'operation'] == 'update_access_policy':
      self.execute_update_access_policy(operation)
    elif operation[u'operation'] == 'update_replication_policy':
      self.execute_update_replication_policy(operation)
    else:
      assert False, u'Invalid operation: {0}'.format(operation[u'operation'])

  def execute_create(self, operation):
    pid = operation[u'parameters']['identifier']
    path = operation[u'parameters']['science-file']
    sys_meta = self._create_system_metadata(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    with open(cli_util.os.path.expanduser(path), u'r') as f:
      client.create(pid, f, sys_meta)

  def execute_update(self, operation):
    pid_new = operation[u'parameters']['identifier-new']
    pid_old = operation[u'parameters']['identifier-old']
    path = operation[u'parameters']['science-file']
    sys_meta = self._create_system_metadata_for_update(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    with open(cli_util.os.path.expanduser(path), u'r') as f:
      client.update(pid_old, f, pid_new, sys_meta)

  def execute_create_package(self, operation):
    pid_package = operation[u'parameters']['identifier-package']
    pid_sci_meta = operation[u'parameters']['identifier-science-meta']
    pid_sci_datas = operation[u'parameters']['identifier-science-data']
    resource_map = self._generate_resource_map(
      operation, pid_package, pid_sci_meta, pid_sci_datas
    )
    sys_meta = self._create_system_metadata_for_package(resource_map, operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    client.create(pid_package, StringIO.StringIO(resource_map), sys_meta)

  def execute_archive(self, operation):
    pid = operation[u'parameters']['identifier']
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    client.archive(pid)

  def execute_update_access_policy(self, operation):
    pid = operation[u'parameters']['identifier']
    sys_meta = self._create_system_metadata(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    client.setAccessPolicy(pid, access_policy, metadata.serialVersion)

  def execute_valid_update_replication_policy(self, operation):
    pid = operation[u'parameters']['identifier']
    sys_meta = self._create_system_metadata(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(
        operation
      )
    )
    client.setReplicationPolicy(
      pid, policy=replication_policy,
      serialVersion=metadata.serialVersion
    )

  #
  # Private.
  #

  def _mn_client_connect_params_from_operation(self, operation):
    return {
      'base_url': operation['parameters']['member-node'],
      'cert_path': operation['authentication']['cert-file'],
      'key_path': operation['authentication']['key-file'],
    }

  def _create_system_metadata(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata(operation)

  def _create_system_metadata_for_update(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata_for_update(operation)

  def _generate_resource_map(self, operation, package_pid, pid_sci_meta, pid_sci_datas):
    resource_map_generator = d1_client.data_package.ResourceMapGenerator(
      dataone_root=operation[u'parameters']['member-node']
    )
    return resource_map_generator.simple_generate_resource_map(
      package_pid, pid_sci_meta, pid_sci_datas
    )

  def _create_system_metadata_for_package(self, resource_map, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata_for_package(resource_map, operation)

#def create_get_url_for_pid(baseurl, pid, session=None):
#  return create_url_for_pid(baseurl, u'resolve', pid, session)
#
#
#def create_meta_url_for_pid(baseurl, pid, session=None):
#  return create_url_for_pid(baseurl, u'meta', pid, session)
#
#
#def create_url_for_pid(baseurl, action, pid, session=None):
#  '''  Create a URL for the specified pid.
#  '''
#  if baseurl:
#    endpoint = baseurl
#  elif session:
#    endpoint = session.get(MN_URL_SECT, MN_URL_NAME)
#  else:
#    raise cli_exceptions.InvalidArguments(u'You must specify either the base URL or the session')
#  if not pid:
#    raise cli_exceptions.InvalidArguments(u'You must specify the pid')
#  if not action:
#    raise cli_exceptions.InvalidArguments(u'You must specify the action')
#  encoded_pid = urllib.quote_plus(pid)
#  return u'%s/%s/%s/%s' % (endpoint, REST_Version, action, encoded_pid)
#
#
#def create_resolve_url_for_pid(baseurl, pid, session=None):
#  '''  Create a URL for the specified pid.
#  '''
#  if baseurl:
#    endpoint = baseurl
#  elif session:
#    endpoint = session.get(CN_URL_SECT, CN_URL_NAME)
#  else:
#    raise cli_exceptions.InvalidArguments(u'You must specify either the base URL or the session')
#  if not pid:
#    raise cli_exceptions.InvalidArguments(u'You must specify the pid')
#  encoded_pid = urllib.quote_plus(pid)
#  return u'%s/%s/resolve/%s' % (endpoint, REST_Version, encoded_pid)
#
#
#def get_object_by_pid(session, pid, filename=None, resolve=True):
#  ''' Create a mnclient and look for the object.  If the object is not found,
#      simply return a None, don't throw an exception.  If found, return the
#      filename.
#  '''
#  if session is None:
#    raise cli_exceptions.InvalidArguments(u'Missing session')
#  if pid is None:
#    raise cli_exceptions.InvalidArguments(u'Missing pid')
#  # Create member node client and try to get the object.
#  mn_client = CLIMNClient(session)
#  try:
#    response = mn_client.get(pid)
#    if response is not None:
#      fname = _get_fname(filename)
#      cli_util.output(response, fname, session.is_verbose())
#      return fname
#  except d1_common.types.exceptions.DataONEException as e:
#    if e.errorCode != 404:
#      raise cli_exceptions.CLIError(
#        u'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format()))
#  if resolve:
#    cn_client = CLICNClient(session)
#    object_location_list = None
#    try:
#      object_location_list = cn_client.resolve(pid)
#      if ((object_location_list is not None)
#          and (len(object_location_list.objectLocation) > 0)):
#        baseUrl = object_location_list.objectLocation[0].baseURL
#        # If there is an object, go get it.
#        mn_client = CLIMNClient(session, mn_url=baseUrl)
#        response = mn_client.get(pid)
#        if response is not None:
#          fname = _get_fname(filename)
#          cli_util.output(response, os.path.expanduser(fname))
#          return fname
#    except d1_common.types.exceptions.DataONEException as e:
#      if e.errorCode != 404:
#        raise cli_exceptions.CLIError(
#          u'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format()))
#  # Nope, didn't find anything
#  return None
#
#
#def _get_fname(filename):
#  ''' If fname is none, create a name.
#  '''
#  fname = filename
#  if fname is None:
#    tmp_flo = tempfile.mkstemp(prefix= u'd1obj-', suffix='.dat')
#    os.close(tmp_flo[0])
#    fname = tmp_flo[1]
#  return fname
#
#
#def get_baseUrl(session, nodeId):
#  '''  Get the base url of the given node id.
#  '''
#  cn_client = CLICNClient(session)
#  try:
#    nodes = cn_client.listNodes()
#    for node in list(nodes.node):
#      if node.identifier.value() == nodeId:
#        return node.baseURL
#  except (d1_common.types.exceptions.ServiceFailure) as e:
#    cli_util.print_error("Unable to get node list.")
#  return None
#
#
#def get_sys_meta_by_pid(session, pid, search_mn = False):
#  '''  Get the system metadata object for this particular pid.
#  '''
#  if not session:
#    raise cli_exceptions.InvalidArguments(u'Missing session')
#  if not pid:
#    raise cli_exceptions.InvalidArguments(u'Missing pid')
#
#  sys_meta = None
#  try:
#    cn_client = CLICNClient(session)
#    obsolete = True;
#    while obsolete:
#      obsolete = False;
#      sys_meta = cn_client.getSystemMetadata(pid)
#      if not sys_meta:
#        return None
#      if sys_meta.obsoletedBy:
#        msg = (u'Object "%s" has been obsoleted by "%s".  '
#            + u'Would you rather use that?') % (pid, sys_meta.obsoletedBy)
#        if not cli_util.confirm(msg):
#          break;
#        pid = sys_meta.obsoletedBy
#        obsolete = True
#    return sys_meta
#  except d1_common.types.exceptions.DataONEException as e:
#      if e.errorCode != 404:
#        raise cli_exceptions.CLIError(
#          u'Unable to get system metadata for: {0}\n{1}'.format(pid, e.friendly_format()))
#  # Search the member node?
#  if not sys_meta and (search_mn is not None) and search_mn:
#    try:
#      mn_client = CLIMNClient(session)
#      obsolete = True;
#      while obsolete:
#        obsolete = False;
#        sys_meta = mn_client.getSystemMetadata(pid)
#        if not sys_meta:
#          return None
#        if sys_meta.obsoletedBy:
#          msg = (u'Object "%s" has been obsoleted by "%s".  '
#              + u'Would you rather use that?') % (pid, sys_meta.obsoletedBy)
#          if not cli_util.confirm(msg):
#            break;
#          pid = sys_meta.obsoletedBy
#          obsolete = True
#      return sys_meta
#    except d1_common.types.exceptions.DataONEException as e:
#        if e.errorCode != 404:
#          raise cli_exceptions.CLIError(
#            u'Unable to get system metadata for: {0}\n{1}'.format(pid, e.friendly_format()))
#
#  return sys_meta
