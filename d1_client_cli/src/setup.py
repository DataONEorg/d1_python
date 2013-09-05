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
:Author: DataONE (Pippin)
"""

from setuptools import setup, find_packages
import d1_client_cli

setup(
  name='dataone.cli',
  version=d1_client_cli.__version__,
  description='A DataONE Command-line interface',
  author='DataONE Project',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  packages=find_packages(),

  # Accept all data files and directories matched by MANIFEST.in or found in
  # source control.
  #include_package_data = True,

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    'dataone.common == 1.1.2RC1',
    'dataone.libclient == 1.2.1',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  },
  entry_points={
    'console_scripts': ['dataone = d1_client_cli.dataone:main', ]
  },
)
