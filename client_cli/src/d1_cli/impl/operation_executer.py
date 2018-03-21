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
"""Execute queued write operations.
"""

import io

import d1_cli.impl.cli_client as cli_client
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.operation_validator as operation_validator
import d1_cli.impl.system_metadata as system_metadata

import d1_common.resource_map


class OperationExecuter(object):
  def __init__(self):
    self._operation_validator = operation_validator.OperationValidator()

  def execute(self, operation):
    self._operation_validator.assert_valid(operation)
    if operation['operation'] == 'create':
      self._execute_create(operation)
    elif operation['operation'] == 'update':
      self._execute_update(operation)
    elif operation['operation'] == 'create_package':
      self._execute_create_package(operation)
    elif operation['operation'] == 'archive':
      self._execute_archive(operation)
    elif operation['operation'] == 'update_access_policy':
      self._execute_update_access_policy(operation)
    elif operation['operation'] == 'update_replication_policy':
      self._execute_update_replication_policy(operation)
    else:
      assert False, 'Invalid operation: {}'.format(operation['operation'])

  #
  # Private.
  #

  def _execute_create(self, operation):
    pid = operation['parameters']['identifier']
    path = operation['parameters']['science-file']
    sys_meta = self._create_system_metadata(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(operation)
    )
    with open(cli_util.os.path.expanduser(path), 'rb') as f:
      client.create(pid, f, sys_meta)

  def _execute_update(self, operation):
    pid_new = operation['parameters']['identifier-new']
    pid_old = operation['parameters']['identifier-old']
    path = operation['parameters']['science-file']
    sys_meta = self._create_system_metadata_for_update(operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(operation)
    )
    with open(cli_util.os.path.expanduser(path), 'rb') as f:
      client.update(pid_old, f, pid_new, sys_meta)

  def _execute_create_package(self, operation):
    pid_package = operation['parameters']['identifier-package']
    pid_sci_meta = operation['parameters']['identifier-science-meta']
    pid_sci_datas = operation['parameters']['identifier-science-data']
    resource_map = self._generate_resource_map(
      operation, pid_package, pid_sci_meta, pid_sci_datas
    )
    sys_meta = self._create_system_metadata_for_package(resource_map, operation)
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(operation)
    )
    client.create(pid_package, io.StringIO(resource_map), sys_meta)

  def _execute_archive(self, operation):
    pid = operation['parameters']['identifier']
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_operation(operation)
    )
    client.archive(pid)

  def _execute_update_access_policy(self, operation):
    pid = operation['parameters']['identifier']
    policy = self._create_access_policy(operation)
    client = cli_client.CLICNClient(
      **self._cn_client_connect_params_from_operation(operation)
    )
    sys_meta = client.getSystemMetadata(pid)
    client.setAccessPolicy(pid, policy, sys_meta.serialVersion)

  def _execute_update_replication_policy(self, operation):
    pid = operation['parameters']['identifier']
    policy = self._create_replication_policy(operation)
    client = cli_client.CLICNClient(
      **self._cn_client_connect_params_from_operation(operation)
    )
    sys_meta = client.getSystemMetadata(pid)
    client.setReplicationPolicy(
      pid, policy, serialVersion=sys_meta.serialVersion
    )

  def _mn_client_connect_params_from_operation(self, operation):
    return {
      'base_url': operation['parameters']['mn-url'],
      'cert_pem_path': operation['authentication']['cert-file'],
      'cert_key_path': operation['authentication']['key-file'],
    }

  def _cn_client_connect_params_from_operation(self, operation):
    return {
      'base_url': operation['parameters']['cn-url'],
      'cert_pem_path': operation['authentication']['cert-file'],
      'cert_key_path': operation['authentication']['key-file'],
    }

  def _create_system_metadata(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata(operation)

  def _create_system_metadata_for_update(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata_for_update(operation)

  def _generate_resource_map(
      self, operation, package_pid, pid_sci_meta, pid_sci_datas
  ):
    resource_map_generator = d1_common.resource_map.ResourceMapGenerator(
      dataone_root=operation['parameters']['mn-url']
    )
    return resource_map_generator.simple_generate_resource_map(
      package_pid, pid_sci_meta, pid_sci_datas
    )

  def _create_system_metadata_for_package(self, resource_map, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_system_metadata_for_package(resource_map, operation)

  def _create_access_policy(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_access_policy(operation)

  def _create_replication_policy(self, operation):
    c = system_metadata.SystemMetadataCreator()
    return c.create_replication_policy(operation)
