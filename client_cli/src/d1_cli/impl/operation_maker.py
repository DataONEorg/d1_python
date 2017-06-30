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

from __future__ import absolute_import

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
      u'operation': 'create',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier':
          pid,
        u'science-file':
          path,
        u'mn-url':
          self._session.get(session.MN_URL_NAME),
        u'algorithm':
          self._session.get(session.CHECKSUM_NAME),
        u'authoritative-mn':
          self._session.get(session.AUTH_MN_NAME),
        u'format-id':
          format_id
          if format_id is not None else self._session.get(session.FORMAT_NAME),
        u'rights-holder':
          self._session.get(session.OWNER_NAME),
        u'allow':
          self._session.get_access_control().get_list(),
        u'replication': {
          u'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          u'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          u'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          u'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update(self, pid, path, pid_new, format_id=None):
    operation = {
      u'operation': 'update',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier-new':
          pid_new,
        u'identifier-old':
          pid,
        u'science-file':
          path,
        u'mn-url':
          self._session.get(session.MN_URL_NAME),
        u'algorithm':
          self._session.get(session.CHECKSUM_NAME),
        u'authoritative-mn':
          self._session.get(session.AUTH_MN_NAME),
        u'format-id':
          format_id
          if format_id is not None else self._session.get(session.FORMAT_NAME),
        u'rights-holder':
          self._session.get(session.OWNER_NAME),
        u'allow':
          self._session.get_access_control().get_list(),
        u'replication': {
          u'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          u'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          u'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          u'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def create_package(self, pids):
    operation = {
      u'operation': 'create_package',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier-package': pids[0],
        u'identifier-science-meta': pids[1],
        u'identifier-science-data': pids[2:],
        u'mn-url': self._session.get(session.MN_URL_NAME),
        u'algorithm': self._session.get(session.CHECKSUM_NAME),
        u'authoritative-mn': self._session.get(session.AUTH_MN_NAME),
        u'rights-holder': self._session.get(session.OWNER_NAME),
        u'allow': self._session.get_access_control().get_list(),
        u'replication': {
          u'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          u'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          u'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          u'number-of-replicas':
            self._session.get_replication_policy().get_number_of_replicas(),
        },
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def archive(self, pid):
    operation = {
      u'operation': 'archive',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier': pid,
        u'mn-url': self._session.get(session.MN_URL_NAME),
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update_access_policy(self, pid):
    operation = {
      u'operation': 'update_access_policy',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier': pid,
        u'cn-url': self._session.get(session.CN_URL_NAME),
        u'allow': self._session.get_access_control().get_list(),
      }
    }
    self._operation_validator.assert_valid(operation)
    return operation

  def update_replication_policy(self, pid):
    operation = {
      u'operation': 'update_replication_policy',
      u'authentication': {
        u'anonymous': self._session.get(session.ANONYMOUS_NAME),
        u'cert-file': self._get_certificate(),
        u'key-file': self._get_certificate_key(),
      },
      u'parameters': {
        u'identifier': pid,
        u'cn-url': self._session.get(session.CN_URL_NAME),
        u'replication': {
          u'replication-allowed':
            self._session.get_replication_policy().get_replication_allowed(),
          u'preferred-nodes':
            self._session.get_replication_policy().get_preferred(),
          u'blocked-nodes':
            self._session.get_replication_policy().get_blocked(),
          u'number-of-replicas':
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
    return u'/tmp/x509up_u{}'.format(os.getuid())

  def _get_certificate_key(self):
    if not self._session.get(session.ANONYMOUS_NAME):
      return self._session.get(session.KEY_FILENAME_NAME)
    else:
      return None
