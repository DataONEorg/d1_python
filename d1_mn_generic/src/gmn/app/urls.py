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
"""URL to view mapping
"""

from __future__ import absolute_import

# Django
from django.conf.urls import url
import django.conf

# App
import app.views.diagnostics
import app.views.external
import app.views.internal

urlpatterns = [
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  url(
    r'^v[12]/monitor/ping/?$',
    app.views.external.get_monitor_ping,
    name='get_monitor_ping',
  ),
  # MNCore.getLogRecords() - GET /log
  url(
    r'^v[12]/log/?$',
    app.views.external.get_log,
    name='get_log',
  ),
  # MNCore.getCapabilities() - GET / and GET /node
  url(
    r'^v[12]/?$',
    app.views.external.get_node,
    name='get_node',
  ),
  url(
    r'^v[12]/node/?$',
    app.views.external.get_node,
  ),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{did}
  url(
    r'^v[12]/object/(.+)$',
    app.views.external.dispatch_object,
    name='dispatch_object',
  ),
  # MNRead.getSystemMetadata() - GET /meta/{did}
  url(
    r'^v[12]/meta/(.+)$',
    app.views.external.get_meta,
    name='get_meta',
  ),
  # MNStorage.updateSystemMetadata() - PUT /meta
  url(
    r'^v2/meta$',
    app.views.external.put_meta,
    name='put_meta',
  ),
  # MNRead.describe() - HEAD /object/{did}
  # (handled by object dispatcher)
  # MNRead.getChecksum() - GET /checksum/{did}
  url(
    r'^v[12]/checksum/(.+)$',
    app.views.external.get_checksum,
    name='get_checksum',
  ),
  # MNRead.listObjects() - GET /object
  url(
    r'^v[12]/object/?$',
    app.views.external.dispatch_object_list,
    name='dispatch_object_list',
  ),
  # MNRead.synchronizationFailed() - POST /error
  url(
    r'^v[12]/error/?$',
    app.views.external.post_error,
    name='post_error',
  ),
  # MNRead.getReplica() - GET /replica/{did}
  url(
    r'^v[12]/replica/(.+)/?$',
    app.views.external.get_replica,
    name='get_replica',
  ),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{did}
  url(
    r'^v[12]/isAuthorized/(.+)/?$',
    app.views.external.get_is_authorized,
    name='get_is_authorized',
  ),
  # MNStorage.systemMetadataChanged() - POST /refreshSystemMetadata/{did}
  url(
    r'^v[12]/dirtySystemMetadata/?$',
    app.views.external.post_refresh_system_metadata,
    name='post_refresh_system_metadata',
  ),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{did}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  url(
    r'^v[12]/generate/?$',
    app.views.external.post_generate_identifier,
    name='post_generate_identifier',
  ),
  # MNStorage.delete() - DELETE /object/{did}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{did}
  url(
    r'^v[12]/archive/(.+)/?$',
    app.views.external.put_archive,
    name='put_archive',
  ),

  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate
  url(
    r'^v[12]/replicate/?$',
    app.views.external.post_replicate,
    name='post_replicate',
  ),
]

urlpatterns.extend([url(r'^home/?$', app.views.internal.home, name='home')])

# Diagnostic APIs that can be made available in production.

if django.conf.settings.DEBUG_GMN or django.conf.settings.MONITOR:
  urlpatterns.extend([
    # Replication.
    url(
      r'^diag/get_replication_queue/?$',
      app.views.diagnostics.get_replication_queue,
      name='get_replication_queue',
    ),
    # Authentication.
    url(
      r'^diag/echo_session/?$',
      app.views.diagnostics.echo_session,
      name='echo_session',
    ),
    # Misc.
    url(
      r'^diag/echo_request_object/?$',
      app.views.diagnostics.echo_request_object,
      name='echo_request_object',
    ),
    url(
      r'^diag/echo_raw_post_data/?$',
      app.views.diagnostics.echo_raw_post_data,
      name='echo_raw_post_data',
    ),
  ])

# Diagnostic APIs that should only be available in debug mode.

if django.conf.settings.DEBUG_GMN:
  urlpatterns.extend([
    # Diagnostics portal
    url(
      r'^diag$',
      app.views.diagnostics.diagnostics,
      name='diag',
    ),
    # Replication.
    url(
      r'^diag/get_replication_queue$',
      app.views.diagnostics.get_replication_queue,
      name='get_replication_queue',
    ),
    url(
      r'^diag/clear_replication_queue$',
      app.views.diagnostics.clear_replication_queue,
      name='clear_replication_queue',
    ),
    # Access Policy.
    url(
      r'^diag/delete_all_access_policies$',
      app.views.diagnostics.delete_all_access_policies,
      name='delete_all_access_policies',
    ),
    # Misc.
    url(
      r'^diag/create/(.+)$',
      app.views.diagnostics.create,
      name='create',
    ),
    url(
      r'^diag/slash/(.+?)/(.+?)/(.+?)$',
      app.views.diagnostics.slash,
      name='slash',
    ),
    url(
      r'^diag/exception/(.+?)$', app.views.diagnostics.exception,
      name='exception'
    ),
    url(
      r'^diag/delete_all_objects$',
      app.views.diagnostics.delete_all_objects_view,
      name='delete_all_objects_view',
    ),
    url(
      r'^diag/trusted_subjects$',
      app.views.diagnostics.trusted_subjects,
      name='trusted_subjects',
    ),
    url(
      r'^diag/whitelist_subject$',
      app.views.diagnostics.whitelist_subject,
      name='whitelist_subject',
    ),
    url(
      r'^diag/permissions_for_object/(.+?)$',
      app.views.diagnostics.permissions_for_object,
      name='permissions_for_object',
    ),
    url(
      r'^diag/get_setting/(.+)$',
      app.views.diagnostics.get_setting,
      name='get_setting',
    ),
    # Event Log.
    url(
      r'^diag/delete_event_log$',
      app.views.diagnostics.delete_event_log,
      name='delete_event_log',
    ),
    url(
      r'^diag/inject_fictional_event_log$',
      app.views.diagnostics.inject_fictional_event_log,
      name='inject_fictional_event_log',
    ),
  ])
