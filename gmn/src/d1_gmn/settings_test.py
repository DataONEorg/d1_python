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
"""Test and debug settings for GMN
- These settings are in effect when GMN is called through unit tests.
"""

# noinspection PyUnresolvedReferences
# flake8: noqa: F403,F401

import logging
import warnings
import d1_common.util

from d1_gmn.app.settings_default import *

# When running tests, turn Django's RuntimeWarning into exception
warnings.filterwarnings(
  'error', r"DateTimeField .* received a naive datetime", RuntimeWarning,
  r'django\.db\.models\.fields'
)

DEBUG = True
DEBUG_GMN = True
DEBUG_ECHO_REQUEST = False
DEBUG_PROFILE_SQL = False

STAND_ALONE = True

TRUST_CLIENT_SUBMITTER = True
TRUST_CLIENT_ORIGINMEMBERNODE = True
TRUST_CLIENT_AUTHORITATIVEMEMBERNODE = True
TRUST_CLIENT_DATESYSMETADATAMODIFIED = True
TRUST_CLIENT_SERIALVERSION = True
TRUST_CLIENT_DATEUPLOADED = True

NODE_IDENTIFIER = 'urn:node:GMNUnitTestInstance'
NODE_NAME = 'GMN Unit Test Instance'
NODE_DESCRIPTION = 'GMN instance launched via pytest'
NODE_BASEURL = 'https://localhost/mn'

NODE_SUBJECT = 'CN=urn:node:GMNUnitTestInstance,DC=dataone,DC=org'
NODE_CONTACT_SUBJECT = 'CN=NodeContactSubject,O=Google,C=US,DC=cilogon,DC=org'

CLIENT_CERT_PATH = None
CLIENT_CERT_PRIVATE_KEY_PATH = None
OBJECT_STORE_PATH = '/tmp/gmn_test_obj_store'
LOG_PATH = d1_common.util.abs_path('/tmp/gmn_test.log')

DATAONE_ROOT = 'http://mock/root/cn'

ADMINS = (('GMN Unit Test Admin', 'admin@test.tld'),)

RESOURCE_MAP_CREATE = 'block'

PROXY_MODE_BASIC_AUTH_ENABLED = False
PROXY_MODE_BASIC_AUTH_USERNAME = ''
PROXY_MODE_BASIC_AUTH_PASSWORD = ''
PROXY_MODE_STREAM_TIMEOUT = 30

MAX_XML_DOCUMENT_SIZE = 10 * 1024**2
NUM_CHUNK_BYTES = 1024**2
MAX_SLICE_ITEMS = 5000

# mk_db_fixture:
# - Uses DATABASES.default
# - The default database is flushed then populated with test data by
# mk_db_fixture
#
# Unit tests:
# - Use DATABASES.default.NAME as a base name for temporary databases created
# from the template database.
# - Use DATABASES.template.NAME as the source database name when creating
# databases from template.

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn_test_db',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    'ATOMIC_REQUESTS': False,
    # 'AUTOCOMMIT': False,
  },
  'template': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn_test_db_template',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    'ATOMIC_REQUESTS': False,
    # 'AUTOCOMMIT': False,
  },
}

STATIC_SERVER = True

# Capture everything that is logged and write it to stdout.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
      'format': '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s',
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
      'level': logging.DEBUG,
      'propagate': True
    },
  }
}

FIXTURE_DIRS = (
  d1_common.util.abs_path('./fixtures'),
)
