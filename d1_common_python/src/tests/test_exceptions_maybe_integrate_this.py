#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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

import d1_common.types.exceptions as exceptions

ex = """<?xml version="1.0" encoding="UTF-8"?>
<error detailCode="test" errorCode="409" name="IdentifierNotUnique" identifier="somedataonepid">
    <description>description0</description>
    <traceInformation>traceInformation0</traceInformation>
</error>"""

ex2 = '''<?xml version="1.0" encoding="UTF-8"?>
<error  detailCode="123.456.789"
        errorCode="456"
        identifier="SomeDataONEPID"
        name="IdentifierNotUnique"
        nodeId="urn:node:SomeNode">
  <description>description0</description>
  <traceInformation><value>traceInformation0</value></traceInformation>
</error>
'''

exobj = exceptions.deserialize(ex)

print exobj.serialize()
