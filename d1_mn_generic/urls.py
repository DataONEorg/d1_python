#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`urls`
===========

:Synopsis:
  Django URL to service mapping.

.. moduleauthor:: Roger Dahl
"""

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
  '',
  (r'^', include('mn_prototype.mn_service.urls')),
  (
    r'^accounts/login/$', 'django.contrib.auth.views.login'
  ),

  # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
  # to INSTALLED_APPS to enable admin documentation:
  # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # (r'^admin/', include(admin.site.urls)),
)
