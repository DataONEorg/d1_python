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
'''Module d1_client.d1baseclient_2_0
====================================
'''

# Stdlib.
import logging
import sys

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
  import d1_common.types.dataoneTypes_v2_0
  import d1_common.util
  import d1_common.url
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

import d1_client.d1baseclient_1_1

#=============================================================================


class DataONEBaseClient_2_0(d1_client.d1baseclient_1_1.DataONEBaseClient_1_1):
  '''Implements DataONE client functionality common between Member and
  Coordinating nodes by extending the RESTClient.

  Wraps REST methods that have the same signatures on Member Nodes and
  Coordinating Nodes.

  On error response, an attempt to raise a DataONE exception is made.

  Unless otherwise indicated, methods with names that end in "Response" return
  the HTTPResponse object, otherwise the deserialized object is returned.
  '''

  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 2)
    kwargs.setdefault('api_minor', 0)
    d1_client.d1baseclient_1_1.DataONEBaseClient_1_1.__init__(
      self, *args, **kwargs
    )

  #=============================================================================
  # v2.0 APIs shared between CNs and MNs.
  #=============================================================================

  # TODO: Implement or move shared methods here.
