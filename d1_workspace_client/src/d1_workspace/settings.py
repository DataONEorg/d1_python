#!/usr/bin/env python
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
""":mod:`settings`
==================

:Synopsis:
 - Default settings for the DataONE Workspace Client.
:Author:
  DataONE (Dahl)
"""

import os

import d1_common.util

################################################################################
# User configurable settings.
################################################################################

# In addition to the default production environment, DataONE maintains several
# separate environments for use when developing and testing DataONE components.
# There are no connections between the environments. For instance, certificates,
# DataONE identities and science objects are exclusive to the environment in
# which they were created. This setting controls to which environment ONEDrive
# connects.

# Round-robin CN endpoints
BASE_URL = d1_common.const.URL_DATAONE_ROOT # (recommended, production)
#BASE_URL = 'https://cn-dev.test.dataone.org/cn'
#BASE_URL = 'https://cn-stage.test.dataone.org/cn'
#BASE_URL = 'https://cn-sandbox.dataone.org/cn'
#BASE_URL = 'https://cn-stage.dataone.org/cn/'
#BASE_URL = 'https://cn-stage.test.dataone.org/cn'

# Bypass round-robin and go directly to a specific CN.
#BASE_URL = 'https://cn-dev-unm-1.test.dataone.org/cn'

# The username and encrypted password to use for accessing the workspace.
#WORKSPACE_USERNAME = ''
#WORKSPACE_PASSWORD = ''

# Cache locations.

# By default, the workspace is cached in the user's home folder.
WORKSPACE_CACHE_ROOT = os.path.expanduser('~/.dataone/workspace') # (default)

WORKSPACE_DEF_PATH = os.path.join(WORKSPACE_CACHE_ROOT, 'workspace.xml')
# WORKSPACE_DEF = './workspace.xml' # (in the current directory)

# Location of the local cache of the online workspace.
WORKSPACE_CACHE_PATH = os.path.join(WORKSPACE_CACHE_ROOT, 'wcache')

# Location of the local cache of Science Data objects.
SCI_OBJ_CACHE_PATH = os.path.join(WORKSPACE_CACHE_ROOT, 'science_data')

# Location of the local cache of System Metadata.
SYS_META_CACHE_PATH = os.path.join(WORKSPACE_CACHE_ROOT, 'sys_meta')

# Cache sizes

# The maximum number of science objects to cache. Increasing this number may
# give better performance, but also a larger memory footprint. Default value:
# 10000.
SCI_OBJ_MAX_CACHE_ITEMS = 10000

# The maximum number of system metadata objects to cache. Increasing this number
# may give better performance, but also a larger memory footprint. Default
# value: 10000.
SYS_META_MAX_CACHE_ITEMS = 10000

# Resource maps (data packages) can be considered to be containers that contain
# science data and metadata objects. The fastest way to process resource maps
# is to simply return the size of the resource map itself because that information
# is directly available in the SOLR index. However, depending on the
# workspace client, it may make more sense to return the total size of the objects
# contained by the resource map. This is a much slower operation because the
# resource map must be retrieved and parsed. Then, the system metadata for each
# object in the resource map must be retrieved via the DataONE API and parsed.
# As an alternative, the returned size can be the number of objects in the
# resource map, which only requires retrieving the resource map, not the
# contained objects.

# 'size': Show the size of the resource map itself (fast)
# 'objects': Show number of objects in resource map (medium fast)
# 'total': Show total size of all objects in resource maps (slow)
RESOURCE_MAP_SIZE = 'size'

# The maximum number of Science Object records to retrieve for a query item.
# Increasing this setting causes longer lists of Science Objects to to appear in
# Workspace client applications, such as ONEDrive, increases memory footprint
# for the application and causes longer response times when refreshing Workspace
# folders. Default value: 50.
MAX_OBJECTS_FOR_QUERY = 50

################################################################################
# Settings below this line are not intended to be modified by the user.
################################################################################

# Debug mode.
# True: Turn on verbose logging and various other debugging facilities.
# False: Log only error messages (for normal use, default)
DEBUG = True

# Set the default file to log to or None for logging to stdout
LOG_FILE_PATH = d1_common.util.abs_path('workspace.log')

# The maximum number of Solr query results to cache.
MAX_SOLR_QUERY_CACHE_SIZE = 1000

# Type of connection to use when connecting to the Solr server.
# True: A persistent connection is maintained (default)
# False: A new connection is created each time a query is sent
#SOLR_PERSIST_CONNECTION = True

# The path that is appended to the DataONE root URL to reach the endpoint for
# the DataONE CNRead.query() API.
SOLR_QUERY_PATH = '/v1/query/solr/'

# The amount of time to wait for the result of a Solr query result before
# considering the query as failed.
SOLR_QUERY_TIMEOUT = 30.0

# Setting this value to 1 causes the Solr client to output debug information.
# True: Turn on debug output in the Solr Client (for debugging)
# False: Turn off debug output (for normal use)
SOLR_DEBUG = True if DEBUG else False # (enabled when running in debug mode)

# Set up logging.

# Set the level of logging that should be performed. Choices are:
# DEBUG, INFO, WARNING, ERROR, CRITICAL or NOTSET.
if DEBUG:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'INFO'

# Needs Python 2.7

#LOGGING = {
#  'version': 1,
#  'disable_existing_loggers': True,
#  'formatters': {
#    'verbose': {
#        'format': '%(asctime)s %(levelname)-8s %(name)s %(module)s ' \
#                  '%(process)d %(thread)d %(message)s',
#        'datefmt': '%Y-%m-%d %H:%M:%S'
#    },
#    'simple': {
#      'format': '%(levelname)s %(message)s'
#    },
#  },
#  'handlers': {
#    'file': {
#      'level': LOG_LEVEL,
#      'class': 'logging.FileHandler',
#      'filename': LOG_FILE_PATH,
#      'formatter': 'verbose'
#    },
#  },
#  'loggers': {
#    # The "catch all" logger is denoted by ''.
#    '': {
#      'handlers': ['file'],
#      'propagate': True,
#      'level': LOG_LEVEL,
#    },
#  }
#}
