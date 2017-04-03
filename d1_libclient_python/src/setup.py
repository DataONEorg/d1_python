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
"""DataONE Client Library package
"""
import setuptools

import d1_client


def main():
  setuptools.setup(
    name='dataone.libclient',
    version=d1_client.__version__,
    description='A DataONE client library for Python',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='http://dataone.org',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'dataone.common == 2.1.0rc2',
      'rdflib == 4.2.2',
      'google.foresite-toolkit == 1.3.3',
      'python-dateutil == 2.1',
      # Requests
      'requests[security] == 2.12.4',
      'cachecontrol == 0.11.7',
      'requests-toolbelt == 0.7.0',
    ],
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
  )


if __name__ == '__main__':
  main()
