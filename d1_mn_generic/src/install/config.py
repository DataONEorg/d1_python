#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
:mod:`config.py`
====================

* Set up mod_wsgi entry for GMN.
* Create sqlite db file for GMN.
* Fix permissions.
* Copy fixed config values from .cfg file to database.
* Update GMN version from SVN revision number.
* Restart Apache.

.. moduleauthor:: Roger Dahl
'''

# StdLib.
import logging
import optparse
import os
import sys
import re
import ConfigParser

try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

import config_util
import svn_update


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  file_logger = logging.FileHandler(os.path.splitext(__file__)[0] + '.log', 'a')
  file_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(file_logger)
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def setup_mod_wsgi(httpd_conf_path, gmn_home_path):
  '''Set up mod_wsgi entry for GMN.'''

  gmn = '''
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias /mn {1}

<Directory {0}>
  WSGIApplicationGroup %{{GLOBAL}}
  Order deny,allow
  Allow from all
</Directory>
'''.format(gmn_home_path, os.path.join(gmn_home_path, 'gmn.wsgi'))

  # Write new config.
  conf_gmn_path = os.path.join(httpd_conf_path, 'gmn')
  try:
    cfg_file = open(conf_gmn_path, 'w')
    cfg_file.write(gmn)
  except EnvironmentError:
    logging.error('Could not write: {0}\n'.format(conf_gmn_path))
    raise


def apache_restart():
  '''Restart Apache.'''
  config_util.run(['apache2ctl', 'restart'])


def db_setup(gmn_home_path):
  '''Create sqlite db file for GMN.'''

  res = os.system('./manage.py syncdb')
  if res != 0:
    logging.error('db_setup failed.')
    sys.exit()


def fix_permissions(gmn_home_path):
  config_util.run(['chmod', 'g+w', '-R', gmn_home_path])
  config_util.run(['chown', ':www-data', '-R', gmn_home_path])


def copy_cfg_values():
  config = ConfigParser.ConfigParser()
  config.read(['./gmn.cfg'])
  for key, val in config.items('gmn'):
    config_util.set_node_val(key, val)


def update_version_from_svn():
  svn_update.update_version_from_svn()


def main():
  log_setup()

  # Command line options.
  parser = optparse.OptionParser()
  parser.add_option(
    '-g',
    '--gmn-home-path',
    dest='gmn_home_path',
    action='store',
    type='string',
    default='./'
  )
  parser.add_option(
    '-a',
    '--apache2-conf-path',
    dest='apache2_conf_path',
    action='store',
    type='string',
    default='/etc/apache2/conf.d/'
  )
  parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  if not options.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  gmn_home_path = os.path.abspath(options.gmn_home_path)

  # Set up mod_wsgi entry for GMN.
  setup_mod_wsgi(options.apache2_conf_path, gmn_home_path)

  # Create sqlite db file for GMN.
  db_setup(gmn_home_path)

  # Fix permissions.
  fix_permissions(gmn_home_path)

  # Copy fixed config values from .cfg file to database.
  copy_cfg_values()

  # Update GMN version from SVN revision number.
  update_version_from_svn()

  # Restart Apache.
  apache_restart()


if __name__ == '__main__':
  main()
