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

"""Generate Node document
"""

# Example Node document:
#
# <?xml version="1.0" ?>
# <ns1:node replicate="false" state="up" synchronize="true" type="mn"
#   xmlns:ns1="http://ns.dataone.org/service/types/v1">
#   <identifier>urn:node:mnDevGMN</identifier>
#   <name>GMN Dev</name>
#   <description>Test Member Node operated by DataONE</description>
#   <baseURL>https://localhost/mn</baseURL>
#   <services>
#     <service available="true" name="MNCore" version="v1"/>
#     <service available="true" name="MNRead" version="v1"/>
#     <service available="true" name="MNAuthorization" version="v1"/>
#     <service available="true" name="MNStorage" version="v1"/>
#     <service available="true" name="MNReplication" version="v1"/>
#   </services>
#   <synchronization>
#     <schedule hour="*" mday="*" min="0/3" mon="*" sec="0" wday="?" year="*"/>
#   </synchronization>
#   <subject>CN=urn:node:mnDevGMN,DC=dataone,DC=org</subject>
#   <contactSubject>CN=MyName,O=Google,C=US,DC=cilogon,DC=org</contactSubject>
# </ns1:node>

# Django.
from django.conf import settings

# D1.
import d1_common.types.dataoneTypes_v2_0

# App


class Node(object):
  def __init__(self, binding=None):
    """binding:
    d1_common.types.dataoneTypes_v1
    or
    d1_common.types.dataoneTypes_v2_0
    """
    self._binding = binding or d1_common.types.dataoneTypes_v2_0

  def get_xml_str(self):
    return self.get().toxml('utf8')

  def get(self):
    node = self._binding.node()
    node.identifier = settings.NODE_IDENTIFIER
    node.name = settings.NODE_NAME
    node.description = settings.NODE_DESCRIPTION
    node.baseURL = settings.NODE_BASEURL
    node.replicate = settings.NODE_REPLICATE
    node.synchronize = settings.NODE_SYNCHRONIZE
    node.type = 'mn'
    node.state = settings.NODE_STATE
    node.subject.append(self._binding.Subject(settings.NODE_SUBJECT))
    node.contactSubject.append(self._binding.Subject(settings.NODE_CONTACT_SUBJECT))
    node.services = self._create_service_list()
    if settings.NODE_SYNCHRONIZE:
      node.synchronization = self._create_sync_policy()
    if settings.TIER >= 4 and settings.NODE_REPLICATE:
      node.nodeReplicationPolicy = self._create_replication_policy()
    return node

  def _create_sync_policy(self):
    schedule = self._binding.Schedule()
    schedule.year = settings.NODE_SYNC_SCHEDULE_YEAR
    schedule.mon = settings.NODE_SYNC_SCHEDULE_MONTH
    schedule.wday = settings.NODE_SYNC_SCHEDULE_WEEKDAY
    schedule.mday = settings.NODE_SYNC_SCHEDULE_MONTHDAY
    schedule.hour = settings.NODE_SYNC_SCHEDULE_HOUR
    schedule.min = settings.NODE_SYNC_SCHEDULE_MINUTE
    schedule.sec = settings.NODE_SYNC_SCHEDULE_SECOND
    sync = self._binding.Synchronization()
    sync.schedule = schedule
    return sync

  def _create_replication_policy(self):
    replication = self._binding.nodeReplicationPolicy()
    if settings.REPLICATION_MAXOBJECTSIZE != -1:
      replication.maxObjectSize = settings.REPLICATION_MAXOBJECTSIZE
    if settings.REPLICATION_SPACEALLOCATED != -1:
      replication.spaceAllocated = settings.REPLICATION_SPACEALLOCATED
    for allowed_node in settings.REPLICATION_ALLOWEDNODE:
      replication.allowedNode.append(self._binding.NodeReference(allowed_node))
    for allowed_object in settings.REPLICATION_ALLOWEDOBJECTFORMAT:
      replication.allowedObjectFormat.append(
        self._binding.ObjectFormatIdentifier(allowed_object)
      )
    return replication

  def _create_service_list(self):
    service_list = self._binding.services()
    self._append_services_for_version(service_list, 'v1')
    self._append_services_for_version(service_list, 'v2')
    return service_list

  def _append_services_for_version(self, service_list, service_version):
    if settings.TIER >= 1:
      self._append_service(service_list, 'MNCore', service_version)
      self._append_service(service_list, 'MNRead', service_version)
    if settings.TIER >= 2:
      self._append_service(service_list, 'MNAuthorization', service_version)
    if settings.TIER >= 3:
      self._append_service(service_list, 'MNStorage', service_version)
    if settings.TIER >= 4:
      self._append_service(service_list, 'MNReplication', service_version)

  def _append_service(self, service_list, service_name, service_version):
    service = self._binding.Service()
    service.name = self._binding.ServiceName(service_name)
    service.version = self._binding.ServiceVersion(service_version)
    service.available = True
    service_list.append(service)
