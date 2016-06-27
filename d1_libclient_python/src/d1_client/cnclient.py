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
'''Module d1_client.cnclient
============================

:Synopsis:
  This module implements CoordinatingNodeClient, which extends DataONEBaseClient
  with functionality specific to Coordinating Nodes.

  See the `Coordinating Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html>`_
  for details on how to use the methods in this class.
:Created: 2011-01-22
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import logging
import sys

# D1.
try:
  import d1_common.const
  import d1_common.types.dataoneTypes_v2_0 as dataoneTypes
  import d1_common.util
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import d1baseclient


class CoordinatingNodeClient(d1baseclient.DataONEBaseClient):
  '''Connect to a Coordinating Node and perform REST calls against the CN API.


    #=========================================================================
    # Core API
    #=========================================================================

    # CNCore.ping() → null
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.ping
    # Implemented in d1baseclient.py

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
        return self._read_dataone_type_response(
            response, 1, 0, 'ObjectFormatList')

    # CNCore.getFormat(formatId) → ObjectFormat
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getFormat

    @d1_common.util.utf8_to_unicode
    def getFormatResponse(self, formatId):
        url = self._rest_url('formats/%(formatId)s', formatId=formatId)
        return self.GET(url)

    @d1_common.util.utf8_to_unicode
    def getFormat(self, formatId):
        response = self.getFormatResponse(formatId)
        return self._read_dataone_type_response(response, 1, 0, 'ObjectFormat')

    # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.getLogRecords
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
        return self._read_dataone_type_response(response, 1, 0, 'Identifier')

    # CNCore.listChecksumAlgorithms() → ChecksumAlgorithmList
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listChecksumAlgorithms

    @d1_common.util.utf8_to_unicode
    def listChecksumAlgorithmsResponse(self):
        url = self._rest_url('checksum')
        return self.GET(url)

    @d1_common.util.utf8_to_unicode
    def listChecksumAlgorithms(self):
        response = self.listChecksumAlgorithmsResponse()
        return self._read_dataone_type_response(
            response, 1, 0, 'ChecksumAlgorithmList')

    # CNCore.setObsoletedBy(session, pid, obsoletedByPid, serialVersion) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.setObsoletedBy

    @d1_common.util.utf8_to_unicode
    def setObsoletedByResponse(self, pid, obsoletedByPid, serialVersion):
        url = self._rest_url('/obsoletedBy/%(pid)s', pid=pid)
        mime_multipart_fields = [
            ('obsoletedByPid', obsoletedByPid.encode('utf-8')),
            ('serialVersion', str(serialVersion)),
        ]
        return self.PUT(url, fields=mime_multipart_fields)

    @d1_common.util.utf8_to_unicode
    def setObsoletedBy(self, pid, obsoletedByPid, serialVersion):
        response = self.setObsoletedByResponse(
            pid,
            obsoletedByPid,
            serialVersion)
        return self._read_boolean_response(response)

    # CNCore.listNodes() → NodeList
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.listNodes

    def listNodesResponse(self):
        url = self._rest_url('node')
        response = self.GET(url)
        return response

    def listNodes(self):
        response = self.listNodesResponse()
        return self._read_dataone_type_response(response, 1, 0, 'NodeList')

    # CNCore.registerSystemMetadata(session, pid, sysmeta) → Identifier
    # CN INTERNAL

    # CNCore.hasReservation(session, pid) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNCore.hasReservation

    @d1_common.util.utf8_to_unicode
    def hasReservationResponse(self, pid, subject):
        url = self._rest_url('reserve/%(pid)s?subject=%(subject)s', pid=pid,
                             subject=subject)
        return self.GET(url)

    @d1_common.util.utf8_to_unicode
    def hasReservation(self, pid, subject):
        response = self.hasReservationResponse(pid, subject)
        return self._read_boolean_404_response(response)

    #=========================================================================
    # Read API
    #=========================================================================

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
        return self._read_dataone_type_response(response, 1, 0, 'ObjectLocationList',
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
        return self._read_dataone_type_response(response, 1, 0, 'Checksum')

    # CNRead.search(session, queryType, query) → ObjectList
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.search

    #@d1_common.util.utf8_to_unicode
    def searchResponse(self, queryType, query=None, **kwargs):

        # url = self._rest_url('/solr/d1-cn-index/select/',
        # queryType=queryType,
        url = self._rest_url('search/%(queryType)s/%(query)s', queryType=queryType,
                             query=query if query is not None else '')
        return self.GET(url, query=kwargs)

    #@d1_common.util.utf8_to_unicode
    def search(self, queryType, query=None, **kwargs):
        response = self.searchResponse(queryType, query, **kwargs)
        return self._read_dataone_type_response(response, 1, 0, 'ObjectList')

    # CNRead.query(session, queryEngine, query) → OctetStream
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.query

    #@d1_common.util.utf8_to_unicode
    def queryResponse(self, queryEngine, query=None, **kwargs):
        url = self._rest_url('query/%(queryEngine)s/%(query)s', queryEngine=queryEngine,
                             query=query if query is not None else '')
        return self.GET(url, query=kwargs)

    #@d1_common.util.utf8_to_unicode
    def query(self, queryEngine, query=None, **kwargs):
        response = self.queryResponse(queryEngine, query, **kwargs)
        return self._read_stream_response(response)

    # CNRead.getQueryEngineDescription(session, queryEngine) → QueryEngineDescription
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRead.getQueryEngineDescription

    #@d1_common.util.utf8_to_unicode
    def getQueryEngineDescriptionResponse(self, queryEngine, **kwargs):
        url = self._rest_url('query/%(queryEngine)s', queryEngine=queryEngine)
        return self.GET(url, query=kwargs)

    #@d1_common.util.utf8_to_unicode
    def getQueryEngineDescription(self, queryEngine, **kwargs):
        response = self.getQueryEngineDescriptionResponse(
            queryEngine,
            **kwargs)
        return self._read_dataone_type_response(
            response, 1, 0, 'QueryEngineDescription')

    #=========================================================================
    # Authorization API
    #=========================================================================

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
        return self._read_boolean_401_response(response)

    # CNAuthorization.setAccessPolicy(session, pid, accessPolicy, serialVersion) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNAuthorization.setAccessPolicy

    @d1_common.util.utf8_to_unicode
    def setAccessPolicyResponse(self, pid, accessPolicy, serialVersion):
        url = self._rest_url('accessRules/%(pid)s', pid=pid)
        mime_multipart_fields = [
            ('serialVersion', str(serialVersion)),
        ]
        mime_multipart_files = [
            ('accessPolicy',
             'accessPolicy.xml',
             accessPolicy.toxml().encode('utf-8')),
        ]
        return self.PUT(url, fields=mime_multipart_fields,
                        files=mime_multipart_files)

    @d1_common.util.utf8_to_unicode
    def setAccessPolicy(self, pid, accessPolicy, serialVersion):
        response = self.setAccessPolicyResponse(
            pid,
            accessPolicy,
            serialVersion)
        return self._read_boolean_response(response)

    #=========================================================================
    # Identity API
    #=========================================================================

    # CNIdentity.registerAccount(session, person) → Subject
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.registerAccount

    @d1_common.util.utf8_to_unicode
    def registerAccountResponse(self, person):
        url = self._rest_url('accounts')
        mime_multipart_files = [
            ('person', 'person.xml', person.toxml().encode('utf-8')),
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
        url = self._rest_url('accounts/%(subject)s', subject=person.value())
        mime_multipart_files = [
            ('person', 'person.xml', person.toxml().encode('utf-8')),
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
        url = self._rest_url(
            'accounts/verification/%(subject)s',
            subject=subject.value())
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
        return self._read_dataone_type_response(response, 1, 0, 'SubjectInfo')

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
        return self._read_dataone_type_response(response, 1, 0, 'SubjectInfo')

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

    # CNIdentity.removeMapIdentity(session, subject) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.removeMapIdentity

    @d1_common.util.utf8_to_unicode
    def removeMapIdentityResponse(self, subject):
        url = self._rest_url(
            'accounts/map/%(subject)s',
            subject=subject.value())
        return self.DELETE(url)

    @d1_common.util.utf8_to_unicode
    def removeMapIdentity(self, subject):
        response = self.removeMapIdentityResponse(subject)
        return self._read_boolean_response(response)

    # CNIdentity.denyMapIdentity(session, subject) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.denyMapIdentity

    @d1_common.util.utf8_to_unicode
    def denyMapIdentityResponse(self, subject):
        url = self._rest_url(
            'accounts/pendingmap/%(subject)s',
            subject=subject.value())
        return self.DELETE(url)

    @d1_common.util.utf8_to_unicode
    def denyMapIdentity(self, subject):
        response = self.denyMapIdentityResponse(subject)
        return self._read_boolean_response(response)

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
        url = self._rest_url(
            'accounts/pendingmap/%(subject)s',
            subject=subject.value())
        mime_multipart_fields = [
            ('subject', subject.value().encode('utf-8')),
        ]
        return self.PUT(url, fields=mime_multipart_fields)

    @d1_common.util.utf8_to_unicode
    def confirmMapIdentity(self, subject):
        response = self.confirmMapIdentityResponse(subject)
        return self._read_boolean_response(response)

    # CNIdentity.createGroup(session, groupName) → Subject
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNIdentity.createGroup

    @d1_common.util.utf8_to_unicode
    def createGroupResponse(self, group):
        url = self._rest_url('groups')
        mime_multipart_files = [
            ('group', 'group.xml', group.toxml().encode('utf-8')),
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
            ('group', 'group.xml', group.toxml().encode('utf-8')),
        ]
        return self.PUT(url, files=mime_multipart_files)

    @d1_common.util.utf8_to_unicode
    def updateGroup(self, group):
        response = self.updateGroupResponse(group)
        return self._read_boolean_response(response)

    #=========================================================================
    # Replication API
    #=========================================================================

    # CNReplication.setReplicationStatus(session, pid, nodeRef, status, failure) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.setReplicationStatus

    @d1_common.util.utf8_to_unicode
    def setReplicationStatusResponse(self, pid, nodeRef, status, failure=None):
        url = self._rest_url('replicaNotifications/%(pid)s', pid=pid)
        mime_multipart_fields = [
            ('nodeRef', nodeRef.encode('utf-8')),
            ('status', status.encode('utf-8')),
        ]
#    mime_multipart_files = [
#      ('failure', 'failure.xml', failure.serialize().encode('utf-8') if failure
#       else '')
#    ]
        return self.PUT(url, fields=mime_multipart_fields, dump_path=None  # 'out.dump'
                        )  # files=mime_multipart_files

    @d1_common.util.utf8_to_unicode
    def setReplicationStatus(self, pid, nodeRef, status, failure=None):
        response = self.setReplicationStatusResponse(
            pid,
            nodeRef,
            status,
            failure)
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
            ('replicaMetadata',
             'replicaMetadata.xml',
             replicaMetadata.toxml().encode('utf-8')),
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
        mime_multipart_files = [
            ('policy', 'policy.xml', policy.toxml().encode('utf-8')),
        ]
        mime_multipart_fields = [
            ('serialVersion', str(serialVersion)),
        ]
        return self.PUT(
            url, fields=mime_multipart_fields, files=mime_multipart_files)

    @d1_common.util.utf8_to_unicode
    def setReplicationPolicy(self, pid, policy, serialVersion):
        response = self.setReplicationPolicyResponse(pid=pid, policy=policy,
                                                     serialVersion=serialVersion)
        return self._read_boolean_response(response)

    # CNReplication.isNodeAuthorized(session, targetNodeSubject, pid, replicatePermission) → boolean()
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNReplication.isNodeAuthorized
    # TODO. Spec unclear.

    @d1_common.util.utf8_to_unicode
    def isNodeAuthorizedResponse(self, targetNodeSubject, pid):
        url = self._rest_url(
            'replicaAuthorizations/%(pid)s?targetNodeSubject=%(targetNodeSubject)s',
            pid=pid, targetNodeSubject=targetNodeSubject)
        return self.GET(url)

    @d1_common.util.utf8_to_unicode
    def isNodeAuthorized(self, targetNodeSubject, pid):
        response = self.isNodeAuthorizedResponse(targetNodeSubject, pid)
        return self._read_boolean_401_response(response)

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

    #=========================================================================
    # Register API
    #=========================================================================

    # CNRegister.updateNodeCapabilities(session, nodeId, node) → boolean
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.updateNodeCapabilities

    @d1_common.util.utf8_to_unicode
    def updateNodeCapabilitiesResponse(self, nodeId, node):
        url = self._rest_url('node/%(nodeId)s', nodeId=nodeId)
        mime_multipart_files = [
            ('node', 'node.xml', node.toxml().encode('utf-8')),
        ]
        return self.PUT(url, files=mime_multipart_files)

    @d1_common.util.utf8_to_unicode
    def updateNodeCapabilities(self, nodeId, node):
        response = self.updateNodeCapabilitiesResponse(nodeId, node)
        return self._read_boolean_response(response)

    # CNRegister.register(session, node) → NodeReference
    # http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html#CNRegister.register

    @d1_common.util.utf8_to_unicode
    def registerResponse(self, node):
        url = self._rest_url('node')
        mime_multipart_files = [
            ('node', 'node.xml', node.toxml().encode('utf-8')),
        ]
        return self.POST(url, files=mime_multipart_files)

    @d1_common.util.utf8_to_unicode
    def register(self, node):
        response = self.registerResponse(node)
        return self._read_boolean_response(response)
  See the `Coordinating Node APIs <http://mule1.dataone.org/ArchitectureDocs-current/apis/CN_APIs.html>`_
  for details on how to use the methods in this class.
  '''

  def __init__(self, *args, **kwargs):
    """See d1baseclient.DataONEBaseClient for args."""
    self.logger = logging.getLogger(__file__)
    kwargs.setdefault('api_major', 1)
    kwargs.setdefault('api_minor', 0)
    d1baseclient.DataONEBaseClient.__init__(self, *args, **kwargs)

