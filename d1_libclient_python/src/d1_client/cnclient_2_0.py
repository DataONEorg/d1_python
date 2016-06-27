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
'''Module d1_client.cnclient_1_1_2_0
================================

:Synopsis:
  This is where the new CN APIs in CCI 2.0 will be added.

  This module implements the DataONE Coordinating Node v2.0 API methods. It
  extends CoordinatingNodeClient_1_1, making 1.0 and 1.1 methods available as
  well.

  See the `Coordinating Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html>`_
  for details on how to use the methods in this class.
:Created: 2014-08-18
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
  import d1_common.const
  import d1_common.types.dataoneTypes_v2_0
  import d1_common.util
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import d1baseclient_2_0
import cnclient_1_1


class CoordinatingNodeClient_2_0(
  d1baseclient_2_0.DataONEBaseClient_2_0,
  cnclient_1_1.CoordinatingNodeClient_1_1,
):
  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 2)
    kwargs.setdefault('api_minor', 0)
    d1baseclient_2_0.DataONEBaseClient_2_0.__init__(self, *args, **kwargs)
    cnclient_1_1.CoordinatingNodeClient_1_1.__init__(self, *args, **kwargs)

  #=========================================================================
  # Core API
  #=========================================================================

  # CNCore.listFormats() → ObjectFormatList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listFormats
  # v2.0: The structure of v2_0.Types.ObjectFormat has changed.

  def listFormatsResponse(self):
    url = self._rest_url('formats')
    return self.GET(url)

  def listFormats(self):
    response = self.listFormatsResponse()
    return self._read_dataone_type_response(response, 'ObjectFormatList')

