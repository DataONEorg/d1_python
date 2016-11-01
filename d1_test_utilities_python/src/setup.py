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
"""DataONE Test Utilities package
"""
import os
import re
import setuptools

import d1_test


def main():
  setuptools.setup(
    name='dataone.test_utilities',
    version=d1_test.__version__,
    description='Utilities for testing DataONE infrastructure components',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='http://dataone.org',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'multi-mechanize',
      'dataone.libclient == 1.2.5',
      'dataone.certificate_extensions == 1.1.1',
    ],
    setup_requires=[
      'setuptools_git >= 1.1'
    ],
  )


if __name__ == '__main__':
  main()
