#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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

'''Module d1_client.d1baseclient_2_0
====================================

:Synopsis:
  This module implements DataONEBaseClient_2_0, which extends DataONEBaseClient
  with functionality defined in v2.0 of the DataONE service specifications.

  Methods that are common for CN and MN:

  # CNRead.query(session, queryEngine, query) → OctetStream
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.query

  CNCore/MNCore.getLogRecords()
  CNRead/MNRead.get()
  CNRead/MNRead.getSystemMetadata()
  CNRead/MNRead.describe()
  CNRead/MNRead.listObjects()
  CNAuthorization/MNAuthorization.isAuthorized()

  See the `Coordinating Node <http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html>`_
  and `Member Node <http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_
  APIs for details on how to use the methods in this class.
:Created: 2014-08-18
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import re
import urlparse
import StringIO
import sys
import d1client

# 3rd party.
try:
    import pyxb
except ImportError as e:
    sys.stderr.write('Import error: {0}\n'.format(str(e)))
    sys.stderr.write('Try: easy_install PyXB\n')
    raise

# D1.
try:
    import d1_common.const
    import d1_common.restclient
    import d1_common.types.generated.dataoneTypes_2_0 as dataoneTypes_2_0
    import d1_common.util
    import d1_common.url
except ImportError as e:
    sys.stderr.write('Import error: {0}\n'.format(str(e)))
    sys.stderr.write('Try: easy_install DataONE_Common\n')
    raise

import d1baseclient

#=============================================================================


class DataONEBaseClient_2_0(d1baseclient.DataONEBaseClient):

    '''Implements DataONE client functionality common between Member and
    Coordinating nodes by extending the RESTClient.

    Wraps REST methods that have the same signatures on Member Nodes and
    Coordinating Nodes.

    On error response, an attempt to raise a DataONE exception is made.

    Unless otherwise indicated, methods with names that end in "Response" return
    the HTTPResponse object, otherwise the deserialized object is returned.
    '''

    def __init__(self, *args, **kwargs):
        '''Connect to a DataONE Coordinating Node or Member Node.

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
        :param response_contains_303_redirect: Allow server to return a 303 See Other instead of 200 OK.
        :type response_contains_303_redirect: boolean
        :param version: Value to insert in the URL version section.
        :type version: string
        :param types: The PyXB bindings to use for XML serialization and
          deserialization.
        :type types: PyXB
        :returns: None
        '''
        d1baseclient.DataONEBaseClient.__init__(
            self,
            *
            args,
            **kwargs)

    #=========================================================================
    # v2.0 APIs shared between CNs and MNs.
    #=========================================================================
