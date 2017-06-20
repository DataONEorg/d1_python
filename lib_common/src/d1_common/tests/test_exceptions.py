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

from __future__ import absolute_import

import xml.dom.minidom

import pytest

from d1_common.types import exceptions

import d1_test.d1_test_case

TRACE_SECTION = """  <traceInformation>
    <value>traceInformation0</value>
    <value>traceInformation2</value>
  </traceInformation>"""

VALID_ERROR_DOC = """<?xml version="1.0" encoding="UTF-8"?>
<error  detailCode="123.456.789"
        errorCode="456"
        identifier="SomeDataONEPID"
        name="IdentifierNotUnique"
        nodeId="urn:node:SomeNode">
  <description>description0</description>""" + TRACE_SECTION + """
</error>
"""

VALID_ERROR_DOC_NOTFOUND = """<?xml version="1.0" encoding="UTF-8"?>
<error detailCode="1800" errorCode="404" name="NotFound">
    <description>No system metadata could be found for given PID: something_bogus/</description>
</error>
"""

VALID_ERROR_DOC_NOTFOUND_2 = """<?xml version="1.0"?>
<error detailCode="0" errorCode="404" name="NotFound" nodeId="urn:node:LTER">
<description>Attempted to perform operation on non-existing object</description>
<traceInformation><value>1. something_bogus
2. on two lines</value></traceInformation>
</error>"""

VALID_ERROR_DOC_NOTFOUND_3 = """<?xml version="1.0"?>
<error detailCode="0" errorCode="404" name="NotFound" nodeId="urn:node:LTER">
<description>Attempted to perform operation on non-existing object</description>
<traceInformation><value>1. Σολυτα βωνορυμ θε κυο,
2. ναμ ετ νοσθερ σιμιλικυε.</value></traceInformation>
</error>"""

#  'SHA-1',
#  '3f56de593b6ffc536253b799b429453e3673fc19'
#)

# Missing detailCode.
INVALID_ERROR_DOC = (
  """<?xml version="1.0" encoding="UTF-8"?>
  <d1:error xmlns:d1="http://ns.dataone.org/service/types/exceptions"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://ns.dataone.org/service/types/exceptions"
  errorCode="0" name="IdentifierNotUnique" pid="somedataonepid">
  <description>description0</description>
  <traceInformation>traceInformation0</traceInformation>
  </d1:error>""", '', ''
)


class TestExceptions(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """deserialize()"""
    d1_exception = exceptions.deserialize(VALID_ERROR_DOC)
    assert isinstance(d1_exception, exceptions.IdentifierNotUnique)
    assert d1_exception.detailCode == '123.456.789'
    assert d1_exception.errorCode == 409
    assert d1_exception.name == 'IdentifierNotUnique'
    assert d1_exception.identifier == 'SomeDataONEPID'
    assert d1_exception.nodeId == 'urn:node:SomeNode'
    assert d1_exception.description == 'description0'
    assert d1_exception.traceInformation == TRACE_SECTION.strip()

  def test_1010(self):
    """deserialize, serialize, deserialize"""
    x1 = exceptions.deserialize(VALID_ERROR_DOC_NOTFOUND)
    sxml = x1.serialize()
    x2 = exceptions.deserialize(sxml)
    assert isinstance(x2, exceptions.NotFound)
    assert x1.errorCode == x2.errorCode
    assert x1.detailCode == x2.detailCode
    assert x1.name == x2.name
    assert x1.description == x2.description
    assert x1.nodeId == x2.nodeId
    assert x1.identifier == x2.identifier
    assert x1.traceInformation == x2.traceInformation

  def test_1020(self):
    """deserialize, serialize, deserialize"""
    x1 = exceptions.deserialize(VALID_ERROR_DOC_NOTFOUND_2)
    sxml = x1.serialize()
    x2 = exceptions.deserialize(sxml)
    assert isinstance(x2, exceptions.NotFound)
    assert x1.errorCode == x2.errorCode
    assert x1.detailCode == x2.detailCode
    assert x1.name == x2.name
    assert x1.description == x2.description
    assert x1.nodeId == x2.nodeId
    assert x1.identifier == x2.identifier
    assert x1.traceInformation == x2.traceInformation

  def test_1030(self):
    """deserialize, serialize, deserialize"""
    x1 = exceptions.deserialize(VALID_ERROR_DOC_NOTFOUND_3)
    sxml = x1.serialize()
    x2 = exceptions.deserialize(sxml)
    assert isinstance(x2, exceptions.NotFound)
    assert x1.errorCode == x2.errorCode
    assert x1.detailCode == x2.detailCode
    assert x1.name == x2.name
    assert x1.description == x2.description
    assert x1.nodeId == x2.nodeId
    assert x1.identifier == x2.identifier
    assert x1.traceInformation == x2.traceInformation

  def test_1040(self):
    """deserialize() of bad document raises ServiceFailure"""
    with pytest.raises(exceptions.ServiceFailure):
      exceptions.deserialize(INVALID_ERROR_DOC[0])

  def test_1050(self):
    """String representation"""
    d1_exception = exceptions.deserialize(VALID_ERROR_DOC)
    assert 'name: IdentifierNotUnique' in str(d1_exception)
    assert 'errorCode: 409' in str(d1_exception)
    assert 'detailCode: 123.456.789' in str(d1_exception)

  def test_1060(self):
    """create with only detailCode then serialize()"""
    e = exceptions.ServiceFailure(123)
    assert e.serialize() == u'<?xml version="1.0" encoding="utf-8"?>' \
      u'<error detailCode="123" errorCode="500" name="ServiceFailure"/>'

  def test_1070(self):
    """create with string detailCode and description, then serialize()"""
    e = exceptions.ServiceFailure('123.456.789', 'test description')
    se = e.serialize()
    assert se == u'<?xml version="1.0" encoding="utf-8"?>' \
      u'<error detailCode="123.456.789" errorCode="500" name="ServiceFailure">' \
      u'<description>test description</description></error>'

  def test_1080(self):
    """create with detailCode, description and traceInformation, then serialize()"""
    e = exceptions.ServiceFailure(
      '123.456.789', description='test description',
      traceInformation='test traceInformation'
    )
    se = e.serialize()
    assert se == u'<?xml version="1.0" encoding="utf-8"?>' \
      u'<error detailCode="123.456.789" errorCode="500" name="ServiceFailure">' \
      u'<description>test description</description>' \
      u'<traceInformation>test traceInformation</traceInformation></error>'

  def test_1090(self):
    """serialize_to_headers()"""
    e = exceptions.ServiceFailure(
      '123.456.789', 'test description', 'test traceInformation'
    )
    header_dict = e.serialize_to_headers()
    expected_dict = {
      'DataONE-Exception-TraceInformation': u'test traceInformation',
      'DataONE-Exception-DetailCode': u'123.456.789',
      'DataONE-Exception-Name': 'ServiceFailure',
      'DataONE-Exception-Description': u'test description',
      'DataONE-Exception-NodeID': '',
      'DataONE-Exception-Identifier': '',
      'DataONE-Exception-ErrorCode': u'500'
    }
    assert header_dict == expected_dict

  def test_1100(self):
    """deserialize_from_headers()"""
    headers = {
      'DataONE-Exception-Name': 'IdentifierNotUnique', # required
      'DataONE-Exception-DetailCode': '123.456.789', # required
      'DataONE-Exception-Description':
        'test description', # provided but not required
      'dataone-exception-traceinformation':
        'test traceInformation', # not required but provided in lower case
      #'DataONE-Exception-Identifier' not required or provided
      #'DataONE-Exception-NodeId' not required or provided
    }
    e = exceptions.deserialize_from_headers(headers)
    assert e.name == 'IdentifierNotUnique'
    assert e.errorCode == 409
    assert e.detailCode == '123.456.789'
    assert e.description == 'test description'
    assert e.traceInformation == 'test traceInformation'

  def test_1110(self):
    """Serialization and deserialization of DataONE Exceptions

    Test serialization and deserialization of DataONE Exceptions by performing
    a round trip:

    1) Create a native DataONE Exception object
    2) Serialize the object to XML
    3) Deserialize XML to object
    4) Verify that the object contains the same information as in (1)
    """
    # Create a native DataONE IdentifierNotUnique Exception object.
    exc = exceptions.IdentifierNotUnique(
      1010, 'description_test', 'test trace information', 'test_pid', 'node_id'
    )
    # Serialize to XML.
    exc_ser_xml = exc.serialize()
    # Check XML.
    dom = xml.dom.minidom.parseString(exc_ser_xml)
    root = dom.firstChild
    assert root.tagName == u'error'
    assert root.attributes['detailCode'].value == u'1010'
    assert root.attributes['errorCode'].value == u'409'
    assert root.attributes['name'].value == u'IdentifierNotUnique'
    assert root.attributes['identifier'].value == u'test_pid'
    assert root.getElementsByTagName('description')[0].childNodes[0].nodeValue == \
      u'description_test'
    # Disabled until we have decided how to encode traceInformation.
    #self.assertEqual(root.getElementsByTagName('traceInformation')[0]\
    #                 .childNodes[0].nodeValue, u'test trace information')
    # Deserialize XML.
    exc_deser = exceptions.deserialize(exc_ser_xml)
    # Check deserialized native object.
    assert exc_deser.detailCode == '1010'
    assert exc_deser.errorCode == 409
    assert exc_deser.name == 'IdentifierNotUnique'
    assert exc_deser.identifier == 'test_pid'
    assert exc_deser.description == 'description_test'
    # Disabled until we have decided how to encode traceInformation.
    #self.assertEqual(exc_deser.traceInformation, 'test trace information')
