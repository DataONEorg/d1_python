#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`urls`
===========

:Synopsis:
  Django URL to function mapping.

.. moduleauthor:: Roger Dahl
"""

from django.conf.urls.defaults import *

# Enable admin.
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
  'mn_prototype.mn_service.views',
  # CN interface.

  # /object/
  (r'^object/$', 'object_collection'),
  (r'^object/(.*)/meta/$', 'object_guid_meta'),
  (r'^object/(.*)/$', 'object_guid'),

  # /log/
  (r'^log/$', 'access_log_view'),
  (r'^register/$', 'register'),
  (r'^upload/$', 'upload'),

  # Diagnostic / Debugging.
  (r'^get_ip/$', 'auth_test'),

  # Admin.
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^admin/', include(admin.site.urls)),
)
