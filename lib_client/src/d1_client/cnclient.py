#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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

import d1_common.type_conversions

import d1_client.baseclient


class CoordinatingNodeClient(d1_client.baseclient.DataONEBaseClient):
    """Extend DataONEBaseClient by adding REST API wrappers for APIs that are available
    on Coordinating Nodes.

    For details on how to use these methods, see:

    https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html

    """

    def __init__(self, *args, **kwargs):
        """See d1_client.baseclient.DataONEBaseClient for args."""
        super().__init__(*args, **kwargs)

        self._log = logging.getLogger(__name__)

        self._api_major = 1
        self._api_minor = 0
        self._pyxb_binding = d1_common.type_conversions.get_pyxb_binding_by_api_version(
            self._api_major, self._api_minor
        )

    # =========================================================================
    # Core API
    # =========================================================================

    def listFormatsResponse(self, vendorSpecific=None):
        """CNCore.ping() → null https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.ping Implemented in
        d1_client.baseclient.py.

        CNCore.create(session, pid, object, sysmeta) → Identifier
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.create
        CN INTERNAL

        CNCore.listFormats() → ObjectFormatList
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.listFormats

        Args:
          vendorSpecific:

        Returns:

        """
        return self.GET('formats', headers=vendorSpecific)

    def listFormats(self, vendorSpecific=None):
        """See Also: listFormatsResponse()

        Args:
          vendorSpecific:

        Returns:

        """
        response = self.listFormatsResponse(vendorSpecific)
        return self._read_dataone_type_response(response, 'ObjectFormatList')

    def getFormatResponse(self, formatId, vendorSpecific=None):
        """CNCore.getFormat(formatId) → ObjectFormat
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.getFormat.

        Args:
          formatId:
          vendorSpecific:

        Returns:

        """
        return self.GET(['formats', formatId], headers=vendorSpecific)

    def getFormat(self, formatId, vendorSpecific=None):
        """See Also: getFormatResponse()

        Args:
          formatId:
          vendorSpecific:

        Returns:

        """
        response = self.getFormatResponse(formatId, vendorSpecific)
        return self._read_dataone_type_response(response, 'ObjectFormat')

    def reserveIdentifierResponse(self, pid, vendorSpecific=None):
        """CNCore.getLogRecords(session[, fromDate][, toDate][, event][, start][,
        count]) → Log https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.getLogRecords Implemented in
        d1_client.baseclient.py.

        CNCore.reserveIdentifier(session, pid) → Identifier
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.reserveIdentifier

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'pid': pid}
        return self.POST(['reserve', pid], fields=mmp_dict, headers=vendorSpecific)

    def reserveIdentifier(self, pid, vendorSpecific=None):
        """See Also: reserveIdentifierResponse()

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        response = self.reserveIdentifierResponse(pid, vendorSpecific)
        return self._read_dataone_type_response(response, 'Identifier', vendorSpecific)

    def listChecksumAlgorithmsResponse(self, vendorSpecific=None):
        """CNCore.listChecksumAlgorithms() → ChecksumAlgorithmList
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.listChecksumAlgorithms.

        Args:
          vendorSpecific:

        Returns:

        """
        return self.GET('checksum', headers=vendorSpecific)

    def listChecksumAlgorithms(self, vendorSpecific=None):
        """See Also: listChecksumAlgorithmsResponse()

        Args:
          vendorSpecific:

        Returns:

        """
        response = self.listChecksumAlgorithmsResponse(vendorSpecific)
        return self._read_dataone_type_response(response, 'ChecksumAlgorithmList')

    def setObsoletedByResponse(
        self, pid, obsoletedByPid, serialVersion, vendorSpecific=None
    ):
        """CNCore.setObsoletedBy(session, pid, obsoletedByPid, serialVersion) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.setObsoletedBy.

        Args:
          pid:
          obsoletedByPid:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {
            'obsoletedByPid': obsoletedByPid,
            'serialVersion': str(serialVersion),
        }
        return self.PUT(['obsoletedBy', pid], fields=mmp_dict, headers=vendorSpecific)

    def setObsoletedBy(self, pid, obsoletedByPid, serialVersion, vendorSpecific=None):
        """See Also: setObsoletedByResponse()

        Args:
          pid:
          obsoletedByPid:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.setObsoletedByResponse(
            pid, obsoletedByPid, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    def listNodesResponse(self, vendorSpecific=None):
        """CNCore.listNodes() → NodeList https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNCore.listNodes.

        Args:
          vendorSpecific:

        Returns:

        """
        return self.GET('node', headers=vendorSpecific)

    def listNodes(self, vendorSpecific=None):
        """See Also: listNodesResponse()

        Args:
          vendorSpecific:

        Returns:

        """
        response = self.listNodesResponse(vendorSpecific)
        return self._read_dataone_type_response(response, 'NodeList')

    def hasReservationResponse(self, pid, subject, vendorSpecific=None):
        """CNCore.registerSystemMetadata(session, pid, sysmeta) → Identifier CN
        INTERNAL.

        CNCore.hasReservation(session, pid) → boolean
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNCore.hasReservation

        Args:
          pid:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.GET(['reserve', pid, subject], headers=vendorSpecific)

    def hasReservation(self, pid, subject, vendorSpecific=None):
        """See Also: hasReservationResponse()

        Args:
          pid:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.hasReservationResponse(pid, subject, vendorSpecific)
        return self._read_boolean_404_response(response)

    # =========================================================================
    # Read API
    # =========================================================================

    def resolveResponse(self, pid, vendorSpecific=None):
        """CNRead.get(session, pid) → OctetStream Implemented in
        d1_client.baseclient.py.

        CNRead.getSystemMetadata(session, pid) → SystemMetadata
        Implemented in d1_client.baseclient.py

        CNRead.resolve(session, pid) → ObjectLocationList
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.resolve

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        return self.GET(['resolve', pid], headers=vendorSpecific)

    def resolve(self, pid, vendorSpecific=None):
        """See Also: resolveResponse()

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        response = self.resolveResponse(pid, vendorSpecific)
        return self._read_dataone_type_response(
            response, 'ObjectLocationList', response_is_303_redirect=True
        )

    def getChecksumResponse(self, pid, vendorSpecific=None):
        """CNRead.getChecksum(session, pid) → Checksum
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNRead.getChecksum.

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        return self.GET(['checksum', pid], headers=vendorSpecific)

    def getChecksum(self, pid, vendorSpecific=None):
        """See Also: getChecksumResponse()

        Args:
          pid:
          vendorSpecific:

        Returns:

        """
        response = self.getChecksumResponse(pid, vendorSpecific)
        return self._read_dataone_type_response(response, 'Checksum')

    def searchResponse(self, queryType, query, vendorSpecific=None, **kwargs):
        """CNRead.search(session, queryType, query) → ObjectList
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNRead.search.

        Args:
          queryType:
          query:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        return self.GET(
            ['search', queryType, query], headers=vendorSpecific, query=kwargs
        )

    def search(self, queryType, query=None, vendorSpecific=None, **kwargs):
        """See Also: searchResponse()

        Args:
          queryType:
          query:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        response = self.searchResponse(queryType, query, vendorSpecific, **kwargs)
        return self._read_dataone_type_response(response, 'ObjectList')

    def queryResponse(self, queryEngine, query=None, vendorSpecific=None, **kwargs):
        """CNRead.query(session, queryEngine, query) → OctetStream
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNRead.query.

        Args:
          queryEngine:
          query:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        return self.GET(
            ['query', queryEngine, query], headers=vendorSpecific, query=kwargs
        )

    def query(self, queryEngine, query=None, vendorSpecific=None, **kwargs):
        """See Also: queryResponse()

        Args:
          queryEngine:
          query:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        response = self.queryResponse(queryEngine, query, vendorSpecific, **kwargs)
        return self._read_stream_response(response)

    def getQueryEngineDescriptionResponse(
        self, queryEngine, vendorSpecific=None, **kwargs
    ):
        """CNRead.getQueryEngineDescription(session, queryEngine) →
        QueryEngineDescription https://releases.dataone.org/online/api-document
        ation-v2.0.1/apis/CN_APIs.html#CNRead.getQueryEngineDescription.

        Args:
          queryEngine:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        return self.GET(['query', queryEngine], headers=vendorSpecific, query=kwargs)

    def getQueryEngineDescription(self, queryEngine, vendorSpecific=None, **kwargs):
        """See Also: getQueryEngineDescriptionResponse()

        Args:
          queryEngine:
          vendorSpecific:
          **kwargs:

        Returns:

        """
        response = self.getQueryEngineDescriptionResponse(
            queryEngine, vendorSpecific, **kwargs
        )
        return self._read_dataone_type_response(response, 'QueryEngineDescription')

    # =========================================================================
    # Authorization API
    # =========================================================================

    def setRightsHolderResponse(self, pid, userId, serialVersion, vendorSpecific=None):
        """CNAuthorization.setRightsHolder(session, pid, userId, serialVersion)

        → Identifier https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNAuthorization.setRightsHolder.

        Args:
          pid:
          userId:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'userId': userId, 'serialVersion': str(serialVersion)}
        return self.PUT(['owner', pid], headers=vendorSpecific, fields=mmp_dict)

    def setRightsHolder(self, pid, userId, serialVersion, vendorSpecific=None):
        """See Also: setRightsHolderResponse()

        Args:
          pid:
          userId:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.setRightsHolderResponse(
            pid, userId, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    def setAccessPolicyResponse(
        self, pid, accessPolicy, serialVersion, vendorSpecific=None
    ):
        """CNAuthorization.setAccessPolicy(session, pid, accessPolicy, serialVersion) →
        boolean https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNAuthorization.setAccessPolicy.

        Args:
          pid:
          accessPolicy:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {
            'serialVersion': str(serialVersion),
            'accessPolicy': ('accessPolicy.xml', accessPolicy.toxml('utf-8')),
        }
        return self.PUT(['accessRules', pid], fields=mmp_dict, headers=vendorSpecific)

    def setAccessPolicy(self, pid, accessPolicy, serialVersion, vendorSpecific=None):
        """See Also: setAccessPolicyResponse()

        Args:
          pid:
          accessPolicy:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.setAccessPolicyResponse(
            pid, accessPolicy, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    # =========================================================================
    # Identity API
    # =========================================================================

    def registerAccountResponse(self, person, vendorSpecific=None):
        """CNIdentity.registerAccount(session, person) → Subject
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.registerAccount.

        Args:
          person:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'person': ('person.xml', person.toxml('utf-8'))}
        return self.POST('accounts', fields=mmp_dict, headers=vendorSpecific)

    def registerAccount(self, person, vendorSpecific=None):
        """See Also: registerAccountResponse()

        Args:
          person:
          vendorSpecific:

        Returns:

        """
        response = self.registerAccountResponse(person, vendorSpecific)
        return self._read_boolean_response(response)

    def updateAccountResponse(self, subject, person, vendorSpecific=None):
        """CNIdentity.updateAccount(session, person) → Subject
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.updateAccount.

        Args:
          subject:
          person:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'person': ('person.xml', person.toxml('utf-8'))}
        return self.PUT(['accounts', subject], fields=mmp_dict, headers=vendorSpecific)

    def updateAccount(self, subject, person, vendorSpecific=None):
        """See Also: updateAccountResponse()

        Args:
          subject:
          person:
          vendorSpecific:

        Returns:

        """
        response = self.updateAccountResponse(subject, person, vendorSpecific)
        return self._read_boolean_response(response)

    def verifyAccountResponse(self, subject, vendorSpecific=None):
        """CNIdentity.verifyAccount(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.verifyAccount.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.PUT(['accounts', subject], headers=vendorSpecific)

    def verifyAccount(self, subject, vendorSpecific=None):
        """See Also: verifyAccountResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.verifyAccountResponse(subject, vendorSpecific)
        return self._read_boolean_response(response)

    def getSubjectInfoResponse(self, subject, vendorSpecific=None):
        """CNIdentity.getSubjectInfo(session, subject) → SubjectList
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.getSubjectInfo.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.GET(['accounts', subject], headers=vendorSpecific)

    def getSubjectInfo(self, subject, vendorSpecific=None):
        """See Also: getSubjectInfoResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.getSubjectInfoResponse(subject, vendorSpecific)
        return self._read_dataone_type_response(response, 'SubjectInfo')

    def listSubjectsResponse(
        self, query, status=None, start=None, count=None, vendorSpecific=None
    ):
        """CNIdentity.listSubjects(session, query, status, start, count) → SubjectList
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.listSubjects.

        Args:
          query:
          status:
          start:
          count:
          vendorSpecific:

        Returns:

        """
        url_query = {'status': status, 'start': start, 'count': count, 'query': query}
        return self.GET('accounts', query=url_query, headers=vendorSpecific)

    def listSubjects(
        self, query, status=None, start=None, count=None, vendorSpecific=None
    ):
        """See Also: listSubjectsResponse()

        Args:
          query:
          status:
          start:
          count:
          vendorSpecific:

        Returns:

        """
        response = self.listSubjectsResponse(
            query, status, start, count, vendorSpecific
        )
        return self._read_dataone_type_response(response, 'SubjectInfo')

    def mapIdentityResponse(
        self, primarySubject, secondarySubject, vendorSpecific=None
    ):
        """CNIdentity.mapIdentity(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.mapIdentity.

        Args:
          primarySubject:
          secondarySubject:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {
            'primarySubject': primarySubject.toxml('utf-8'),
            'secondarySubject': secondarySubject.toxml('utf-8'),
        }
        return self.POST(['accounts', 'map'], fields=mmp_dict, headers=vendorSpecific)

    def mapIdentity(self, primarySubject, secondarySubject, vendorSpecific=None):
        """See Also: mapIdentityResponse()

        Args:
          primarySubject:
          secondarySubject:
          vendorSpecific:

        Returns:

        """
        response = self.mapIdentityResponse(
            primarySubject, secondarySubject, vendorSpecific
        )
        return self._read_boolean_response(response)

    def removeMapIdentityResponse(self, subject, vendorSpecific=None):
        """CNIdentity.removeMapIdentity(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.removeMapIdentity.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.DELETE(['accounts', 'map', subject], headers=vendorSpecific)

    def removeMapIdentity(self, subject, vendorSpecific=None):
        """See Also: removeMapIdentityResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.removeMapIdentityResponse(subject, vendorSpecific)
        return self._read_boolean_response(response)

    def denyMapIdentityResponse(self, subject, vendorSpecific=None):
        """CNIdentity.denyMapIdentity(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.denyMapIdentity.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.DELETE(['accounts', 'pendingmap', subject], headers=vendorSpecific)

    def denyMapIdentity(self, subject, vendorSpecific=None):
        """See Also: denyMapIdentityResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.denyMapIdentityResponse(subject, vendorSpecific)
        return self._read_boolean_response(response)

    def requestMapIdentityResponse(self, subject, vendorSpecific=None):
        """CNIdentity.requestMapIdentity(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.requestMapIdentity.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'subject': subject.toxml('utf-8')}
        return self.POST('accounts', fields=mmp_dict, headers=vendorSpecific)

    def requestMapIdentity(self, subject, vendorSpecific=None):
        """See Also: requestMapIdentityResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.requestMapIdentityResponse(subject, vendorSpecific)
        return self._read_boolean_response(response)

    def confirmMapIdentityResponse(self, subject, vendorSpecific=None):
        """CNIdentity.confirmMapIdentity(session, subject) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.confirmMapIdentity.

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        return self.PUT(['accounts', 'pendingmap', subject], headers=vendorSpecific)

    def confirmMapIdentity(self, subject, vendorSpecific=None):
        """See Also: confirmMapIdentityResponse()

        Args:
          subject:
          vendorSpecific:

        Returns:

        """
        response = self.confirmMapIdentityResponse(subject, vendorSpecific)
        return self._read_boolean_response(response)

    def createGroupResponse(self, group, vendorSpecific=None):
        """CNIdentity.createGroup(session, groupName) → Subject
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.createGroup.

        Args:
          group:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'group': ('group.xml', group.toxml('utf-8'))}
        return self.POST('groups', fields=mmp_dict, headers=vendorSpecific)

    def createGroup(self, group, vendorSpecific=None):
        """See Also: createGroupResponse()

        Args:
          group:
          vendorSpecific:

        Returns:

        """
        response = self.createGroupResponse(group, vendorSpecific)
        return self._read_boolean_response(response)

    def updateGroupResponse(self, group, vendorSpecific=None):
        """CNIdentity.addGroupMembers(session, groupName, members) → boolean
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNIdentity.addGroupMembers.

        Args:
          group:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'group': ('group.xml', group.toxml('utf-8'))}
        return self.PUT('groups', fields=mmp_dict, headers=vendorSpecific)

    def updateGroup(self, group, vendorSpecific=None):
        """See Also: updateGroupResponse()

        Args:
          group:
          vendorSpecific:

        Returns:

        """
        response = self.updateGroupResponse(group, vendorSpecific)
        return self._read_boolean_response(response)

    # =========================================================================
    # Replication API
    # =========================================================================

    def setReplicationStatusResponse(
        self, pid, nodeRef, status, dataoneError=None, vendorSpecific=None
    ):
        """CNReplication.setReplicationStatus(session, pid, nodeRef, status, failure) →
        boolean https://releases.dataone.org/online/api-documentatio
        n-v2.0.1/apis/CN_APIs.html#CNReplication.setReplicationStatus.

        Args:
          pid:
          nodeRef:
          status:
          dataoneError:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'nodeRef': nodeRef, 'status': status}  # .toxml('utf-8'),
        if dataoneError is not None:
            mmp_dict['failure'] = ('failure.xml', dataoneError.serialize_to_transport())
        return self.PUT(
            ['replicaNotifications', pid], fields=mmp_dict, headers=vendorSpecific
        )

    def setReplicationStatus(
        self, pid, nodeRef, status, dataoneError=None, vendorSpecific=None
    ):
        """See Also: setReplicationStatusResponse()

        Args:
          pid:
          nodeRef:
          status:
          dataoneError:
          vendorSpecific:

        Returns:

        """
        response = self.setReplicationStatusResponse(
            pid, nodeRef, status, dataoneError, vendorSpecific
        )
        return self._read_boolean_response(response)

    def updateReplicationMetadataResponse(
        self, pid, replicaMetadata, serialVersion, vendorSpecific=None
    ):
        """CNReplication.updateReplicationMetadata(session, pid, replicaMetadata,
        serialVersion) → boolean https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_AP Is.html#CNReplication.updateReplicationMetadata
        Not implemented.

        Args:
          pid:
          replicaMetadata:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {
            'replicaMetadata': ('replicaMetadata.xml', replicaMetadata.toxml('utf-8')),
            'serialVersion': str(serialVersion),
        }
        return self.PUT(
            ['replicaMetadata', pid], fields=mmp_dict, headers=vendorSpecific
        )

    def updateReplicationMetadata(
        self, pid, replicaMetadata, serialVersion, vendorSpecific=None
    ):
        """See Also: updateReplicationMetadataResponse()

        Args:
          pid:
          replicaMetadata:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.updateReplicationMetadataResponse(
            pid, replicaMetadata, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    def setReplicationPolicyResponse(
        self, pid, policy, serialVersion, vendorSpecific=None
    ):
        """CNReplication.setReplicationPolicy(session, pid, policy, serialVersion) →
        boolean https://releases.dataone.org/online/api-docume
        ntation-v2.0.1/apis/CN_APIs.html#CNReplication.setReplicationPolicy.

        Args:
          pid:
          policy:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {
            'policy': ('policy.xml', policy.toxml('utf-8')),
            'serialVersion': (str(serialVersion)),
        }
        return self.PUT(
            ['replicaPolicies', pid], fields=mmp_dict, headers=vendorSpecific
        )

    def setReplicationPolicy(self, pid, policy, serialVersion, vendorSpecific=None):
        """See Also: setReplicationPolicyResponse()

        Args:
          pid:
          policy:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.setReplicationPolicyResponse(
            pid, policy, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    # TODO. Spec unclear.

    def isNodeAuthorizedResponse(self, targetNodeSubject, pid, vendorSpecific=None):
        """CNReplication.isNodeAuthorized(session, targetNodeSubject, pid,
        replicatePermission) → boolean() https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNReplication.isNodeAuthorized.

        Args:
          targetNodeSubject:
          pid:
          vendorSpecific:

        Returns:

        """
        query_dict = {'targetNodeSubject': targetNodeSubject}
        return self.GET(
            ['replicaAuthorizations', pid], query=query_dict, headers=vendorSpecific
        )

    def isNodeAuthorized(self, targetNodeSubject, pid, vendorSpecific=None):
        """See Also: isNodeAuthorizedResponse()

        Args:
          targetNodeSubject:
          pid:
          vendorSpecific:

        Returns:

        """
        response = self.isNodeAuthorizedResponse(targetNodeSubject, pid, vendorSpecific)
        return self._read_boolean_401_response(response)

    def deleteReplicationMetadataResponse(
        self, pid, nodeId, serialVersion, vendorSpecific=None
    ):
        """CNReplication.deleteReplicationMetadata(session, pid, policy, serialVersion)

        → boolean https://releases.dataone.org/online/api-docume
        ntation-v2.0.1/apis/CN_APIs.html#CNReplication.deleteReplicationMetadat a.

        Args:
          pid:
          nodeId:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'nodeId': nodeId, 'serialVersion': str(serialVersion)}
        return self.PUT(
            ['removeReplicaMetadata', pid], fields=mmp_dict, headers=vendorSpecific
        )

    def deleteReplicationMetadata(
        self, pid, nodeId, serialVersion, vendorSpecific=None
    ):
        """See Also: deleteReplicationMetadataResponse()

        Args:
          pid:
          nodeId:
          serialVersion:
          vendorSpecific:

        Returns:

        """
        response = self.deleteReplicationMetadataResponse(
            pid, nodeId, serialVersion, vendorSpecific
        )
        return self._read_boolean_response(response)

    # =========================================================================
    # Register API
    # =========================================================================

    def updateNodeCapabilitiesResponse(self, nodeId, node, vendorSpecific=None):
        """CNRegister.updateNodeCapabilities(session, nodeId, node) → boolean
        https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_AP
        Is.html#CNRegister.updateNodeCapabilities.

        Args:
          nodeId:
          node:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'node': ('node.xml', node.toxml('utf-8'))}
        return self.PUT(['node', nodeId], fields=mmp_dict, headers=vendorSpecific)

    def updateNodeCapabilities(self, nodeId, node, vendorSpecific=None):
        """See Also: updateNodeCapabilitiesResponse()

        Args:
          nodeId:
          node:
          vendorSpecific:

        Returns:

        """
        response = self.updateNodeCapabilitiesResponse(nodeId, node, vendorSpecific)
        return self._read_boolean_response(response)

    def registerResponse(self, node, vendorSpecific=None):
        """CNRegister.register(session, node) → NodeReference
        https://releases.dataone.org/online/api-
        documentation-v2.0.1/apis/CN_APIs.html#CNRegister.register.

        Args:
          node:
          vendorSpecific:

        Returns:

        """
        mmp_dict = {'node': ('node.xml', node.toxml('utf-8'))}
        return self.POST('node', fields=mmp_dict, headers=vendorSpecific)

    def register(self, node, vendorSpecific=None):
        """See Also: registerResponse()

        Args:
          node:
          vendorSpecific:

        Returns:

        """
        response = self.registerResponse(node, vendorSpecific)
        return self._read_boolean_response(response)
