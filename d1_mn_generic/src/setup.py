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
"""Generic Member Node (GMN) package
"""

import setuptools

import gmn.app


def main():
  setuptools.setup(
    name='dataone.gmn',
    version=gmn.app.__version__,
    description='DataONE Generic Member Node (GMN)',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='http://dataone-python.readthedocs.io/en/latest/gmn/index.html',
    license='Apache License, Version 2.0',

    packages=setuptools.find_packages(),
    include_package_data=True,

    install_requires=[
      # GMN uses dataone.common directly but, to keep the versions consistent,
      # let it be included by dataone.libclient.
      #'dataone.common',
      'dataone.libclient == 2.0.0',
      'django == 1.10.1',
      'pyxb == 1.2.5',
      'iso8601 == 0.1.11',
      'psycopg2 == 2.5.2',
      'pyjwt == 1.4.2',
      'cryptography == 1.5.2',
      # GMN does not use the CLI programmatically -- it's just included because
      # the CLI is a convenient way to interact with GMN. So the latest version
      # is installed instead of a specific version.
      'dataone.cli >= 1.0.0',
      # Temporary, until upgrading libclient to 2.0.1.
      'requests[security] == 2.12.4',
    ],

    setup_requires=[
      'setuptools_git >= 1.1'
    ],
  )


if __name__ == '__main__':
  main()
