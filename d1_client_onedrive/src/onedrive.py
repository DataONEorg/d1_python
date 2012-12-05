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
 - Argument parser.
:Author: DataONE (Dahl)
'''

# Std.
import logging
import os
import sys
import optparse

# 3rd party.
import fuse

# D1.
import d1_common.const

# App.
sys.path.append('impl')
sys.path.append('impl/drivers/fuse')
sys.path.append('impl/resolver')
import settings
import check_dependencies
import callbacks

# Set up logger for this module.
log = logging.getLogger(__name__)


def main():
  log_setup()

  if not check_dependencies.check_dependencies():
    raise Exception('Dependency check failed')

  parser = optparse.OptionParser('%prog [options] [mountpoint]')
  parser.add_option(
    '-v',
    '--version',
    dest='version',
    action='store_true',
    default=False,
    help='Display version information and exit'
  )

  (options, arguments) = parser.parse_args()

  if len(arguments) > 1:
    log.error('Too many command line arguments')
    parser.print_help()
    sys.exit()

  if len(arguments) == 1:
    mount_point = arguments[0]
  else:
    mount_point = settings.MOUNTPOINT

  log.setLevel(map_level_string_to_level(settings.LOG_LEVEL))

  if options.version:
    log_library_versions()
    sys.exit()

  fuse_args = {
    'foreground': settings.FOREGROUND,
    'fsname': 'ONEDrive',
    'nothreads': settings.NOTHREADS,
    'nonempty': True,
  }
  if os.uname()[0] == 'Darwin':
    fuse_args['volicon'] = settings.ICON
    fuse_args['local'] = True

  log_startup_parameters(options, arguments, fuse_args)
  log_settings()

  # Mount the drive and handle callbacks forever.
  fuse.FUSE(callbacks.FUSECallbacks(), mount_point, **fuse_args)


def log_setup():
  # Set up logging.
  # Log entries are written to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s'
    '(%(lineno)d): %(message)s', '%Y-%m-%d %H:%M:%S'
  )
  # File.
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  # Stdout.
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


def log_settings():
  log.info('Settings:')
  for k, v in sorted(settings.__dict__.items()):
    if k == k.upper():
      log.info('  {0}: {1}'.format(k, v))


if __name__ == '__main__':
  main()
