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

import logging

import d1_common.const
import d1_common.type_conversions
import d1_common.util

import d1_client.baseclient


class CoordinatingNodeClient(
    d1_client.baseclient.DataONEBaseClient,
):
  """Extend DataONEBaseClient by adding REST API wrappers for APIs that are available on
  Coordinating Nodes.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See d1_client.baseclient.DataONEBaseClient for args."""
    super().__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 1
    self._api_minor = 0
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  #=========================================================================
  # Core API
  #=========================================================================

  # CNCore.ping() → null
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.ping
  # Implemented in d1_client.baseclient.py

  # CNCore.create(session, pid, object, sysmeta) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.create
  # CN INTERNAL

  # CNCore.listFormats() → ObjectFormatList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.listFormats

  def listFormatsResponse(self, vendorSpecific=None):
    return self.GET('formats', headers=vendorSpecific)

  def listFormats(self, vendorSpecific=None):
    response = self.listFormatsResponse(vendorSpecific)
    return self._read_dataone_type_response(response, 'ObjectFormatList')

  # CNCore.getFormat(formatId) → ObjectFormat
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getFormat

  def getFormatResponse(self, formatId, vendorSpecific=None):
    return self.GET(['formats', formatId], headers=vendorSpecific)

  def getFormat(self, formatId, vendorSpecific=None):
    response = self.getFormatResponse(formatId, vendorSpecific)
    return self._read_dataone_type_response(response, 'ObjectFormat')

  # CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][, count]) → Log
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords
  # Implemented in d1_client.baseclient.py

  # CNCore.reserveIdentifier(session, pid) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.reserveIdentifier

  def reserveIdentifierResponse(self, pid, vendorSpecific=None):
    mmp_dict = {
      'pid': pid,
    }
    return self.POST(['reserve', pid], fields=mmp_dict, headers=vendorSpecific)

  def reserveIdentifier(self, pid, vendorSpecific=None):
    response = self.reserveIdentifierResponse(pid, vendorSpecific)
    return self._read_dataone_type_response(
      response, 'Identifier', vendorSpecific
    )

  # CNCore.listChecksumAlgorithms() → ChecksumAlgorithmList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.listChecksumAlgorithms

  def listChecksumAlgorithmsResponse(self, vendorSpecific=None):
    return self.GET('checksum', headers=vendorSpecific)

  def listChecksumAlgorithms(self, vendorSpecific=None):
    response = self.listChecksumAlgorithmsResponse(vendorSpecific)
    return self._read_dataone_type_response(response, 'ChecksumAlgorithmList')

  # CNCore.setObsoletedBy(session, pid, obsoletedByPid, serialVersion) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.setObsoletedBy

  def setObsoletedByResponse(
      self, pid, obsoletedByPid, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'obsoletedByPid': obsoletedByPid,
      'serialVersion': str(serialVersion),
    }
    return self.PUT(['obsoletedBy', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def setObsoletedBy(
      self, pid, obsoletedByPid, serialVersion, vendorSpecific=None
  ):
    response = self.setObsoletedByResponse(
      pid, obsoletedByPid, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNCore.listNodes() → NodeList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.listNodes

  def listNodesResponse(self, vendorSpecific=None):
    return self.GET('node', headers=vendorSpecific)

  def listNodes(self, vendorSpecific=None):
    response = self.listNodesResponse(vendorSpecific)
    return self._read_dataone_type_response(response, 'NodeList')

  # CNCore.registerSystemMetadata(session, pid, sysmeta) → Identifier
  # CN INTERNAL

  # CNCore.hasReservation(session, pid) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.hasReservation

  def hasReservationResponse(self, pid, subject, vendorSpecific=None):
    return self.GET(['reserve', pid, subject], headers=vendorSpecific)

  def hasReservation(self, pid, subject, vendorSpecific=None):
    response = self.hasReservationResponse(pid, subject, vendorSpecific)
    return self._read_boolean_404_response(response)

  #=========================================================================
  # Read API
  #=========================================================================

  # CNRead.get(session, pid) → OctetStream
  # Implemented in d1_client.baseclient.py

  # CNRead.getSystemMetadata(session, pid) → SystemMetadata
  # Implemented in d1_client.baseclient.py

  # CNRead.resolve(session, pid) → ObjectLocationList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.resolve

  def resolveResponse(self, pid, vendorSpecific=None):
    return self.GET(['resolve', pid], headers=vendorSpecific)

  def resolve(self, pid, vendorSpecific=None):
    response = self.resolveResponse(pid, vendorSpecific)
    return self._read_dataone_type_response(
      response, 'ObjectLocationList', response_is_303_redirect=True
    )

  # CNRead.getChecksum(session, pid) → Checksum
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.getChecksum

  def getChecksumResponse(self, pid, vendorSpecific=None):
    return self.GET(['checksum', pid], headers=vendorSpecific)

  def getChecksum(self, pid, vendorSpecific=None):
    response = self.getChecksumResponse(pid, vendorSpecific)
    return self._read_dataone_type_response(response, 'Checksum')

  # CNRead.search(session, queryType, query) → ObjectList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.search

  def searchResponse(self, queryType, query, vendorSpecific=None, **kwargs):
    return self.GET(['search', queryType, query], headers=vendorSpecific,
                    query=kwargs)

  def search(self, queryType, query=None, vendorSpecific=None, **kwargs):
    response = self.searchResponse(queryType, query, vendorSpecific, **kwargs)
    return self._read_dataone_type_response(response, 'ObjectList')

  # CNRead.query(session, queryEngine, query) → OctetStream
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.query

  def queryResponse(
      self, queryEngine, query=None, vendorSpecific=None, **kwargs
  ):
    return self.GET(['query', queryEngine, query], headers=vendorSpecific,
                    query=kwargs)

  def query(self, queryEngine, query=None, vendorSpecific=None, **kwargs):
    response = self.queryResponse(queryEngine, query, vendorSpecific, **kwargs)
    return self._read_stream_response(response)

  # CNRead.getQueryEngineDescription(session, queryEngine) → QueryEngineDescription
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.getQueryEngineDescription

  def getQueryEngineDescriptionResponse(
      self, queryEngine, vendorSpecific=None, **kwargs
  ):
    return self.GET(['query', queryEngine], headers=vendorSpecific,
                    query=kwargs)

  def getQueryEngineDescription(
      self, queryEngine, vendorSpecific=None, **kwargs
  ):
    response = self.getQueryEngineDescriptionResponse(
      queryEngine, vendorSpecific, **kwargs
    )
    return self._read_dataone_type_response(response, 'QueryEngineDescription')

  #=========================================================================
  # Authorization API
  #=========================================================================

  # CNAuthorization.setRightsHolder(session, pid, userId, serialVersion) → Identifier
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNAuthorization.setRightsHolder

  def setRightsHolderResponse(
      self, pid, userId, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'userId': userId,
      'serialVersion': str(serialVersion),
    }
    return self.PUT(['owner', pid], headers=vendorSpecific, fields=mmp_dict)

  def setRightsHolder(self, pid, userId, serialVersion, vendorSpecific=None):
    response = self.setRightsHolderResponse(
      pid, userId, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNAuthorization.setAccessPolicy(session, pid, accessPolicy, serialVersion) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNAuthorization.setAccessPolicy

  def setAccessPolicyResponse(
      self, pid, accessPolicy, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'serialVersion': str(serialVersion),
      'accessPolicy': ('accessPolicy.xml', accessPolicy.toxml('utf-8')),
    }
    return self.PUT(['accessRules', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def setAccessPolicy(
      self, pid, accessPolicy, serialVersion, vendorSpecific=None
  ):
    response = self.setAccessPolicyResponse(
      pid, accessPolicy, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  #=========================================================================
  # Identity API
  #=========================================================================

  # CNIdentity.registerAccount(session, person) → Subject
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.registerAccount

  def registerAccountResponse(self, person, vendorSpecific=None):
    mmp_dict = {
      'person': ('person.xml', person.toxml('utf-8')),
    }
    return self.POST('accounts', fields=mmp_dict, headers=vendorSpecific)

  def registerAccount(self, person, vendorSpecific=None):
    response = self.registerAccountResponse(person, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.updateAccount(session, person) → Subject
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.updateAccount

  def updateAccountResponse(self, subject, person, vendorSpecific=None):
    mmp_dict = {
      'person': ('person.xml', person.toxml('utf-8')),
    }
    return self.PUT(['accounts', subject], fields=mmp_dict,
                    headers=vendorSpecific)

  def updateAccount(self, subject, person, vendorSpecific=None):
    response = self.updateAccountResponse(subject, person, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.verifyAccount(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.verifyAccount

  def verifyAccountResponse(self, subject, vendorSpecific=None):
    return self.PUT(['accounts', subject], headers=vendorSpecific)

  def verifyAccount(self, subject, vendorSpecific=None):
    response = self.verifyAccountResponse(subject, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.getSubjectInfo(session, subject) → SubjectList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.getSubjectInfo

  def getSubjectInfoResponse(self, subject, vendorSpecific=None):
    return self.GET(['accounts', subject], headers=vendorSpecific)

  def getSubjectInfo(self, subject, vendorSpecific=None):
    response = self.getSubjectInfoResponse(subject, vendorSpecific)
    return self._read_dataone_type_response(response, 'SubjectInfo')

  # CNIdentity.listSubjects(session, query, status, start, count) → SubjectList
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.listSubjects

  def listSubjectsResponse(
      self, query, status=None, start=None, count=None, vendorSpecific=None
  ):
    url_query = {
      'status': status,
      'start': start,
      'count': count,
      'query': query
    }
    return self.GET('accounts', query=url_query, headers=vendorSpecific)

  def listSubjects(
      self, query, status=None, start=None, count=None, vendorSpecific=None
  ):
    response = self.listSubjectsResponse(
      query, status, start, count, vendorSpecific
    )
    return self._read_dataone_type_response(response, 'SubjectInfo')

  # CNIdentity.mapIdentity(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.mapIdentity

  def mapIdentityResponse(
      self, primarySubject, secondarySubject, vendorSpecific=None
  ):
    mmp_dict = {
      'primarySubject': primarySubject.toxml('utf-8'),
      'secondarySubject': secondarySubject.toxml('utf-8'),
    }
    return self.POST(['accounts', 'map'], fields=mmp_dict,
                     headers=vendorSpecific)

  def mapIdentity(self, primarySubject, secondarySubject, vendorSpecific=None):
    response = self.mapIdentityResponse(
      primarySubject, secondarySubject, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNIdentity.removeMapIdentity(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.removeMapIdentity

  def removeMapIdentityResponse(self, subject, vendorSpecific=None):
    return self.DELETE(['accounts', 'map', subject], headers=vendorSpecific)

  def removeMapIdentity(self, subject, vendorSpecific=None):
    response = self.removeMapIdentityResponse(subject, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.denyMapIdentity(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.denyMapIdentity

  def denyMapIdentityResponse(self, subject, vendorSpecific=None):
    return self.DELETE(['accounts', 'pendingmap', subject],
                       headers=vendorSpecific)

  def denyMapIdentity(self, subject, vendorSpecific=None):
    response = self.denyMapIdentityResponse(subject, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.requestMapIdentity(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.requestMapIdentity

  def requestMapIdentityResponse(self, subject, vendorSpecific=None):
    mmp_dict = {
      'subject': subject.toxml('utf-8'),
    }
    return self.POST('accounts', fields=mmp_dict, headers=vendorSpecific)

  def requestMapIdentity(self, subject, vendorSpecific=None):
    response = self.requestMapIdentityResponse(subject, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.confirmMapIdentity(session, subject) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.confirmMapIdentity

  def confirmMapIdentityResponse(self, subject, vendorSpecific=None):
    return self.PUT(['accounts', 'pendingmap', subject], headers=vendorSpecific)

  def confirmMapIdentity(self, subject, vendorSpecific=None):
    response = self.confirmMapIdentityResponse(subject, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.createGroup(session, groupName) → Subject
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.createGroup

  def createGroupResponse(self, group, vendorSpecific=None):
    mmp_dict = {
      'group': ('group.xml', group.toxml('utf-8')),
    }
    return self.POST('groups', fields=mmp_dict, headers=vendorSpecific)

  def createGroup(self, group, vendorSpecific=None):
    response = self.createGroupResponse(group, vendorSpecific)
    return self._read_boolean_response(response)

  # CNIdentity.addGroupMembers(session, groupName, members) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.addGroupMembers

  def updateGroupResponse(self, group, vendorSpecific=None):
    mmp_dict = {
      'group': ('group.xml', group.toxml('utf-8')),
    }
    return self.PUT('groups', fields=mmp_dict, headers=vendorSpecific)

  def updateGroup(self, group, vendorSpecific=None):
    response = self.updateGroupResponse(group, vendorSpecific)
    return self._read_boolean_response(response)

  #=========================================================================
  # Replication API
  #=========================================================================

  # CNReplication.setReplicationStatus(session, pid, nodeRef, status, failure) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNReplication.setReplicationStatus

  def setReplicationStatusResponse(
      self, pid, nodeRef, status, dataoneError=None, vendorSpecific=None
  ):
    mmp_dict = {
      'nodeRef': nodeRef, # .toxml('utf-8'),
      'status': status,
    }
    if dataoneError is not None:
      mmp_dict['failure'] = (
        'failure.xml', dataoneError.serialize_to_transport()
      )
    return self.PUT(['replicaNotifications', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def setReplicationStatus(
      self, pid, nodeRef, status, dataoneError=None, vendorSpecific=None
  ):
    response = self.setReplicationStatusResponse(
      pid, nodeRef, status, dataoneError, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNReplication.updateReplicationMetadata(session, pid, replicaMetadata, serialVersion) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNReplication.updateReplicationMetadata
  # Not implemented.

  def updateReplicationMetadataResponse(
      self, pid, replicaMetadata, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'replicaMetadata':
        ('replicaMetadata.xml', replicaMetadata.toxml('utf-8')),
      'serialVersion':
        str(serialVersion),
    }
    return self.PUT(['replicaMetadata', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def updateReplicationMetadata(
      self, pid, replicaMetadata, serialVersion, vendorSpecific=None
  ):
    response = self.updateReplicationMetadataResponse(
      pid, replicaMetadata, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNReplication.setReplicationPolicy(session, pid, policy, serialVersion) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNReplication.setReplicationPolicy

  def setReplicationPolicyResponse(
      self, pid, policy, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'policy': ('policy.xml', policy.toxml('utf-8')),
      'serialVersion': (str(serialVersion)),
    }
    return self.PUT(['replicaPolicies', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def setReplicationPolicy(
      self, pid, policy, serialVersion, vendorSpecific=None
  ):
    response = self.setReplicationPolicyResponse(
      pid, policy, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  # CNReplication.isNodeAuthorized(session, targetNodeSubject, pid, replicatePermission) → boolean()
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNReplication.isNodeAuthorized
  # TODO. Spec unclear.

  def isNodeAuthorizedResponse(
      self, targetNodeSubject, pid, vendorSpecific=None
  ):
    query_dict = {
      'targetNodeSubject': targetNodeSubject,
    }
    return self.GET(['replicaAuthorizations', pid], query=query_dict,
                    headers=vendorSpecific)

  def isNodeAuthorized(self, targetNodeSubject, pid, vendorSpecific=None):
    response = self.isNodeAuthorizedResponse(
      targetNodeSubject, pid, vendorSpecific
    )
    return self._read_boolean_401_response(response)

  # CNReplication.deleteReplicationMetadata(session, pid, policy, serialVersion) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNReplication.deleteReplicationMetadata

  def deleteReplicationMetadataResponse(
      self, pid, nodeId, serialVersion, vendorSpecific=None
  ):
    mmp_dict = {
      'nodeId': nodeId,
      'serialVersion': str(serialVersion),
    }
    return self.PUT(['removeReplicaMetadata', pid], fields=mmp_dict,
                    headers=vendorSpecific)

  def deleteReplicationMetadata(
      self, pid, nodeId, serialVersion, vendorSpecific=None
  ):
    response = self.deleteReplicationMetadataResponse(
      pid, nodeId, serialVersion, vendorSpecific
    )
    return self._read_boolean_response(response)

  #=========================================================================
  # Register API
  #=========================================================================

  # CNRegister.updateNodeCapabilities(session, nodeId, node) → boolean
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRegister.updateNodeCapabilities

  def updateNodeCapabilitiesResponse(self, nodeId, node, vendorSpecific=None):
    mmp_dict = {'node': ('node.xml', node.toxml('utf-8'))}
    return self.PUT(['node', nodeId], fields=mmp_dict, headers=vendorSpecific)

  def updateNodeCapabilities(self, nodeId, node, vendorSpecific=None):
    response = self.updateNodeCapabilitiesResponse(nodeId, node, vendorSpecific)
    return self._read_boolean_response(response)

  # CNRegister.register(session, node) → NodeReference
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRegister.register

  def registerResponse(self, node, vendorSpecific=None):
    mmp_dict = {
      'node': ('node.xml', node.toxml('utf-8')),
    }
    return self.POST('node', fields=mmp_dict, headers=vendorSpecific)

  def register(self, node, vendorSpecific=None):
    response = self.registerResponse(node, vendorSpecific)
    return self._read_boolean_response(response)
