#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
:mod:`detail_codes`
=========================

:Synopsis:
  Get Detail Code for DataONE exception based on REST call path.

.. moduleauthor:: Roger Dahl
'''

import re


class dataone_exception_to_detail_code():
  def __init__(self):
    self.detail_codes_mapping = [
      (r'', 'CN_authentication', 'login', 'ServiceFailure', 500, 1620),
      (r'', 'CN_authentication', 'login', 'InvalidCredentials', 401, 1640),
      (r'', 'CN_authentication', 'login', 'AuthenticationTimeout', 408, 1680),
      (r'', 'CN_authentication', 'login', 'NotImplemented', 501, 1600),
      (r'', 'CN_authentication', 'login', 'InvalidRequest', 400, 1601),
      (r'', 'CN_authentication', 'setOwner', 'ServiceFailure', 500, 4490),
      (r'', 'CN_authentication', 'setOwner', 'InvalidToken', 401, 4480),
      (r'', 'CN_authentication', 'setOwner', 'NotAuthorized', 401, 4440),
      (r'', 'CN_authentication', 'setOwner', 'NotFound', 404, 4460),
      (r'', 'CN_authentication', 'setOwner', 'NotImplemented', 501, 4441),
      (r'', 'CN_authentication', 'setOwner', 'InvalidRequest', 400, 4442),
      (r'', 'CN_authentication', 'newAccount', 'ServiceFailure', 500, 4530),
      (r'', 'CN_authentication', 'newAccount', 'IdentifierNotUnique', 409, 4500),
      (r'', 'CN_authentication', 'newAccount', 'InvalidCredentials', 401, 4520),
      (r'', 'CN_authentication', 'newAccount', 'NotImplemented', 501, 4501),
      (r'', 'CN_authentication', 'newAccount', 'InvalidRequest', 400, 4502),
      (r'', 'CN_authentication', 'verifyToken', 'ServiceFailure', 500, 4550),
      (r'', 'CN_authentication', 'verifyToken', 'NotAuthorized', 401, 4540),
      (r'', 'CN_authentication', 'verifyToken', 'NotImplemented', 501, 4541),
      (r'', 'CN_authentication', 'verifyToken', 'InvalidToken', 401, 4555),
      (r'', 'CN_authentication', 'verifyToken', 'InvalidRequest', 400, 4542),
      (r'', 'CN_authorization', 'isAuthorized', 'ServiceFailure', 500, 1760),
      (r'', 'CN_authorization', 'isAuthorized', 'InvalidToken', 401, 1840),
      (r'', 'CN_authorization', 'isAuthorized', 'NotFound', 404, 1800),
      (r'', 'CN_authorization', 'isAuthorized', 'NotAuthorized', 401, 1820),
      (r'', 'CN_authorization', 'isAuthorized', 'NotImplemented', 501, 1780),
      (r'', 'CN_authorization', 'isAuthorized', 'InvalidRequest', 400, 1761),
      (r'', 'CN_authorization', 'setAccess', 'InvalidToken', 401, 4410),
      (r'', 'CN_authorization', 'setAccess', 'ServiceFailure', 500, 4430),
      (r'', 'CN_authorization', 'setAccess', 'NotFound', 404, 4400),
      (r'', 'CN_authorization', 'setAccess', 'NotAuthorized', 401, 4420),
      (r'', 'CN_authorization', 'setAccess', 'NotImplemented', 501, 4401),
      (r'', 'CN_authorization', 'setAccess', 'InvalidRequest', 400, 4402),
      (r'', 'CN_crud', 'get', 'NotAuthorized', 401, 1000),
      (r'', 'CN_crud', 'get', 'NotImplemented', 501, 1001),
      (r'', 'CN_crud', 'get', 'NotFound', 404, 1020),
      (r'', 'CN_crud', 'get', 'ServiceFailure', 500, 1030),
      (r'', 'CN_crud', 'get', 'InvalidToken', 401, 1010),
      (r'', 'CN_crud', 'get', 'InvalidRequest', 400, 1002),
      (r'', 'CN_crud', 'getSystemMetadata', 'InvalidToken', 401, 1050),
      (r'', 'CN_crud', 'getSystemMetadata', 'NotImplemented', 501, 1041),
      (r'', 'CN_crud', 'getSystemMetadata', 'ServiceFailure', 500, 1090),
      (r'', 'CN_crud', 'getSystemMetadata', 'NotAuthorized', 401, 1040),
      (r'', 'CN_crud', 'getSystemMetadata', 'NotFound', 404, 1060),
      (r'', 'CN_crud', 'getSystemMetadata', 'InvalidRequest', 400, 1080),
      (r'', 'CN_crud', 'resolve', 'InvalidToken', 401, 4130),
      (r'', 'CN_crud', 'resolve', 'ServiceFailure', 500, 4150),
      (r'', 'CN_crud', 'resolve', 'NotAuthorized', 401, 4120),
      (r'', 'CN_crud', 'resolve', 'NotFound', 404, 4140),
      (r'', 'CN_crud', 'resolve', 'NotImplemented', 501, 4131),
      (r'', 'CN_crud', 'resolve', 'InvalidRequest', 400, 4132),
      (r'', 'CN_crud', 'create', 'ServiceFailure', 500, 4115),
      (r'', 'CN_crud', 'create', 'UnsupportedMetadataType', 400, 4100),
      (r'', 'CN_crud', 'create', 'IdentifierNotUnique', 409, 4110),
      (r'', 'CN_crud', 'create', 'NotImplemented', 501, 4101),
      (r'', 'CN_crud', 'create', 'InvalidRequest', 400, 4102),
      (r'', 'CN_crud', 'reserveIdentifier', 'InvalidToken', 401, 4190),
      (r'', 'CN_crud', 'reserveIdentifier', 'ServiceFailure', 500, 4210),
      (r'', 'CN_crud', 'reserveIdentifier', 'NotAuthorized', 401, 4180),
      (r'', 'CN_crud', 'reserveIdentifier', 'InvalidRequest', 400, 4200),
      (r'', 'CN_crud', 'reserveIdentifier', 'IdentifierNotUnique', 409, 4210),
      (r'', 'CN_crud', 'reserveIdentifier', 'NotImplemented', 501, 4191),
      (r'', 'CN_crud', 'assertRelation', 'InvalidToken', 401, 4230),
      (r'', 'CN_crud', 'assertRelation', 'ServiceFailure', 500, 4270),
      (r'', 'CN_crud', 'assertRelation', 'NotAuthorized', 401, 4220),
      (r'', 'CN_crud', 'assertRelation', 'NotFound', 404, 4240),
      (r'', 'CN_crud', 'assertRelation', 'InvalidRequest', 400, 4260),
      (r'', 'CN_crud', 'assertRelation', 'NotImplemented', 501, 4221),
      (r'', 'CN_crud', 'log', 'InvalidRequest', 400, 1500),
      (r'', 'CN_crud', 'log', 'ServiceFailure', 500, 1510),
      (r'', 'CN_crud', 'log', 'NotImplemented', 501, 1501),
      (r'', 'CN_crud', 'getChecksum', 'NotImplemented', 501, 1402),
      (r'', 'CN_crud', 'getChecksum', 'ServiceFailure', 500, 1410),
      (r'', 'CN_crud', 'getChecksum', 'NotFound', 404, 1420),
      (r'', 'CN_crud', 'getChecksum', 'NotAuthorized', 401, 1400),
      (r'', 'CN_crud', 'getChecksum', 'InvalidRequest', 400, 1402),
      (r'', 'CN_crud', 'getChecksum', 'InvalidToken', 401, 1430),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'ServiceFailure', 500, 4700),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'NotImplemented', 501, 4701),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'InvalidToken', 401, 4710),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'NotAuthorized', 401, 4720),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'InvalidRequest', 400, 4730),
      (r'', 'CN_data_replication', 'setReplicationStatus', 'NotFound', 404, 4740),
      (r'', 'CN_query', 'search', 'InvalidToken', 401, 4290),
      (r'', 'CN_query', 'search', 'ServiceFailure', 500, 4310),
      (r'', 'CN_query', 'search', 'NotAuthorized', 401, 4280),
      (r'', 'CN_query', 'search', 'InvalidRequest', 400, 4300),
      (r'', 'CN_query', 'search', 'NotImplemented', 501, 4281),
      (r'', 'CN_query', 'getLogRecords', 'InvalidToken', 401, 1470),
      (r'', 'CN_query', 'getLogRecords', 'ServiceFailure', 500, 1490),
      (r'', 'CN_query', 'getLogRecords', 'NotAuthorized', 401, 1460),
      (r'', 'CN_query', 'getLogRecords', 'NotImplemented', 501, 1461),
      (r'', 'CN_query', 'getLogRecords', 'InvalidRequest', 400, 1480),
      (r'', 'CN_register', 'listNodes', 'NotImplemented', 501, 4800),
      (r'', 'CN_register', 'listNodes', 'ServiceFailure', 500, 4801),
      (r'', 'CN_register', 'addNodeCapabilities', 'NotImplemented', 501, 4820),
      (r'', 'CN_register', 'addNodeCapabilities', 'NotAuthorized', 401, 4821),
      (r'', 'CN_register', 'addNodeCapabilities', 'ServiceFailure', 500, 4822),
      (r'', 'CN_register', 'addNodeCapabilities', 'InvalidRequest', 400, 4823),
      (r'', 'CN_register', 'register', 'NotImplemented', 501, 4840),
      (r'', 'CN_register', 'register', 'NotAuthorized', 401, 4841),
      (r'', 'CN_register', 'register', 'ServiceFailure', 500, 4842),
      (r'', 'CN_register', 'register', 'InvalidRequest', 400, 4843),
      (r'', 'MN_authentication', 'login', 'NotImplemented', 501, 1600),
      (r'', 'MN_authentication', 'login', 'ServiceFailure', 500, 1620),
      (r'', 'MN_authentication', 'login', 'InvalidCredentials', 401, 1640),
      (r'', 'MN_authentication', 'login', 'AuthenticationTimeout', 408, 1680),
      (r'', 'MN_authentication', 'login', 'InvalidRequest', 400, 1601),
      (r'', 'MN_authentication', 'logout', 'ServiceFailure', 500, 1700),
      (r'', 'MN_authentication', 'logout', 'NotImplemented', 501, 1720),
      (r'', 'MN_authentication', 'logout', 'InvalidToken', 401, 1740),
      (r'', 'MN_authentication', 'logout', 'InvalidRequest', 400, 1701),
      (r'', 'MN_authorization', 'isAuthorized', 'ServiceFailure', 500, 1760),
      (r'', 'MN_authorization', 'isAuthorized', 'NotImplemented', 501, 1780),
      (r'', 'MN_authorization', 'isAuthorized', 'NotFound', 404, 1800),
      (r'', 'MN_authorization', 'isAuthorized', 'NotAuthorized', 401, 1820),
      (r'', 'MN_authorization', 'isAuthorized', 'InvalidToken', 401, 1840),
      (r'', 'MN_authorization', 'isAuthorized', 'InvalidRequest', 400, 1761),
      (r'/object/', 'MN_crud', 'get', 'NotAuthorized', 401, 1000),
      (r'/object/', 'MN_crud', 'get', 'NotFound', 404, 1020),
      (r'/object/', 'MN_crud', 'get', 'ServiceFailure', 500, 1030),
      (r'/object/', 'MN_crud', 'get', 'InvalidToken', 401, 1010),
      (r'/object/', 'MN_crud', 'get', 'NotImplemented', 501, 1001),
      (r'/object/', 'MN_crud', 'get', 'InvalidRequest', 400, 1002),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'NotAuthorized', 401, 1040),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'NotImplemented', 501, 1041),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'NotFound', 404, 1060),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'InvalidRequest', 400, 1080),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'ServiceFailure', 500, 1090),
      (r'/meta/', 'MN_crud', 'getSystemMetadata', 'InvalidToken', 401, 1050),
      (r'', 'MN_crud', 'create', 'NotAuthorized', 401, 1100),
      (r'', 'MN_crud', 'create', 'IdentifierNotUnique', 409, 1120),
      (r'', 'MN_crud', 'create', 'UnsupportedType', 400, 1140),
      (r'', 'MN_crud', 'create', 'InsufficientResources', 413, 1160),
      (r'', 'MN_crud', 'create', 'InvalidSystemMetadata', 400, 1180),
      (r'', 'MN_crud', 'create', 'ServiceFailure', 500, 1190),
      (r'', 'MN_crud', 'create', 'InvalidToken', 401, 1110),
      (r'', 'MN_crud', 'create', 'NotImplemented', 501, 1101),
      (r'', 'MN_crud', 'create', 'InvalidRequest', 400, 1102),
      (r'', 'MN_crud', 'update', 'NotAuthorized', 401, 1200),
      (r'', 'MN_crud', 'update', 'IdentifierNotUnique', 409, 1220),
      (r'', 'MN_crud', 'update', 'UnsupportedType', 400, 1240),
      (r'', 'MN_crud', 'update', 'InsufficientResources', 413, 1260),
      (r'', 'MN_crud', 'update', 'NotFound', 404, 1280),
      (r'', 'MN_crud', 'update', 'InvalidSystemMetadata', 400, 1300),
      (r'', 'MN_crud', 'update', 'ServiceFailure', 500, 1310),
      (r'', 'MN_crud', 'update', 'InvalidToken', 401, 1210),
      (r'', 'MN_crud', 'update', 'NotImplemented', 501, 1201),
      (r'', 'MN_crud', 'update', 'InvalidRequest', 400, 1202),
      (r'', 'MN_crud', 'delete', 'NotAuthorized', 401, 1320),
      (r'', 'MN_crud', 'delete', 'NotFound', 404, 1340),
      (r'', 'MN_crud', 'delete', 'ServiceFailure', 500, 1350),
      (r'', 'MN_crud', 'delete', 'InvalidToken', 401, 1330),
      (r'', 'MN_crud', 'delete', 'NotImplemented', 501, 1321),
      (r'', 'MN_crud', 'delete', 'InvalidRequest', 400, 1322),
      (r'', 'MN_crud', 'describe', 'NotAuthorized', 401, 1360),
      (r'', 'MN_crud', 'describe', 'NotFound', 404, 1380),
      (r'', 'MN_crud', 'describe', 'ServiceFailure', 500, 1390),
      (r'', 'MN_crud', 'describe', 'InvalidToken', 401, 1370),
      (r'', 'MN_crud', 'describe', 'NotImplemented', 501, 1361),
      (r'', 'MN_crud', 'describe', 'InvalidRequest', 400, 1362),
      (r'', 'MN_crud', 'getChecksum', 'NotAuthorized', 401, 1400),
      (r'', 'MN_crud', 'getChecksum', 'NotFound', 404, 1420),
      (r'', 'MN_crud', 'getChecksum', 'InvalidRequest', 400, 1402),
      (r'', 'MN_crud', 'getChecksum', 'ServiceFailure', 500, 1410),
      (r'', 'MN_crud', 'getChecksum', 'InvalidToken', 401, 1430),
      (r'', 'MN_crud', 'getChecksum', 'NotImplemented', 501, 1401),
      (r'/log$', 'MN_crud', 'getLogRecords', 'NotAuthorized', 401, 1460),
      (r'/log$', 'MN_crud', 'getLogRecords', 'InvalidRequest', 400, 1480),
      (r'/log$', 'MN_crud', 'getLogRecords', 'ServiceFailure', 500, 1490),
      (r'/log$', 'MN_crud', 'getLogRecords', 'InvalidToken', 401, 1470),
      (r'/log$', 'MN_crud', 'getLogRecords', 'NotImplemented', 501, 1461),
      (r'/log/', 'MN_crud', 'log', 'InvalidRequest', 400, 1500),
      (r'/log/', 'MN_crud', 'log', 'ServiceFailure', 500, 1510),
      (r'/log/', 'MN_crud', 'log', 'NotImplemented', 501, 1501),
      (r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'NotImplemented', 501, 0),
      (r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'ServiceFailure', 500, 0),
      (r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'NotAuthorized', 401, 0),
      (r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'InvalidRequest', 400, 0),
      (
        r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'InsufficientResources',
        413, 0
      ),
      (r'/monitor/object$', 'MN_health', 'getObjectStatistics', 'UnsupportedType', 400,
       0),
      (
        r'/monitor/event$', 'MN_health', 'getOperationStatistics', 'NotImplemented', 501,
        0
      ),
      (
        r'/monitor/event$', 'MN_health', 'getOperationStatistics', 'ServiceFailure', 500,
        0
      ),
      (r'/monitor/event$', 'MN_health', 'getOperationStatistics', 'NotAuthorized', 401,
       0),
      (
        r'/monitor/event$', 'MN_health', 'getOperationStatistics', 'InvalidRequest', 400,
        0
      ),
      (
        r'/monitor/event$', 'MN_health', 'getOperationStatistics',
        'InsufficientResources', 413, 0
      ),
      (
        r'/monitor/event$', 'MN_health', 'getOperationStatistics', 'UnsupportedType', 400,
        0
      ),
      (r'/object$', 'MN_replication', 'listObjects', 'NotAuthorized', 401, 1520),
      (r'/object$', 'MN_replication', 'listObjects', 'InvalidRequest', 400, 1540),
      (r'/object$', 'MN_replication', 'listObjects', 'NotImplemented', 501, 1560),
      (r'/object$', 'MN_replication', 'listObjects', 'ServiceFailure', 500, 1580),
      (r'/object$', 'MN_replication', 'listObjects', 'InvalidToken', 401, 1530),
      (r'/object$', 'MN_replication', 'listObjects', 'NotImplemented', 501, 1521),
      (r'', 'MN_replication', 'replicate', 'NotImplemented', 501, 2000),
      (r'', 'MN_replication', 'replicate', 'ServiceFailure', 500, 2001),
      (r'', 'MN_replication', 'replicate', 'NotAuthorized', 401, 2010),
      (r'', 'MN_replication', 'replicate', 'InvalidRequest', 400, 2020),
      (r'', 'MN_replication', 'replicate', 'InsufficientResources', 413, 2030),
      (r'', 'MN_replication', 'replicate', 'UnsupportedType', 400, 2040),
    ]

  def detail_code(self, request, exception):
    for path_rx, module, method, exception_name, error_code, detail_code in self.detail_codes_mapping:
      if path_rx == '':
        continue
      if exception.name == exception_name and re.search(path_rx, request.path):
        return detail_code
    return 0
