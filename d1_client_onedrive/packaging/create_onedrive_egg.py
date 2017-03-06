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
"""
Created on Jan 11, 2013

@author: brumgard
"""
import sys
import tarfile
from setuptools import setup, find_packages

sys.argv = [sys.argv[0], 'bdist_egg']

#tarball = tarfile.open(name='deps/dataone.common-1.1.0-RC3.tar.gz', mode='r:gz')
#tarball.extractall('./tmp')

setup(
  name="Onedrive", version="0.1",
  py_modules=['main', '__main__', 'onedrive', 'settings'], package_dir={
    'impl': '../src/impl',
    'onedrive': '../src/',
    'd1_common': 'deps/dataone.common-1.1.0/d1_common',
    'iso8601': 'deps/iso8601-0.1.4/iso8601',
    'd1_client': 'deps/dataone.libclient-1.1.0/d1_client',
    'pyxb': 'deps/PyXB-1.2.1/pyxb',
    'rdflib': 'deps/rdflib-2.4.2/rdflib',
    'foresite': 'deps/foresite-1.2/foresite',
    'lxml': 'deps/lxml-3.1beta1/lxml',
    'fuse': 'deps/fuse'
  }, packages=[
    'onedrive', 'impl', 'impl.drivers', 'impl.drivers.fuse', 'impl.resolver',
    'd1_common', 'd1_common.types', 'd1_common.types.generated', 'iso8601',
    'd1_client', 'pyxb', 'pyxb.namespace', 'pyxb.utils', 'pyxb.binding',
    'rdflib', 'rdflib.syntax', 'rdflib.store', 'rdflib.syntax.serializers',
    'rdflib.syntax.parsers', 'rdflib.sparql', 'foresite', 'lxml', 'fuse'
  ], entry_points={
    'setuptools.installation': [
      'eggsecutable = main:entrypoint0',
    ]
  }, package_data={
    'lxml':
      [
        'resources/macosx/*.dylib',
        'resources/linux/x86_64/*.so',
        'resources/windows/amd64/*.pyd',
      ],
    'd1_client': [
      'mime_mappings.csv',
    ],
  }
)
