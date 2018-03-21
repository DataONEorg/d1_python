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
"""Get Detail Code for DataONE exception based on REST call path
"""

import re


class DataoneExceptionToDetailCode(object):
  def __init__(self):
    self.detail_codes_dict = [
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
      (
        r'/object$', 'MN_replication', 'listObjects', 'NotAuthorized', 401, 1520
      ),
      (
        r'/object$', 'MN_replication', 'listObjects', 'InvalidRequest', 400,
        1540
      ),
      (
        r'/object$', 'MN_replication', 'listObjects', 'NotImplemented', 501,
        1560
      ),
      (
        r'/object$', 'MN_replication', 'listObjects', 'ServiceFailure', 500,
        1580
      ),
      (r'/object$', 'MN_replication', 'listObjects', 'InvalidToken', 401, 1530),
      (
        r'/object$', 'MN_replication', 'listObjects', 'NotImplemented', 501,
        1521
      ),
      (r'', 'MN_replication', 'replicate', 'NotImplemented', 501, 2000),
      (r'', 'MN_replication', 'replicate', 'ServiceFailure', 500, 2001),
      (r'', 'MN_replication', 'replicate', 'NotAuthorized', 401, 2010),
      (r'', 'MN_replication', 'replicate', 'InvalidRequest', 400, 2020),
      (r'', 'MN_replication', 'replicate', 'InsufficientResources', 413, 2030),
      (r'', 'MN_replication', 'replicate', 'UnsupportedType', 400, 2040),
    ]

  def detail_code(self, request, exception):
    for path_rx, module, method, exception_name, error_code, detail_code \
        in self.detail_codes_dict:
      if path_rx == '':
        continue
      try:
        if exception.name == exception_name and re.search(
            path_rx, request.path
        ):
          return detail_code
      except AttributeError:
        pass

    return 0
