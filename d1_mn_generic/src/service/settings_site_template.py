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
'''

# Stdlib.
import os
import sys

# D1.
import d1_common.const

# Given a relative path that is relative to the path of this module, create
# an absolute path.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

# The name under which this Member Node was registered with DataONE.
# On the form, "urn:node:*"
NODE_IDENTIFIER = 'urn:node:mnMyDataONEMemberNode'

# Create a unique string for this node and do not share it.
SECRET_KEY = 'MySecretKey'

# Enable Django debug mode.
# True:
# * May expose sensitive information.
# * GMN returns a HTML Django exception page with extensive debug information
#   for internal errors.
# * GMN returns a HTML Django 404 page that lists all valid URL patterns for
#   invalid URLs.
# * The profiling subsystem can be accessed.
# False:
# * Use for production.
# * GMN returns a stack trace in a DataONE ServiceFailure exception for
#   internal errors.
# * GMN returns a regular 404 page for invalid URLs. The page contains a link
#   to the GMN home page.
DEBUG = False

# Enable GMN debug mode.
# True:
# * Enables GMN functionality that should be accessible only during testing and
#   debugging. Use only when there is no sensitive information on the MN.
# * Clients can override all access control rules and retrieve, delete or
#   replace any object on the MN.
# * Skips authentication check for trusted subjects, async processes and
#   create/update/delete.
# False:
# * Use for production.
GMN_DEBUG = False

# Enable monitoring.
# * Enables aspects of internal GMN operations to be monitored by public
#   subjects. This function does not expose any sensitive information and should
#   be safe to keep enabled in production.
# * When GMN_DEBUG is True, this setting is ignored and monitoring is enabled.
MONITOR = True

# Enable request echo.
# * True: GMN will not process any requests. Instead, it will echo the requests
#   back to the client. The requests are formatted to be human readable. This
#   enables a client to see exactly what GMN receives after processing by
#   Apache, mod_wsgi and Django. It is useful for debugging both clients and
#   GMN.
# * False: GMN processes all requests as normal.
# * Only available in debug mode.
ECHO_REQUEST_OBJECT = False

# Set the level of logging that GMN should perform. Choices are:
# DEBUG, INFO, WARNING, ERROR, CRITICAL or NOTSET.
if DEBUG or GMN_DEBUG:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'WARNING'

# On startup, GMN connects to the DataONE root CN to discover details about the
# DataONE environment. For a production instance of GMN, this should be set to
# the default DataONE root for production systems. For test instances of GMN,
# this should be set to the root of the environment in which GMN is to run.
# If GMN_DEBUG is True, the trusted subjects are not required, as the
# authentication checks for them are skipped. Therefore, they are not retrieved.
#DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT
#DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-sandbox.test.dataone.org/cn'
DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn/'

# Subjects for implicitly trusted DataONE infrastructure. Connections containing
# client side certificates with these subjects bypass access control rules and
# have access to REST interfaces meant only for use by CNs.
DATAONE_TRUSTED_SUBJECTS = set([])

# Subjects for asynchronous GMN processes. Connections containing client side
# certificates with these subjects are allowed to connect to REST services
# internal to GMN. The internal REST interfaces provide functionality required
# by the asynchronous components.
GMN_INTERNAL_SUBJECTS = set([])

# As an alternative to the certificate based authentication for asynchronous
# GMN processes set up in GMN_INTERNAL_SUBJECTS, this setting can be used
# for allowing the processes to connect based on the IP address of the
# originating server.
GMN_INTERNAL_HOSTS = ['127.0.0.1', ]

# In debug mode, a special test subject is added to the list of trusted
# subjects.
if GMN_DEBUG:
  DATAONE_TRUSTED_SUBJECTS.add('gmn_test_subject_trusted')

# When DEBUG=False and a view raises an exception, Django will send emails to
# these addresses with the full exception information.
ADMINS = (('Your Name', 'your-email@your-email.tld'), )

# Database connection.
# GMN supports PostgreSQL and SQLite3. MySQL is NOT supported. Oracle is
# untested.
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3', # SQLite3
    'NAME': _here('gmn.sqlite'),
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2', # PostgreSQL
    #    'NAME': 'gmn',
    'USER': 'gmn',
    'PASSWORD': 'gmn',
    'HOST': '', # Set to empty string for localhost.
    'PORT': '', # Set to empty string for default.
  }
}

# Path to the directory that holds media.
MEDIA_ROOT = _here('stores')

# Paths to the GMN data stores. The bytes of all the objects handled by
# GMN are stored here.
SYSMETA_STORE_PATH = os.path.join(MEDIA_ROOT, 'sysmeta')
OBJECT_STORE_PATH = os.path.join(MEDIA_ROOT, 'object')
STATIC_STORE_PATH = os.path.join(MEDIA_ROOT, 'static')

# The Node Registry XML Document
NODE_REGISTRY_XML_PATH = os.path.join(STATIC_STORE_PATH, 'nodeRegistry.xml')

# Path to the log file.
LOG_PATH = _here('./gmn.log')

# Set up logging.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': True,
  'formatters': {
    'verbose': {
        'format': '%(asctime)s %(levelname)-8s %(name)s %(module)s ' \
                  '%(process)d %(thread)d %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
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
    'null': {
      'level': 'DEBUG',
      'class': 'django.utils.log.NullHandler',
    },
  },
  'loggers': {
    # The "catch all" logger is denoted by ''.
    '': {
      'handlers': ['file'],
      'propagate': True,
      'level': 'DEBUG',
    },
    # Django uses this logger.
    'django': {
      'handlers': ['file'],
      'propagate': True,
      'level': 'DEBUG', #LOG_LEVEL,
    },
    # Messages relating to the interaction of code with the database. For
    # example, every SQL statement executed by a request is logged at the DEBUG
    # level to this logger.
    'django.db.backends': {
      'handlers': ['null'],
      # Set logging level to "WARNING" to suppress logging of SQL statements.
      'level': 'WARNING',
      'propagate': False
    },
  }
}
