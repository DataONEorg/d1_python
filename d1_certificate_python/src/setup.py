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
'''
:mod:`setup`
============

:Synopsis:
  - Build the DataONE Python Certificate extensions.
  - Create egg.
:Author: DataONE (Dahl)
'''

from setuptools import setup, find_packages, Extension
import d1_certificate_python

x509v3_certificate_extractor = Extension(
  'd1_x509v3_certificate_extractor',
  sources=[
    'extensions/d1_x509v3_certificate_extractor.c'
  ]
)

x509v3_certificate_generator = Extension(
  'd1_x509v3_certificate_generator',
  sources=[
    'extensions/d1_x509v3_certificate_generator.c'
  ]
)

setup(
  name='dataone.certificate_extensions',
  version=d1_certificate_python.__version__,
  description='Python extensions for generating and extracting PEM formatted X.509 v3 certificates that contain DataONE Session information',
  author='DataONE Project',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',

  # Accept all data files and directories matched by MANIFEST.in or found in
  # source control.
  include_package_data=True,
  install_requires=[
    'dataone.common == 1.1.2RC1',
  ],
  ext_modules=[
    x509v3_certificate_extractor,
    x509v3_certificate_generator,
  ],
)
