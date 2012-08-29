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
:mod:setup.py`
==============

:Synopsis: Build the DataONE Python Certificate extension.
:Author: DataONE (Dahl, Pippin)

'''

#from distutils.core import Extension
from setuptools import setup, find_packages, Extension
import d1_certificate_python

x509v3_module = Extension(
  'd1_x509v3_certificate_extractor',
  sources=[
    'extensions/d1_x509v3_certificate_extractor.c'
  ]
)

setup(
  name='d1_certificate',
  version=d1_certificate_python.__version__,
  author='Roger Dahl, Andy Pippin, and the DataONE Development Team',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  description='Python extension for extracting DataONE Session information from PEM formatted X.509 v3 certificates',
  packages=find_packages(),
  install_requires=[
    'DataONE_Common >= 1.0.0c7-SNAPSHOT',
  ],
  ext_modules=[
    x509v3_module,
  ],
)
