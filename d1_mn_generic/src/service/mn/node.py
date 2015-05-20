#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
'''
:mod:`node`
===========

:Synopsis:
  Generate Node document.
:Author:
  DataONE (Dahl)
'''

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

# App.
import service.settings as settings

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# For debugging the population of PyXB objects, it can be convenient to turn off
# PyXB's validation.
#import pyxb
#pyxb.RequireValidWhenGenerating(False)


class Node():
  def __init__(self):
    pass

  def get(self):
    node = dataoneTypes.node()
    node.identifier = settings.NODE_IDENTIFIER
    node.name = settings.NODE_NAME
    node.description = settings.NODE_DESCRIPTION
    node.baseURL = settings.NODE_BASEURL
    node.replicate = settings.NODE_REPLICATE
    node.synchronize = settings.NODE_SYNCHRONIZE
    node.type = 'mn'
    node.state = settings.NODE_STATE
    node.subject.append(dataoneTypes.Subject(settings.NODE_SUBJECT))
    node.contactSubject.append(dataoneTypes.Subject(settings.NODE_CONTACT_SUBJECT))
    node.services = self._create_services()
    node.synchronization = self._create_sync_policy()
    node.nodeReplicationPolicy = self._create_replication_policy()
    return node

  def _create_sync_policy(self):
    schedule = dataoneTypes.Schedule()
    schedule.year = settings.NODE_SYNC_SCHEDULE_YEAR
    schedule.mon = settings.NODE_SYNC_SCHEDULE_MONTH
    schedule.wday = settings.NODE_SYNC_SCHEDULE_WEEKDAY
    schedule.mday = settings.NODE_SYNC_SCHEDULE_MONTHDAY
    schedule.hour = settings.NODE_SYNC_SCHEDULE_HOUR
    schedule.min = settings.NODE_SYNC_SCHEDULE_MINUTE
    schedule.sec = settings.NODE_SYNC_SCHEDULE_SECOND
    sync = dataoneTypes.Synchronization()
    sync.schedule = schedule
    return sync

  def _create_replication_policy(self):
    replication = dataoneTypes.nodeReplicationPolicy()

    if settings.REPLICATION_MAXOBJECTSIZE != -1:
      replication.maxObjectSize = settings.REPLICATION_MAXOBJECTSIZE
    if settings.REPLICATION_SPACEALLOCATED != -1:
      replication.spaceAllocated = settings.REPLICATION_SPACEALLOCATED
    #if len(settings.REPLICATION_ALLOWEDNODE):
    for allowed_node in settings.REPLICATION_ALLOWEDNODE:
      replication.allowedNode.append(dataoneTypes.NodeReference(allowed_node))
    #if len(settings.REPLICATION_ALLOWEDOBJECTFORMAT):
    for allowed_object in settings.REPLICATION_ALLOWEDOBJECTFORMAT:
      replication.allowedObjectFormat.append(
        dataoneTypes.ObjectFormatIdentifier(
          allowed_object
        )
      )

    return replication

  def _create_services(self):
    services = dataoneTypes.Services()
    if settings.TIER >= 1:
      self._append_tier_1_services(services)
    if settings.TIER >= 2:
      self._append_tier_2_services(services)
    if settings.TIER >= 3:
      self._append_tier_3_services(services)
    if settings.TIER >= 4:
      self._append_tier_4_services(services)
    return services

  def _append_tier_1_services(self, services):
    # <service name="MNCore" version="v1" available="true"/>
    service = dataoneTypes.Service()
    service.name = dataoneTypes.ServiceName('MNCore')
    service.version = dataoneTypes.ServiceVersion('v1')
    service.available = True
    services.append(service)
    # <service name="MNRead" version="v1" available="true"/>
    service = dataoneTypes.Service()
    service.name = dataoneTypes.ServiceName('MNRead')
    service.version = dataoneTypes.ServiceVersion('v1')
    service.available = True
    services.append(service)

  def _append_tier_2_services(self, services):
    # <service name="MNAuthorization" version="v1" available="true"/>
    service = dataoneTypes.Service()
    service.name = dataoneTypes.ServiceName('MNAuthorization')
    service.version = dataoneTypes.ServiceVersion('v1')
    service.available = True
    services.append(service)

  def _append_tier_3_services(self, services):
    # <service name="MNStorage" version="v1" available="true"/>
    service = dataoneTypes.Service()
    service.name = dataoneTypes.ServiceName('MNStorage')
    service.version = dataoneTypes.ServiceVersion('v1')
    service.available = True
    services.append(service)

  def _append_tier_4_services(self, services):
    # <service name="MNReplication" version="v1" available="true"/>
    service = dataoneTypes.Service()
    service.name = dataoneTypes.ServiceName('MNReplication')
    service.version = dataoneTypes.ServiceVersion('v1')
    service.available = True
    services.append(service)
