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
  Django URL to service mapping.

.. moduleauthor:: Roger Dahl
'''

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
  '',
  (r'^', include('mn_prototype.mn_service.urls')),
  (r'^accounts/login/$', 'django.contrib.auth.views.login'),

  # Enable admin documentation:
  (r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Enable admin interface:
  (r'^admin/', include(admin.site.urls)),
)

#'''
#:mod:`Top level __init__.py`
#==============
#
#:Synopsis:
#  System Logging is used for logging internal events that are not exposed
#  through any of the DataONE interfaces. Used for monitoring service and doing
#  post mortem debugging.
#
#.. moduleauthor:: Roger Dahl
#'''

#Stdlib.
import logging
import sys

# App.
import settings

# Set up logging.
# We output everything to both file and stdout.
logging.getLogger('').setLevel(logging.DEBUG)
formatter = logging.Formatter(
  '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
)
# Log file.
file_logger = logging.FileHandler(settings.LOG_PATH, 'a')
file_logger.setFormatter(formatter)
logging.getLogger('').addHandler(file_logger)
# Console.
#console_logger = StreamHandler(sys.stdout)
#console_logger.setFormatter(formatter)
#getLogger('').addHandler(console_logger)
