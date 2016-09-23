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
"""
:mod:`urls`
===========

:Synopsis: URL to function mapping.
:Author: DataONE (Dahl)
"""

# Django
#from django.conf.urls.defaults import *
#import django.conf.urls.defaults
from django.conf.urls import url
from django.conf import settings

# App
import mn.views.external
import mn.views.internal
import mn.views.diagnostics

urlpatterns = [
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  url(r'^v[12]/monitor/ping/?$', mn.views.external.get_monitor_ping),
  # MNCore.getLogRecords() - GET /log
  url(r'^v[12]/log/?$', mn.views.external.get_log),
  # MNCore.getCapabilities() - GET / and GET /node
  url(r'^v[12]/?$', mn.views.external.get_node),
  url(r'^v[12]/node/?$', mn.views.external.get_node),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{sid_or_pid}
  url(r'^v[12]/object/(.+)$', mn.views.external.dispatch_object),
  # MNRead.getSystemMetadata() - GET /meta/{sid_or_pid}
  url(r'^v[12]/meta/(.+)$', mn.views.external.get_meta),
  # MNRead.describe() - HEAD /object/{sid_or_pid}
  # (handled by object dispatcher)
  # MNRead.getChecksum() - GET /checksum/{sid_or_pid}
  url(r'^v[12]/checksum/(.+)$', mn.views.external.get_checksum),
  # MNRead.listObjects() - GET /object
  url(r'^v[12]/object/?$', mn.views.external.dispatch_object_list),
  # MNRead.synchronizationFailed() - POST /error
  url(r'^v[12]/error/?$', mn.views.external.post_error),
  # MNRead.getReplica() - GET /replica/{sid_or_pid}
  url(r'^v[12]/replica/(.+)/?$', mn.views.external.get_replica),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{sid_or_pid}
  url(r'^v[12]/isAuthorized/(.+)/?$', mn.views.external.get_is_authorized),
  # MNStorage.systemMetadataChanged() - POST /refreshSystemMetadata/{sid_or_pid}
  url(r'^v[12]/dirtySystemMetadata/?$', mn.views.external.post_refresh_system_metadata),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{sid_or_pid}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  url(r'^v[12]/generate/?$', mn.views.external.post_generate_identifier),
  # MNStorage.delete() - DELETE /object/{sid_or_pid}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{sid_or_pid}
  url(r'^v[12]/archive/(.+)/?$', mn.views.external.put_archive),

  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate
  url(r'^v[12]/replicate/?$', mn.views.external.post_replicate),
]

urlpatterns.extend([
  url(r'^home/?$', mn.views.internal.home)
])

# Diagnostic APIs that can be made available in production.

if settings.GMN_DEBUG or settings.MONITOR:
  urlpatterns.extend([
    # Replication.
    url(r'^diag/get_replication_queue/?$', mn.views.diagnostics.get_replication_queue),
    # Authentication.
    url(r'^diag/echo_session/?$', mn.views.diagnostics.echo_session),
    # Misc.
    url(r'^diag/echo_request_object/?$', mn.views.diagnostics.echo_request_object),
    url(r'^diag/echo_raw_post_data/?$', mn.views.diagnostics.echo_raw_post_data),
  ])

# Diagnostic APIs that should only be available in debug mode.

if settings.GMN_DEBUG:
  urlpatterns.extend([
    # Diagnostics portal.
    url(r'^diag$', mn.views.diagnostics.diagnostics),
    # Replication.
    url(r'^diag/get_replication_queue$', mn.views.diagnostics.get_replication_queue),
    url(r'^diag/clear_replication_queue$', mn.views.diagnostics.clear_replication_queue),
    # Access Policy.
    url(r'^diag/set_access_policy/(.+?)$', mn.views.diagnostics.set_access_policy),
    url(r'^diag/delete_all_access_policies$', mn.views.diagnostics.delete_all_access_policies),
    # Misc.
    url(r'^diag/create/(.+)$', mn.views.diagnostics.create),
    url(r'^diag/slash/(.+?)/(.+?)/(.+?)$', mn.views.diagnostics.slash),
    url(r'^diag/exception/(.+?)$', mn.views.diagnostics.exception),
    url(r'^diag/delete_all_objects$', mn.views.diagnostics.delete_all_objects),
    url(r'^diag/delete_single_object/(.+?)$', mn.views.diagnostics.delete_single_object),
    url(r'^diag/trusted_subjects$', mn.views.diagnostics.trusted_subjects),
    url(r'^diag/whitelist_subject$', mn.views.diagnostics.whitelist_subject),
    url(r'^diag/permissions_for_object/(.+?)$', mn.views.diagnostics.permissions_for_object),
    url(r'^diag/get_setting/(.+)$', mn.views.diagnostics.get_setting),
    # Event Log.
    url(r'^diag/delete_event_log$', mn.views.diagnostics.delete_event_log),
    url(r'^diag/inject_fictional_event_log$', mn.views.diagnostics.inject_fictional_event_log),
  ])
