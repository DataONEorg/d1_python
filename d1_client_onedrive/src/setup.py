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
import locale
import os
import re
import setuptools
import sys

from setuptools import setup, find_packages

# py2exe only needs to be present when building an executable on Windows.
# When py2exe is not present, the py2exe specific options below are ignored.
try:
  import py2exe
except ImportError:
  pass

try:
  import pysvn
except ImportError:
  has_svn = False
else:
  has_svn = True

import d1_client_onedrive

# http://www.py2exe.org/index.cgi/WorkingWithVariousPackagesAndModules
#
# lxml
#
# if missing _elementhpath, either pull whole lxml library in packages=..., or
# put "from lxml import _elementhpath as _dummy" somewhere in code; in both
# cases also pull gzip in packages=...

# Windows executable setup
if sys.platform == 'win32':
  opts = {
    'py2exe': {
      'packages': [
        'd1_client_onedrive',
        'd1_client_onedrive.impl',
        'd1_client_onedrive.impl.drivers',
        'd1_client_onedrive.impl.drivers.dokan',
        'd1_client_onedrive.impl.drivers.fuse',
        'd1_client_onedrive.impl.resolver',
        'rdflib.plugins',
        'lxml'
      ],
      'skip_archive': True,
    }
  }
  extra_opts = dict(console=['d1_client_onedrive/onedrive.py'], )
# Mac App setup
elif sys.platform == 'darwin':
  opts = dict(
    py2app=dict(
      argv_emulation=True,
      iconfile='mac/mac_dataone.icns',
      packages=['rdflib', 'lxml'],
      site_packages=True,
      resources=['d1_client_onedrive/impl/d1.icon']
      #resources = ['mime_mappings.csv',]
    )
  )
  extra_opts = dict(
    #app = ['d1_client_onedrive/onedrive.py'],
    app=['mac/start_app.py'],
    setup_requires=['py2app'],
  )
# Normal setup
else:
  opts = dict()
  extra_opts = dict()

# Metadata.
name = 'dataone.onedrive'
version = d1_client_onedrive.__version__
description = 'Filesystem access to the DataONE Workspace'
author = 'DataONE Project'
author_email = 'developers@dataone.org'
url = 'http://dataone.org'
license = 'Apache License, Version 2.0'


def main():
  # Enable SVN to work with filenames containing Unicode.
  locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

  if has_svn:
    create_manifest_in()

  setuptools.setup(
    # Metadata
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    # Dependencies that are available through PyPI.
    install_requires=[
      'dataone.common == 1.1.3',
      'dataone.libclient == 1.2.3',
      'dataone.workspace_client == 0.0.2',
      'fusepy',
      'rdflib',
    ],
    data_files=[
      ('d1_client', ['./mime_mappings.csv']),
      (
        '', [
          './workspace.xml'
        ]
      ),
    ],
    # Options for py2exe and py2app.
    options=opts,
    **extra_opts
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
