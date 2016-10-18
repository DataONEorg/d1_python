#!/usr/bin/env python
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
"""
:mod:`settings`
===============

:Synopsis:
  App level settings.
  This file contains settings that do not normally need to be modified when
  installing GMN. See settings_site.py for site specific settings.
:Author:
  DataONE (Dahl)
"""

# Stdlib.
import os
import sys


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

BASE_DIR = os.path.dirname(os.path.dirname(make_absolute((''))))

# Add site specific settings.
from settings_site import *

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

MIDDLEWARE_CLASSES = (
  # Custom GMN middleware.
  'mn.middleware.request_handler.RequestHandler',
  'mn.middleware.exception_handler.ExceptionHandler',
  'mn.middleware.response_handler.ResponseHandler',
  'mn.middleware.profiling_handler.ProfilingHandler',
  'mn.middleware.view_handler.ViewHandler',
  'mn.middleware.startup_handler.StartupHandler',
)

TEMPLATES = [{
  'BACKEND': 'django.template.backends.django.DjangoTemplates',
  'DIRS': [
    make_absolute('../mn/templates'),
  ],
  # 'APP_DIRS': True,
  'OPTIONS': {
    'context_processors': [
      'django.contrib.auth.context_processors.auth',
      'django.template.context_processors.debug',
      'django.template.context_processors.i18n',
      'django.template.context_processors.media',
      'django.template.context_processors.static',
      'django.template.context_processors.tz',
      'django.contrib.messages.context_processors.messages',
    ],
    'loaders': [
      'django.template.loaders.filesystem.Loader',
      # 'django.template.loaders.app_directories.Loader',
    ],
  },
}, ]

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'TIMEOUT': 60 * 60,
  }
}

ROOT_URLCONF = 'mn.urls'

INSTALLED_APPS = [
  'django.contrib.staticfiles',
  'mn',
]

# Because the entire XML document must be in memory while being deserialized,
# limit the size that can be handled.
MAX_XML_DOCUMENT_SIZE = 1024**2

# Default chunk size for stream iterators.
NUM_CHUNK_BYTES = 1024**2
