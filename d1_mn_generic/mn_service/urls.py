#!/usr/bin/env python
# -*- coding: utf-8 -*-
""":mod:`models` -- URLs
========================

:module: urls
:platform: Linux
:synopsis: URLs

.. moduleauthor:: Roger Dahl
"""

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
  'mn_prototype.mn_service.views',
  (r'^object/(.*)/meta$', 'object_sysmeta'),
  (r'^object/(.*)$', 'object'),
  (r'^log/$', 'access_log_get'),
  (r'^get_ip/$', 'auth_test'),
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  (r'^admin/', include(admin.site.urls)),
)
