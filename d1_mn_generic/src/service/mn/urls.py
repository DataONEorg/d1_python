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

urlpatterns = patterns(
  'service.mn.views',
  # /session/
  (r'^session/?$', 'session'),

  # /object
  (r'^object/?$', 'object_collection'),
  (r'^meta/(.+)$', 'meta_pid'),
  (r'^object/(.+)$', 'object_pid'),
  (r'^checksum/(.+)$', 'checksum_pid'),

  # /log/
  (r'^log/?$', 'event_log_view'),

  # /health/
  (r'^health/ping/?$', 'health_ping'),
  (r'^health/status/?$', 'health_status'),

  # /monitor/
  (r'^monitor/object/?$', 'monitor_object'),
  (r'^monitor/event/?$', 'monitor_event'),

  # /node/ (also available at root)
  (r'^node/?$', 'node'),
  (r'^/?$', 'node'),

  # /replicate/
  (r'^replicate/?$', 'replicate'),
  # Internal
  (r'^_replicate_store/?$', '_replicate_store'),

  # Diagnostics, debugging and testing.
  (r'^test/?$', 'test'),
  (r'^test_replicate_post/?$', 'test_replicate_post'),
  (r'^test_replicate_get/?$', 'test_replicate_get'),
  (r'^test_replicate_clear/?$', 'test_replicate_clear'),
  (r'^test_slash/(.+?)/(.+?)/(.+?)/?$', 'test_slash'),
  (r'^test_exception/(.+?)/?$', 'test_exception'),
  (r'^test_get_request/?$', 'test_get_request'),
  (r'^test_inject_log/?$', 'test_inject_log'),

  # Admin.
  (r'^admin/doc/?$', include('django.contrib.admindocs.urls')),
  (r'^admin/?$', include(admin.site.urls)),
)
