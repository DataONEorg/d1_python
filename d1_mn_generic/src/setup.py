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
"""
:mod:`setup`
============

:Synopsis: Create egg.
:Author: DataONE (Dahl)
:Notes:
  The script should be run in the current directory with ./setup.py.

  The setup() parameters are described here:
  http://pythonhosted.org/setuptools/setuptools.html
  http://docs.python.org/2/distutils/setupscript.html

  This uses an explicit MANIFEST file. Remember to update it when files are
  added or removed.
"""
import os
import re
from setuptools import setup, find_packages

import service

# Metadata.
name = 'dataone.generic_member_node'
version = service.__version__
description = 'DataONE Generic Member Node (GMN)'
author = 'DataONE Project'
author_email = 'developers@dataone.org'
url = 'http://dataone.org'
license = 'Apache License, Version 2.0'


def main():
  setup(
    # Metadata
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    # Contents (modified by MANIFEST.in)
    packages=find_packages(),
    include_package_data=True,
    # Dependencies that are available through PyPI.
    install_requires=[
      # GMN uses dataone.common directly but, to keep the versions consistent,
      # let it be included by dataone.libclient.
      #'dataone.common',
      'dataone.libclient == 1.2.6',
      'dataone.certificate_extensions == 1.1.3',
      'django == 1.6.1',
      'pyxb == 1.2.3',
      'iso8601 == 0.1.4',
      'psycopg2 == 2.5.2',
      # GMN does not use the CLI programmatically -- it's just included because
      # the CLI is a convenient way to interact with GMN . So the latest version
      # is installed instead of a specific version.
      'dataone.cli >= 1.0.0',
    ],
  )


if __name__ == '__main__':
  main()
