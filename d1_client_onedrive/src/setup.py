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
"""
:mod:`setup`
============

:Synopsis: Create egg.
:Author: DataONE (Dahl)
"""

from setuptools import setup, find_packages
import sys

# py2exe only needs to be present when building an executable on Windows.
# When py2exe is not present, the py2exe specific options below are ignored.
try:
  import py2exe
except ImportError:
  pass

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
    "py2exe": {
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
      resources=[
        'd1_client_onedrive/impl/d1.icon'
      ]
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

# The setup() parameters are described here:
# http://pythonhosted.org/setuptools/setuptools.html

setup(
  options = opts,
  name = 'dataone.onedrive',
  version = d1_client_onedrive.__version__,
  description = 'Filesystem access to the DataONE Workspace',
  author = 'DataONE Project',
  author_email = 'developers@dataone.org',
  url = 'http://dataone.org',
  license = 'Apache License, Version 2.0',
  packages = find_packages(),

  # Accept all data files and directories matched by MANIFEST.in or found in
  # source control.
  #include_package_data = True,

  # Dependencies that are available through PYPI / easy_install.
  install_requires = [
    'dataone.common == 1.1.2RC1',
    'dataone.libclient == 1.2.2',
    'dataone.workspace_client==0.0.1RC1',
    'fusepy',
    'rdflib',
  ],

  package_data = {
  },

  #entry_points = {
  #  'console_scripts': ['onedrive = d1_client_onedrive.onedrive:main',]
  #},

  data_files = [
    ('d1_client', ['./mime_mappings.csv']),
    ('', ['./workspace.xml']),
  ],

  **extra_opts
)
