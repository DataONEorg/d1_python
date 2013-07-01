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
''':mod:`onedrive`
==================

:Synopsis:
 - Top level module for ONEDrive.
 - Parse arguments.
 - Instantiate the Root resolver.
 - Mount FUSE.
:Author: DataONE (Dahl)
'''

# Std.
import logging
#import logging.config # Needs 2.7.
import os
import sys
import optparse

# 3rd party.
import fuse

# D1.
import d1_common.const

# App.
#sys.path.append('impl')
#sys.path.append('impl/drivers/fuse')
#sys.path.append('impl/resolver')
import settings
from impl import check_dependencies
from impl.drivers.fuse import callbacks
import impl.resolver.root

from impl import cache_memory as cache

# Set up logger for this module.
log = logging.getLogger(__name__)


def main():
  if not check_dependencies.check_dependencies():
    raise Exception('Dependency check failed')

  parser = optparse.OptionParser('%prog [options]')
  parser.add_option(
    '-v',
    '--version',
    dest='version',
    action='store_true',
    default=False,
    help='Display version information and exit'
  )

  # Add options to override defaults in settings.py.
  for k, v in settings.__dict__.items():
    # Only allow overriding strings and ints.
    if not (isinstance(v, str) or isinstance(v, int)):
      continue
    if k == k.upper():
      parser.add_option(
        '--{0}'.format(k.lower().replace('_', '-')),
        action='store',
        type='str',
        dest=k.upper(),
        default=v,
        metavar=v
      )

  (options, arguments) = parser.parse_args()

  if len(arguments) > 0:
    parser.print_help()
    sys.exit()

  ## Handles the logfile option
  #if options.logfile is not None:
  #    self._options.LOG_FILE = options.logfile

  # Setup logging
  # logging.config.dictConfig(self._options.LOGGING) # Needs 2.7
  log_setup(options)
  log.setLevel(map_level_string_to_level(options.LOG_LEVEL))

  if options.version:
    log_library_versions()
    sys.exit()

  # FUSE settings common to FUSE and MacFUSE.
  fuse_args = {
    'foreground': options.FUSE_FOREGROUND,
    'fsname': options.FUSE_FILESYSTEM_NAME,
    'nothreads': options.FUSE_NOTHREADS,
    # Allow sharing the mount point with Samba / smb / smbd.
    # Requires user_allow_other in /etc/fuse.conf
    # 'allow_other': True,
  }
  # FUSE settings specific to MacFUSE.
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = options.MACFUSE_ICON
    fuse_args['local'] = options.MACFUSE_LOCAL_DISK
  # FUSE settings specific to regular FUSE.
  else:
    fuse_args['nonempty'] = options.FUSE_NONEMPTY

  log_startup_parameters(options, arguments, fuse_args)
  log_settings(options)

  #create the caches here and add references to them in options.
  #enables child resolvers to invalidate entries so that 
  #changes can be reflected in the listings
  options.attribute_cache = cache.Cache(options.MAX_ATTRIBUTE_CACHE_SIZE)
  options.directory_cache = cache.Cache(options.MAX_DIRECTORY_CACHE_SIZE)

  # Instantiate the Root resolver.
  root_resolver = impl.resolver.root.RootResolver(options)

  # Mount the drive and handle callbacks forever.
  fuse.FUSE(
    callbacks.FUSECallbacks(
      options, root_resolver
    ), options.MOUNTPOINT, **fuse_args
  )


def log_setup(options):
  # Set up logging.
  # Log entries are written to both file and stdout.
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s'
    '(%(lineno)d): %(message)s', '%Y-%m-%d %H:%M:%S'
  )
  # Log to a file
  if options.LOG_FILE_PATH is not None:
    file_logger = logging.FileHandler(options.LOG_FILE_PATH, 'a')
    file_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(file_logger)
  # Also log to stdout
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def map_level_string_to_level(level_string):
  return {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
  }[level_string]


def log_library_versions():
  import d1_common.svnrevision
  import d1_client.svnrevision
  import svnrevision

  d1_common_rev = str(d1_common.svnrevision.getSvnRevision(update_static=True))
  d1_client_rev = str(d1_client.svnrevision.getSvnRevision(update_static=True))
  onedrive_rev = str(svnrevision.getSvnRevision(update_static=True))

  log.info('Software revisions:')
  log.info('  d1_common SVN revision: {0}'.format(d1_common_rev))
  log.info('  d1_client SVN revision: {0}'.format(d1_client_rev))
  log.info('  ONEDrive SVN revision: {0}'.format(onedrive_rev))


def log_startup_parameters(options, arguments, fuse_args):
  log.info('Mounting ONEDrive (FUSE)')
  log.info('  Options: {0}'.format(str(options)))
  log.info('  Arguments: {0}'.format(str(arguments)))
  log.info('  FUSE arguments: {0}'.format(str(fuse_args)))


def log_settings(options):
  log.info('Settings:')
  for k, v in sorted(options.__dict__.items()):
    if k == k.upper():
      log.info('  {0}: {1}'.format(k, v))


if __name__ == '__main__':
  main()
