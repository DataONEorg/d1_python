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

:Synopsis:
  This module implements CoordinatingNodeClient, which extends DataONEBaseClient
  with functionality specific to Coordinating Nodes.
:Created: 2011-01-22
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import urllib
import urlparse

# D1.
import d1_common.const
import d1_common.date_time
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.url
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
    url = self._rest_url('formats')
    return self.GET(url)


  def listFormats(self):
    response = self.listFormatsResponse()
    return self._read_dataone_type_response(response)

  # CNCore.getFormat(formatId) → ObjectFormat
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getFormat

  @d1_common.util.utf8_to_unicode
  def getFormatResponse(self, formatId):
    url = self._rest_url('formats/%(formatId)s', formatId=formatId)
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def getFormat(self, formatId):
    response = self.getFormatResponse(formatId)
    return self._read_dataone_type_response(response)

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # Implemented in d1baseclient.py

  # CNCore.reserveIdentifier(session, pid) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.reserveIdentifier

  @d1_common.util.utf8_to_unicode
  def reserveIdentifierResponse(self, pid):
    url = self._rest_url('reserve')
    mime_multipart_fields = [
      ('pid', pid.encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def reserveIdentifier(self, pid):
    response = self.reserveIdentifierResponse(pid)
    return self._read_dataone_type_response(response)


  # CNCore.generateIdentifier(session, scheme[, fragment]) → Identifier
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.generateIdentifier

  @d1_common.util.utf8_to_unicode
  def generateIdentifierResponse(self, scheme, fragment=None):
    url = self._rest_url('generate')
    mime_multipart_fields = [
      ('scheme', scheme.encode('utf-8')),
      ('fragment', fragment.encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def generateIdentifier(self, scheme, fragment=None):
    response = self.generateIdentifierResponse(scheme, fragment)
    return self._read_dataone_type_response(response)


  # CNCore.listChecksumAlgorithms() → ChecksumAlgorithmList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listChecksumAlgorithms

  @d1_common.util.utf8_to_unicode
  def listChecksumAlgorithmsResponse(self):
    url = self._rest_url('checksum')
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def listChecksumAlgorithms(self):
    response = self.listChecksumAlgorithmsResponse()
    return self._read_dataone_type_response(response)

  # CNCore.listNodes() → NodeList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listNodes

  def listNodesResponse(self):
    url = self._rest_url('node')
    response = self.GET(url)
    return response


  def listNodes(self):
    response = self.listNodesResponse()
    return self._read_dataone_type_response(response)


  # CNCore.registerSystemMetadata(session, pid, sysmeta) → Identifier
  # CN INTERNAL


  # CNCore.hasReservation(session, pid) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.hasReservation

  @d1_common.util.utf8_to_unicode
  def hasReservationResponse(self, pid):
    url = self._rest_url('reserve/%(pid)s', pid=pid)
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def hasReservation(self, pid):
    response = self.hasReservationResponse(pid)
    return self._read_dataone_type_response(response)

  #=============================================================================
  # Read API
  #=============================================================================


  # CNRead.get(session, pid) → OctetStream
  # Implemented in d1baseclient.py

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # Implemented in d1baseclient.py

  # CNRead.resolve(session, pid) → ObjectLocationList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.resolve

  @d1_common.util.utf8_to_unicode
  def resolveResponse(self, pid):
    url = self._rest_url('resolve/%(pid)s', pid=pid)
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def resolve(self, pid):
    response = self.resolveResponse(pid)
    return self._read_dataone_type_response(response,
      response_contains_303_redirect=True)


  # CNRead.getChecksum(session, pid) → Checksum
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.getChecksum

  @d1_common.util.utf8_to_unicode
  def getChecksumResponse(self, pid):
    url = self._rest_url('checksum/%(pid)s', pid=pid)
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def getChecksum(self, pid):
    response = self.getChecksumResponse(pid)
    return self._read_dataone_type_response(response)


  # CNRead.search(session, queryType, query) → ObjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.search

  @d1_common.util.utf8_to_unicode
  def searchResponse(self, queryType, query):
    url = self._rest_url('search')
    url_query = {
      'query': query,
    }
    return self.GET(url, query=url_query)


  @d1_common.util.utf8_to_unicode
  def search(self, queryType, query):
    response = self.searchResponse(queryType, query)
    return self._read_dataone_type_response(response)

#  @d1_common.util.utf8_to_unicode
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

  @d1_common.util.utf8_to_unicode
  def setRightsHolderResponse(self, pid, userId, serialVersion):
    url = self._rest_url('owner/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('userId', userId.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def setRightsHolder(self, pid, userId, serialVersion):
    response = self.setRightsHolderResponse(pid, userId, serialVersion)
    return self._read_boolean_response(response)

  # CNAuthorization.isAuthorized(session, pid, action) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.isAuthorized

  @d1_common.util.utf8_to_unicode
  def isAuthorizedResponse(self, pid, action):
    url = self._rest_url('isAuthorized/%(pid)s?action=%(action)s', pid=pid,
                         action=action)
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def isAuthorized(self, pid, action):
    response = self.isAuthorizedResponse(pid, action)
    return self._read_boolean_response(response)

  # CNAuthorization.setAccessPolicy(session, pid, accessPolicy, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.setAccessPolicy

  @d1_common.util.utf8_to_unicode
  def setAccessPolicyResponse(self, pid, accessPolicy, serialVersion):
    url = self._rest_url('accessRules/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('serialVersion', str(serialVersion)),
    ]
    mime_multipart_files = [
      ('accessPolicy', 'accessPolicy', accessPolicy.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields,
                    files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def setAccessPolicy(self, pid, accessPolicy, serialVersion):
    response = self.setAccessPolicyResponse(pid, accessPolicy, serialVersion)
    return self._read_boolean_response(response)

  #=============================================================================
  # Identity API 
  #=============================================================================

  # CNIdentity.registerAccount(session, person) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.registerAccount

  @d1_common.util.utf8_to_unicode
  def registerAccountResponse(self, person):
    url = self._rest_url('accounts')
    mime_multipart_files = [
      ('person', 'person', person.toxml().encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def registerAccount(self, person):
    response = self.registerAccountResponse(person)
    return self._read_boolean_response(response)

  # CNIdentity.updateAccount(session, person) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.updateAccount

  @d1_common.util.utf8_to_unicode
  def updateAccountResponse(self, person):
    url = self._rest_url('accounts/%(subject)s', subject=subject.value())
    mime_multipart_files = [
      ('person', 'person', person.toxml().encode('utf-8')),
    ]
    return self.PUT(url, files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def updateAccount(self, person):
    response = self.updateAccountResponse(person)
    return self._read_boolean_response(response)

  # CNIdentity.verifyAccount(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.verifyAccount

  @d1_common.util.utf8_to_unicode
  def verifyAccountResponse(self, subject):
    url = self._rest_url('accounts/verification/%(subject)s', subject=subject.value())
    return self.PUT(url)


  @d1_common.util.utf8_to_unicode
  def verifyAccount(self, subject):
    response = self.verifyAccountResponse(subject)
    return self._read_boolean_response(response)

  # CNIdentity.getSubjectInfo(session, subject) → SubjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.getSubjectInfo

  @d1_common.util.utf8_to_unicode
  def getSubjectInfoResponse(self, subject):
    url = self._rest_url('accounts/%(subject)s', subject=subject.value())
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def getSubjectInfo(self, subject):
    response = self.getSubjectInfoResponse(subject)
    return self._read_dataone_type_response(response)

  # CNIdentity.listSubjects(session, query, status, start, count) → SubjectList
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.listSubjects

  @d1_common.util.utf8_to_unicode
  def listSubjectsResponse(self, query, status=None, start=None, count=None):
    url = self._rest_url('accounts?query=%(query)s', query=query)
    url_query = {
      'status': status,
      'start': start,
      'count': count,
    }
    return self.GET(url, query=url_query)


  @d1_common.util.utf8_to_unicode
  def listSubjects(self, query, status=None, start=None, count=None):
    response = self.listSubjectsResponse(query, status, start, count)
    return self._read_dataone_type_response(response)

  # CNIdentity.mapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.mapIdentity

  @d1_common.util.utf8_to_unicode
  def mapIdentityResponse(self, primary_subject, secondary_subject):
    url = self._rest_url('accounts/map')
    mime_multipart_fields = [
      ('primarySubject', primary_subject.value().encode('utf-8')),
      ('secondarySubject', secondary_subject.value().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def mapIdentity(self, primary_subject, secondary_subject):
    response = self.mapIdentityResponse(primary_subject, secondary_subject)
    return self._read_boolean_response(response)

  # CNIdentity.denyMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.denyMapIdentity

  @d1_common.util.utf8_to_unicode
  def denyMapIdentityResponse(self, subject):
    url = self._rest_url('accounts/map/%(subject)s', subject=subject.value())
    return self.DELETE(url)


  @d1_common.util.utf8_to_unicode
  def denyMapIdentity(self, subject):
    response = self.denyMapIdentityResponse(subject)
    return self._read_dataone_type_response(response)

  # CNIdentity.requestMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.requestMapIdentity

  @d1_common.util.utf8_to_unicode
  def requestMapIdentityResponse(self, subject):
    url = self._rest_url('accounts')
    mime_multipart_fields = [
      ('subject', subject.value().encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def requestMapIdentity(self, subject):
    response = self.requestMapIdentityResponse(subject)
    return self._read_boolean_response(response)

  # CNIdentity.confirmMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.confirmMapIdentity

  @d1_common.util.utf8_to_unicode
  def confirmMapIdentityResponse(self, subject):
    url = self._rest_url('accounts/pendingmap/%(subject)s', subject=subject.value())
    mime_multipart_fields = [
      ('subject', subject.value().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def confirmMapIdentity(self, subject):
    response = self.confirmMapIdentityResponse(subject)
    return self._read_boolean_response(response)

  # CNIdentity.denyMapIdentity(session, subject) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.denyMapIdentity

  @d1_common.util.utf8_to_unicode
  def denyMapIdentityResponse(self, subject):
    url = self._rest_url('accounts/pendingmap/%(subject)s', subject=subject.value())
    return self.DELETE(url)


  @d1_common.util.utf8_to_unicode
  def denyMapIdentity(self, subject):
    response = self.denyMapIdentityResponse(subject)
    return self._read_dataone_type_response(response)

  # CNIdentity.createGroup(session, groupName) → Subject
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.createGroup

  @d1_common.util.utf8_to_unicode
  def createGroupResponse(self, group):
    url = self._rest_url('groups')
    mime_multipart_files = [
      ('group', groupName.toxml().encode('utf-8')),
    ]
    return self.POST(url, files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def createGroup(self, groupName):
    response = self.createGroupResponse(groupName)
    return self._read_boolean_response(response)

  # CNIdentity.addGroupMembers(session, groupName, members) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.addGroupMembers

  @d1_common.util.utf8_to_unicode
  def updateGroupResponse(self, group):
    url = self._rest_url('groups')
    mime_multipart_files = [
      ('group', 'group', group.toxml().encode('utf-8')),
    ]
    return self.PUT(url, files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def updateGroup(self, group):
    response = self.updateGroupResponse(group)
    return self._read_boolean_response(response)

  #=============================================================================
  # Replication API
  #=============================================================================

  # CNReplication.setReplicationStatus(session, pid, nodeRef, status, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.setReplicationStatus

  @d1_common.util.utf8_to_unicode
  def setReplicationStatusResponse(self, pid, nodeRef, status, failure=None):
    url = self._rest_url('replicaNotifications/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('nodeRef', nodeRef.encode('utf-8')),
      ('status', status.encode('utf-8')),
    ]
    mime_multipart_files = []
    if failure is not None:
      mime_multipart_files.append(('failure', 'failure',
                                   failure.toxml().encode('utf-8')))
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def setReplicationStatus(self, pid, nodeRef, status, failure=None):
    response = self.setReplicationStatusResponse(pid, nodeRef, status, failure)
    return self._read_boolean_response(response)

  # CNReplication.updateReplicationMetadata(session, pid, replicaMetadata, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.updateReplicationMetadata
  # Not implemented.

  @d1_common.util.utf8_to_unicode
  def updateReplicationMetadataResponse(self, pid, replicaMetadata,
                                        serialVersion):
    url = self._rest_url('replicaMetadata/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('serialVersion', str(serialVersion)),
    ]
    mime_multipart_files = [
      ('replicaMetadata', replicaMetadata.toxml().encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields,
                    files=mime_multipart_files)


  @d1_common.util.utf8_to_unicode
  def updateReplicationMetadata(self, pid, replicaMetadata, serialVersion):
    response = self.updateReplicationMetadataResponse(pid, replicaMetadata,
                                                      serialVersion)
    return self._read_boolean_response(response)


  # CNReplication.setReplicationPolicy(session, pid, policy, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.setReplicationPolicy

  @d1_common.util.utf8_to_unicode
  def setReplicationPolicyResponse(self, pid, policy, serialVersion):
    url = self._rest_url('replicaPolicies/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('policy', policy.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def setReplicationPolicy(self, pid, policy, serialVersion):
    response = self.setReplicationPolicyResponse(pid, policy, serialVersion)
    return self._read_boolean_response(response)

  # CNReplication.isNodeAuthorized(session, targetNodeSubject, pid, replicatePermission) → boolean()
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.isNodeAuthorized
  # TODO. Spec unclear.

  @d1_common.util.utf8_to_unicode
  def isNodeAuthorizedResponse(self, targetNodeSubject, pid,
                               replicatePermission):
    url = self._rest_url('replicaAuthorizations/%(pid)s', pid=pid,
                         targetNodeSubject=targetNodeSubject.value())
    return self.GET(url)


  @d1_common.util.utf8_to_unicode
  def isNodeAuthorized(self, targetNodeSubject, pid, replicatePermission):
    response = self.isNodeAuthorizedResponse(targetNodeSubject, pid, replicatePermission)
    return self._read_boolean_response(response)


  # CNReplication.deleteReplicationMetadata(session, pid, policy, serialVersion) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.deleteReplicationMetadata

  @d1_common.util.utf8_to_unicode
  def deleteReplicationMetadataResponse(self, pid, nodeId, serialVersion):
    url = self._rest_url('removeReplicaMetadata/%(pid)s', pid=pid)
    mime_multipart_fields = [
      ('nodeId', nodeId.encode('utf-8')),
      ('serialVersion', str(serialVersion)),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def deleteReplicationMetadata(self, pid, nodeId, serialVersion):
    response = self.deleteReplicationMetadataResponse(pid, nodeId,
                                                      serialVersion)
    return self._read_boolean_response(response)

  #=============================================================================
  # Register API 
  #=============================================================================


  # CNRegister.updateNodeCapabilities(session, nodeId, node) → boolean
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.updateNodeCapabilities

  @d1_common.util.utf8_to_unicode
  def updateNodeCapabilitiesResponse(self, nodeId, node):
    url = self._rest_url('node/%(nodeId)s', nodeId=nodeId)
    mime_multipart_fields = [
      ('node', node.encode('utf-8')),
    ]
    return self.PUT(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def updateNodeCapabilities(self, nodeId, node):
    response = self.updateNodeCapabilitiesResponse(nodeId, node)
    return self._read_boolean_response(response)

  # CNRegister.register(session, node) → NodeReference
  # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.register

  @d1_common.util.utf8_to_unicode
  def registerResponse(self, node):
    url = self._rest_url('node')
    mime_multipart_fields = [
      ('node', node.encode('utf-8')),
    ]
    return self.POST(url, fields=mime_multipart_fields)


  @d1_common.util.utf8_to_unicode
  def register(self, node):
    response = self.registerResponse(node)
    return self._read_boolean_response(response)

