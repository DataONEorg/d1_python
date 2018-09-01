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
"""Top level module for ONEDrive

- Parse arguments
- Instantiate the Root resolver
- Mount FUSE / Dokan
"""

import logging
import optparse
import platform
import sys

import d1_onedrive.impl
import d1_onedrive.impl.clients
import d1_onedrive.impl.resolver

# flake8: noqa: F402

# if not hasattr(sys, 'frozen'):
#   sys.path.append(os.path.abspath(os.path.join('__file__', '../..')))

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


def main():
  if not check_dependencies.check_dependencies():
    raise Exception('Dependency check failed')

  parser = optparse.OptionParser('%prog [options]')
  parser.add_option(
    '-v', '--version', action='store_true',
    help='Display version information and exit'
  )

  # Add options to override defaults in settings.py.
  for k, v in list(settings.__dict__.items()):
    # Only allow overriding strings, ints and bools.
    if k.isupper():
      param_name = '--{}'.format(k.lower().replace('_', '-'))
      if type(v) is str or type(v) is int:
        parser.add_option(
          param_name, action='store', type=str(type(v).__name__),
          dest=k.lower(), default=v, metavar=v
        )
      elif type(v) is bool:
        if v:
          parser.add_option(
            '--disable-{}'.format(k.lower().replace('_', '-')),
            action='store_false', dest=k.lower(), metavar=v
          )
        else:
          parser.add_option(
            param_name, action='store_true', dest=k.lower(), metavar=v
          )

  (options, arguments) = parser.parse_args()

  # Copy non-string/int settings into options.
  for k, v in list(settings.__dict__.items()):
    if not (type(v) is str or type(v) is int or type(v) is bool) and k.isupper():
      options.__dict__[k.lower()] = v

  if len(arguments) > 0:
    parser.print_help()
    sys.exit()

  util.ensure_dir_exists(options.onedrive_cache_root)

  # Setup logging
  # logging.config.dictConfig(self._options.logging) # Needs 2.7
  log_setup(options)

  if options.version:
    log_version()
    sys.exit()

  #create the caches here and add references to them in options.
  #enables child resolvers to invalidate entries so that
  #changes can be reflected in the listings
  #options.attribute_cache = cache_disk.DiskCache(options.attribute_max_cache_items, 'cache_attribute')
  #options.directory_cache = cache_disk.DiskCache(options.directory_max_cache_items, 'cache_directory')
  options.attribute_cache = cache.Cache(options.attribute_max_cache_items)
  options.directory_cache = cache.Cache(options.directory_max_cache_items)

  log.info("Starting ONEDrive...")
  log_startup_parameters(options, arguments)

  if platform.system() == 'Linux' or platform.system() == 'Darwin':
    import d1_onedrive.impl.drivers.fuse.d1_fuse as filesystem_callbacks
  elif platform.system() == 'Windows':
    import d1_onedrive.impl.drivers.dokan.d1_dokan as filesystem_callbacks
  else:
    log.error('Unknown platform: {}'.format(platform.system()))
    exit()

  # Instantiate the Root resolver.
  with onedrive_zotero_client.ZoteroClient(options) as z:
    with object_tree.ObjectTree(options, z) as o:
      #with d1_object_tree.object_tree.ObjectTree(**options.__dict__) as object_tree:
      root_resolver = root.RootResolver(options, o)
      filesystem_callbacks.run(options, root_resolver)

  log.info("Exiting ONEDrive")


def log_setup(options):
  # Set up logging.
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(name)s'
    '(%(lineno)d): %(message)s', '%Y-%m-%d %H:%M:%S'
  )
  # Log to a file
  if options.log_file_path is not None:
    file_logger = logging.FileHandler(
      options.log_file_path, 'a', encoding='utf-8'
    )
    file_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(file_logger)
  # Also log to stdout
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger().addHandler(console_logger)
  # Shared log level for all loggers.
  logging.getLogger().setLevel(getattr(logging, options.log_level.upper()))


def log_version():
  log.info('ONEDrive version: {}'.format(d1_onedrive.__version__))


def log_startup_parameters(options, arguments):
  log.debug('Options: {}'.format(str(options)))
  log.debug('Arguments: {}'.format(str(arguments)))


if __name__ == '__main__':
  sys.exit(main())
