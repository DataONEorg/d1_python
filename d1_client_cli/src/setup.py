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
====================

:Synopsis: Create egg.
:Author: DataONE (Pippin)
"""

from setuptools import setup, find_packages
import d1_client_cli

setup(
  name='DataONE_CLI',
  version=d1_client_cli.__version__,
  author='Roger Dahl, and the DataONE Development Team',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  description='A DataONE Command-line interface',
  packages=find_packages(),

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    'DataONE_Common >= 1.0.0',
    'DataONE_ClientLib >= 1.0.0',
    'rdflib >= 2.4.2',
    'python-dateutil',
    'PyXB >= 1.1.2',
    'iso8601',
  ],
  dependency_links=[
    'http://foresite-toolkit.googlecode.com/files/foresite-1.2.tgz',
    'http://downloads.sourceforge.net/project/pyxb/pyxb/1.1.3/PyXB-full-1.1.3.tar.gz',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  },
  entry_points={
    'console_scripts': ['dataone = d1_client_cli.dataone:main', ]
  },
)
