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
"""

# noinspection PyUnresolvedReferences
# flake8: noqa: F403,F401

#import logging
#import d1_common.const
from d1_gmn.app.settings_default import *

import d1_common.util

# ==============================================================================
# Debugging

# Enable Django debug mode.
# True:
# - Use only for debugging and testing on non-production instances.
# - May expose sensitive information.
# - Django will serve static files, which are required for the web UI.
# - GMN returns a HTML Django exception page with extensive debug information
#   for internal errors.
# - GMN returns a HTML Django 404 page that lists all valid URL patterns for
#   invalid URLs.
# - The profiling subsystem can be accessed.
# False (default):
# - Use for production.
# - Django will not serve static files. For the UI to work, the web server must
#   be set up to serve them directly.
#   serve static files, which are required for the web UI.
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
# False (default):
# - Use for production.
DEBUG_GMN = False

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
DEBUG_ECHO_REQUEST = False

# Enable SQL profiling.
# True:
# - Requests are processed as normal up to the point where the response would be
#   returned to the client. At that point, the response is discarded and a page
#   with timing information about the SQL queries that were used during
#   processing of the request is returned instead.
# - When GMN_DEBUG = True, this functionality is also available on a call by
#   call basis by including an HTTP header with key VENDOR-PROFILE-SQL in the
#   request.
# False (default):
# - The request is processed as normal.
DEBUG_PROFILE_SQL = False

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
# dateUploaded is an immutable value that cannot be changed after create() or
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

# Hosts/domain names that are valid for this site.
# Ignored if DEBUG is True. Required if DEBUG is False.
ALLOWED_HOSTS = [
  # Allow local connections
  'localhost',
  '127.0.0.1',
  # Add FQDN to allow external clients to access GMN
  #'my.server.name.com',
  # Add to allow external clients to access GMN by IP address
  #'my.external.ip.address',
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

# ==============================================================================
# Object "read" event logging
#
# Object related events are logged in order to generate statistics. Objects will
# have exactly one "create" event, zero or one "update" and "delete" events, and
# zero to a few "replicate" and "synchronization_failed" events. As these events
# designate rare events in the history of an object, they are always logged.
#
# The only events that are not considered to be rare are "read" events.
#
# Nodes are often accessed as part of normal operations performed by automated
# systems, usually running on a fixed schedule. Tracking the large numbers of
# object "read" events that are often triggered by these automated systems is
# not desirable as it skews the actual usage counts for the objects, and takes
# up system resources.
#
# No "read" events will be logged for any request that matches one or more of
# the following filters.

# Ignore "read" events by user agent, ip address or subject. These are
# lists of case insensitive regular expressions that are applied one by one
# using re.match(). If a match is found, the "read" event is not logged.
LOG_IGNORE_USER_AGENT = []
LOG_IGNORE_IP_ADDRESS = []
LOG_IGNORE_SUBJECT = []

# Ignore "read" events for DataONE trusted subjects.
# True (default):
# - "read" events are not logged in requests made by subjects which are in the
# DATAONE_TRUSTED_SUBJECTS list or are CN subjects in the DataONE environment in
# which this node is registered.
# False:
# - Do not apply this filter.
LOG_IGNORE_TRUSTED_SUBJECT = True

# Ignore "read" event for subjects authenticated by the client side certificate.
# True (default):
# - "read" events are not logged in requests which where authenticated using
# this MN's local client side certificate.
# False:
# - Do not apply this filter.
LOG_IGNORE_NODE_SUBJECT = True

# ==============================================================================

# Path to the client side certificate that GMN uses when initiating TLS/SSL
# connections to Coordinating Nodes. The certificate must be in PEM format.
CLIENT_CERT_PATH = '/var/local/dataone/certs/client/client_cert.pem'

# Path to the private key for the client side certificate set in
# CLIENT_CERT_PATH. The private key must be in PEM format. This is only
# required to be set if the certificate does not contain an embedded private
# key. Otherwise, set it to None.
CLIENT_CERT_PRIVATE_KEY_PATH = '/var/local/dataone/certs/client/client_key_nopassword.pem'

# Absolute Path to the root of the GMN object store. The object store is a
# directory hierarchy in which the bytes of science objects are stored by
# default.
OBJECT_STORE_PATH = '/var/local/dataone/gmn_object_store'

# Enable this node to be used as a replication target.
# True:
# - DataONE can use this node to store replicas of science objects.
# False (default):
# - This node will advertise that it is not available as a replication target
#   in the Replication Policy section of the Node document. It will also enforce
#   this setting by refusing calls to MNReplication.replicate().
NODE_REPLICATE = False

# The maximum size, in octets (8-bit bytes), of each object this node is willing
# to accept for replication. Set to -1 to allow objects of any size. E.g. for a
# maximum object size of 1GiB: 1024**3
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

# Accept only public objects for replication
# True:
# - This node will deny any replication requests for access controlled objects.
# False (default):
# - Replication requests are accepted for access controlled objects provided
# that all other criteria are met.
REPLICATION_ALLOW_ONLY_PUBLIC = False

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
  # This circumvents all access control, making all content publicly accessible.
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

# This setting determines how Open Archives Initiative Object Reuse and Exchange
# (OAI-ORE) Resource Maps are handled if one or more of the objects referenced
# in the Resource Map do not (yet) exist on this node.
#
# Resource Maps are documents that describe aggregations of web resources. In
# DataONE, they are used for defining data packages, where a data package is a
# collection of science objects. A data package can be downloaded as a
# compressed archive with the MNPackage.getPackage() API method.
#
# For more information about data packages in DataONE, see
# https://releases.dataone.org/online/api-documentation-v2.0.1/design
# /DataPackage.html
#
# To ensure that a Resource Map references only the intended objects, it should
# reference only objects on this node and be created after all referenced
# objects are created. This setting takes effect only when that is not the case.
#
# 'block' (default):
# - Resource Maps can only be created if all referenced objects exist on this
# node. This ensures that Resource Maps only reference the intended objects but
# makes it impossible to create Resource Maps that include science objects on
# remote nodes or any other web resources.
#
# 'reserve':
# - Resource Maps are created like regular objects. Identifiers for referenced
# non-existing objects are reserved for use by the same subject that uploaded
# the Resource Map. This ensures that the identifiers remain available to the
# subject but will block the identifiers indefinitely if they are not used by
# the subject.
#
# 'open':
# - Resource Maps are created like regular objects. Identifiers for referenced
# non-existing objects remain open for use by any subject. This may cause
# Resource Maps to reference unintended objects if the referenced identifier is
# used for an unrelated object created by another subject before the intended
# object is created by the Resource Map subject.
RESOURCE_MAP_CREATE = 'block'

# Validate Science Metadata objects against local XML Schema (XSD)
# True (default):
# - When a SciMeta format that is recognized and parsed by CNs is
#   received in MNStorage.create() or MNStorage.update(), GMN rejects the
#   operation and returns an InvalidRequest with details to the client if the
#   object is not well formed, valid, and matching the SysMeta formatId.
# False:
# - SciMeta objects are not validated. This is not recommended, as any invalid
#   objects will be rejected by the CN during synchronization.
# Notes:
# - Objects affected by this setting have formatType of METADATA in the CN's
# objectFormatList.
# - Actual validation is performed by the d1_sciobj package, which may not
#   support all SciMeta formats. Validation is silently skipped for any
#   unsupported formats.
# - Objects that are stored remotely (using GMN's proxy support), are not
#   validated.
SCIMETA_VALIDATION_ENABLED = True

# The maximum size in bytes of SciMeta objects received in MNStorage.create()
# and MNStorage.update() that will be validated. SciMeta objects larger than
# this size are not validated and are handled according to the
# SCIMETA_VALIDATION_OVER_SIZE_ACTION setting.
#
# This setting applies only when SCIMETA_VALIDATION is set to True.
#
# As SciMeta documents are read into memory for validation, limiting the maximum
# size of objects that will be validated helps reduce the chance of the server
# running out of memory.
#
# E.g.: 100 MiB = 1024**2 (default)
# To validate SciMeta of any size, set to -1 (not recommended).
SCIMETA_VALIDATION_MAX_SIZE = 100 * 1024**2

# The action to perform for SciMeta objects received in MNStorage.create()
# and MNStorage.update() larger than size set in SCIMETA_VALIDATION_MAX_SIZE.
#
# This setting applies only when SCIMETA_VALIDATION_ENABLED is set to True and
# SCIMETA_VALIDATION_MAX_SIZE is not set to -1.
#
# - 'reject' (default): SciMeta over Max Size is rejected and GMN returns an
#   InvalidRequest with explanation to the client.
# - 'accept': SciMeta over Max Size is accepted but not validated. This is not
#   recommended, as any invalid objects will later be rejected by the CN during
#   synchronization.
SCIMETA_VALIDATION_OVER_SIZE_ACTION = 'reject'

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

# As the XML documents holding the DataONE types, such as SystemMetadata, must
# be in memory while being deserialized and parsed, we limit the size that can
# be handled. The default limit is set much higher than the expected size of any
# valid DataONE type and is intended to guard against invalid or malicious
# documents that may exhaust the server's memory. The limit does not apply to
# XML documents submitted as science data objects, as they are streamed directly
# to disk without being loaded to memory.
# E.g.: 10 MiB = 10 * 1024**2 (default)
MAX_XML_DOCUMENT_SIZE = 10 * 1024**2

# Chunk size for stream iterators.
# E.g.: 1 MiB = 1024**2 (default)
NUM_CHUNK_BYTES = 1024**2

# The maximum number of items that can be returned in a single page of results
# from MNRead.listObjects() (ObjectList) and MNCore.getLogRecords() (Log). A
# lower number reduces memory usage, but causes more round-trips between client
# and server.
MAX_SLICE_ITEMS = 5000

# Postgres database connection.
d1_common.util.nested_update(
  DATABASES,
  {
    'default': {
      # The database in tables required by GMN are stored. The database itself
      # is typically owned by the postgres user while the tables are owned by the
      # GMN user.
      'NAME': 'gmn3',
    }
  }
)

# Logging
#
# Log levels determine which types of messages get written to GMN's log file
# Levels range from DEBUG, which is used for messages expected to occur during
# regular operations, to CRITICAL, which is used for messages indicating
# critical errors.
#
# The DEBUG log level is very verbose and will create large log files over time,
# so its mainly useful for troubleshooting.
#
# By default, we set debug level logging when GMN is in debug mode and
# informational level logging when GMN runs in regular mode.
if DEBUG or DEBUG_GMN:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'INFO'

d1_common.util.nested_update(
  LOGGING, {
    'handlers': {
      'file': {
        'level': LOG_LEVEL,
      },
    },
    'loggers': {
      '': {
        'level': LOG_LEVEL,
      },
      'django': {
        'level': LOG_LEVEL
      },
    }
  }
)
