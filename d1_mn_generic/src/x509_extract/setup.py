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
  Build the DataONE Session object extraction Python extension.
:Author:
  DataONE (Dahl)
'''

from distutils.core import setup, Extension

module1 = Extension('x509_extract_session', sources=['x509_extract_session.c'])

setup(
  name='ExtractDataONESession',
  version='1.0',
  description='Extract DataONE Session object from PEM formatted X.509'
  'v3 certificate',
  ext_modules=[module1]
)
