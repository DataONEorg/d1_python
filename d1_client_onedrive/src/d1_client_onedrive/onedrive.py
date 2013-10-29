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
 - Mount FUSE / Dokan.
:Author: DataONE (Dahl)
'''

# Std.
import logging
#import logging.config # Needs 2.7.
import os
import sys
import codecs
import optparse
import platform

# D1.
import d1_common.const

# App.
if not hasattr(sys, 'frozen'):
  sys.path.append(os.path.abspath(os.path.join('__file__', '../..')))

from d1_client_onedrive import settings
from d1_client_onedrive.impl import check_dependencies
from d1_client_onedrive.impl.resolver import root
from d1_client_onedrive.impl import cache_memory as cache
from d1_client_onedrive.impl import cache_disk

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName( \
               getattr(logging, 'ONEDRIVE_MODULES')[__name__]) )
except KeyError:
  pass


def main():
  if not check_dependencies.check_dependencies():
    raise Exception(u'Dependency check failed')

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
    if k.isupper():
      #if k == k.upper():
      parser.add_option(
        '--{0}'.format(k.lower().replace('_', '-')),
        action='store',
        type='str',
        dest=k.upper(),
        default=v,
        metavar=v
      )

  (options, arguments) = parser.parse_args()

  # Copy non-string/int settings into options.
  for k, v in settings.__dict__.items():
    if not (isinstance(v, str) or isinstance(v, int)) and k.isupper():
      options.__dict__[k] = v

  if len(arguments) > 0:
    parser.print_help()
    sys.exit()

  ## Handles the logfile option
  #if options.logfile is not None:
  #    self._options.LOG_FILE = options.logfile

  # Setup logging
  # logging.config.dictConfig(self._options.LOGGING) # Needs 2.7
  log_setup(options)

  try:
    log.setLevel(logging.getLevelName(getattr(logging, 'ONEDRIVE_MODULES')[__name__]))
  except KeyError:
    pass

  if options.version:
    log_version()
    sys.exit()

  #create the caches here and add references to them in options.
  #enables child resolvers to invalidate entries so that
  #changes can be reflected in the listings
  #options.attribute_cache = cache_disk.DiskCache(options.MAX_ATTRIBUTE_CACHE_SIZE, 'cache_attribute')
  #options.directory_cache = cache_disk.DiskCache(options.MAX_DIRECTORY_CACHE_SIZE, 'cache_directory')
  options.attribute_cache = cache.Cache(options.MAX_ATTRIBUTE_CACHE_SIZE)
  options.directory_cache = cache.Cache(options.MAX_DIRECTORY_CACHE_SIZE)

  # Instantiate the Root resolver.
  root_resolver = root.RootResolver(options)

  log.info("Starting ONEDrive...")
  log.info("Base URL = %s" % settings.BASE_URL)

  log_startup_parameters(options, arguments)
  log_settings(options)

  if platform.system() == 'Linux':
    import d1_client_onedrive.impl.drivers.fuse.d1_fuse as filesystem_callbacks
  elif platform.system() == 'Windows':
    import d1_client_onedrive.impl.drivers.dokan.d1_dokan as filesystem_callbacks
  else:
    log.error('Unknown platform: {0}'.format(platform.system()))
    exit()

  filesystem_callbacks.run(options, root_resolver)
  log.info("Exiting ONEDrive")


def log_setup(options):
  # Set up logging.
  log.setLevel(map_level_string_to_level(options.LOG_LEVEL))
  formatter = logging.Formatter(
    u'%(asctime)s %(levelname)-8s %(name)s'
    u'(%(pathname)s/%(lineno)d): %(message)s', u'%Y-%m-%d %H:%M:%S'
  )
  ## Log to a file
  #if options.LOG_FILE_PATH is not None:
  #    file_logger = logging.FileHandler(options.LOG_FILE_PATH, 'a', encoding='UTF-8')
  #    file_logger.setFormatter(formatter)
  #    logging.getLogger('').addHandler(file_logger)
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


def log_version():
  log.info('ONEDrive version: {0}'.format(impl.__version__))


def log_startup_parameters(options, arguments):
  log.debug('Mounting ONEDrive')
  log.debug('  Options: {0}'.format(str(options)))
  log.debug('  Arguments: {0}'.format(str(arguments)))


def log_settings(options):
  log.debug('Settings:')
  for k, v in sorted(options.__dict__.items()):
    if k == k.upper():
      log.debug('  {0}: {1}'.format(k, v))


if __name__ == '__main__':
  main()
