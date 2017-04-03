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
"""DataONE Command-Line Interface package
"""
import setuptools

import d1_client_cli


def main():
  setuptools.setup(
    name='dataone.cli',
    version=d1_client_cli.__version__,
    description='A DataONE Command-line interface',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='http://dataone.org',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      # The CLI uses dataone.common directly but, to keep the versions
      # consistent, let it be included by dataone.libclient.
      'dataone.libclient == 2.1.0rc2',
    ],
    entry_points={'console_scripts': [
      'dataone = d1_client_cli.dataone:main',
    ]},
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
  )


if __name__ == '__main__':
  main()
