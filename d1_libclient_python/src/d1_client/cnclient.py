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

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.util

# App.
import d1baseclient

# SOLRclient is used to support search against the SOLR instance running on the
# coordinating node. 
import solrclient


class CoordinatingNodeClient(d1baseclient.DataONEBaseClient):
  '''Connect to a Coordinating Node and perform REST calls against the CN API
  '''  
  def __init__(self,
               base_url=d1_common.const.URL_DATAONE_ROOT, 
               timeout=d1_common.const.RESPONSE_TIMEOUT, 
               defaultHeaders=None, 
               cert_path=None,
               key_path=None, 
               strict=True,
               capture_response_body=False,
               version='v1'):
    '''Connect to a DataONE Coordinating Node.
    
    :param base_url: DataONE Node REST service BaseURL
    :type host: string
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param defaultHeaders: headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param cert_path: Path to a PEM formatted certificate file.
    :type cert_path: string
    :param key_path: Path to a PEM formatted file that contains the private key
      for the certificate file. Only required if the certificate file does not
      itself contain a private key. 
    :type key_path: string
    :param strict: Raise BadStatusLine if the status line can’t be parsed
      as a valid HTTP/1.0 or 1.1 status line.
    :type strict: boolean
    :param capture_response_body: Capture the response body from the last
      operation and make it available in last_response_body.
    :type capture_response_body: boolean
    :returns: None
    '''
    self.logger = logging.getLogger('CoordinatingNodeClient')
    if defaultHeaders is None:
      defaultHeaders = {}
    # Init the DataONEBaseClient base class.
    d1baseclient.DataONEBaseClient.__init__(self, base_url, timeout=timeout,
      defaultHeaders=defaultHeaders, cert_path=cert_path, key_path=key_path,
      strict=strict, capture_response_body=capture_response_body,
      version=version)
    # A dictionary that provides a mapping from method name (from the DataONE
    # APIs) to a string format pattern that will be appended to the URL.
    self.methodmap.update({
      # Core API
      # create(): CN internal
      'listFormats': u'formats',
      'getFormat': u'formats/%(formatId)s',
      # getLogRecords(): Implemented in d1baseclient
      'reserveIdentifier': u'reserve',
      'generateIdentifier': u'generate',      
      'listChecksumAlgorithms': u'checksum',
      'listNodes': u'node',
      # registerSystemMetadata(): CN internal
      'hasReservation': u'reserve/%(pid)s',
            
      # Read API
      # get(): Implemented in d1baseclient
      # getSystemMetadata(): Implemented in d1baseclient
      'resolve': u'resolve/%(pid)s',
      # assertRelation(): Deprecated      
      # listObjects(): implemented in d1baseclient
      'search': u'search',
      
      # Authorization API
      'setRightsHolder': u'owner/%(pid)s',
      'isAuthorized()': u'isAuthorized/%(pid)s?action=%(action)s',
      'setAccessPolicy': u'accessRules/%(pid)s',

      # Identity API
      'registerAccount': u'accounts',
      'updateAccount': u'accounts',
      'verifyAccount': u'accounts/%(subject)s',
      'getSubjectInfo': u'accounts/%(subject)s',
      'listSubjects': u'accounts?query=%(query)s', #[&status=(status)&start=(start)&count=(count)]
      'mapIdentity': u'accounts/map',
      'denyMapIdentity': u'accounts/map/%(subject)s',
      'requestMapIdentity': u'accounts/pendingmap/%(subject)s',
      'confirmMapIdentity': u'accounts/pendingmap/%(subject)s',
      'denyMapIdentity': u'accounts/pendingmap/%(subject)s',
      'createGroup': u'groups/%(groupName)s',
      'addGroupMembers': u'groups/%(groupName)s',
      'removeGroupMembers': u'groups/%(groupName)s',

      # Replication API
      'setReplicationStatus': u'replicaNotifications/%(pid)s',
      'updateReplicationMetadata': u'replicaMetadata/%(pid)s', 
      'setReplicationPolicy': u'replicaPolicies/%(pid)s',
      'isNodeAuthorized': u'replicaAuthorizations/%(pid)s',

      # Register API
      'updateNodeCapabilities': u'node/%(nodeId)s',
      'register': 'node',
    })
    self.last_response_body = None
    # Set this to True to preserve a copy of the last response.read() as the
    # body attribute of self.last_response_body
    self.capture_response_body = capture_response_body


  #=============================================================================
  # Core API
  #=============================================================================
  
  # CNCore.create(session, pid, object, sysmeta) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.create
  # CN INTERNAL

  # CNCore.listFormats() → ObjectFormatList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listFormats
  
  def listFormatsResponse(self):
    url = self._rest_url('listFormats')
    return self.GET(url)
    

  def listFormats(self):
    response = self.listFormatsResponse()
    return self._capture_and_deserialize(response)

  # CNCore.getFormat(formatId) → ObjectFormat
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getFormat
  
  @d1_common.util.str_to_unicode
  def getFormatResponse(self, formatId):
    url = self._rest_url('getFormat', formatId=formatId)
    return self.GET(url)
    

  @d1_common.util.str_to_unicode
  def getFormat(self, formatId):
    response = self.getFormatResponse(formatId)
    return self._capture_and_deserialize(response)

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # Implemented in d1baseclient.py

  # CNCore.reserveIdentifier(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.reserveIdentifier
  
  @d1_common.util.str_to_unicode
  def reserveIdentifierResponse(self, pid):
    url = self._rest_url('reserveIdentifier')
    mime_multipart_files = [
      ('pid', 'pid', pid.toxml().encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files)


  @d1_common.util.str_to_unicode
  def reserveIdentifier(self, pid):
    response = self.reserveIdentifierResponse(pid)
    return self._capture_and_deserialize(response)


  # CNCore.generateIdentifier(session, scheme[, fragment]) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.generateIdentifier
  
  @d1_common.util.str_to_unicode
  def generateIdentifierResponse(self, scheme, fragment=None):
    url = self._rest_url('generateIdentifier')
    mime_multipart_files = [
      ('scheme', 'scheme', scheme.encode('utf-8')),
      ('fragment', 'fragment', fragment.encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files)


  @d1_common.util.str_to_unicode
  def generateIdentifier(self, scheme, fragment=None):
    response = self.generateIdentifierResponse(scheme, fragment)
    return self._capture_and_deserialize(response)


  # CNCore.listChecksumAlgorithms() → ChecksumAlgorithmList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listChecksumAlgorithms
  
  @d1_common.util.str_to_unicode
  def listChecksumAlgorithmsResponse(self):
    url = self._rest_url('listChecksumAlgorithms')
    return self.GET(url)
    

  @d1_common.util.str_to_unicode
  def listChecksumAlgorithms(self):
    response = self.listChecksumAlgorithmsResponse()
    return self._capture_and_deserialize(response)

  # CNCore.listNodes() → NodeList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listNodes
    
  def listNodesResponse(self):
    url = self._rest_url('listNodes')
    response = self.GET(url)
    return response


  def listNodes(self):
    response = self.listNodesResponse()
    return self._capture_and_deserialize(response)

  
  # CNCore.registerSystemMetadata(session, pid, sysmeta) → Identifier
  # CN INTERNAL
  
  
  # CNCore.hasReservation(session, pid) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.hasReservation
  
  @d1_common.util.str_to_unicode
  def hasReservationResponse(self, pid):
    url = self._rest_url('hasReservation', pid=pid)
    return self.GET(url)
    

  @d1_common.util.str_to_unicode
  def hasReservation(self, pid):
    response = self.hasReservationResponse(pid)
    return self._capture_and_deserialize(response)

  #=============================================================================
  # Read API
  #=============================================================================


  # CNRead.get(session, pid) → OctetStream
  # Implemented in d1baseclient.py

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # Implemented in d1baseclient.py
  
  # CNRead.resolve(session, pid) → ObjectLocationList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.resolve
  
  @d1_common.util.str_to_unicode
  def resolveResponse(self, pid):
    url = self._rest_url('resolve', pid=pid)
    return self.GET(url)

  
  @d1_common.util.str_to_unicode
  def resolve(self, pid):
    response = self.resolveResponse(pid)
    return self._capture_and_deserialize(response)


  # CNRead.assertRelation(session, pidOfSubject, relationship, pidOfObject) → boolean
  # DEPRECATED FOR v1.0.0
  
  @d1_common.util.str_to_unicode
  def assertRelation(self, pidOfSubject, relationship, pidOfObject):
    raise Exception('Deprecated')



  # CNRead.search(session, queryType, query) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.search

  @d1_common.util.str_to_unicode
  def searchResponse(self, queryType, query):
    url = self._rest_url('search')
    url_params = {
      'query': query,
    }
    return self.GET(url, url_params=url_params)


  @d1_common.util.str_to_unicode
  def search(self, queryType, query):
    response = self.searchResponse(queryType, query)
    return self._capture_and_deserialize(response)

#  @d1_common.util.str_to_unicode
#  def search(self, query, fields="pid,origin_mn,datemodified,size,objectformat,title",
#             start=0, count=100):
#    '''This is a place holder for search against the SOLR search engine.     
#    '''
#    hostinfo = self._parseURL(self.baseurl)
#    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
#                                     persistent=True)
#    params = {'q':query,
#              'fl': fields,
#              'start':str(start),
#              'rows':str(count)}
#    sres = solr.search(params)
#    return sres['response']    
#    #response = self.searchResponse(query)
#    #return dataoneTypes.CreateFromDocument(response.read())

#  def getSearchFields(self):
#    #getFields
#    hostinfo = self._parseURL(self.baseurl)
#    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
#                                     persistent=True)
#    sres = solr.getFields()
#    return sres['fields']
  
#  def searchSolr(self, query):
#    '''Executes a search against SOLR. The literal query string is passed as
#    the q parameter to SOLR, so it must be properly escaped
#    '''
#    pass

  
  #=============================================================================
  # Authorization API
  #=============================================================================

  # CNAuthorization.setRightsHolder(session, pid, userId, serialVersion) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.setRightsHolder
  
  @d1_common.util.str_to_unicode
  def setRightsHolderResponse(self, pid, userId, serialVersion):
    url = self._rest_url('setRightsHolder', pid=pid)
    mime_multipart_fields = [
      ('userId', userId.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def setRightsHolder(self, pid, userId, serialVersion):
    response = self.setRightsHolderResponse(pid, userId, serialVersion)
    return self.capture_and_get_ok_status(response)

  # CNAuthorization.isAuthorized(session, pid, action) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.isAuthorized
  
  @d1_common.util.str_to_unicode
  def isAuthorizedResponse(self, pid, action):
    url = self._rest_url('isAuthorized', pid=pid, action=action)
    return self.GET(url)

  
  @d1_common.util.str_to_unicode
  def isAuthorized(self, pid, action):
    response = self.isAuthorizedResponse(pid, action)
    return self.capture_and_get_ok_status(response)

  # CNAuthorization.setAccessPolicy(session, pid, accessPolicy, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.setAccessPolicy
  
  @d1_common.util.str_to_unicode
  def setAccessPolicyResponse(self, pid, accessPolicy, serialVersion):
    url = self._rest_url('setAccessPolicy', pid=pid)
    mime_multipart_fields = [
      ('accessPolicy', accessPolicy.toxml().encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def setAccessPolicy(self, pid, accessPolicy, serialVersion):
    response = self.setAccessPolicyResponse(pid, accessPolicy, serialVersion)
    return self.capture_and_get_ok_status(response)

  #=============================================================================
  # Identity API 
  #=============================================================================

  # CNIdentity.registerAccount(session, person) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.registerAccount
  
  @d1_common.util.str_to_unicode
  def registerAccountResponse(self, person):
    url = self._rest_url('registerAccount')
    mime_multipart_fields = [
      ('person', person.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def registerAccount(self, person):
    response = self.registerAccountResponse(person)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.updateAccount(session, person) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.updateAccount
  
  @d1_common.util.str_to_unicode
  def updateAccountResponse(self, person):
    url = self._rest_url('updateAccount')
    mime_multipart_fields = [
      ('person', person.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def updateAccount(self, person):
    response = self.updateAccountResponse(person)
    return self.capture_and_get_ok_status(response)
  
  # CNIdentity.verifyAccount(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.verifyAccount
  
  @d1_common.util.str_to_unicode
  def verifyAccountResponse(self, subject):
    url = self._rest_url('verifyAccount')
    mime_multipart_fields = [
      ('subject', subject.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def verifyAccount(self, subject):
    response = self.verifyAccountResponse(subject)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.getSubjectInfo(session, subject) → SubjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.getSubjectInfo
  
  @d1_common.util.str_to_unicode
  def getSubjectInfoResponse(self, subject):
    url = self._rest_url('getSubjectInfo', subject=subject.value())
    return self.GET(url)


  @d1_common.util.str_to_unicode
  def getSubjectInfo(self, subject):
    response = self.getSubjectInfoResponse(subject)
    return self._capture_and_deserialize(response)

  # CNIdentity.listSubjects(session, query, status, start, count) → SubjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.listSubjects
  
  @d1_common.util.str_to_unicode
  def listSubjectsResponse(self, query, status=None, start=None, count=None):
    url = self._rest_url('listSubjects', query=query)

    url_params = {}
    if status is not None:
      url_params['status'] = status
    if start is not None:
      url_params['start'] = str(int(start))
    if count is not None:
      url_params['count'] = str(int(count))
    return self.GET(url, url_params=url_params)


  @d1_common.util.str_to_unicode
  def listSubjects(self, query, status=None, start=None, count=None):
    response = self.listSubjectsResponse(query, status, start, count)
    return self._capture_and_deserialize(response)
  
  # CNIdentity.mapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.mapIdentity
  
  @d1_common.util.str_to_unicode
  def mapIdentityResponse(self, subject):
    url = self._rest_url('mapIdentity')
    mime_multipart_fields = [
      ('subject', subject.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def mapIdentity(self, subject):
    response = self.mapIdentityResponse(subject)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.denyMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.denyMapIdentity
  
  @d1_common.util.str_to_unicode
  def denyMapIdentityResponse(self, subject):
    url = self._rest_url('denyMapIdentity', subject=subject.value())
    return self.DELETE(url)


  @d1_common.util.str_to_unicode
  def denyMapIdentity(self, subject):
    response = self.denyMapIdentityResponse(subject)
    return self._capture_and_deserialize(response)

  # CNIdentity.requestMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.requestMapIdentity
  
  @d1_common.util.str_to_unicode
  def requestMapIdentityResponse(self, subject):
    url = self._rest_url('requestMapIdentity', subject=subject.value())
    mime_multipart_fields = [
      ('subject', subject.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def requestMapIdentity(self, subject):
    response = self.requestMapIdentityResponse(subject)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.confirmMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.confirmMapIdentity
  
  @d1_common.util.str_to_unicode
  def confirmMapIdentityResponse(self, subject):
    url = self._rest_url('confirmMapIdentity', subject=subject.value())
    mime_multipart_fields = [
      ('subject', subject.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def confirmMapIdentity(self, subject):
    response = self.confirmMapIdentityResponse(subject)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.denyMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.denyMapIdentity
  
  @d1_common.util.str_to_unicode
  def denyMapIdentityResponse(self, subject):
    url = self._rest_url('denyMapIdentity', subject=subject.value())
    return self.DELETE(url)


  @d1_common.util.str_to_unicode
  def denyMapIdentity(self, subject):
    response = self.denyMapIdentityResponse(subject)
    return self._capture_and_deserialize(response)

  # CNIdentity.createGroup(session, groupName) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.createGroup
  
  @d1_common.util.str_to_unicode
  def createGroupResponse(self, groupName):
    url = self._rest_url('createGroup', groupName=groupName.value())
    mime_multipart_fields = [
      ('groupName', groupName.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def createGroup(self, groupName):
    response = self.createGroupResponse(groupName)
    return self.capture_and_get_ok_status(response)

  # CNIdentity.addGroupMembers(session, groupName, members) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.addGroupMembers
  
  @d1_common.util.str_to_unicode
  def addGroupMembersResponse(self, groupName, members):
    url = self._rest_url('addGroupMembers', groupName=groupName.value())
    mime_multipart_fields = [
      ('members', members.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def addGroupMembers(self, groupName, members):
    response = self.addGroupMembersResponse(groupName, members)
    return self.capture_and_get_ok_status(response)  

  # CNIdentity.removeGroupMembers(session, groupName, members) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.removeGroupMembers 
    
  @d1_common.util.str_to_unicode
  def removeGroupMembersResponse(self, groupName, members):
    url = self._rest_url('removeGroupMembers', groupName=groupName.value())
    mime_multipart_fields = [
      ('members', members.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def removeGroupMembers(self, groupName, members):
    response = self.removeGroupMembersResponse(groupName, members)
    return self.capture_and_get_ok_status(response)  

  #=============================================================================
  # Replication API
  #=============================================================================

  # CNReplication.setReplicationStatus(session, pid, nodeRef, status, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.setReplicationStatus
  
  @d1_common.util.str_to_unicode
  def setReplicationStatusResponse(self, pid, nodeRef, status, serialVersion):
    url = self._rest_url('setReplicationStatus', pid=pid)
    mime_multipart_fields = [
      ('nodeRef', nodeRef.encode('utf-8')),
      ('status', status.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def setReplicationStatus(self, pid, nodeRef, status, serialVersion):
    response = self.setReplicationStatusResponse(pid, nodeRef, status,
                                                 serialVersion)
    return self.capture_and_get_ok_status(response)

  # CNReplication.updateReplicationMetadata(session, pid, replicaMetadata, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.updateReplicationMetadata
  # Not implemented.
  
  # CNReplication.setReplicationPolicy(session, pid, policy, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.setReplicationPolicy
  
  @d1_common.util.str_to_unicode
  def setReplicationPolicyResponse(self, pid, policy, serialVersion):
    url = self._rest_url('setReplicationPolicy', pid=pid)
    mime_multipart_fields = [
      ('policy', policy.toxml().encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def setReplicationPolicy(self, pid, policy, serialVersion):
    response = self.setReplicationPolicyResponse(pid, policy, serialVersion)
    return self.capture_and_get_ok_status(response)
  
  # CNReplication.isNodeAuthorized(session, targetNodeSubject, pid, replicatePermission) → boolean()
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.isNodeAuthorized
  # TODO. Spec unclear.
  
  @d1_common.util.str_to_unicode
  def isNodeAuthorizedResponse(self, targetNodeSubject, pid,
                               replicatePermission):
    url = self._rest_url('isNodeAuthorized', pid=pid,
                               targetNodeSubject=targetNodeSubject.value())
    return self.GET(url)

  
  @d1_common.util.str_to_unicode
  def isNodeAuthorized(self, targetNodeSubject, pid, replicatePermission):
    response = self.isNodeAuthorizedResponse(targetNodeSubject, pid, replicatePermission)
    return self.capture_and_get_ok_status(response)
  

  #=============================================================================
  # Register API 
  #=============================================================================


  # CNRegister.updateNodeCapabilities(session, nodeId, node) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.updateNodeCapabilities
  
  @d1_common.util.str_to_unicode
  def updateNodeCapabilitiesResponse(self, nodeId, node):
    url = self._rest_url('updateNodeCapabilities', nodeId=nodeId)
    mime_multipart_fields = [
      ('node', node.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def updateNodeCapabilities(self, nodeId, node):
    response = self.updateNodeCapabilitiesResponse(nodeId, node)
    return self.capture_and_get_ok_status(response)
    
  # CNRegister.register(session, node) → NodeReference
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.register
  
  @d1_common.util.str_to_unicode
  def registerResponse(self, node):
    url = self._rest_url('register')
    mime_multipart_fields = [
      ('node', node.toxml().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.str_to_unicode
  def register(self, node):
    response = self.registerResponse(node)
    return self.capture_and_get_ok_status(response)

