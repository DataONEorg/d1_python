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

'''Module d1_client.mnclient_2_0
================================

:Synopsis:
  This is where the new MN APIs in CCI 2.0 will be added.

  This module implements the DataONE Member Node v2.0 API methods. It extends
  MemberNodeClient_1_1, making 1.0 and 1.1 methods available as well.

  See the `Member Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/MN_APIs.html>`_
  details on how to use the methods in this class.

:Created: 2014-08-18
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
  import d1_common.const
  import d1_common.types.dataoneTypes_v2_0 as dataoneTypes
  import d1_common.util
  import d1_common.date_time
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import d1baseclient_2_0
import mnclient_1_1


class MemberNodeClient_2_0(d1baseclient_2_0.DataONEBaseClient_2_0, mnclient_1_1.MemberNodeClient_1_1):
  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 2)
    kwargs.setdefault('api_minor', 0)
    d1baseclient_2_0.DataONEBaseClient_2_0.__init__(self, *args, **kwargs)
    mnclient_1_1.MemberNodeClient_1_1.__init__(self, *args, **kwargs)

  # MNStorage.updateSystemMetadata(session, pid, sysmeta) → boolean
  # http://jenkins-1.dataone.org/documentation/unstable/API-Documentation-development/apis/MN_APIs.html#MNStorage.updateSystemMetadata

  @d1_common.util.utf8_to_unicode
  def updateSystemMetadataResponse(self, pid, sysmeta, vendorSpecific=None):
      if vendorSpecific is None:
          vendorSpecific = {}

      url = self._rest_url('meta')
      mime_multipart_fields = [
          ('pid', pid.encode('utf-8')),
      ]
      mime_multipart_files = [
          ('sysmeta', 'sysmeta.xml', sysmeta.toxml().encode('utf-8')),
      ]
      return self.PUT(url, fields=mime_multipart_fields, files=mime_multipart_files,headers=vendorSpecific)


  @d1_common.util.utf8_to_unicode
  def updateSystemMetadata(self, pid, sysmeta):
      response = self.updateSystemMetadataResponse(pid, sysmeta)
      #cn_client =
      return self._read_boolean_response(response)

