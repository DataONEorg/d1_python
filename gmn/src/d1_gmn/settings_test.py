# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

from __future__ import absolute_import

import logging

import d1_common.const
# noinspection PyUnresolvedReferences
import d1_common.util

DEBUG = True
DEBUG_GMN = True
DEBUG_PYCHARM = False
DEBUG_PYCHARM_BIN = 'pycharm.sh'
DEBUG_ECHO_REQUEST = False
DEBUG_ALLOW_INTEGRATION_TESTS = False

STAND_ALONE = True

TRUST_CLIENT_SUBMITTER = True
TRUST_CLIENT_ORIGINMEMBERNODE = True
TRUST_CLIENT_AUTHORITATIVEMEMBERNODE = True
TRUST_CLIENT_DATESYSMETADATAMODIFIED = True
TRUST_CLIENT_SERIALVERSION = True
TRUST_CLIENT_DATEUPLOADED = True

MONITOR = True
ALLOWED_HOSTS = [
  'localhost',
  '127.0.0.1', # Allow local connections.
  #'my.server.name.com', # Add to allow GMN to be accessed by name from remote server.
  #'my.external.ip.address', # Add to allow GMN to be accessed by ip from remote server.
]
NODE_IDENTIFIER = 'urn:node:MyMemberNode'
NODE_NAME = 'My Member Node'
NODE_DESCRIPTION = 'Test Member Node'
NODE_BASEURL = 'https://localhost/mn'
NODE_SYNCHRONIZE = True

NODE_SYNC_SCHEDULE_YEAR = '*'
NODE_SYNC_SCHEDULE_MONTH = '*'
NODE_SYNC_SCHEDULE_WEEKDAY = '?'
NODE_SYNC_SCHEDULE_MONTHDAY = '*'
NODE_SYNC_SCHEDULE_HOUR = '*'
NODE_SYNC_SCHEDULE_MINUTE = '42'
NODE_SYNC_SCHEDULE_SECOND = '0'

NODE_SUBJECT = 'CN=urn:node:MyMemberNode,DC=dataone,DC=org'
NODE_CONTACT_SUBJECT = 'CN=My Name,O=Google,C=US,DC=cilogon,DC=org'
NODE_STATE = 'up'

CLIENT_CERT_PATH = None
CLIENT_CERT_PRIVATE_KEY_PATH = None

NODE_REPLICATE = False

REPLICATION_MAXOBJECTSIZE = -1
REPLICATION_SPACEALLOCATED = 10 * 1024**3
REPLICATION_ALLOWEDNODE = ()
REPLICATION_ALLOWEDOBJECTFORMAT = ()
REPLICATION_MAX_ATTEMPTS = 24

SYSMETA_REFRESH_MAX_ATTEMPTS = 24

DATAONE_ROOT = 'http://mock/root/cn'
DATAONE_TRUSTED_SUBJECTS = set([])

ADMINS = (('Test Admin', 'admin@test.tld'),)

PUBLIC_OBJECT_LIST = True
PUBLIC_LOG_RECORDS = True

REQUIRE_WHITELIST_FOR_UPDATE = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'test_gmn2',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    # Transactions
    'ATOMIC_REQUESTS': False,
    'AUTOCOMMIT': False,
  },
  'template': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'test_gmn2_templ',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    # Transactions
    'ATOMIC_REQUESTS': False,
    'AUTOCOMMIT': False,
  },
}

OBJECT_STORE_PATH = '/tmp/gmn_test_obj_store'

PROXY_MODE_BASIC_AUTH_ENABLED = False
PROXY_MODE_BASIC_AUTH_USERNAME = ''
PROXY_MODE_BASIC_AUTH_PASSWORD = ''
PROXY_MODE_STREAM_TIMEOUT = 30

LOG_PATH = d1_common.util.abs_path('/tmp/gmn_test.log')
MAX_XML_DOCUMENT_SIZE = 10 * 1024**2
NUM_CHUNK_BYTES = 1024**2
SESSION_COOKIE_SECURE = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
MEDIA_URL = ''
STATIC_URL = '/static/'

# Capture everything that is logged
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format':
        '%(asctime)s %(levelname)-8s %(name)s %(module)s '
        '%(process)d %(thread)d %(message)s',
      'datefmt': '%Y-%m-%d %H:%M:%S'
    },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'verbose',
      'level': logging.DEBUG,
      'stream': 'ext://sys.stdout',
    },
  },
  'loggers': {
    '': {
      'handlers': ['console'],
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
    },
    # SQL query profiling
    # 'django.db.backends': {
    #   'handlers': ['console'],
    #   'level': logging.DEBUG,
    #   'propagate': False,
    # },
    # 'django.db.backends.schema': {
    #   # don't log schema queries, django >= 1.7
    #   'propagate': False,
    # },
  }
}

MIDDLEWARE_CLASSES = (
  # Custom GMN middleware.
  'd1_gmn.app.middleware.request_handler.RequestHandler',
  'd1_gmn.app.middleware.exception_handler.ExceptionHandler',
  'd1_gmn.app.middleware.response_handler.ResponseHandler',
  'd1_gmn.app.middleware.profiling_handler.ProfilingHandler',
  'd1_gmn.app.middleware.view_handler.ViewHandler',
)

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
      d1_common.util.abs_path('./app/templates'), # noqa: F405
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
  },
]

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'TIMEOUT': 60 * 60,
  }
}

ROOT_URLCONF = 'd1_gmn.app.urls'

INSTALLED_APPS = [
  'django.contrib.staticfiles',
  'd1_gmn.app',
  'd1_gmn.app.startup.GMNStartupChecks',
]

SECRET_KEY = '<Do not modify this placeholder value>'
