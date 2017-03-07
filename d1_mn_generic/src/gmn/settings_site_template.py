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
"""Global settings for GMN

This file contains settings that are specific to an instance of GMN.
"""

from __future__ import absolute_import
import d1_common.const

# ==============================================================================
# Debugging

# Enable Django debug mode.
# True:
# - Use only for debugging and testing on non-production instances.
# - May expose sensitive information.
# - GMN returns a HTML Django exception page with extensive debug information
#   for internal errors.
# - GMN returns a HTML Django 404 page that lists all valid URL patterns for
#   invalid URLs.
# - The profiling subsystem can be accessed.
# False (default):
# - Use for production.
# - GMN returns a stack trace in a DataONE ServiceFailure exception for
#   internal errors.
# - GMN returns a regular 404 page for invalid URLs. The page contains a link
#   to the GMN home page.
DEBUG = False

# Enable GMN debug mode.
# True:
# - Enables GMN functionality that should be accessible only during testing and
#   debugging. Use only when there is no sensitive information on the MN.
# - Clients can override all access control rules and authentication checks, and
#   retrieve, delete or replace any object on the MN.
# - Required for running the integration tests (gmn_integration_tests.py). Also
#   see ALLOW_INTEGRATION_TESTS.
# False (default):
# - Use for production.
DEBUG_GMN = False

# Enable PyCharm debugging.
# True:
# - If GMN encounters an unhandled internal exception, GMN will attempt to move
#   the cursor in the PyCharm IDE to the code that was being executed when the
#   exception was raised. The exception is then handled as normal.
# False (default):
# - GMN handles exceptions as normal.
DEBUG_PYCHARM = False

# Path to the PyCharm IDE binary.
# - Only used if DEBUG_PYCHARM = True.
# - If PyCharm is in the path, can typically left at 'pycharm.sh'
# - If PyCharm is not in path, can be set to an absolute path. E.g.
#   '~/JetBrains/pycharm'
PYCHARM_BIN = 'pycharm.sh'

# Enable request echo.
# True:
# - GMN will not process any requests. Instead, it will echo the requests
#   back to the client. The requests are formatted to be human readable. This
#   enables a client to see exactly what GMN receives after processing by
#   Apache, mod_wsgi and Django. It is useful for debugging both clients and
#   GMN.
# False (default):
# - GMN processes all requests as normal.
# Only available when DEBUG_GMN is set to True.
ECHO_REQUEST_OBJECT = False

# Allow integration tests.
# True:
# - Destructive integration tests will be allowed to run.
# False (default):
# - Destructive integration tests will not run.
# GMN comes with a set of integration tests, in gmn_integration_tests.py. These
# are destructive. They put the MN into a known state by erasing all objects and
# populating the MN with a specific set of test objects. The integration tests
# check that both DEBUG_GMN and this setting are set to True before running.
# This helps prevent accidental deletion of objects on a MN that is in the
# process of being deployed, and still has DEBUG_GMN set to True while also
# holding objects that are intended to be used in production.
ALLOW_INTEGRATION_TESTS = False

# Enable stand-alone mode.
# True (default):
# - GMN will not attempt to connect to the root CN on startup.
# False:
# - On startup, GMN attempts to connect to the root CN of the environment
#   that has been configured in the DATAONE_ROOT setting. If the connection
#   fails, GMN does not serve any requests.
# - Use for production.
STAND_ALONE = True

# DataONE specifies which System Metadata values are initialized and controlled
# by CNs, MNs and clients. Normally, GMN will ignore and overwrite any values
# submitted by a client that are intended to be controlled by MNs.
#
# These settings allow trusting clients to supply values that are normally
# initialized and controlled by the MN. They are useful in various situations
# where clients can be considered to be part of the MN, such as when GMN
# is used as the DataONE interface in a SlenderNode configuration.
#
# The settings apply to MNStorage.create(), MNStorage.update() and, with the
# exception of TRUST_CLIENT_DATEUPLOADED, to MNStorage.updateSystemMetadata().
# dataUploaded is an immutable value that cannot be changed after create() or
# update().
#
# True:
# - GMN will use any value that is submitted by the client. If a value is not
#   provided by the client, GMN will initialize the value.
#
# False (default):
# - GMN will overwrite any value that is submitted by the client. E.g., the
#   submitter field is set to the primary subject of the certificate with which
#   the call was made.
TRUST_CLIENT_SUBMITTER = False
TRUST_CLIENT_ORIGINMEMBERNODE = False
TRUST_CLIENT_AUTHORITATIVEMEMBERNODE = False
TRUST_CLIENT_DATESYSMETADATAMODIFIED = False
TRUST_CLIENT_SERIALVERSION = False
TRUST_CLIENT_DATEUPLOADED = False

# Enable monitoring.
# True (default):
# - Aspects of internal GMN operations can be monitored by public subjects.
# False:
# - Prevent public subjects from accessing monitoring functions.
# This function does not expose any sensitive information and should
# be safe to keep enabled in production.
# When DEBUG_GMN is True, this setting is ignored and monitoring is always
# enabled.
MONITOR = True

# Hosts/domain names that are valid for this site.
# Ignored if DEBUG is True. Required if DEBUG is False.
ALLOWED_HOSTS = [
  'localhost',
  '127.0.0.1', # Allow local connections.
  #'my.server.name.com', # Add to allow GMN to be accessed by name from remote server.
  #'my.external.ip.address', # Add to allow GMN to be accessed by ip from remote server.
]

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
# True (default):
# - Enable the DataONE Coordinating Nodes to synchronize (discover new
#   content and other changes) on this node.
# False:
# - Prevent the DataONE Coordinating Nodes from synchronizing.
NODE_SYNCHRONIZE = True

# The schedule on which synchronization should run for this node. The schedule
# should reflect the frequency at which content is expected to change on the
# node. The schedule is only a hint to the CNs. The syntax for each time slot
# follows that of the Quartz Scheduler:
# http://www.quartz-scheduler.org/documentation/quartz-2.1.x/tutorials/crontrigger.html
# These settings are ignored if NODE_SYNCHRONIZE is False.
# E.g.: YEAR = '*', MONTH = '*', WEEKDAY = '?', MONTHDAY = '*', HOUR = '*',
# MINUTE = '0/3', SECOND = '0'.
NODE_SYNC_SCHEDULE_YEAR = '*'
NODE_SYNC_SCHEDULE_MONTH = '*'
NODE_SYNC_SCHEDULE_WEEKDAY = '?'
NODE_SYNC_SCHEDULE_MONTHDAY = '*'
NODE_SYNC_SCHEDULE_HOUR = '*'
NODE_SYNC_SCHEDULE_MINUTE = '42'
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

# Create a unique string for this node and do not share it.
SECRET_KEY = 'MySecretKey'

# Path to the client side certificate that GMN uses when initiating TLS/SSL
# connections to Coordinating Nodes. The certificate must be in PEM format.
CLIENT_CERT_PATH = '/var/local/dataone/certs/client/client_cert.pem'

# Path to the private key for the client side certificate set in
# CLIENT_CERT_PATH. The private key must be in PEM format. This is only
# required to be set if the certificate does not contain an embedded private
# key. Otherwise, set it to None.
CLIENT_CERT_PRIVATE_KEY_PATH = '/var/local/dataone/certs/client/client_key_nopassword.pem'

# Enable this node to be used as a replication target.
# True:
# - DataONE can use this node to store replicas of science objects.
# False (default):
# - This node will advertise that it is not available as a replication target
#   in the Replication Policy section of the Node document. It will also enforce
#   this setting by refusing calls to MNReplication.replicate().
NODE_REPLICATE = False

# The maximum size, in octets (8-bit bytes), of each object this node is willing to
# accept for replication. Set to -1 to allow objects of any size.
# E.g. for a maximum object size of 1GiB: 1024**3
REPLICATION_MAXOBJECTSIZE = -1

# The total space, in octets (8-bit bytes), that this node is providing for
# replication. Set to -1 to provide unlimited space (not recommended).
# E.g. for a total space of 10 GiB: 10 * 1024**3
REPLICATION_SPACEALLOCATED = 10 * 1024**3

# A list of nodes for which this node is willing to replicate content. To allow
# objects from any node to be replicated, set to an empty list.
# E.g.: ('urn:node:MemberNodeA','urn:node:MemberNodeB','urn:node:MemberNodeC')
REPLICATION_ALLOWEDNODE = ()

# A list of object formats for objects which this node is willing replicate.
# To allow any object type to be replicated, set to an empty list.
# E.g.: ('eml://ecoinformatics.org/eml-2.0.0', 'CF-1.0')
REPLICATION_ALLOWEDOBJECTFORMAT = ()

# The maximum number of attempts to complete a CN replication request. When this
# number is exceeded, the CN is notified that the requested replica could not be
# created and the request is recorded as failed. By default, replication
# processing occurs once per hour, so a value of 24 (default) causes replication
# to be retried for 24 hours.
REPLICATION_MAX_ATTEMPTS = 24

# The maximum number of attempts to complete a CN System Metadata refresh
# request. When this number is exceeded, the request is recorded as failed and
# permanently removed. By default, System Metadata refresh processing occurs
# once per hour, so a value of 24 (default) causes the refresh to be retried for
# 24 hours.
SYSMETA_REFRESH_MAX_ATTEMPTS = 24

# On startup, GMN connects to the DataONE root CN to get the subject strings of
# the CNs in the environment. For a production instance of GMN, this should be
# set to the default DataONE root for production systems. For a test instance,
# this should be set to the root of the test environment in which GMN is to run.
# The CN subjects are used for controlling access to MN API methods for which
# only CNs should have access. See also the STAND_ALONE setting.
DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT
#DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-sandbox.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'

# Subjects for implicitly trusted DataONE infrastructure. Connections containing
# client side certificates with these subjects bypass access control rules and
# have access to REST interfaces meant only for use by CNs. These subjects are
# added to the ones discovered by connecting to the DataONE root CN. See the
# DATAONE_ROOT setting. If the STAND_ALONE setting is set to True, these become
# the only trusted subjects.
DATAONE_TRUSTED_SUBJECTS = set([
  # For testing and debugging, it's possible to add the public subject here.
  # This circumvents all access control, allowing any method to be called
  # from an unauthenticated connection.
  #d1_common.const.SUBJECT_PUBLIC, # Only use for testing and debugging
  # As with the public subject, it's possible to add the authenticatedUser
  # subject here, to let any authenticated user access any method.
  #d1_common.const.SUBJECT_AUTHENTICATED, # Only use for testing and debugging
  # Specific authenticated users can also be added.
  #'any-authenticated-user-subject',
])

# When DEBUG=False and a view raises an exception, Django will send emails to
# these addresses with the full exception information.
ADMINS = (('My Name', 'my_address@my_email.tld'),)

# Enable MNRead.listObjects() for public and regular authenticated users.
#
# True (default):
# - MNRead.listObjects() can be called by any level of user (trusted
#   infrastructure, authenticated and public), and results are filtered
#   to list only objects to which the user has access.
# False:
# - MNRead.listObjects() can only be called by trusted infrastructure (CNs).
#
# The primary means for a user to discover objects is to use the search
# facilities exposed by CNs. By enabling this option, regular users can also
# discover objects directly on the node by iterating over the object list. This
# is disabled by default because the call can be expensive (as it must create a
# filtered list of all objects on the node for each page that is returned).
# These are also the reasons that DataONE specified implementation of access
# control for public and regular users to be optional for this API.
PUBLIC_OBJECT_LIST = True

# Enable MNCore.getLogRecords() access for public and regular authenticated
# users.
#
# True (default):
# - MNCore.getLogRecords() can be called by any level of user (trusted
#   infrastructure, authenticated and public), and results are filtered
#   to list only log records to which the user has access. In particular,
#   this means that all users can retrieve log records for public objects.
# False:
# - MNCore.getLogRecords() can only be called by trusted infrastructure (CNs).
#
# Regardless of this setting, the DataONE Coordinating Nodes provide access
# controlled log records which are aggregated across all Member Nodes that hold
# replicas of a given object. Setting this to True allows users to get log
# records directly from this Member Node in addition to the aggregated logs
# available from CNs.
PUBLIC_LOG_RECORDS = True

# Set permissions required for calling the MNStorage.update() API method.
# True (default):
# - A user must both have write permission on an object and be in the
#   whitelist for Create, Update and Delete in order to update the object.
# False:
# - Any user that has write permission on an object can update it.
REQUIRE_WHITELIST_FOR_UPDATE = True

# Postgres database connection.
DATABASES = {
  'default': {
    # Postgres
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gmn2',
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

# Paths to the GMN object store. The bytes of all the objects handled by GMN are
# stored in a directory hierarchy that starts below this folder.
OBJECT_STORE_PATH = '/var/local/dataone/gmn_object_store'

# GMN implements a vendor specific extension for MNStorage.create(). Instead of
# providing an object for GMN to manage, the object can be left empty and the
# URL of the object on a 3rd party server be provided instead. In that case, GMN
# will stream the object bytes from the remote server while handling all other
# object related operations like usual. An object that is created using this
# extension is said to be proxied. GMN can stream proxied objects from HTTP and
# HTTPS.
#
# GMN provides limited support for streaming objects that are access controlled
# on the remote server. GMN has the ability to supply credentials to the remote
# server via simple HTTP Basic Authentication. This type of authentication is
# secure only when it is performed over an HTTPS connection. The username and
# password provided here must provide access to all the proxied objects handled
# by this instance of GMN. Because of this, this type of authentication is ONLY
# secure if ALL subjects that have permission to create objects on this GMN
# instance also have full access to ALL objects on the remote server. The attack
# vector would be that someone could gain access to an object on the remote
# server for which they do not have access by creating a proxied object on GMN,
# supplying the URL for the access controlled object together with an access
# control list that lets them access the object on GMN.
PROXY_MODE_BASIC_AUTH_ENABLED = False
PROXY_MODE_BASIC_AUTH_USERNAME = ''
PROXY_MODE_BASIC_AUTH_PASSWORD = ''
PROXY_MODE_STREAM_TIMEOUT = 30

# Path to the log file.
LOG_PATH = d1_common.util.abs_path('./gmn.log')

# Set up logging.

# Set the level of logging that GMN should perform. Choices are:
# DEBUG, INFO, WARNING, ERROR, CRITICAL or NOTSET.
if DEBUG or DEBUG_GMN:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'WARNING'

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
      # Set logging level to "WARNING" to suppress logging of SQL statements.
      'level': 'WARNING',
      'propagate': False
    },
  }
}
