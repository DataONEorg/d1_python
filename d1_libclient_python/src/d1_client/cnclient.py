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

'''Module d1_client.cnclient
============================

This module implements CoordinatingNodeClient, which extends DataONEBaseClient
with functionality specific to Coordinating Nodes.

:Created: 2011-01-22
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import urllib
import urlparse

# 3rd party.

# D1.
from d1_common import const
from d1_common import util
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
from d1baseclient import DataONEBaseClient

#SOLRclient is used to support search against the SOLR instance running on the
#coordinating node. 
import solrclient


class CoordinatingNodeClient(DataONEBaseClient):
  
  def __init__(self, baseurl=const.URL_DATAONE_ROOT, 
                     defaultHeaders={},
                     timeout=const.RESPONSE_TIMEOUT, 
                     keyfile=None, 
                     certfile=None,
                     strictHttps=True):
    '''Connect to a Coordinating Node.
    
    :param baseurl: Coordinating Node REST service endpoint URL.
    :type baseurl: str
    :param defaultHeaders: list of headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: int
    :param keyfile: name of a PEM formatted file that contains a private key. 
    :type keyfile: str
    :param certfile: PEM formatted certificate chain file.
    :type certfile: str
    :param strictHttps: Raise BadStatusLine if the status line can’t be parsed
    as a valid HTTP/1.0 or 1.1 status line.
    :type strictHttps: bool
    :returns: None
    :return type: NoneType
    '''
    DataONEBaseClient.__init__(self, baseurl, defaultHeaders=defaultHeaders,
                               timeout=timeout, keyfile=keyfile, 
                               certfile=certfile, strictHttps=strictHttps)
    self.logger = logging.getLogger('CoordinatingNodeClient')
    self.methodmap.update({
      'resolve': u'resolve/%(pid)s',
      'search': u'object',
      'listobjects': u'object?qt=path',
      'register': u'node/',
      'setreplicationstatus': u'replicaNotifications/%(pid)s',
      'setreplicationpolicy': u'replicaPolicies/%(pid)s',
    })


  @util.str_to_unicode
  def resolveResponse(self, pid):
    '''Wrap the CNRead.resolve() DataONE REST call.
    
    Returns the nodes (MNs or CNs) known to hold copies of the object identified
    by pid.

    :param pid: Identifier
    :type pid: string containing ASCII or UTF-8 | unicode string
    :returns: List of object locations.
    :return type: Serialized ObjectLocationList in HTTPResponse
    '''
    url = self.RESTResourceURL('resolve', pid=pid)
    return self.GET(url)

  
  @util.str_to_unicode
  def resolve(self, pid):
    '''See resolveResponse().
    
    :returns: List of object locations. 
    :return type: PyXB ObjectLocationList.
    '''
    response = self.resolveResponse(pid)
    return dataoneTypes.CreateFromDocument(response.read())


  @util.str_to_unicode
  def reserveIdentifier(self, pid=None, scope=None, format=None):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def assertRelation(self, pidOfSubject, relationship, pidOfObject):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def searchResponse(self, query):
    '''
    Wraps the CNRead.search() DataONE REST call.

    Search the metadata catalog and return identifiers of metadata records that
    match the criteria.
    
    :param query: Query string.
    :type query: str
    :returns: List of objects
    :return type: Serialized ObjectList in HttpResponse.
    '''
    url = self.RESTResourceURL('search')
    url_params = {
      'query': query,
    }
    return self.GET(url, url_params=url_params)


  @util.str_to_unicode
  def search(self, query, fields="pid,origin_mn,datemodified,size,objectformat,title",
             start=0, count=100):
    '''This is a place holder for search against the SOLR search engine.     
    '''
    hostinfo = self._parseURL(self.baseurl)
    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
                                     persistent=True)
    params = {'q':query,
              'fl': fields,
              'start':str(start),
              'rows':str(count)}
    sres = solr.search(params)
    return sres['response']    
    #response = self.searchResponse(query)
    #return dataoneTypes.CreateFromDocument(response.read())


  def getSearchFields(self):
    #getFields
    hostinfo = self._parseURL(self.baseurl)
    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
                                     persistent=True)
    sres = solr.getFields()
    return sres['fields']
  
  
  def searchSolr(self, query):
    '''Executes a search against SOLR. The literal query string is passed as
    the q parameter to SOLR, so it must be properly escaped
    '''
    pass


  @util.str_to_unicode
  def registerResponse(self, node, vendorSpecific=None):
    '''
    Register a new Member Node with DataONE.
    
    :param sysmeta: Node registration document for the Member Node being
      registered.
    :type sysmeta: PyXB Node
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Unprocessed response from server.
    :return type: httplib.HTTPResponse 
    '''
    url = self.RESTResourceURL('register')
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    node_xml = node.toxml()
    mime_multipart_files = [
      ('node', 'node', node_xml.encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files, headers=headers)


  @util.str_to_unicode
  def setReplicationStatus(self, pid, node, vendorSpecific=None):
    response = self.createResponse(node,
                                   vendorSpecific=vendorSpecific)
    return self.isHttpStatusOK(response.status)

  #=============================================================================
  # Replication API
  #=============================================================================

  # CNReplication.setReplicationStatus()
  
  @util.str_to_unicode
  def setReplicationStatusResponse(self, pid, nodeRef, status, serialVersion,
                                   vendorSpecific=None):
    '''
    Update the status of a current replication request.

    :param pid: Identifier of the object to be replicated between Member Nodes
    :type pid: str
    :param nodeRef: Reference to the Node which made the setReplicationStatus
      call
    :type nodeRef: str
    :param status: Replication status. See system metadata schema for possible
      values.
    :type status: str
    :param serialVersion: The serialVersion of the system metadata that is the
      intended target for the change.
    :type serialVersion: str
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Unprocessed response from server.
    :return type: httplib.HTTPResponse 
    '''
    url = self.RESTResourceURL('setreplicationstatus', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    mime_multipart_fields = [
      ('nodeRef', nodeRef.encode('utf-8')),
      ('status', status.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields, headers=headers)


  @util.str_to_unicode
  def setReplicationStatus(self, pid, nodeRef, status, serialVersion,
                           vendorSpecific=None):
    response = self.setReplicationStatusResponse(pid, nodeRef, status,
                                                 serialVersion,
                                                 vendorSpecific=vendorSpecific)
    return self.isHttpStatusOK(response.status)

  # CNReplication.updateReplicationMetadata()
  # Not implemented.
  
  # CNReplication.setReplicationPolicy()
  
  @util.str_to_unicode
  def setReplicationPolicyResponse(self, pid, policy, serialVersion,
                                   vendorSpecific=None):
    '''
    Update the replication policy for an object.

    :param pid: Identifier of the object to be replicated between Member Nodes
    :type pid: str
    :param policy: ReplicationPolicy
    :type policy: PyXB ReplicationPolicy
    :param serialVersion: The serialVersion of the system metadata that is the
      intended target for the change.
    :type serialVersion: str
    :param vendorSpecific: Dictionary of vendor specific extensions.
    :type vendorSpecific: dict
    :returns: Unprocessed response from server.
    :return type: httplib.HTTPResponse 
    '''
    url = self.RESTResourceURL('setreplicationstatus', pid=pid)
    headers = {}
    if vendorSpecific is not None:
      headers.update(vendorSpecific)
    mime_multipart_fields = [
      ('nodeRef', nodeRef.encode('utf-8')),
      ('status', status.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields, headers=headers)


  @util.str_to_unicode
  def setReplicationPolicy(self, pid, policy, serialVersion,
                           vendorSpecific=None):
    response = self.setReplicationPolicyResponse(pid, policy, serialVersion,
                                   vendorSpecific=vendorSpecific)
    return self.isHttpStatusOK(response.status)
  
  @util.str_to_unicode
  def getAuthToken(self, cert):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def setOwner(self, pid, userId):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def newAccount(self, username, password, authSystem=None): 
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def verifyToken(self, token):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def mapIdentity(self, token1, token2):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def createGroup(self, token, groupName):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def addGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def removeGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def setReplicationStatus(self, token, pid, status): 
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def addNodeCapabilities(self, token, pid):
    raise Exception('Not Implemented')

