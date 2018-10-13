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
"""Default settings for GMN
- These settings are only used as fallbacks in case the corresponding settings
in settings.py are missing.
- This allows settings to be added without having to modify settings.py
in existing deployments.
- The settings are described in settings.py.
"""

# noinspection PyUnresolvedReferences
# flake8: noqa: F403,F401

from d1_gmn.app.settings_default import *

import d1_common.const
import d1_common.util

#import logging
#import d1_common.const

DEBUG = False
DEBUG_GMN = False
DEBUG_PYCHARM = False
DEBUG_PYCHARM_BIN = 'pycharm.sh'
DEBUG_ECHO_REQUEST = False
DEBUG_PROFILE_SQL = False

STAND_ALONE = True

TRUST_CLIENT_SUBMITTER = False
TRUST_CLIENT_ORIGINMEMBERNODE = False
TRUST_CLIENT_AUTHORITATIVEMEMBERNODE = False
TRUST_CLIENT_DATESYSMETADATAMODIFIED = False
TRUST_CLIENT_SERIALVERSION = False
TRUST_CLIENT_DATEUPLOADED = False

ALLOWED_HOSTS = [
  'localhost',
  '127.0.0.1',
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

LOG_IGNORE_USER_AGENT = []
LOG_IGNORE_IP_ADDRESS = []
LOG_IGNORE_SUBJECT = []
LOG_IGNORE_TRUSTED_SUBJECT = True
LOG_IGNORE_NODE_SUBJECT = True

CLIENT_CERT_PATH = '/var/local/dataone/certs/client/client_cert.pem'
CLIENT_CERT_PRIVATE_KEY_PATH = '/var/local/dataone/certs/client/client_key_nopassword.pem'

NODE_REPLICATE = False

REPLICATION_MAXOBJECTSIZE = -1
REPLICATION_SPACEALLOCATED = 10 * 1024**3
REPLICATION_ALLOWEDNODE = ()
REPLICATION_ALLOWEDOBJECTFORMAT = ()
REPLICATION_MAX_ATTEMPTS = 24
REPLICATION_ALLOW_ONLY_PUBLIC = False

SYSMETA_REFRESH_MAX_ATTEMPTS = 24

DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT

DATAONE_TRUSTED_SUBJECTS = set([])

ADMINS = (('unset', 'unset@unset.tld'),)
PUBLIC_OBJECT_LIST = True
PUBLIC_LOG_RECORDS = True
REQUIRE_WHITELIST_FOR_UPDATE = True
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn2',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    'ATOMIC_REQUESTS': True,
  }
}

OBJECT_STORE_PATH = '/var/local/dataone/gmn_object_store'

RESOURCE_MAP_CREATE = 'block'

SCIMETA_VALIDATION_ENABLED = True
SCIMETA_VALIDATION_MAX_SIZE = 100 * 1024**2
SCIMETA_VALIDATION_OVER_SIZE_ACTION = 'reject'

PROXY_MODE_BASIC_AUTH_ENABLED = False
PROXY_MODE_BASIC_AUTH_USERNAME = ''
PROXY_MODE_BASIC_AUTH_PASSWORD = ''
PROXY_MODE_STREAM_TIMEOUT = 30

LOG_PATH = d1_common.util.abs_path('../gmn.log')

MAX_XML_DOCUMENT_SIZE = 10 * 1024**2
NUM_CHUNK_BYTES = 1024**2
SESSION_COOKIE_SECURE = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
MEDIA_URL = ''
STATIC_URL = '/static/'

if DEBUG or DEBUG_GMN:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'INFO'

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
    'simple': {
      'format': '%(levelname)s %(message)s'
    },
  },
  'handlers': {
    'file': {
      'level': LOG_LEVEL,
      'class': 'logging.FileHandler',
      'filename': LOG_PATH,
      'formatter': 'verbose'
    },
    'null': {
      'level': LOG_LEVEL,
      'class': 'logging.NullHandler',
    },
  },
  'loggers': {
    # The "catch all" logger is denoted by ''.
    '': {
      'handlers': ['file'],
      'propagate': True,
      'level': LOG_LEVEL,
    },
    # Django uses this logger.
    'django': {
      'handlers': ['file'],
      'propagate': False,
      'level': LOG_LEVEL
    },
    # Messages relating to the interaction of code with the database. For
    # example, every SQL statement executed by a request is logged at the DEBUG
    # level to this logger.
    'django.db.backends': {
      'handlers': ['null'],
      'level': 'WARNING',
      'propagate': False
    },
  }
}

MIDDLEWARE = (
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
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

TEMPLATE_CONTEXT_PROCESSORS = ('app.context_processors.global_settings',)

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'TIMEOUT': 60 * 60,
  }
}

ROOT_URLCONF = 'd1_gmn.app.urls'

INSTALLED_APPS = [
  # These are required in order for 404 not to trigger 500 when DEBUG=False
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.staticfiles',
  # App for GMN configuration and startup checks (list before the GMN main app)
  'd1_gmn.app.startup.GMNStartupChecks',
  # GMN main app
  'd1_gmn.app',
]

SECRET_KEY = '<Do not modify this placeholder value>'

MAX_SLICE_ITEMS = 5000
