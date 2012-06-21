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

:platform:
  Linux
:Synopsis:
  Build and install the DataONE x509v3 Certificate Generator extension.
:Author:
  DataONE (Dahl)
'''

from distutils.core import setup, Extension

module1 = Extension(
  'd1_x509v3_certificate_generator',
  sources=['d1_x509v3_certificate_generator.c']
)

setup(
  name='DataONEx509v3CertificateGenerator',
  version='1.0',
  description='Python extension for creating a PEM formatted X.509 v3 '
  'certificate that contains a DataONE Session object and is '
  'signed by the DataONE Test CA',
  ext_modules=[module1]
)
