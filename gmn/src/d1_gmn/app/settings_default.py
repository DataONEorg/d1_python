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
- Settings that are not described here are described in settings_template.py.
"""

# noinspection PyUnresolvedReferences
# flake8: noqa: F403,F401

import os.path

import d1_common.const
import d1_common.util

DEBUG = False
DEBUG_GMN = False
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
NODE_SUBJECT = 'CN=urn:node:MyMemberNode,DC=dataone,DC=org'
NODE_CONTACT_SUBJECT = 'CN=My Name,O=Google,C=US,DC=cilogon,DC=org'
NODE_STATE = 'up'
NODE_LOGO_ROOT = (
  'https://raw.githubusercontent.com/'
  'DataONEorg/member-node-info/master/production/graphics/web/'
)
NODE_SYNC_SCHEDULE_YEAR = '*'
NODE_SYNC_SCHEDULE_MONTH = '*'
NODE_SYNC_SCHEDULE_WEEKDAY = '?'
NODE_SYNC_SCHEDULE_MONTHDAY = '*'
NODE_SYNC_SCHEDULE_HOUR = '*'
NODE_SYNC_SCHEDULE_MINUTE = '42'
NODE_SYNC_SCHEDULE_SECOND = '0'

LOG_IGNORE_USER_AGENT = []
LOG_IGNORE_IP_ADDRESS = []
LOG_IGNORE_SUBJECT = []
LOG_IGNORE_TRUSTED_SUBJECT = True
LOG_IGNORE_NODE_SUBJECT = True

CLIENT_CERT_PATH = '/var/local/dataone/certs/client/client_cert.pem'
CLIENT_CERT_PRIVATE_KEY_PATH = '/var/local/dataone/certs/client/client_key_nopassword.pem'

OBJECT_STORE_PATH = '/var/local/dataone/gmn_object_store'
LOG_PATH = d1_common.util.abs_path('../gmn.log')

NODE_REPLICATE = False

REPLICATION_MAXOBJECTSIZE = -1
REPLICATION_SPACEALLOCATED = 10 * 1024**3
REPLICATION_ALLOWEDNODE = ()
REPLICATION_ALLOWEDOBJECTFORMAT = ()
REPLICATION_MAX_ATTEMPTS = 24
REPLICATION_ALLOW_ONLY_PUBLIC = False

SYSMETA_REFRESH_MAX_ATTEMPTS = 24

DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT
DATAONE_SEARCH = d1_common.const.URL_DATAONE_SEARCH

DATAONE_TRUSTED_SUBJECTS = set([])

ADMINS = (('unset', 'unset@unset.tld'),)

PUBLIC_OBJECT_LIST = True
PUBLIC_LOG_RECORDS = True
REQUIRE_WHITELIST_FOR_UPDATE = True

RESOURCE_MAP_CREATE = 'block'

SCIMETA_VALIDATION_ENABLED = True
SCIMETA_VALIDATION_MAX_SIZE = 100 * 1024**2
SCIMETA_VALIDATION_OVER_SIZE_ACTION = 'reject'

PROXY_MODE_BASIC_AUTH_ENABLED = False
PROXY_MODE_BASIC_AUTH_USERNAME = ''
PROXY_MODE_BASIC_AUTH_PASSWORD = ''
PROXY_MODE_STREAM_TIMEOUT = 30

MAX_XML_DOCUMENT_SIZE = 10 * 1024**2
NUM_CHUNK_BYTES = 1024**2
MAX_SLICE_ITEMS = 5000

# Serving of static files, such as images

# For security and performance reasons, Django only serves static files when
# DEBUG=True. This stops the UI from working when testing GMN in production
# mode.
# False (default):
# - GMN only serves static files when DEBUG=True.
# True:
# - GNM always serves static files. This is not safe for production.
STATIC_SERVER = False

STATIC_URL = '/static/'
STATIC_ROOT = d1_common.util.abs_path('./static')

# Postgres database connection.
DATABASES = {
  'default': {
    # Postgres
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    # The database in tables required by GMN are stored. The database itself
    # is typically owned by the postgres user while the tables are owned by the
    # gmn user.
    'NAME': 'gmn3',
    # By default, GMN uses Postgres Peer authentication, which does not
    # require a username and password.
    'USER': '',
    'PASSWORD': '',
    # Set HOST to empty string for localhost.
    'HOST': '',
    # Set PORT to empty string for default.
    'PORT': '',
    # Wrap each HTTP request in an implicit transaction. The transaction is
    # rolled back if the view does not return successfully. Upon a successful
    # return, the transaction is committed, thus making all modifications that
    # the view made to the database visible simultaneously, bringing the
    # database directly from one valid state to the next.
    #
    # Transactions are also important for views that run only select queries and
    # run more than a single query, as they hide any transitions between valid
    # states that may happen between queries.
    #
    # Do not change ATOMIC_REQUESTS from "True", as implicit transactions form
    # the basis of concurrency control in GMN.
    'ATOMIC_REQUESTS': True,
  }
}

# Logging

LOG_LEVEL = 'DEBUG' if DEBUG or DEBUG_GMN else 'INFO'

# Write log files to /var/local/dataone/logs if the directory exists. Else,
# write to the root of the d1_gmn package directory.
LOG_FILE_PATH = (
  '/var/local/dataone/logs/gmn.log' if os.path.isdir('/var/local/dataone/logs')
  else d1_common.util.abs_path('../gmn.log')
)

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
    # Write logs to a rotating set of files, much like logrotate.
    'rotating_file': {
      'level': LOG_LEVEL,
      'class': 'logging.handlers.RotatingFileHandler',
      'filename': LOG_FILE_PATH,
      'maxBytes': 10 * 1024 * 1024,
      'backupCount': 5,
      'formatter': 'verbose',
    },
    # Write logs to stdout. Useful when running via ./manage.py runserver.
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'verbose',
      'level': LOG_LEVEL,
      'stream': 'ext://sys.stdout',
    },
  },
  'loggers': {
    # The "catch all" logger is at the root of the tree, denoted by ''.
    '': {
      'handlers': ['rotating_file'],
      'level': LOG_LEVEL,
      'propagate': True
    },
    # Examples for how to capture and redirect log records written by loggers
    # below the root logger in the tree. When these are disabled, all logs
    # flow to the root logger.
    #
    # Root of the Django loggers.
    # 'django': {
    #   'handlers': ['rotating_file'],
    #   'propagate': False,
    #   'level': LOG_LEVEL
    # },
    # Messages related to database interactions. Every SQL statement executed by
    # a request is logged at the DEBUG level to this logger. Suppress by setting
    # the level to "WARNING".
    # 'django.db.backends': {
    #   'handlers': ['rotating_file'],
    #   'level': 'WARNING',
    #   'propagate': False
    # },
    # Log messages related to the handling of requests.
    # 'django.request': {
    #   'handlers': ['rotating_file'],
    #   'level': LOG_LEVEL,
    #   'propagate': False
    # },
    # Set propagate to False without setting a handler in order to suppress
    # messages from specific loggers.
    #
    # Suppress schema queries
    # 'django.db.backends.schema': {
    #   'propagate': False,
    # },
  }
}

MIDDLEWARE = (
  'd1_gmn.app.middleware.request_handler.RequestHandler',
  'd1_gmn.app.middleware.exception_handler.ExceptionHandler',
  'd1_gmn.app.middleware.response_handler.ResponseHandler',
  # 'd1_gmn.app.middleware.profiling_handler.ProfilingHandler',
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
  # Check settings and start GMN
  'd1_gmn.app.gmn.Startup',
]

# Django uses SECRET_KEY for a number of security related features, such as
# salting passwords, signing cookies and securing sessions. DataONE uses a
# different security model based on X.509 certificates and JSON Web Tokens, so
# SECRET_KEY is currently unused. However, to guard against future changes in
# Django that may cause this setting to be used, GMN automatically generates a
# persistent SECRET_KEY, which is used instead of the placeholder value
# specified here. Also see SECRET_KEY_PATH setting.
SECRET_KEY = '<Do not modify this placeholder value>'

# Path to file holding the secret key. Typically, the file does not exist when
# GMN is first installed, and is automatically created and written with a
# generated key when GMN is first launched after install. If the file exists,
# the contents are used as the key. The file and key may be created manually if
# desired. The parent directories must exist. Also see the SECRET_KEY setting.
SECRET_KEY_PATH = d1_common.util.abs_path('./secret_key.txt')

# Only set cookies when running through SSL.
# Default: True
SESSION_COOKIE_SECURE = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Django's internationalization support is not used by GMN.
#
# False (default):
# - Django will skip loading some of the internationalization machinery.
# True:
# - Internationalization is supported.
USE_I18N = False

USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Not used by GMN.
# Default: ''
MEDIA_URL = ''
