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

# Stdlib
import logging

# App
import baseclient_1_1
import mnclient


class MemberNodeClient_1_1(
    baseclient_1_1.DataONEBaseClient_1_1,
    mnclient.MemberNodeClient,
):
  """Extend DataONEBaseClient_1_1 and MemberNodeClient with functionality
  for Member nodes that was added in v1.1 of the DataONE infrastructure.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 1)
    kwargs.setdefault('api_minor', 1)
    baseclient_1_1.DataONEBaseClient_1_1.__init__(self, *args, **kwargs)
    mnclient.MemberNodeClient.__init__(self, *args, **kwargs)
