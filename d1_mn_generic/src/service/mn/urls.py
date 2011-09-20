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

:Synopsis:
  Django URL to function mapping.

.. moduleauthor:: Roger Dahl
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

urlpatterns = patterns(
  'service.mn.views',
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # ----------------------------------------------------------------------------
  # Public API
  # ----------------------------------------------------------------------------

  # Tier 1: Core API  

  # GET /monitor/ping
  (r'^monitor/ping/?$', 'monitor_ping'),
  # GET /log
  (r'^log/?$', 'event_log_view'),
  # GET /  or  GET /node
  (r'^/?$', 'node'),
  (r'^node/?$', 'node'),

  # Tier 1: Read API

  # GET /object/{pid}
  # HEAD /object/{pid}
  (r'^object/(.+)$', 'object_pid'),
  # GET /meta/{pid}
  (r'^meta/(.+)$', 'meta_pid'),
  # GET /checksum/{pid}[?checksumAlgorithm={checksumAlgorithm}]
  (r'^checksum/(.+)$', 'checksum_pid'),
  # GET /object <filters>
  (r'^object/?$', 'object'),
  # POST /error
  (r'^error/?$', 'error'),

  # Tier 2: Authorization API

  # GET /isAuthorized/{pid}?action={action}
  (r'^assertAuthorized/(.+)/?$', 'assert_authorized'),
  # PUT /accessRules/{pid}
  (r'^setAccessPolicy/(.+)$', 'access_policy_pid'),
  (r'^setAccessPolicy_put/(.+)$', 'access_policy_pid_put_workaround'),

  # Tier 3: Storage API

  # POST /object/{pid}
  # Handled by the object_pid dispatcher.
  # PUT /object/{pid}
  # TODO: This is a workaround for issue with PUT in Django.
  (r'^object_put/(.+)$', 'object_pid_put'),
  # DELETE /object/{pid}
  # Handled by the object_pid dispatcher.

  # Tier 4: Replication API

  # POST /replicate  
  (r'^replicate/?$', 'replicate'),

  # ----------------------------------------------------------------------------
  # Private API
  # ----------------------------------------------------------------------------

  # Replication.

  # replicate_store
  (r'^replicate_store/?$', 'replicate_store'),

  # ----------------------------------------------------------------------------
  # Diagnostics, debugging and testing
  # ----------------------------------------------------------------------------

  # Test portal.
  (r'^test/?$', 'test'),

  # Replication.
  (r'^test_replicate_post/?$', 'test_replicate_post'),
  (r'^test_replicate_get/?$', 'test_replicate_get'),
  (r'^test_replicate_get_xml/?$', 'test_replicate_get_xml'),
  (r'^test_replicate_clear/?$', 'test_replicate_clear'),

  # Misc.
  (r'^test_slash/(.+?)/(.+?)/(.+?)/?$', 'test_slash'),
  (r'^test_exception/(.+?)/?$', 'test_exception'),
  (r'^test_clear_database/(.+?)/?$', 'test_clear_database'),
  (r'^test_delete_all_objects/?$', 'test_delete_all_objects'),
  (r'^test_delete_single_object/(.+?)/?$', 'test_delete_single_object'),
  (r'^test_delete_event_log/?$', 'test_delete_event_log'),
  (r'^test_inject_event_log/?$', 'test_inject_event_log'),
  (r'^test_delete_all_access_rules/?$', 'test_delete_all_access_rules'),
  (r'^test_cert/?$', 'test_cert'),

  # Concurrency.
  (r'^test_concurrency_clear/?$', 'test_concurrency_clear'),
  (r'^test_concurrency_read_lock/(.+?)/(.+?)/(.+?)/?$', 'test_concurrency_read_lock'),
  (
    r'^test_concurrency_write_lock/(.+?)/(.+?)/(.+?)/(.+?)/?$',
    'test_concurrency_write_lock'
  ),
  (r'^test_concurrency_get_dictionary_id/?$', 'test_concurrency_get_dictionary_id'),

  # ----------------------------------------------------------------------------
  # Administration.
  # ----------------------------------------------------------------------------
  (r'^admin/doc/?$', include('django.contrib.admindocs.urls')),
  (r'^admin/?$', include(admin.site.urls)),
)
