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

from django.conf.urls.defaults import *

# Django does not have a location that is designated for setting up global
# objects. For testing, we need a global dictionary and the top level urls.py
# file is suggested as a good location for this.

# TODO: Only set dictionary up in debug mode.
import collections
test_shared_dict = collections.defaultdict(lambda: '<undef>')

import settings
#import sys, os
#_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
#sys.path.append(_here('./views'))
#print sys.path

urlpatterns = patterns(
  'service.mn.views.v1',
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  (r'^v1/monitor/ping/?$', 'get_monitor_ping'),
  # MNCore.getLogRecords() - GET /log
  (r'^v1/log/?$', 'get_log'),
  # MNCore.getCapabilities() - GET / and GET /node
  (r'^v1/?$', 'get_node'),
  (r'^v1/node/?$', 'get_node'),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{pid}
  (r'^v1/object/(.+)$', 'dispatch_object_pid'),
  # MNRead.getSystemMetadata() - GET /meta/{pid} 
  (r'^v1/meta/(.+)$', 'get_meta_pid'),
  # MNRead.describe() - HEAD /object/{pid}
  # (handled by object_pid dispatcher)
  # MNRead.getChecksum() - GET /checksum/{pid}
  (r'^v1/checksum/(.+)$', 'get_checksum_pid'),
  # MNRead.listObjects() - GET /object
  (r'^v1/object/?$', 'dispatch_object'),
  # MNRead.synchronizationFailed() - POST /error
  (r'^v1/error/?$', 'post_error'),
  # MNRead.getReplica() - GET /replica/{pid}
  (r'^v1/replica/(.+)/?$', 'get_replica_pid'),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{pid}
  (r'^v1/isAuthorized/(.+)/?$', 'get_is_authorized_pid'),
  # MNStorage.systemMetadataChanged() - POST /dirtySystemMetadata/{pid}
  (r'^v1/dirtySystemMetadata/?$', 'post_dirty_system_metadata'),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{pid}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  (r'^v1/generate/?$', 'post_generate_identifier'),
  # MNStorage.delete() - DELETE /object/{pid}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{pid}
  (r'^v1/archive/(.+)/?$', 'put_archive_pid'),

  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate  
  (r'^v1/replicate/?$', 'post_replicate'),
)

urlpatterns += patterns(
  'service.mn.views.internal',
  (r'^internal/replicate/task_get$', 'replicate_task_get'),
  (r'^internal/replicate/task_update/(.+?)/(.+?)/?$', 'replicate_task_update'),
  (r'^internal/replicate/create/(.+)$', 'replicate_create'),
  (r'^internal/update_sysmeta/(.+)$', 'update_sysmeta'),
  (r'^internal/home/?$', 'home'),
)

if settings.GMN_DEBUG or settings.MONITOR:
  urlpatterns += patterns(
    'service.mn.views.diagnostics',
    # Replication.
    (r'^test/get_replication_queue/?$', 'get_replication_queue'),
    # Authentication.
    (r'^test/echo_session/?$', 'echo_session'),
    # Misc.
    (r'^test/echo_request_object/?$', 'echo_request_object'),
    (r'^test/echo_raw_post_data/?$', 'echo_raw_post_data'),
  )

# Block access to the GMN diagnostic functions if not in debug mode.
if settings.GMN_DEBUG:
  urlpatterns += patterns(
    'service.mn.views.diagnostics',
    # Diagnostics portal.
    (r'^test/?$', 'diagnostics'),
    # Replication.
    (r'^test/get_replication_queue/?$', 'get_replication_queue'),
    (r'^test/clear_replication_queue/?$', 'clear_replication_queue'),
    # Access Policy
    (r'^test/set_access_policy/(.+?)/?$', 'set_access_policy'),
    (r'^test/delete_all_access_policies/?$', 'delete_all_access_policies'),
    # Misc.
    (r'^test/create/(.+)$', 'create'),
    (r'^test/slash/(.+?)/(.+?)/(.+?)/?$', 'slash'),
    (r'^test/exception/(.+?)/?$', 'exception'),
    (r'^test/delete_all_objects/?$', 'delete_all_objects'),
    (r'^test/delete_single_object/(.+?)/?$', 'delete_single_object'),
    (r'^test/trusted_subjects/?$', 'trusted_subjects'),
    (r'^test/permissions_for_object/(.+?)/?$', 'permissions_for_object'),
    # Event Log.
    (r'^test/delete_event_log/?$', 'delete_event_log'),
    (r'^test/inject_fictional_event_log/?$', 'inject_fictional_event_log'),
    # Concurrency.
    (r'^test/concurrency_clear/?$', 'concurrency_clear'),
    (r'^test/concurrency_read_lock/(.+?)/(.+?)/(.+?)/?$', 'concurrency_read_lock'),
    (r'^test/concurrency_write_lock/(.+?)/(.+?)/(.+?)/(.+?)/?$',
     'concurrency_write_lock'),
    (r'^test/concurrency_get_dictionary_id/?$', 'concurrency_get_dictionary_id'),
  )
