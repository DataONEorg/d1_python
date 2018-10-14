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

import d1_gmn.app.views.external
import d1_gmn.app.views.get_package
import d1_gmn.app.views.gmn
import d1_gmn.app.views.internal

import d1_common.util

import django.conf.urls as urls
import django.views.static

# from django.urls import path
# from django.views.generic import TemplateView

# Return 404 and 500 as UI page when DEBUG=False
handler404 = 'd1_gmn.app.views.internal.error_404'
handler500 = 'd1_gmn.app.views.internal.error_500'

urlpatterns = [
  # Django's URL dispatcher does not take HTTP method into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # methods against the same URL, the methods are dispatched to the same view
  # function, which checks the method and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  urls.url(
    r'^v[12]/monitor/ping/?$',
    d1_gmn.app.views.external.get_monitor_ping,
    kwargs={'allowed_method_list': ['GET']},
    name='get_monitor_ping',
  ),
  # MNCore.getLogRecords() - GET /log
  urls.url(
    r'^v[12]/log/?$',
    d1_gmn.app.views.external.get_log,
    kwargs={'allowed_method_list': ['GET']},
    name='get_log',
  ),
  # MNCore.getCapabilities() - GET /node
  # Also available via Apache redirect from /
  urls.url(
    r'^v[12]/(?:node/?)?$',
    d1_gmn.app.views.external.get_node,
    kwargs={'allowed_method_list': ['GET']},
    name='get_node',
  ),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{did}
  urls.url(
    r'^v[12]/object/(.+)$',
    d1_gmn.app.views.external.dispatch_object,
    kwargs={'allowed_method_list': ['GET', 'HEAD', 'PUT', 'DELETE']},
    name='dispatch_object',
  ),
  # MNRead.getSystemMetadata() - GET /meta/{did}
  urls.url(
    r'^v[12]/meta/(.+)$',
    d1_gmn.app.views.external.get_meta,
    kwargs={'allowed_method_list': ['GET']},
    name='get_meta',
  ),
  # MNStorage.updateSystemMetadata() - PUT /meta
  urls.url(
    r'^v2/meta$',
    d1_gmn.app.views.external.put_meta,
    kwargs={'allowed_method_list': ['PUT']},
    name='put_meta',
  ),
  # MNRead.describe() - HEAD /object/{did}
  # (handled by object dispatcher)
  # MNRead.getChecksum() - GET /checksum/{did}
  urls.url(
    r'^v[12]/checksum/(.+)$',
    d1_gmn.app.views.external.get_checksum,
    kwargs={'allowed_method_list': ['HEAD', 'GET']},
    name='get_checksum',
  ),
  # MNRead.listObjects() - GET /object
  urls.url(
    r'^v[12]/object/?$',
    d1_gmn.app.views.external.dispatch_object_list,
    kwargs={'allowed_method_list': ['GET', 'POST']},
    name='dispatch_object_list',
  ),
  # MNRead.synchronizationFailed() - POST /error
  urls.url(
    r'^v[12]/error/?$',
    d1_gmn.app.views.external.post_error,
    kwargs={'allowed_method_list': ['POST']},
    name='post_error',
  ),
  # MNRead.getReplica() - GET /replica/{did}
  urls.url(
    r'^v[12]/replica/(.+)/?$',
    d1_gmn.app.views.external.get_replica,
    kwargs={'allowed_method_list': ['GET']},
    name='get_replica',
  ),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{did}
  urls.url(
    r'^v[12]/isAuthorized/(.+)/?$',
    d1_gmn.app.views.external.get_is_authorized,
    kwargs={'allowed_method_list': ['GET']},
    name='get_is_authorized',
  ),
  # MNStorage.systemMetadataChanged() - POST /refreshSystemMetadata/{did}
  urls.url(
    r'^v[12]/dirtySystemMetadata/?$',
    d1_gmn.app.views.external.post_refresh_system_metadata,
    kwargs={'allowed_method_list': ['POST']},
    name='post_refresh_system_metadata',
  ),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{did}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  urls.url(
    r'^v[12]/generate/?$',
    d1_gmn.app.views.external.post_generate_identifier,
    kwargs={'allowed_method_list': ['POST', 'PUT']},
    name='post_generate_identifier',
  ),
  # MNStorage.delete() - DELETE /object/{did}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{did}
  urls.url(
    r'^v[12]/archive/(.+)/?$',
    d1_gmn.app.views.external.put_archive,
    kwargs={'allowed_method_list': ['delete', 'PUT']},
    name='put_archive',
  ),
  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate
  urls.url(
    r'^v[12]/replicate/?$',
    d1_gmn.app.views.external.post_replicate,
    kwargs={'allowed_method_list': ['POST']},
    name='post_replicate',
  ),
  # Package API
  # MNPackage.getPackage() - GET /package
  urls.url(
    r'^v2/packages/(?P<package_type>.+)/(?P<pid>.+)/?$',
    d1_gmn.app.views.get_package.get_package,
    kwargs={'allowed_method_list': ['GET']},
    name='get_package',
  ),

  #
  # Web UI
  #

  # Redirect / to /home
  urls.url(
    r'^$',
    d1_gmn.app.views.internal.root,
    kwargs={'allowed_method_list': ['GET']},
    name='root',
  ),
  urls.url(
    r'^home/?$',
    d1_gmn.app.views.internal.home,
    kwargs={'allowed_method_list': ['GET']},
    name='home',
  ),
  urls.url(
    r'^templates/home.xsl$',
    d1_gmn.app.views.internal.home_xslt,
    kwargs={'allowed_method_list': ['GET']},
    name='home_xslt',
  ),

  #
  # GMN vendor specific extensions
  #
  urls.url(
    r'^gmn/object/?$',
    d1_gmn.app.views.gmn.get_object_list_json,
    kwargs={'allowed_method_list': ['GET']},
    name='get_object_list_json',
  ),
  urls.url(
    r'^gmn/echo/session/?$',
    d1_gmn.app.views.gmn.echo_session,
    kwargs={'allowed_method_list': ['GET']},
    name='echo_session',
  ),
  urls.url(
    r'^gmn/echo/request/?$',
    d1_gmn.app.views.gmn.echo_request,
    kwargs={'allowed_method_list': ['GET']},
    name='echo_request_object',
  ),
]

if django.conf.settings.STATIC_SERVER:
  urlpatterns.append(
    urls.url(
      r'^static/(?P<path>.*)$',
      django.views.static.serve,
      kwargs={
        # 'static': d1_common.util.abs_path('.'),
        'document_root': d1_common.util.abs_path('./static'),
        'show_indexes': True,
        'allowed_method_list': ['GET'],
      },
    )
  )
