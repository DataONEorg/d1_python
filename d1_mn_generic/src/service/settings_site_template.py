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


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

# ==============================================================================
# Debuging

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

# Enable request echo.
# * True: GMN will not process any requests. Instead, it will echo the requests
#   back to the client. The requests are formatted to be human readable. This
#   enables a client to see exactly what GMN receives after processing by
#   Apache, mod_wsgi and Django. It is useful for debugging both clients and
#   GMN.
# * False: GMN processes all requests as normal.
# * Only available in debug mode.
ECHO_REQUEST_OBJECT = False

# ==============================================================================
# Node parameters

# The unique identifier for this node, represented as a DataONE Node URN.
# E.g.: 'urn:node:MyMemberNode'
NODE_IDENTIFIER = 'urn:node:MyMemberNode'

# The human readable name of this node.
# E.g.: 'My Member Node'
NODE_NAME = 'My Member Node'

# Description of content maintained by this node and any other free style notes.
# E.g.: 'This DataONE Member Node is operated by My Organization. The main
# contents are sea level measurements.'
NODE_DESCRIPTION = 'Test Member Node'

# The URL at which the Node is available.
# The version tag, e.g., /v1/ is not included in this URL.
# E.g.: https://server.example.edu/app/d1/mn
NODE_BASEURL = 'https://localhost/mn'

# Enable synchronization.
# Set to False to prevent the DataONE Coordinating Nodes from synchronizing
# (discovering new content and other changes) on this node.
NODE_SYNCHRONIZE = True

# The schedule on which synchronization should run for this node. The schedule
# should reflect the frequency at which content is expected to change on the
# node. The schedule is only a hint to the CNs. The syntax for each time slot
# follows that of the Quartz Scheduler
# (http://www.quartz-scheduler.org/api/2.1.0/org/quartz/CronExpression.html).
# These settings are ignored if NODE_SYNCHRONIZE is False.
# E.g.: YEAR = '*', MONTH = '*', WEEKDAY = '?', MONTHDAY = '*', HOUR = '*',
# MINUTE = '0/3', SECOND = '0'.
NODE_SYNC_SCHEDULE_YEAR = '*'
NODE_SYNC_SCHEDULE_MONTH = '*'
NODE_SYNC_SCHEDULE_WEEKDAY = '?'
NODE_SYNC_SCHEDULE_MONTHDAY = '*'
NODE_SYNC_SCHEDULE_HOUR = '*'
NODE_SYNC_SCHEDULE_MINUTE = '0/3'
NODE_SYNC_SCHEDULE_SECOND = '0'

# The Subject of this node. The subject is the DataONE compliant serialization
# of the Distinguished Name (DN) of the X.509 client side certificate that has
# been issued for this node by DataONE. The subject must match that of the
# DN in the certificate.
# E.g.: 'CN=urn:node:MyMemberNode,DC=dataone,DC=org'
NODE_SUBJECT = 'CN=urn:node:MyMemberNode,DC=dataone,DC=org'

# The contact subject is a DataONE identity that can be contacted regarding
# issues related to this member node. The subject must match the subject as it
# is displayed for the given identity in the DataONE Identity Manager.
# E.g.: 'CN=My Name,O=Google,C=US,DC=cilogon,DC=org'
NODE_CONTACT_SUBJECT = 'CN=My Name,O=Google,C=US,DC=cilogon,DC=org'

# Signal the status of this node to the DataONE infrastructure.
# E.g.:
# 'up: This node is operating as normal.
# 'down': This node is currently not in operation.
NODE_STATE = 'up'

# Set the Tier for this node.
# For information on selecting a tier, see https://repository.dataone.org/software/cicore/trunk/mn/d1_mn_generic/doc/build/html/setup-tier.html
# Tier 1: Read, public objects
# Tier 2: Access controlled objects (authentication and authorization)
# Tier 3: Write (create, update and delete objects)
# Tier 4: Replication target
# Each tier includes all lower tiers.
# E.g.: 4
TIER = 4

# Enable monitoring.
# * Enables aspects of internal GMN operations to be monitored by public
#   subjects. This function does not expose any sensitive information and should
#   be safe to keep enabled in production.
# * When GMN_DEBUG is True, this setting is ignored and monitoring is enabled.
MONITOR = True

# Create a unique string for this node and do not share it.
SECRET_KEY = 'MySecretKey'

# Path to the client side certificate that GMN uses when initiating TLS/SSL
# connections to Coordinating Nodes. The certificate must be in PEM format.
CLIENT_CERT_PATH = '/var/local/dataone/certs/client/client.crt'

# Path to the private key for the client side certificate set in
# CLIENT_CERT_PATH. The private key must be in PEM format. This is only
# required to be set if the certificate does not contain an embedded private
# key. Otherwise, set it to None.
CLIENT_CERT_PRIVATE_KEY_PATH = '/var/local/dataone/certs/client/client.key'

# Set to True to enable this node to be used as a replication target. DataONE
# uses replication targets to store replicas of science objects. This setting is
# ignored if TIER is set less than 4. It is intended for temporarily disabling
# replication. For permanently disabling replication, set TIER lower than 4 as
# well as this setting to False.
NODE_REPLICATE = True

# The maximum size, in octets (8-bit bytes), of objects this node is willing to
# accept for replication. Set to -1 to allow any size.
# E.g. for a maximum object size of 1GiB: 1024**3
REPLICATION_MAXOBJECTSIZE = -1

# The total space, in octets (8-bit bytes), that this node is providing for
# replication. Set to -1 to provide unlimited space (not recommended).
# E.g. for a total space of 10 TiB: 10 * 1024**4
REPLICATION_SPACEALLOCATED = 10 * 1024**4

# A list of nodes for which this node is willing to replicate content. To allow
# objects from any node to be replicated, set to an empty list.
# E.g.: ('urn:node:MemberNodeA','urn:node:MemberNodeB','urn:node:MemberNodeC')
REPLICATION_ALLOWEDNODE = ()

# A list of object formats for objects which this node is willing replicate.
# To allow any object type to be replicated, set to an empty list.
# E.g.: ('eml://ecoinformatics.org/eml-2.0.0', 'CF-1.0')
REPLICATION_ALLOWEDOBJECTFORMAT = ()

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
DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT
#DATAONE_ROOT = 'https://cn-dev.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-sandbox.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-stage.dataone.org/cn/'

# Additional subjects for implicitly trusted DataONE infrastructure. Connections
# containing client side certificates with these subjects bypass access control
# rules and have access to REST interfaces meant only for use by CNs. The
# subjects in this list are added to the list of subjects that GMN creates on
# startup by reading the NodeList on the root CN of the environment configured
# in the DATAONE_ROOT setting.
DATAONE_TRUSTED_SUBJECTS = set([])

# Additional subjects for internal GMN processes. Connections containing client
# side certificates with these subjects are allowed to connect to REST services
# internal to GMN. The internal REST interfaces provide functionality required
# by the asynchronous processes. The subjects in this list is added to the
# subject of the client side certificate issued by DataONE, configured in the
# CLIENT_CERT_PATH setting.
GMN_INTERNAL_SUBJECTS = set([])

# As an alternative to the certificate based authentication for asynchronous
# GMN processes set up in GMN_INTERNAL_SUBJECTS, this setting can be used
# for allowing the processes to connect based on the IP address of the
# originating server. Note that this method may be vulnerable to IP address
# spoofing attacks.
GMN_INTERNAL_HOSTS = ['127.0.0.1', ]

# Local processes use this URL to connect to GMN.
INTERNAL_BASEURL = 'https://localhost/mn'

# In debug mode, a special test subject is added to the list of trusted
# subjects.
if GMN_DEBUG:
  DATAONE_TRUSTED_SUBJECTS.add('gmn_test_subject_trusted')

# When DEBUG=False and a view raises an exception, Django will send emails to
# these addresses with the full exception information.
ADMINS = (('My Name', 'my_address@my_email.tld'), )

# Enable MNRead.listObjects() for public and regular authenticated users.
# False:
# * MNRead.listObjects() can only be called by trusted infrastructure (CNs).
# True:
# * MNRead.listObjects() can be called by any level of user (trusted
#   infrastructure, authenticated and public), and results are filtered
#   to list only objects to which the user has access.
# The primary means for a user to discover objects is to use the search
# facilities exposed by CNs. By enabling this option, regular users can also
# discover objects directly on the node by iterating over the object list. This
# is disabled by default because the call can be expensive (as it must create a
# filtered list of all objects on the node for each page that is returned).
# These are also the reasons that DataONE specified implementation of access
# control for public and regular users to be optional for this API.
PUBLIC_OBJECT_LIST = True

# Database connection.
# GMN supports PostgreSQL and SQLite3. MySQL is NOT supported. Oracle is
# untested.
DATABASES = {
  'default': {
    # PostgreSQL
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn',

    # MySQL (currently not supported)
    #'ENGINE': 'django.db.backends.mysql',
    #'NAME': 'gmn',

    # SQLite3
    #'ENGINE': 'django.db.backends.sqlite3',
    #'NAME': make_absolute('./gmn.sqlite'),

    # When using PostgreSQL, set these to match the username and password
    # specified for the gmn user during the PostgreSQL install. These are not
    # used for SQLite3.
    'USER': 'gmn',
    'PASSWORD': 'gmn',

    # Set HOST to empty string for localhost.
    'HOST': '',

    # Set PORT to empty string for default.
    'PORT': '',
  }
}

# Paths to the GMN data stores. The bytes of all the objects handled by GMN are
# stored here. By default, these are below the service folder. Typically,
# these are changed to use an area that is dedicated for storage, for instance
# a separate filesystem / disk.
MEDIA_ROOT = make_absolute('./stores') # relative location
#MEDIA_ROOT = '/mnt/my_large_disk/dataone/' # example for absolute location
SYSMETA_STORE_PATH = os.path.join(MEDIA_ROOT, 'sysmeta')
OBJECT_STORE_PATH = os.path.join(MEDIA_ROOT, 'object')

# Path to the log file.
LOG_PATH = make_absolute('./gmn.log')

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

# ==============================================================================
# Validation of settings.


def check_path(path):
  if path is None:
    return
  if not os.path.exists(path):
    raise Exception('Invalid path: {0}'.format(path))


check_path(CLIENT_CERT_PATH)
check_path(CLIENT_CERT_PRIVATE_KEY_PATH)

if SECRET_KEY == 'MySecretKey':
  raise Exception('SECRET_KEY is unset. See install documentation.')
