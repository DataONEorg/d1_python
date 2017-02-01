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
"""Generate Node document based on the current setings for GMN.
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
import d1_common.types.dataoneTypes_v1 as v1
import d1_common.types.dataoneTypes_v2_0 as v2
import d1_common.util

# App


def get_pretty_xml(major_version_int=2):
  node_xml = get_xml(major_version_int)
  return d1_common.util.pretty_xml(node_xml)


def get_xml(major_version_int):
  return _get_pyxb(major_version_int).toxml()


def get_pyxb(major_version_int=2):
  return _get_pyxb(major_version_int)


def _get_pyxb(major_version_int):
  assert major_version_int in (1, 2)
  binding = v1 if major_version_int == 1 else v2

  node_pyxb = binding.node()
  node_pyxb.identifier = settings.NODE_IDENTIFIER
  node_pyxb.name = settings.NODE_NAME
  node_pyxb.description = settings.NODE_DESCRIPTION
  node_pyxb.baseURL = settings.NODE_BASEURL
  node_pyxb.replicate = settings.NODE_REPLICATE
  node_pyxb.synchronize = settings.NODE_SYNCHRONIZE
  node_pyxb.type = 'mn'
  node_pyxb.state = settings.NODE_STATE
  node_pyxb.subject.append(binding.Subject(settings.NODE_SUBJECT))
  node_pyxb.contactSubject.append(binding.Subject(settings.NODE_CONTACT_SUBJECT))
  node_pyxb.services = _create_service_list_pyxb(binding, major_version_int)
  if settings.NODE_SYNCHRONIZE:
    node_pyxb.synchronization = _create_synchronization_policy_pyxb(binding)
  if settings.NODE_REPLICATE:
    node_pyxb.nodeReplicationPolicy = _create_replication_policy_pyxb(binding)
  return node_pyxb


def _create_synchronization_policy_pyxb(binding):
  schedule_pyxb = binding.Schedule()
  schedule_pyxb.year = settings.NODE_SYNC_SCHEDULE_YEAR
  schedule_pyxb.mon = settings.NODE_SYNC_SCHEDULE_MONTH
  schedule_pyxb.wday = settings.NODE_SYNC_SCHEDULE_WEEKDAY
  schedule_pyxb.mday = settings.NODE_SYNC_SCHEDULE_MONTHDAY
  schedule_pyxb.hour = settings.NODE_SYNC_SCHEDULE_HOUR
  schedule_pyxb.min = settings.NODE_SYNC_SCHEDULE_MINUTE
  schedule_pyxb.sec = settings.NODE_SYNC_SCHEDULE_SECOND
  sync = binding.Synchronization()
  sync.schedule = schedule_pyxb
  return sync


def _create_replication_policy_pyxb(binding):
  replication_pyxb = binding.nodeReplicationPolicy()
  if settings.REPLICATION_MAXOBJECTSIZE != -1:
    replication_pyxb.maxObjectSize = settings.REPLICATION_MAXOBJECTSIZE
  if settings.REPLICATION_SPACEALLOCATED != -1:
    replication_pyxb.spaceAllocated = settings.REPLICATION_SPACEALLOCATED
  for allowed_node in settings.REPLICATION_ALLOWEDNODE:
    replication_pyxb.allowedNode.append(binding.NodeReference(allowed_node))
  for allowed_object in settings.REPLICATION_ALLOWEDOBJECTFORMAT:
    replication_pyxb.allowedObjectFormat.append(
      binding.ObjectFormatIdentifier(allowed_object)
    )
  return replication_pyxb


def _create_service_list_pyxb(binding, major_version_int):
  service_list_pyxb = binding.services()
  service_list_pyxb.extend(_create_service_list_for_version_pyxb(binding, 'v1'))
  if major_version_int == 2:
    service_list_pyxb.extend(_create_service_list_for_version_pyxb(binding, 'v2'))
  return service_list_pyxb


def _create_service_list_for_version_pyxb(binding, service_version):
  service_list = []
  service_list.append(_create_service_pyxb(binding, 'MNCore', service_version))
  service_list.append(_create_service_pyxb(binding, 'MNRead', service_version))
  service_list.append(_create_service_pyxb(binding, 'MNAuthorization', service_version))
  service_list.append(_create_service_pyxb(binding, 'MNStorage', service_version))
  service_list.append(_create_service_pyxb(binding, 'MNReplication', service_version))
  return service_list


def _create_service_pyxb(binding, service_name, service_version):
  service_pyxb = binding.Service()
  service_pyxb.name = binding.ServiceName(service_name)
  service_pyxb.version = binding.ServiceVersion(service_version)
  service_pyxb.available = True
  return service_pyxb
