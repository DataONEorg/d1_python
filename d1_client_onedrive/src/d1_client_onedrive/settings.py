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
 - User configurable settings for ONEDrive.
:Author:
  DataONE (Dahl)
"""

# Stdlib
import d1_common.const
import logging
import os

# D1


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


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

# Select the mountpoint on Linux and Mac OS X. The mountpoint is the folder in
# the local filesystem in which the ONEDrive filesystem appears. The default is
# to mount the drive in a folder named "one" in the user's home folder.
#
# This setting is not used on Windows. See MOUNT_DRIVE_LETTER below.
#
# If the mountpoint is set to a folder that already contains files and folders,
# those files and folders become temporarily invisible while ONEDrive is
# running.
MOUNTPOINT = os.path.expanduser('~/one') # (default)
#MOUNTPOINT = '/mnt/onedrive' # (example, absolute path)

# Select the drive letter on Windows. The drive letter designates the drive in
# which the ONEDrive filesystem appears. The drive letter must not already be in
# use. Drive letters that are typically in use include C: and D:.
#
# This setting is not used on Linux and Mac OS X.
MOUNT_DRIVE_LETTER = 'O:'

# Zotero authentication.
# If these settings are not specified, the settings will be retrieved from
# environment variables with corresponding names.
#ZOTERO_USER = 123
#ZOTERO_API_ACCESS_KEY = '123'

# The maximum number of objects to show in a flat list. ONEDrive can display
# science objects in a flat list or in a hierarchy. This settings determines the
# threshold at which ONEDrive switches from a flat to a hierarchical display.
#MAX_OBJECTS_FOR_FLAT_LIST = 10

# Resource maps (data packages) can be considered to be containers that contain
# science data and metadata objects. The fastest way to process resource maps
# is to simply return the size of the resource map itself because that information
# is directly available in the SOLR index. However, depending on the
# object_tree client, it may make more sense to return the total size of the objects
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
# ONEDrive, increases memory footprint for the application and causes longer
# response times when refreshing folders. Default value: 50.
MAX_OBJECTS_FOR_QUERY = 50

################################################################################
# Settings below this line are not intended to be modified by the user.
################################################################################

# Debug mode.
# True: Turn on verbose logging and various other debugging facilities.
# False: Log only error messages (for normal use, default)
DEBUG = True

# Cache paths

# By default, the object_tree is cached in the user's home folder.
ONEDRIVE_CACHE_ROOT = os.path.expanduser('~/.dataone/onedrive') # (default)

# Location of the local cache of the online object_tree.
OBJECT_TREE_CACHE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'object_tree')

# Location of the local cache of Science Data objects.
SCI_OBJ_CACHE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'sci_obj')

# Location of the local cache of System Metadata.
SYS_META_CACHE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'sys_meta')

# Location of the local cache of the Zotero Library.
ZOTERO_CACHE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'zotero_library')

# Location of the local cache of gazetteer results.
REGION_TREE_CACHE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'region_tree')

# Set the default file to log to or None for logging only to stdout
#LOG_FILE_PATH = make_absolute('onedrive.log')
#LOG_FILE_PATH = None
LOG_FILE_PATH = os.path.join(ONEDRIVE_CACHE_ROOT, 'onedrive.log')

# Cache sizes

# The maximum number of science objects to cache. Increasing this number may
# give better performance, but also a larger memory footprint. Default value:
# 10000.
SCI_OBJ_MAX_CACHE_ITEMS = 10000

# The maximum number of system metadata objects to cache. Increasing this number
# may give better performance, but also a larger memory footprint. Default
# value: 10000.
SYS_META_MAX_CACHE_ITEMS = 10000

# The maximum number of path attributes to cache. Increasing this number may
# give better performance, but also a larger memory footprint. A value below 100
# is not recommended. Default value: 10000.
ATTRIBUTE_MAX_CACHE_ITEMS = 10000

# The maximum number of folders to cache. Increasing this number may give better
# performance, but also a larger memory footprint. A value below 10 is not
# recommended. Default value: 10000.
DIRECTORY_MAX_CACHE_ITEMS = 10000

# The maximum number of region trees to cache. A region tree describes to which
# geographical regions a set of Science Objects belong. Default value: 1000
REGION_TREE_MAX_CACHE_ITEMS = 1000

# In the ONEDrive filesystem, resource maps (data packages) are represented as
# folders which can be opened to access the mapped science objects. This setting
# controls how the size is displayed for the resource map folders. To display
# the total size of mapped objects, ONEDrive must retrieve the resource maps,
# parse them and retrieve the sizes of the individual objects, which slows down
# opening of folders that contain many resource maps. Also, many filesystem
# browsers do not show size for folders, so the information retrieved by this
# setting may not be displayed.
#
# 'total': Show total size of all objects in resource maps (slow)
# 'number': Show number of objects in resource maps (less slow)
# 'zero': Show zero size for all resource maps (fast, default)
FOLDER_SIZE_FOR_RESOURCE_MAPS = 'zero'

# The name that will be displayed for the ONEDrive filesystem.
FUSE_FILESYSTEM_NAME = 'ONEDrive'

# Allow the filesystem to be mounted on a folder that is not empty.
FUSE_NONEMPTY = True

# During normal use, the FUSE driver will go into the background, causing the
# onedrive.py command to return immediately. Setting this value to True
# causes the driver to remain in the foreground.
# True: Run driver in foreground (for debugging)
# False: Run driver in background (for normal use)
FUSE_FOREGROUND = DEBUG # (enabled when running in debug mode)
#FUSE_FOREGROUND = True

# During normal use, the FUSE drive will use multiple threads to improve
# performance. Settings this value to True causes the driver to run everything
# in a single thread.
# True: Do not create multiple threads (for debugging)
# False: Create multiple threads (for normal use)
FUSE_NOTHREADS = DEBUG # (enabled when running in debug mode)
#FUSE_NOTHREADS = True

# The following settings are specific for MacFUSE.
# http://code.google.com/p/macfuse/wiki/OPTIONS

# Path to the file containing the icon that is displayed for ONEDrive when
# accessing the filesystem through a GUI.
MACFUSE_ICON = make_absolute(os.path.join('impl', 'd1.icon'))

# Mount the filesystem as a local disk, not a network connected disk.
MACFUSE_LOCAL_DISK = True

# Paths that have special meaning to the operating system and that should be
# ignored by ONEDrive.
IGNORE_SPECIAL = set(
  [
    # OSX / Finder
    '._',
    '.DS_Store',
    'Backups.backupdb',
    '.Trashes',
    '.fseventsd',
    'MobileBackups.trash',
    'Backups.backupdb',
    '.hidden',
    'Contents',
    # KDE / Krusader
    '.directory',
    '.Trash',
    'BDMV',
    '.xdg-volume-info',
    # Windows
    'desktop.ini',
    'folder.jpg',
    'folder.gif',
  ]
)

# Solr

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
