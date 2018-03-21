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
"""Put together all the information required for executing a given operation.
"""

import os

import d1_cli.impl.operation_validator as operation_validator
import d1_cli.impl.session as session

# flake8: noqa: E122


class OperationMaker(object):
  def __init__(self, session):
    self._session = session
    self._operation_validator = operation_validator.OperationValidator()

  def create(self, pid, path, format_id=None):
    operation = {
      'operation': 'create',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier':
          pid,
        'science-file':
          path,
        'mn-url':
          self._session.get(session.MN_URL_NAME),
        'algorithm':
          self._session.get(session.CHECKSUM_NAME),
        'authoritative-mn':
          self._session.get(session.AUTH_MN_NAME),
        'format-id':
          format_id
          if format_id is not None else self._session.get(session.FORMAT_NAME),
        'rights-holder':
          self._session.get(session.OWNER_NAME),
        'allow':
          self._session.get_access_control().get_list(),
        'replication': {
          'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update(self, pid, path, pid_new, format_id=None):
    operation = {
      'operation': 'update',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier-new':
          pid_new,
        'identifier-old':
          pid,
        'science-file':
          path,
        'mn-url':
          self._session.get(session.MN_URL_NAME),
        'algorithm':
          self._session.get(session.CHECKSUM_NAME),
        'authoritative-mn':
          self._session.get(session.AUTH_MN_NAME),
        'format-id':
          format_id
          if format_id is not None else self._session.get(session.FORMAT_NAME),
        'rights-holder':
          self._session.get(session.OWNER_NAME),
        'allow':
          self._session.get_access_control().get_list(),
        'replication': {
          'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def create_package(self, pids):
    operation = {
      'operation': 'create_package',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier-package': pids[0],
        'identifier-science-meta': pids[1],
        'identifier-science-data': pids[2:],
        'mn-url': self._session.get(session.MN_URL_NAME),
        'algorithm': self._session.get(session.CHECKSUM_NAME),
        'authoritative-mn': self._session.get(session.AUTH_MN_NAME),
        'rights-holder': self._session.get(session.OWNER_NAME),
        'allow': self._session.get_access_control().get_list(),
        'replication': {
          'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def archive(self, pid):
    operation = {
      'operation': 'archive',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier': pid,
        'mn-url': self._session.get(session.MN_URL_NAME),
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update_access_policy(self, pid):
    operation = {
      'operation': 'update_access_policy',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier': pid,
        'cn-url': self._session.get(session.CN_URL_NAME),
        'allow': self._session.get_access_control().get_list(),
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update_replication_policy(self, pid):
    operation = {
      'operation': 'update_replication_policy',
      'authentication': {
        'anonymous': self._session.get(session.ANONYMOUS_NAME),
        'cert-file': self._get_certificate(),
        'key-file': self._get_certificate_key(),
      },
      'parameters': {
        'identifier': pid,
        'cn-url': self._session.get(session.CN_URL_NAME),
        'replication': {
          'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def _get_certificate(self):
    if not self._session.get(session.ANONYMOUS_NAME):
      cert_pem_path = self._session.get(session.CERT_FILENAME_NAME)
      if not cert_pem_path:
        cert_pem_path = self._get_cilogon_certificate_path()
      return cert_pem_path
    else:
      return None

  def _get_cilogon_certificate_path(self):
    return '/tmp/x509up_u{}'.format(os.getuid())

  def _get_certificate_key(self):
    if not self._session.get(session.ANONYMOUS_NAME):
      return self._session.get(session.KEY_FILENAME_NAME)
    else:
      return None
