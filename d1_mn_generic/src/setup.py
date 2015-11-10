#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2013 DataONE
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
"""
:mod:`setup`
============

:Synopsis: Create egg.
:Author: DataONE (Dahl)
:Notes:
  The script should be run in the current directory with ./setup.py.

  The setup() parameters are described here:
  http://pythonhosted.org/setuptools/setuptools.html
  http://docs.python.org/2/distutils/setupscript.html

  This setup script excludes unversioned python modules from the build if pysvn
  is installed. The only way I found to do this was to write a list of exclude
  directives to MANIFEST.in before calling setup().

  Unversioned data packages are automatically excluded as only versioned files
  are included with the "include_package_data = True" parameter.

  When creating the package, some warnings on the form:
  warning: no previously-included files found matching '<file>'
  will be generated, as the MANIFEST.in file will contain exclude directives for
  files that would not have been included
"""
import os
import re
from setuptools import setup, find_packages

try:
  import pysvn
except ImportError:
  has_svn = False
else:
  has_svn = True

import service

# Metadata.
name = 'dataone.generic_member_node'
version = service.__version__
description = 'DataONE Generic Member Node (GMN)'
author = 'DataONE Project'
author_email = 'developers@dataone.org'
url = 'http://dataone.org'
license = 'Apache License, Version 2.0'


def main():
  # This overwrites MANIFEST.in and automatically excludes any unversioned
  # python modules if pysvn is installed. This will include settings_site.py.
  # However, even if pysvn is not installed, it's important to exclude any
  # existing settings_site.py. So a default version of MANIFEST.in that excludes
  # settings_site.py is also versioned.
  if has_svn:
    create_manifest_in()

  setup(
    # Metadata
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    # Contents (modified by MANIFEST.in)
    packages=find_packages(),
    include_package_data=True,
    # Dependencies that are available through PyPI.
    install_requires=[
      # GMN uses dataone.common directly but, to keep the versions consistent,
      # let it be included by dataone.libclient.
      #'dataone.common',
      'dataone.libclient == 1.2.15.1',
      'dataone.certificate_extensions == 1.1.3',
      'django == 1.6.1',
      'pyxb == 1.2.3',
      'iso8601 == 0.1.4',
      'psycopg2 == 2.5.2',
      # GMN does not use the CLI programmatically -- it's just included because
      # the CLI is a convenient way to interact with GMN . So the latest version
      # is installed instead of a specific version.
      'dataone.cli >= 1.0.0',
    ],
  )


def create_manifest_in():
  with open('MANIFEST.in', 'w') as f:
    for p in get_unversioned_python_modules():
      f.write(u'exclude {0}\n'.format(p).encode('utf-8'))


def get_unversioned_python_modules():
  paths = []
  client = pysvn.Client()
  for s in client.status('.'):
    if not os.path.isfile(s.path):
      continue
    if not os.path.splitext(s.path)[1] == '.py':
      continue
    if s.is_versioned:
      continue
    paths.append(s.path)
  return paths


if __name__ == '__main__':
  main()
