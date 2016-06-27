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
'''Module d1_client.mnclient_1_1
================================

:Synopsis:
  No functionality was added to the MN APIs in 1.1.

  This module is a placeholder for consistency in the client hierarchy.

:Created: 2011-01-21
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
  import d1_common.const
  import d1_common.util
  import d1_common.date_time
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import d1baseclient_1_1
import mnclient


class MemberNodeClient_1_1(
  d1baseclient_1_1.DataONEBaseClient_1_1,
  mnclient.MemberNodeClient,
):
  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 1)
    kwargs.setdefault('api_minor', 1)
    d1baseclient_1_1.DataONEBaseClient_1_1.__init__(self, *args, **kwargs)
    mnclient.MemberNodeClient.__init__(self, *args, **kwargs)
