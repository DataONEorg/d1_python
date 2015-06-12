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
:mod:`urls`
===========

:Synopsis: URL to function mapping.
:Author: DataONE (Dahl)
'''

#from django.conf.urls.defaults import *
#import django.conf.urls.defaults

from django.conf.urls import patterns, url

import settings

urlpatterns = patterns(
  'service.mn.views.v1',
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  url(r'^v1/monitor/ping/?$', 'get_monitor_ping'),
  # MNCore.getLogRecords() - GET /log
  url(r'^v1/log/?$', 'get_log'),
  # MNCore.getCapabilities() - GET / and GET /node
  url(r'^v1/?$', 'get_node'),
  url(r'^v1/node/?$', 'get_node'),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{pid}
  url(r'^v1/object/(.+)$', 'dispatch_object_pid'),
  # MNRead.getSystemMetadata() - GET /meta/{pid}
  url(r'^v1/meta/(.+)$', 'get_meta_pid'),
  # MNRead.describe() - HEAD /object/{pid}
  # (handled by object_pid dispatcher)
  # MNRead.getChecksum() - GET /checksum/{pid}
  url(r'^v1/checksum/(.+)$', 'get_checksum_pid'),
  # MNRead.listObjects() - GET /object
  url(r'^v1/object/?$', 'dispatch_object'),
  # MNRead.synchronizationFailed() - POST /error
  url(r'^v1/error/?$', 'post_error'),
  # MNRead.getReplica() - GET /replica/{pid}
  url(r'^v1/replica/(.+)/?$', 'get_replica_pid'),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{pid}
  url(r'^v1/isAuthorized/(.+)/?$', 'get_is_authorized_pid'),
  # MNStorage.systemMetadataChanged() - POST /refreshSystemMetadata/{pid}
  url(r'^v1/dirtySystemMetadata/?$', 'post_refresh_system_metadata'),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{pid}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  url(r'^v1/generate/?$', 'post_generate_identifier'),
  # MNStorage.delete() - DELETE /object/{pid}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{pid}
  url(r'^v1/archive/(.+)/?$', 'put_archive_pid'),

  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate
  url(r'^v1/replicate/?$', 'post_replicate'),
)

urlpatterns += patterns('service.mn.views.internal', url(r'^home/?$', 'home'), )

# Diagnostic APIs that can be made available in production.

if settings.GMN_DEBUG or settings.MONITOR:
  urlpatterns += patterns(
    'service.mn.views.diagnostics',
    # Replication.
    url(r'^diag/get_replication_queue/?$', 'get_replication_queue'),
    # Authentication.
    url(r'^diag/echo_session/?$', 'echo_session'),
    # Misc.
    url(r'^diag/echo_request_object/?$', 'echo_request_object'),
    url(r'^diag/echo_raw_post_data/?$', 'echo_raw_post_data'),
  )

# Diagnostic APIs that should only be available in debug mode.

if settings.GMN_DEBUG:
  urlpatterns += patterns(
    'service.mn.views.diagnostics',
    # Diagnostics portal.
    url(r'^diag/?$', 'diagnostics'),
    # Replication.
    url(r'^diag/get_replication_queue/?$', 'get_replication_queue'),
    url(r'^diag/clear_replication_queue/?$', 'clear_replication_queue'),
    # Access Policy.
    url(r'^diag/set_access_policy/(.+?)/?$', 'set_access_policy'),
    url(r'^diag/delete_all_access_policies/?$', 'delete_all_access_policies'),
    # Misc.
    url(r'^diag/create/(.+)$', 'create'),
    url(r'^diag/slash/(.+?)/(.+?)/(.+?)/?$', 'slash'),
    url(r'^diag/exception/(.+?)/?$', 'exception'),
    url(r'^diag/delete_all_objects/?$', 'delete_all_objects'),
    url(r'^diag/delete_single_object/(.+?)/?$', 'delete_single_object'),
    url(r'^diag/trusted_subjects/?$', 'trusted_subjects'),
    url(r'^diag/permissions_for_object/(.+?)/?$', 'permissions_for_object'),
    url(r'^diag/get_setting/(.+)$', 'get_setting'),
    # Event Log.
    url(r'^diag/delete_event_log/?$', 'delete_event_log'),
    url(r'^diag/inject_fictional_event_log/?$', 'inject_fictional_event_log'),
  )
