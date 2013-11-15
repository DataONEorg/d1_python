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

'''Module d1_client.mnclient_1_1
================================

:Synopsis:
  This module is currently a stub, as no functionality was added to the
  MN APIs in 1.1.

  See the `Member Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_
  details on how to use the methods in this class.

:Created: 2011-01-21
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
  import d1_common.const
  import d1_common.types.generated.dataoneTypes_1_1 as dataoneTypes_1_1
  import d1_common.util
  import d1_common.date_time
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import d1baseclient_1_1


class MemberNodeClient(d1baseclient_1_1.DataONEBaseClient_1_1):
  def __init__(self,
               base_url,
               timeout=d1_common.const.RESPONSE_TIMEOUT,
               defaultHeaders=None,
               cert_path=None,
               key_path=None,
               strict=True,
               capture_response_body=False,
               version='v1',
               types=dataoneTypes_1_1):
    '''Connect to a DataONE Member Node.

    :param base_url: DataONE Node REST service BaseURL
    :type host: string
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param defaultHeaders: headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param cert_path: Path to a PEM formatted certificate file.
    :type cert_path: string
    :param key_path: Path to a PEM formatted file that contains the private key
      for the certificate file. Only required if the certificate file does not
      itself contain a private key.
    :type key_path: string
    :param strict: Raise BadStatusLine if the status line can’t be parsed
      as a valid HTTP/1.0 or 1.1 status line.
    :type strict: boolean
    :param capture_response_body: Capture the response body from the last
      operation and make it available in last_response_body.
    :type capture_response_body: boolean
    :param version: Value to insert in the URL version section.
    :type version: string
    :param types: The PyXB bindings to use for XML serialization and
      deserialization.
    :type types: PyXB
    :returns: None
    '''
    d1baseclient_1_1.DataONEBaseClient_1_1.__init__(self, base_url=base_url,
      timeout=timeout, defaultHeaders=defaultHeaders, cert_path=cert_path,
      key_path=key_path, strict=strict,
      capture_response_body=capture_response_body, version=version, types=types)
    self.logger = logging.getLogger('MemberNodeClient')
