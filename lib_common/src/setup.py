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
"""DataONE Common Library package
"""

import setuptools


def main():
  setuptools.setup(
    name='dataone.common',
    version='2.4.2',
    description=(
      'Contains functionality common to projects that interact with '
      'the DataONE infrastructure via Python'
    ),
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='https://github.com/DataONEorg/d1_python',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'contextlib2 == 0.5.5',
      'cryptography == 2.1.4',
      'iso8601 == 0.1.12',
      'PyJWT == 1.5.3',
      'pyasn1 == 0.4.2',
      'pyxb == 1.2.6',
      'rdflib == 4.2.2',
      'zipstream == 1.1.4',
    ],
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
    ],
    keywords=(
      'DataONE client server member-node coordinating-node xml url oai-ore rdf '
      'resource-map'
    ),
  )


if __name__ == '__main__':
  main()
