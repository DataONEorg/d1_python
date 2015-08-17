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
'''
:mod:`settings`
===============

:Synopsis:
  App level settings.
  This file contains settings that do not normally need to be modified when
  installing GMN. See settings_site.py for site specific settings.
:Author:
  DataONE (Dahl)
'''

# Stdlib.
import os
import sys


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

# Add site specific settings.
from settings_site import *

# Add path to gmn types.
sys.path.append(make_absolute('./types/generated'))

# GMN does not use templates in production. However, some of the testing
# functions use them.
TEMPLATE_DEBUG = True

# Only set cookies when running through SSL.
SESSION_COOKIE_SECURE = True

MANAGERS = ADMINS

# GMN MUST run in the UTC time zone. Under Windows, the system time zone must
# also be set to UTC.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# Static files (served directly by Apache).
STATIC_URL = '/static/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', )

MIDDLEWARE_CLASSES = (
  # Custom GMN middleware.
  'service.mn.middleware.request_handler.request_handler',
  'service.mn.middleware.exception_handler.exception_handler',
  'service.mn.middleware.response_handler.response_handler',
  #'service.mn.middleware.profiling_handler.profiling_handler',
  'service.mn.middleware.view_handler.view_handler',
  'service.mn.middleware.startup_handler.startup_handler',
)


CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'TIMEOUT': 60 * 60,
  }
}

ROOT_URLCONF = 'service.urls'

TEMPLATE_DIRS = (make_absolute('./mn/templates'), )

INSTALLED_APPS = ('django.contrib.staticfiles', 'service.mn', )

# Because the entire XML document must be in memory while being deserialized,
# limit the size that can be handled.
MAX_XML_DOCUMENT_SIZE = 1024**2
