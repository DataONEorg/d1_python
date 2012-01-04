#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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

# Enable admin.
from django.contrib import admin
admin.autodiscover()

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
  # GET /monitor/ping
  (r'^v1/monitor/ping/?$', 'monitor_ping'),
  # GET /log
  (r'^v1/log/?$', 'event_log_view'),
  # GET /  or  GET /node
  (r'^v1/?$', 'node'),
  (r'^v1/node/?$', 'node'),

  # Tier 1: Read API (MNRead)
  # GET /object/{pid}
  # HEAD /object/{pid}
  (r'^v1/object/(.+)$', 'object_pid'),
  # GET /meta/{pid}
  (r'^v1/meta/(.+)$', 'meta_pid_get'),
  # GET /checksum/{pid}[?checksumAlgorithm={checksumAlgorithm}]
  (r'^v1/checksum/(.+)$', 'checksum_pid'),
  # GET /object <filters>
  (r'^v1/object/?$', 'object'),
  # POST /error
  (r'^v1/error/?$', 'error'),

  # Tier 2: Authorization API  (MNAuthorization)
  # GET /isAuthorized/{pid}?action={action}
  (r'^v1/isAuthorized/(.+)/?$', 'is_authorized'),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object/{pid}
  # Handled by the object_pid dispatcher.
  # MNStorage.update() - PUT /object/{pid}
  # TODO: This is a workaround for issue with PUT in Django.
  (r'^v1/object_put/(.+)$', 'object_pid_put'),
  # MNStorage.delete() - DELETE /object/{pid}
  # Handled by the object_pid dispatcher.
  # MNStorage.systemMetadataChanged() - POST /dirtySystemMetadata/{pid}
  (r'^v1/dirtySystemMetadata/?$', 'dirty_system_metadata_post'),

  # Tier 4: Replication API (MNReplication)
  # POST /replicate  
  (r'^v1/replicate/?$', 'replicate'),
)

urlpatterns += patterns(
  'service.mn.views.internal',
  (r'^internal/replicate_task_get$', 'replicate_task_get'),
  (r'^internal/replicate_task_update/(.+?)/(.+?)/?$', 'replicate_task_update'),
  (r'^internal/replicate_create/(.+)$', 'replicate_create'),
  (r'^internal/update_sysmeta/(.+)$', 'update_sysmeta'),
)

# Block access to the GMN diagnostic functions if not in debug mode.
if settings.DEBUG:
  urlpatterns += patterns(
    'service.mn.views.diagnostics',
    # Test portal.
    (r'^test/?$', 'test'),
    # Replication.
    (r'^test/replicate_post/?$', 'replicate_post'),
    (r'^test/replicate_get/?$', 'replicate_get'),
    (r'^test/replicate_get_xml/?$', 'replicate_get_xml'),
    (r'^test/replicate_clear/?$', 'replicate_clear'),
    # Misc.
    (r'^test/slash/(.+?)/(.+?)/(.+?)/?$', 'slash'),
    (r'^test/exception/(.+?)/?$', 'exception'),
    (r'^test/clear_database/(.+?)/?$', 'clear_database'),
    (r'^test/delete_all_objects/?$', 'delete_all_objects'),
    (r'^test/delete_single_object/(.+?)/?$', 'delete_single_object'),
    (r'^test/delete_event_log/?$', 'delete_event_log'),
    (r'^test/inject_event_log/?$', 'inject_event_log'),
    (r'^test/delete_all_access_rules/?$', 'delete_all_access_rules'),
    (r'^test/cert/?$', 'cert'),
    # Concurrency.
    (r'^test/concurrency_clear/?$', 'concurrency_clear'),
    (r'^test/concurrency_read_lock/(.+?)/(.+?)/(.+?)/?$', 'concurrency_read_lock'),
    (r'^test/concurrency_write_lock/(.+?)/(.+?)/(.+?)/(.+?)/?$',
     'concurrency_write_lock'),
    (r'^test/concurrency_get_dictionary_id/?$', 'concurrency_get_dictionary_id'),
  )

urlpatterns += patterns(
  'service.mn.views.admin',
  (r'^admin/doc/?$', include('django.contrib.admindocs.urls')),
  (r'^admin/?$', include(admin.site.urls)),
)
