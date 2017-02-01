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
"""
:mod:`operation_validator`
==========================

:Synopsis: Sanity checking of the values which are required by a given operation.
:Created: 2013-07-16
:Author: DataONE (Dahl)
"""

# Stdlib
import types
import urlparse

# D1
import d1_common.checksum

# App
import cli_util
import cli_exceptions


class OperationValidator(object):
  def __init__(self):
    self._type_map = {
      types.IntType: 'number',
      types.BooleanType: 'true or false value',
      types.StringTypes: 'text string',
      types.ListType: 'list',
      types.DictType: 'dictionary'
    }

  def assert_valid(self, operation):
    #pprint.pprint(operation)
    self._assert_operation_has_valid_operation_type(operation)
    self._assert_valid_auth_parameter_combination(operation)
    if operation[u'operation'] == 'create':
      self.assert_valid_create(operation)
    elif operation[u'operation'] == 'update':
      self.assert_valid_update(operation)
    elif operation[u'operation'] == 'create_package':
      self.assert_valid_create_package(operation)
    elif operation[u'operation'] == 'archive':
      self.assert_valid_archive(operation)
    elif operation[u'operation'] == 'update_access_policy':
      self.assert_valid_update_access_policy(operation)
    elif operation[u'operation'] == 'update_replication_policy':
      self.assert_valid_update_replication_policy(operation)
    else:
      assert False, u'Invalid operation: {0}'.format(operation[u'operation'])

  def assert_valid_create(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier')
    self._assert_valid_path(operation, 'parameters', 'science-file')
    self._assert_valid_member_node_url(operation, 'parameters', 'mn-url')
    self._assert_valid_checksum_algorithm(operation)
    self._assert_valid_member_node_urn(operation, 'parameters', 'authoritative-mn')
    self._assert_valid_format_id(operation, 'parameters', 'format-id')
    self._assert_value_type(operation, types.StringTypes, 'parameters', 'rights-holder')
    self._assert_valid_access_control(operation)
    self._assert_valid_replication_policy(operation)

  def assert_valid_update(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier-new')
    self._assert_valid_identifier(operation, 'parameters', 'identifier-old')
    self._assert_valid_path(operation, 'parameters', 'science-file')
    self._assert_valid_member_node_url(operation, 'parameters', 'mn-url')
    self._assert_valid_checksum_algorithm(operation)
    self._assert_valid_member_node_urn(operation, 'parameters', 'authoritative-mn')
    self._assert_valid_format_id(operation, 'parameters', 'format-id')
    self._assert_value_type(operation, types.StringTypes, 'parameters', 'rights-holder')
    self._assert_valid_access_control(operation)
    self._assert_valid_replication_policy(operation)

  def assert_valid_create_package(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier-package')
    self._assert_valid_identifier(operation, 'parameters', 'identifier-science-meta')
    self._assert_valid_identifiers(operation, 'parameters', 'identifier-science-data')
    self._assert_valid_member_node_url(operation, 'parameters', 'mn-url')
    self._assert_valid_checksum_algorithm(operation)
    self._assert_valid_member_node_urn(operation, 'parameters', 'authoritative-mn')
    self._assert_value_type(operation, types.StringTypes, 'parameters', 'rights-holder')
    self._assert_valid_access_control(operation)
    self._assert_valid_replication_policy(operation)

  def assert_valid_archive(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier')
    self._assert_valid_member_node_url(operation, 'parameters', 'mn-url')

  def assert_valid_update_access_policy(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_authenticated_access(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier')
    self._assert_valid_coordinating_node_url(operation)
    self._assert_valid_access_control(operation)

  def assert_valid_update_replication_policy(self, operation):
    self._assert_valid_auth_parameter_combination(operation)
    self._assert_authenticated_access(operation)
    self._assert_valid_identifier(operation, 'parameters', 'identifier')
    self._assert_valid_coordinating_node_url(operation)
    self._assert_valid_replication_policy(operation)

  #
  # Private.
  #

  def _assert_value_type(self, operation, type_, *keys):
    self._assert_present(operation, *keys)
    if not self._is_value_type(operation, type_, *keys):
      raise cli_exceptions.InvalidArguments(
        'Operation parameter "{0}" must be a {1}'.format(keys[-1], self._type_map[type_])
      )

  def _is_value_type(self, operation, type_, *keys):
    for key in keys:
      if key not in operation:
        return False
      operation = operation[key]
    return isinstance(operation, type_)

  def _assert_present(self, operation, *keys):
    operation_type = operation['operation']
    for key in keys:
      if key not in operation:
        raise cli_exceptions.InvalidArguments(
          'Operation parameter "{0}" must be present for {1} operations'
          .format(key, operation_type)
        )
      if operation[key] is None:
        raise cli_exceptions.InvalidArguments(
          'Operation parameter "{0}" must be set for {1} operations'
          .format(key, operation_type)
        )
      operation = operation[key]

  def _assert_operation_has_valid_operation_type(self, operation):
    if 'operation' not in operation:
      raise cli_exceptions.InvalidArguments('Operation is missing the operation type')
    if operation['operation'] not in (
      'create', 'update', 'create_package', 'archive', 'update_access_policy',
      'update_replication_policy'
    ):
      raise cli_exceptions.InvalidArguments(
        'Operation is of invalid type: {0}'.format(operation['operation'])
      )

  def _assert_valid_identifier_value(self, pid):
    if pid.count(' ') or pid.count('\t'):
      raise cli_exceptions.InvalidArguments(
        'Identifier cannot contain space or tab characters: {0}'.format(pid)
      )
    if len(pid) > 800:
      raise cli_exceptions.InvalidArguments(
        'Identifier cannot be longer than 800 characters: {0}'.format(pid)
      )

  def _assert_valid_identifier(self, operation, *keys):
    self._assert_value_type(operation, types.StringTypes, *keys)
    for key in keys:
      operation = operation[key]
    self._assert_valid_identifier_value(operation)

  def _assert_valid_identifiers(self, operation, *keys):
    self._assert_value_type(operation, types.ListType, *keys)
    for key in keys:
      operation = operation[key]
    for pid in operation:
      self._assert_valid_identifier_value(pid)

  def _assert_valid_auth_parameter_combination(self, operation):
    self._assert_value_type(operation, types.BooleanType, 'authentication', 'anonymous')
    auth = operation['authentication']
    if not auth['anonymous']:
      if not self._is_value_type(
        operation, types.StringTypes, 'authentication', 'cert-file'
      ):
        raise cli_exceptions.InvalidArguments(
          'Specified an authenticated connection without providing a certificate'
        )
      cli_util.assert_file_exists(operation['authentication']['cert-file'])
    if self._is_value_type(operation, types.NoneType, 'authentication', 'cert-file') \
      and not self._is_value_type(operation, types.NoneType, 'authentication', 'key-file'):
      raise cli_exceptions.InvalidArguments(
        'Specified a certificate private key without specifying a certificate'
      )

  def _assert_authenticated_access(self, operation):
    self._assert_value_type(operation, types.BooleanType, 'authentication', 'anonymous')
    auth = operation['authentication']
    if auth['anonymous']:
      raise cli_exceptions.InvalidArguments(
        'This operation cannot be performed without authentication'
      )
    cli_util.assert_file_exists(operation['authentication']['cert-file'])

  def _assert_valid_checksum_algorithm(self, operation):
    self._assert_value_type(operation, types.StringTypes, 'parameters', 'algorithm')
    algorithm = operation['parameters']['algorithm']
    try:
      d1_common.checksum.get_checksum_calculator_by_dataone_designator(algorithm)
    except LookupError:
      raise cli_exceptions.InvalidArguments(
        'Invalid checksum algorithm: {0}'.format(algorithm)
      )

  def _assert_valid_path(self, operation, *keys):
    self._assert_value_type(operation, types.StringTypes, *keys)
    for key in keys:
      operation = operation[key]
    cli_util.assert_file_exists(operation)

  def _assert_valid_format_id(self, operation, *keys):
    self._assert_value_type(operation, types.StringTypes, *keys)
    #TODO: Validate against list from CN.

  def _assert_valid_member_node_url(self, operation, *keys):
    self._assert_valid_base_url(operation, *keys)
    #TODO: Validate against member node list from CN.

  def _assert_valid_member_node_urn(self, operation, *keys):
    self._assert_value_type(operation, types.StringTypes, *keys)
    for key in keys:
      operation = operation[key]
    if not operation.startswith('urn:node'):
      raise cli_exceptions.InvalidArguments(
        'Invalid Member Node ID. Must start with "urn:node". parameter={0}, value={1}'.format(
          key, operation
        )
      )

  def _assert_valid_coordinating_node_url(self, operation):
    self._assert_valid_base_url(operation, 'parameters', 'cn-url')
    #TODO: Validate against member node list from CN.

  def _assert_valid_base_url(self, operation, *keys):
    self._assert_value_type(operation, types.StringTypes, *keys)
    for key in keys:
      operation = operation[key]
    o = urlparse.urlparse(operation)
    if o.scheme not in ('http', 'https'):
      raise cli_exceptions.InvalidArguments(
        'Invalid BaseURL. Must use HTTP or HTTPS protocol. parameter={0}, value={1}'.format(
          key, operation
        )
      )

  def _assert_valid_access_control(self, operation):
    self._assert_value_type(operation, types.ListType, 'parameters', 'allow')
    for allow in operation['parameters']['allow']:
      if len(allow) != 2:
        raise cli_exceptions.InvalidArguments(
          'Access control rule must be subject and permission: {0}'
          .format(', '.join(allow))
        )
      if allow[1] not in ('read', 'write', 'changePermission'):
        raise cli_exceptions.InvalidArguments(
          'Access control permission must be read, write or changePermission: {0}'
          .format(allow[1])
        )

  def _assert_valid_replication_policy(self, operation):
    self._assert_value_type(operation, types.DictType, 'parameters', 'replication')
    self._assert_value_type(
      operation, types.BooleanType, 'parameters', 'replication', 'replication-allowed'
    )
    self._assert_value_type(
      operation, types.ListType, 'parameters', 'replication', 'preferred-nodes'
    )
    self._assert_value_type(
      operation, types.ListType, 'parameters', 'replication', 'blocked-nodes'
    )
    self._assert_value_type(
      operation, types.IntType, 'parameters', 'replication', 'number-of-replicas'
    )
