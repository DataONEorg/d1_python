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
'''Module d1_client.mnclient
============================

:Created: 2011-01-21
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6

This module implements MemberNodeClient, which extends DataONEBaseClient
with functionality specific to Member Nodes.
'''

# Stdlib.
import logging
import urlparse

# D1.
from d1_common import const
from d1_common import util
from d1baseclient import DataONEBaseClient
import objectlistiterator
import d1_common.types.generated.dataoneTypes as dataoneTypes


class MemberNodeClient(DataONEBaseClient):
  def __init__(self, baseurl, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True, keep_response_body=False):
    DataONEBaseClient.__init__(
      self,
      baseurl,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )
    self.logger = logging.getLogger('MemberNodeClient')

    self.methodmap.update(
      {
        'create': u'object/%(pid)s',
        'update': u'object_put/%(pid)s',
        'getchecksum': u'checksum/%(pid)s',
        'getcapabilities': u'node',
      }
    )
    self.lastresponse = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.lastresponse
    self.keep_response_body = keep_response_body

  @util.str_to_unicode
  def createResponse(self, pid, obj, sysmeta, vendorSpecific=None):
    '''
    Create a Science Object.
    
    :param pid: The DataONE Persistent Identifier of the object being created. 
    :type pid: Identifier
    :param obj: The bytes of the object to create.
    :type obj: String or File Like Object
    :param sysmeta: System Metadata for the object being created.
    :type sysmeta: PyXB SystemMetadata
        :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict

    :returns: Unprocessed response from server.
    :return type: httplib.HTTPResponse 
    '''
    url = self.RESTResourceURL('create', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    # Serialize sysmeta to XML.
    sysmeta_xml = sysmeta.toxml()
    # Set up structure for use in generating the MIME multipart document
    # that will be POSTed to the server.
    files = [
      ('object', 'content.bin', obj),
      ('sysmeta', 'systemmetadata.abc', sysmeta_xml.encode('utf-8')),
    ]
    # Generate MIME multipart document and post to server.
    return self.POST(url, files=files, headers=headers)

  @util.str_to_unicode
  def create(self, pid, obj, sysmeta, vendorSpecific=None):
    response = self.createResponse(pid, obj, sysmeta, vendorSpecific=vendorSpecific)
    return self.isHttpStatusOK(response.status)

  @util.str_to_unicode
  def updateResponse(self, pid, obj, new_pid, sysmeta, vendorSpecific=None):
    '''
    :param pid: The identifier of the object that is being updated 
    :type pid: Identifier
    :param obj: Science Data
    :type obj: Unicode or file like object
    :param new_pid: The identifier that will become the replacement
                    identifier for the existing object after the
                    update.
    :type new_pid: Identifier
    :param sysmeta:
    :type: sysmeta: Unicode or file like object
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: True on successful completion
    :return type: Boolean
    '''
    url = self.RESTResourceURL('update', pid=pid)
    headers = {}
    headers['newPid'] = new_pid
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    files = [('object', 'content.bin', obj), ('sysmeta', 'systemmetadata.xml', sysmeta), ]
    # TODO: Should be PUT against /object. Instead is POST against
    # /object_put. Change when PUT support in Django is fixed.
    return self.POST(url, files=files, headers=headers)

  @util.str_to_unicode
  def update(self, pid, obj, new_pid, sysmeta, vendorSpecific=None):
    response = self.updateResponse(
      pid, obj, new_pid, sysmeta,
      vendorSpecific=vendorSpecific
    )
    return self.isHttpStatusOK(response.status)

  @util.str_to_unicode
  def deleteResponse(self, pid, vendorSpecific=None):
    '''Delete a SciObj from MN.
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    '''
    url = self.RESTResourceURL('get', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    response = self.DELETE(url, headers=headers)
    return response

  @util.str_to_unicode
  def delete(self, pid, vendorSpecific=None):
    response = self.deleteResponse(pid, vendorSpecific=vendorSpecific)
    doc = response.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  @util.str_to_unicode
  def getChecksumResponse(self, pid, checksumAlgorithm=None, vendorSpecific=None):
    '''
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    '''
    url = self.RESTResourceURL('getchecksum', pid=pid)
    url_params = {'checksumAlgorithm': checksumAlgorithm, }
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    response = self.GET(url, url_params=url_params, headers=headers)
    return response

  @util.str_to_unicode
  def getChecksum(self, pid, checksumAlgorithm=None, vendorSpecific=None):
    response = self.getChecksumResponse(
      pid, checksumAlgorithm, vendorSpecific=vendorSpecific
    )
    doc = response.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  @util.str_to_unicode
  def replicate(self, sysmeta, sourceNode, vendorSpecific=None):
    raise Exception('Not Implemented')

  @util.str_to_unicode
  def synchronizationFailed(self, message):
    raise Exception('Not Implemented')

  def getCapabilitiesResponse(self, vendorSpecific=None):
    url = self.RESTResourceURL('getcapabilities')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    return self.GET(url, headers=headers)

  def getCapabilities(self, vendorSpecific=None):
    '''
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    '''
    response = self.getCapabilitiesResponse(vendorSpecific=vendorSpecific)
    doc = response.read()
    if self.keep_response_body:
      self.lastresponse.body = doc
    return dataoneTypes.CreateFromDocument(doc)

  @util.str_to_unicode
  def describeResponse(self, pid, vendorSpecific=None):
    '''
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    '''
    url = self.RESTResourceURL('get', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    response = self.HEAD(url, headers=headers)
    return response

  @util.str_to_unicode
  def describe(self, pid, vendorSpecific=None):
    '''This method provides a lighter weight mechanism than
    MN_crud.getSystemMetadata() for a client to determine basic properties of
    the referenced object.

    :param: (string) Identifier of object to retrieve.
    :return: mimetools.Message or raises DataONEException.

    TODO: May need to be completely removed (since clients should use CNs for
    object discovery).
    '''
    return self.describeResponse(pid, vendorSpecific=vendorSpecific)
