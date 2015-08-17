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

  Notes:

  - This script automatically includes all files (.py and others) that are in
    Subversion in the package and installs those same files.

  - We don't use MANIFEST or MANIFEST.in because they imply a fixed set of
    files, and we want to automatically include only versioned files.
"""
import locale
import os
import re
import setuptools
import sys

import d1_client

# Metadata.
name = 'dataone.libclient'
version = d1_client.__version__
description = 'A DataONE client library for Python'
author = 'DataONE Project'
author_email = 'developers@dataone.org'
url = 'http://dataone.org'
license = 'Apache License, Version 2.0'


def main():
  # Enable SVN to work with filenames containing Unicode.
  #locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

  # Without a list of packages specified with the packages parameter, nothing
  # gets installed. While, with a list of packages specified, unversioned files
  # are included in the package and are also installed. The solution is to
  # specify packages only at install time, not at build time.
  if 'install' in sys.argv:
    packages = setuptools.find_packages()
  else:
    packages = None

  setuptools.setup(
    # Metadata
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,

    # Selection of files to include in package and to later install.
    packages=packages,
    # include_package_data = True does not affect which files get included in
    # the package, only which files that are installed. Without
    # include_package_data = True, data files that are included in the package
    # because they are versioned are not installed.
    include_package_data=True,
    # package_data is only used when building binary packages (bdist). It is not
    # relevant for source packages (sdist).
    # package_data,

    # Dependencies that are available through PyPI.
    install_requires=[
      'dataone.common == 1.1.8',
      'rdflib == 4.0.1',
      'google.foresite-toolkit == 1.3',
      'python-dateutil == 2.1',
    ],
  )


if __name__ == '__main__':
  main()
