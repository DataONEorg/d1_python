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
:mod:`settings_site`
====================

:Synopsis:
  Site specific app level settings.

  This file contains settings that are specific for an instance of GMN.

:Author:
  DataONE (Dahl)

:Dependencies:
  - python 2.6
'''

# Generic Member Node instance configuration. These settings are unique for
# a given instance of GMN.

IDENTIFIER = 'GMN_TEST'
NAME = 'GMN TEST'
DESCRIPTION = 'GMN'
BASE_URL = 'http://localhost:8000'
REPLICATE = TRUE
SYNCHRONIZE = TRUE
NODE_TYPE = MN

SERVICE_NAME = "GMN TEST"
SERVICE_VERSION = '0.5'
SERVICE_AVAILABLE = TRUE

GMN_SERVICE_NAME = 'test_gmn'

# Enable debug mode.
# * WARNING: IN DEBUG MODE, CLIENTS CAN OVERRIDE ALL ACCESS CONTROL RULES AND
#   RETRIEVE, DELETE OR REPLACE ANY OBJECT ON THE MEMBER NODE.
# * Enables GMN functionality that should be accessible only during testing and
#   debugging.
# * Causes Django to return a page with extensive debug information if a bug is
#   encountered while servicing a request.
DEBUG = True

# Enable Django exception page for internal errors.
# * True: GMN will return a Django exception page for internal errors.
# * False: GMN returns a stack trace in a DataONE ServiceFailure exception for
#   internal errors.
# * Only available in debug mode. In production, GMN never returns a Django
#   exception page.
GET_DJANGO_EXCEPTION_IN_BROWSER = False

# Set the level of logging that GMN should perform. Choices are:
# DEBUG, INFO, WARNING, ERROR, CRITICAL or NOTSET.
if DEBUG:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'WARNING'

DATABASES = {
  'default': {
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn',
    'USER': 'gmn',
    'PASSWORD': 'gmn',
    'HOST': '', # Set to empty string for localhost.
    'PORT': '', # Set to empty string for default.
  }
}

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = _here('stores')

# GMN stores.
SYSMETA_STORE_PATH = os.path.join(MEDIA_ROOT, 'sysmeta')
OBJECT_STORE_PATH = os.path.join(MEDIA_ROOT, 'object')
STATIC_STORE_PATH = os.path.join(MEDIA_ROOT, 'static')

LOG_PATH = _here('./gmn.log')
XSD_PATH = _here('./coordinating_node_sysmeta.xsd')
ROOT_PATH = _here('./')

# Set up logging.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
              'format': '%(asctime)s %(module)s %(levelname)-8s %(message)s',
              'datefmt': '%y/%m/%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': LOG_LEVEL,
        },
    }
}
