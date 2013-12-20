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
''':mod:`settings`
==================

:Synopsis:
 - User configurable settings for ONEDrive.
:Author: DataONE (Dahl)
'''

# Stdlib.
import d1_common.const
import logging
import os

# D1.


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

################################################################################
# User configurable self._options.
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

# The username and encrypted password to use for accessing the ONEDrive
# workspace.
#WORKSPACE_USERNAME = ''
#WORKSPACE_PASSWORD = ''
WORKSPACE_XML = os.path.expanduser('~/workspace.xml') # (default, in user's home folder)
# WORKSPACE_XML = './workspace.xml' # (in the current directory)

# The maximum number of science objects to display for a search item. Increasing
# this setting causes longer lists of science objects to to appear in the
# filesystem, increases memory footprint for the application and causes longer
# response times when opening folders. Default value: 50.
MAX_OBJECTS_FOR_SEARCH = 50

# The maximum number of objects to show in a flat list. ONEDrive can display
# science objects in a flat list or in a hierarchy. This settings determines the
# threshold at which ONEDrive switches from a flat to a hierarchical display.
#MAX_OBJECTS_FOR_FLAT_LIST = 10

################################################################################
# Settings below this line are not intended to be modified by the user.
################################################################################

# Debug mode.
# True: Turn on verbose logging and various other debugging facilities.
# False: Log only error messages (for normal use, default)
DEBUG = True

# Set the default file to log to or None for logging to stdout
LOG_FILE_PATH = make_absolute('onedrive.log')

# The maximum number of path attributes to cache. Increasing this number may
# give better performance, but also a larger memory footprint. A value below 100
# is not recommended. Default value: 1000.
MAX_ATTRIBUTE_CACHE_SIZE = 1000

# The maximum number of folders to cache. Increasing this number may give better
# performance, but also a larger memory footprint. A value below 10 is not
# recommended. Default value: 100.
MAX_DIRECTORY_CACHE_SIZE = 1000

# The maximum number of science objects to cache. Increasing this number may
# give better performance, but also a larger memory footprint. Default value:
# 1000.
MAX_OBJECT_CACHE_SIZE = 1000

# The maximum number of error message file paths to cache. Decreasing this
# number below the default is not recommended, as it may cause error messages
# not to be displayed correctly in the ONEDrive filesystem. Default value: 1000.
MAX_ERROR_PATH_CACHE_SIZE = 1000

# The maximum number of Solr query results to cache.
MAX_SOLR_QUERY_CACHE_SIZE = 1000

# Specify the type of cache to use. Can be MEMORY or DISK
CACHE_TYPE = "DISK"

# Set to True if the cache should be cleared on startup. Has no effect on
# memory cache.
CACHE_STARTUP_CLEAN = True

# Location of the disk caches if used
CACHE_DISK_ROOT = "/tmp/onedrive"

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

# Type of connection to use when connecting to the Solr server.
# True: A persistent connection is maintained (default)
# False: A new connection is created each time a query is sent
#SOLR_PERSIST_CONNECTION = True

# The path that is appended to the DataONE root URL to reach the endpoint for
# the DataONE CNRead.query() API.
SOLR_QUERY_PATH = '/v1/query/solr/'

# Setting this value to 1 causes the Solr client to output debug information.
# True: Turn on debug output in the Solr Client (for debugging)
# False: Turn off debug output (for normal use)
SOLR_DEBUG = True if DEBUG else False # (enabled when running in debug mode)

# The name that will be displayed for the ONEDrive filesystem.
FUSE_FILESYSTEM_NAME = 'ONEDrive'

# Allow the filesystem to be mounted on a folder that is not empty.
FUSE_NONEMPTY = True

# During normal use, the FUSE driver will go into the background, causing the
# onedrive.py command to return immediately. Setting this value to True
# causes the driver to remain in the foreground.
# True: Run driver in foreground (for debugging)
# False: Run driver in background (for normal use)
FUSE_FOREGROUND = True if DEBUG else False # (enabled when running in debug mode)
FUSE_FOREGROUND = True

# During normal use, the FUSE drive will use multiple threads to improve
# performance. Settings this value to True causes the driver to run everything
# in a single thread.
# True: Do not create multiple threads (for debugging)
# False: Create multiple threads (for normal use)
FUSE_NOTHREADS = True if DEBUG else False # (enabled when running in debug mode)
FUSE_NOTHREADS = True

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

# Set up logging.

# Set the level of logging that should be performed. Choices are:
# DEBUG, INFO, WARNING, ERROR, CRITICAL or NOTSET.
if DEBUG:
  LOG_LEVEL = 'DEBUG'
else:
  LOG_LEVEL = 'INFO'

#Kind of a hack - add a module variable to logging that lists the modules that
#will be set to logging at a specific level. Each module needs to check for
#presence of its __name__ in the list. If not present, then logging will
#continue at the app global set level for logging.
logging.ONEDRIVE_MODULES = {
  '__main__': 'INFO',
  'impl.drivers.dokan.d1_dokan': 'DEBUG',
}

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
