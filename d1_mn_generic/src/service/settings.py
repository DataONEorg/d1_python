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
:mod:`settings`
===============

:Synopsis:
  App level settings.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import os
import sys

# Discover the path of this module
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

# Member Node configuration.

# Enable functionality that should only be accessible during testing and
# debugging.
GMN_DEBUG = True

# Enable Django debug mode. Causes Django to return a page with extensive
# debug information if a bug is encountered while servicing a request.
DEBUG = True

# TODO: Check this setting.
TEMPLATE_DEBUG = DEBUG

# Only set cookies when running through SSL.
SESSION_COOKIE_SECURE = True

ADMINS = (
  # ('<name>', '<email address>'),
)

MANAGERS = ADMINS

DATABASES = {
  'default': {
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': _here('gmn.sq3'), # Or path to database file if using sqlite3.
    'USER': '', # Not used with sqlite3.
    'PASSWORD': '', # Not used with sqlite3.
    'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '', # Set to empty string for default. Not used with sqlite3.
  }
}

# GMN must run in the UTC time zone. This is not compatible with running
# Django under Windows because under Windows, Django's time zone must be set
# to match the system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = _here('stores')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# GMN stores.
SYSMETA_STORE_PATH = os.path.join(MEDIA_ROOT, 'sysmeta')
OBJECT_STORE_PATH = os.path.join(MEDIA_ROOT, 'object')
STATIC_STORE_PATH = os.path.join(MEDIA_ROOT, 'static')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(ok#4)+n++u0#x&j1-xsy)u8fijlyv&ycn2t(@cys$ozawzlb-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.load_template_source',
  'django.template.loaders.app_directories.load_template_source',
  'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  #'django.middleware.profile.ProfileMiddleware',
  # TransactionMiddleware causes each view to be wrapped in an implicit
  # transaction. The transaction is automatically committed on successful
  # return from the view and rolled back otherwise.
  'django.middleware.transaction.TransactionMiddleware',
  'service.mn.middleware.request_handler.request_handler',
  'service.mn.middleware.exception_handler.exception_handler',
  'service.mn.middleware.response_handler.response_handler',
  'service.mn.middleware.view_handler.view_handler',

  #    'service.cn.middleware.request_handler.request_handler',
  #    'service.cn.middleware.exception_handler.exception_handler',
  #    'service.cn.middleware.response_handler.response_handler',
  #    'service.cn.middleware.view_handler.view_handler',
)

ROOT_URLCONF = 'service.urls'

TEMPLATE_DIRS = (_here('mn/templates'), _here('cn/templates'), )

FIXTURE_DIRS = (_here('mn/fixtures'), _here('cn/fixtures'), )

INSTALLED_APPS = (
  'service.mn',
  'service.cn',

  #    'django.contrib.auth',
  'django.contrib.contenttypes',
  #    'django.contrib.sessions',
  #    'django.contrib.sites',
  'django.contrib.admin',
  'django.contrib.admindocs',
)

# TODO: May be able to simplify url regexes by turning this on.
APPEND_SLASH = False

LOG_PATH = _here('./gmn.log')
XSD_PATH = _here('./coordinating_node_sysmeta.xsd')
ROOT_PATH = _here('./')

# Test CN.
CN_SYSMETA_STORE_PATH = _here('./cn_sysmeta_store')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './lib')))

## Set up logging.
## We output everything to both file and stdout.
#logging.getLogger('').setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S')
## Log file.
#file_logger = logging.FileHandler(settings.LOG_PATH, 'a')
#file_logger.setFormatter(formatter)
#logging.getLogger('').addHandler(file_logger)
## Console.
##console_logger = StreamHandler(sys.stdout)
##console_logger.setFormatter(formatter)
##getLogger('').addHandler(console_logger)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s %(module)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
  #    'filters': {
  #        'special': {
  #            '()': 'project.logging.SpecialFilter',
  #            'foo': 'bar',
  #        }
  #    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
      #        'mail_admins': {
      #            'level': 'ERROR',
      #            'class': 'django.utils.log.AdminEmailHandler',
      #            'filters': ['special']
      #        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
      #        'django.request': {
      #            'handlers': ['mail_admins'],
      #            'level': 'ERROR',
      #            'propagate': False,
      #        },
      #        'myproject.custom': {
      #            'handlers': ['console', 'mail_admins'],
      #            'level': 'INFO',
      #            'filters': ['special']
      #        }
    }
}
