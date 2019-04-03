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
"""Generate Node document based on the current settings for GMN."""

import d1_common.type_conversions
import d1_common.xml

import django.conf
import django.urls

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

# App


def get_pretty_xml(api_major_int=2):
    return d1_common.xml.serialize_for_transport(
        _get_pyxb(api_major_int), xslt_url=django.urls.base.reverse('home_xslt')
    )


def get_xml(api_major_int):
    return d1_common.xml.serialize_for_transport(
        _get_pyxb(api_major_int),
        pretty=False,
        xslt_url=django.urls.base.reverse('home_xslt'),
    )


def get_pyxb(api_major_int=2):
    return _get_pyxb(api_major_int)


# noinspection PyTypeChecker
def _get_pyxb(api_major_int):
    if api_major_int == 1:
        pyxb_binding = d1_common.type_conversions.get_pyxb_binding_by_api_version(1, 1)
    elif api_major_int == 2:
        pyxb_binding = d1_common.type_conversions.get_pyxb_binding_by_api_version(2, 0)
    else:
        assert False

    node_pyxb = pyxb_binding.node()
    node_pyxb.identifier = django.conf.settings.NODE_IDENTIFIER
    node_pyxb.name = django.conf.settings.NODE_NAME
    node_pyxb.description = django.conf.settings.NODE_DESCRIPTION
    node_pyxb.baseURL = django.conf.settings.NODE_BASEURL
    node_pyxb.replicate = django.conf.settings.NODE_REPLICATE
    node_pyxb.synchronize = django.conf.settings.NODE_SYNCHRONIZE
    node_pyxb.type = 'mn'
    node_pyxb.state = django.conf.settings.NODE_STATE
    node_pyxb.subject.append(pyxb_binding.Subject(django.conf.settings.NODE_SUBJECT))
    node_pyxb.contactSubject.append(
        pyxb_binding.Subject(django.conf.settings.NODE_CONTACT_SUBJECT)
    )
    node_pyxb.services = _create_service_list_pyxb(pyxb_binding)
    if django.conf.settings.NODE_SYNCHRONIZE:
        node_pyxb.synchronization = _create_synchronization_policy_pyxb(pyxb_binding)
    if django.conf.settings.NODE_REPLICATE:
        node_pyxb.nodeReplicationPolicy = _create_replication_policy_pyxb(pyxb_binding)
    return node_pyxb


def _create_synchronization_policy_pyxb(pyxb_binding):
    schedule_pyxb = pyxb_binding.Schedule()
    schedule_pyxb.year = django.conf.settings.NODE_SYNC_SCHEDULE_YEAR
    schedule_pyxb.mon = django.conf.settings.NODE_SYNC_SCHEDULE_MONTH
    schedule_pyxb.wday = django.conf.settings.NODE_SYNC_SCHEDULE_WEEKDAY
    schedule_pyxb.mday = django.conf.settings.NODE_SYNC_SCHEDULE_MONTHDAY
    schedule_pyxb.hour = django.conf.settings.NODE_SYNC_SCHEDULE_HOUR
    schedule_pyxb.min = django.conf.settings.NODE_SYNC_SCHEDULE_MINUTE
    schedule_pyxb.sec = django.conf.settings.NODE_SYNC_SCHEDULE_SECOND
    sync = pyxb_binding.Synchronization()
    sync.schedule = schedule_pyxb
    return sync


def _create_replication_policy_pyxb(pyxb_binding):
    replication_pyxb = pyxb_binding.nodeReplicationPolicy()
    if django.conf.settings.REPLICATION_MAXOBJECTSIZE != -1:
        replication_pyxb.maxObjectSize = django.conf.settings.REPLICATION_MAXOBJECTSIZE
    if django.conf.settings.REPLICATION_SPACEALLOCATED != -1:
        replication_pyxb.spaceAllocated = (
            django.conf.settings.REPLICATION_SPACEALLOCATED
        )
    for allowed_node in django.conf.settings.REPLICATION_ALLOWEDNODE:
        replication_pyxb.allowedNode.append(pyxb_binding.NodeReference(allowed_node))
    for allowed_object in django.conf.settings.REPLICATION_ALLOWEDOBJECTFORMAT:
        replication_pyxb.allowedObjectFormat.append(
            pyxb_binding.ObjectFormatIdentifier(allowed_object)
        )
    return replication_pyxb


def _create_service_list_pyxb(pyxb_binding):
    # Both v1/node and v2/node list v2 services
    service_list_pyxb = pyxb_binding.services()
    service_list_pyxb.extend(_create_service_list_for_version_pyxb(pyxb_binding, 'v1'))
    service_list_pyxb.extend(_create_service_list_for_version_pyxb(pyxb_binding, 'v2'))
    return service_list_pyxb


def _create_service_list_for_version_pyxb(pyxb_binding, service_version):
    return [
        _create_service_pyxb(pyxb_binding, 'MNCore', service_version),
        _create_service_pyxb(pyxb_binding, 'MNRead', service_version),
        _create_service_pyxb(pyxb_binding, 'MNAuthorization', service_version),
        _create_service_pyxb(pyxb_binding, 'MNStorage', service_version),
        _create_service_pyxb(pyxb_binding, 'MNReplication', service_version),
    ]


def _create_service_pyxb(pyxb_binding, service_name, service_version):
    service_pyxb = pyxb_binding.Service()
    service_pyxb.name = pyxb_binding.ServiceName(service_name)
    service_pyxb.version = pyxb_binding.ServiceVersion(service_version)
    service_pyxb.available = True
    return service_pyxb
