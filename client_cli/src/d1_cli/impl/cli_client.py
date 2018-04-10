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
"""CN and MN clients of the DataONE Command Line Interface

The logic was factored out of these and reimplemented in more natural locations.
This is just a placeholder for now. May remove.
"""

import d1_client.cnclient


class CLIClient(object):
  pass


#===============================================================================


class CLIMNClient(CLIClient, d1_client.mnclient.MemberNodeClient):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


#===============================================================================


class CLICNClient(CLIClient, d1_client.cnclient.CoordinatingNodeClient):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


#===============================================================================


class CLIBaseClient(d1_client.baseclient.DataONEBaseClient):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
