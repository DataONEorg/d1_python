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
<d1:error xmlns:d1="http://ns.dataone.org/service/types/exceptions"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://ns.dataone.org/service/types/exceptions file:/home/dahl/eclipse_workspace_d1/d1_common_python/src/d1_schemas/dataoneErrors.xsd"
    detailCode="0" errorCode="0" name="IdentifierNotUnique" pid="somedataonepid">
    <description>description0</description>
    <traceInformation>traceInformation0</traceInformation>
</d1:error>"""

exobj = exceptions.deserialize_exception(ex)

print exobj.toxml()
