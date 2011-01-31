'''
Created on Jan 28, 2011

@author: roger
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_common.types.exception_serialization
==============================================

Implements serializaton and de-serialization for the DataONE Exception type.
'''

# Stdlib.
import logging
import urllib
try:
  import cjson as json
except:
  import json
try:
  from xml.etree import cElementTree as ETree
except:
  from xml.etree import ElementTree as Etree
import xml.dom.minidom

# App.
import d1_common.const
import serialization_base
import d1_common.types.exceptions


def instanceToSimpleType(instance):
  '''Force instance to a simple type- int, float, or string
  '''
  if isinstance(instance, float):
    return instance
  if isinstance(instance, int):
    return instance
  if isinstance(instance, basestring):
    return instance
  return unicode(instance)


class DataONEExceptionSerialization(serialization_base.Serialization):
  '''Implements serialization of DataONE Exception.
  '''

  def __init__(self, dataone_exception):
    serialization_base.Serialization.__init__(self)

    self.log = logging.getLogger('DataONEExceptionSerialization')

    self.pri = [
      d1_common.const.MIMETYPE_XML,
      d1_common.const.MIMETYPE_APP_XML,
      d1_common.const.MIMETYPE_JSON,
      #d1_common.const.MIMETYPE_CSV,
      #d1_common.const.MIMETYPE_RDF,
      d1_common.const.MIMETYPE_HTML,
      #d1_common.const.MIMETYPE_LOG,
      d1_common.const.MIMETYPE_TEXT,
    ]

    self.dataone_exception = dataone_exception

  def serialize_xml(self, pretty=False, jsonvar=False):
    '''Serialize DataONE Exception to XML.

    :rtype: UTF-8 encoded XML string
    '''
    root = ETree.Element(
      u'error', {
        u'name': self.dataone_exception.name,
        u'errorCode': str(self.dataone_exception.errorCode),
        u'detailCode': str(self.dataone_exception.detailCode)
      }
    )
    try:
      ETree.SubElement(root, u'pid').text = self.dataone_exception.pid
    except AttributeError:
      pass
    ETree.SubElement(root, u'description').text = self.dataone_exception.description
    for v in self.dataone_exception.traceInformation:
      ETree.SubElement(root, u'traceInformation').text = unicode(v)

    doc = ETree.tostring(root, 'utf-8')

    if pretty:
      xml_obj = xml.dom.minidom.parseString(doc)
      doc = xml_obj.toprettyxml(encoding='utf-8')

    return doc

  def serialize_json(self, pretty=False, jsonvar=False):
    '''Serialize DataONE Exception to JSON.

    :rtype: UTF-8 encoded JSON string
    '''
    json_obj = {
     u'name': self.dataone_exception.name,
     u'errorCode': self.dataone_exception.errorCode,
     u'detailCode': str(self.dataone_exception.detailCode),
     u'description': self.dataone_exception.description,
     u'traceInformation': [
       instanceToSimpleType(v)
       for v in self.dataone_exception.traceInformation
     ],
    }
    try:
      json_obj['pid'] = self.dataone_exception.pid
    except AttributeError:
      pass

    if not jsonvar:
      return json.dumps(json_obj)

    return u'{0}={1}'.format(jsonvar, json.dumps(json_obj))

  def serialize_html(self, pretty=False, jsonvar=False):
    '''Serialize DataONE Exception to HTML.
    
    :rtype: UTF-8 encoded HTML string
    '''
    root = ETree.Element(u'html')
    head = ETree.SubElement(
      root, u'meta', {
        u'http-equiv': u'content-type',
        u'content': u'text/html;charset=utf-8'
      }
    )
    title = ETree.SubElement(head, u'title')

    title.text = u'Error: {0} {1} ({2})'.format(
      urllib.quote(unicode(self.dataone_exception.errorCode)),
      self.dataone_exception.name, urllib.quote(str(self.dataone_exception.detailCode))
    )

    body = ETree.SubElement(root, u'body')
    dl = ETree.SubElement(body, u'dl')

    ETree.SubElement(dl, u'dt').text = u'Code'
    ETree.SubElement(dl, u'dd', {u'class': u'errorCode'}).text = str(
      self.dataone_exception.errorCode
    )

    ETree.SubElement(dl, u'dt').text = u'Detail Code'
    ETree.SubElement(dl, u'dd', {u'class': u'detailCode'}).text = str(
      self.dataone_exception.detailCode
    )

    ETree.SubElement(dl, u'dt').text = u'Description'
    ETree.SubElement(dl, u'dd', {u'class': u'description'}).text = self.dataone_exception.description

    if len(self.dataone_exception.traceInformation) > 0:
      ETree.SubElement(dl, u'dt').text = u'Trace'
      for v in self.dataone_exception.traceInformation:
        ETree.SubElement(dl, u'dd', {u'class': u'traceInformation'}).text = str(v)

    doc = ETree.tostring(root, 'utf-8')

    # TODO: Add pretty printing for html.

    return doc

  def serialize_text(self, pretty=False, jsonvar=False):
    '''Serialize DataONE Exception to text.

    :rtype: string
    '''
    return str(self.dataone_exception)

  #== Deserialization =========================================================

  def dataone_exception_factory(
    self, exception_name,
    detailCode,
    description,
    pid=None,
    traceInformation=None
  ):
    '''Implements a simple factory that generates a DataONE exception object.

    This class would normally be used by the client to re-raise an exception on 
    the client side from an error that occurred on the server.

    Returns an instance of some subclass of DataONEException.
    
    :param exception_name: The class name of the exception to create. Raises a LookupError based
                           exception if the name is invalid.
    :type data: str
    
    :param detailCode:
    :type data: int

    :param description:
    :type data: str

    :param traceInformation:
    :type data: list

    :param pid:
    :type data: str
    '''

    exception_map = {
      u'AuthenticationTimeout': d1_common.types.exceptions.AuthenticationTimeout,
      u'IdentifierNotUnique': d1_common.types.exceptions.IdentifierNotUnique,
      u'InsufficientResources': d1_common.types.exceptions.InsufficientResources,
      u'InvalidCredentials': d1_common.types.exceptions.InvalidCredentials,
      u'InvalidRequest': d1_common.types.exceptions.InvalidRequest,
      u'InvalidSystemMetadata': d1_common.types.exceptions.InvalidSystemMetadata,
      u'InvalidToken': d1_common.types.exceptions.InvalidToken,
      u'NotAuthorized': d1_common.types.exceptions.NotAuthorized,
      u'NotFound': d1_common.types.exceptions.NotFound,
      u'NotImplemented': d1_common.types.exceptions.NotImplemented,
      u'ServiceFailure': d1_common.types.exceptions.ServiceFailure,
      u'UnsupportedMetadataType': d1_common.types.exceptions.UnsupportedMetadataType,
      u'UnsupportedType': d1_common.types.exceptions.UnsupportedType,
    }

    # Create exception that includes PID.
    if exception_name in (u'IdentifierNotUnique', u'NotFound'):
      return exception_map[exception_name](detailCode, description, pid, traceInformation)

    # Create exception without PID.
    return exception_map[exception_name](detailCode, description, traceInformation)

  def deserialize_xml(self, doc):
    '''Deserialize DataONEException from XML.
    
    :param data: XML serialized DataONEException
    :type data: UTF-8 encoded XML string
    
    :rtype: A DataONEException based object.
    '''
    etree = ETree.fromstring(doc)
    return self.dataone_exception_factory(
      etree.attrib[u'name'], etree.attrib[u'detailCode'].strip(),
      etree.find(u'description').text.strip(), etree.find(u'pid').text.strip(), [
        element.text.strip() for element in etree.findall(
          u'traceInformation'
        )
      ]
    )

  def deserialize_json(self, doc):
    '''Deserialize DataONEException from JSON.
    
    :param data: The exception rendered as a JSON string
    :type data: string

    :rtype: DataONEException
    '''
    exjson = json.loads(doc)

    return self.dataone_exception_factory(
      exjson[u'name'], exjson[u'detailCode'], exjson[u'description'],
      exjson.get(u'pid', None), exjson[u'traceInformation']
    )
