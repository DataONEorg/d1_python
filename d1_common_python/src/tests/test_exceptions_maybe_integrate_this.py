#!/usr/bin/env python

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
