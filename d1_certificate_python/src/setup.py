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
"""DataONE Python X.509 v3 Certificate Extensions package
"""
import setuptools

import d1_certificate

x509v3_certificate_extractor = setuptools.Extension(
  name='d1_certificate.extensions.d1_x509v3_certificate_extractor',
  sources=[
    'd1_certificate/extensions/d1_x509v3_certificate_extractor.c'
  ],
  libraries=[
    #'ssl',
    'crypto'
  ],
)

x509v3_certificate_generator = setuptools.Extension(
  name='d1_certificate.extensions.d1_x509v3_certificate_generator',
  sources=[
    'd1_certificate/extensions/d1_x509v3_certificate_generator.c'
  ],
  libraries=[
    #'ssl'
    'crypto'
  ],
)


def main():
  setuptools.setup(
    # Metadata
    name='dataone.certificate_extensions',
    version=d1_certificate.__version__,
    description='Python extensions for generating and extracting PEM formatted X.509 v3 certificates that contain DataONE Session information',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='http://dataone.org',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'dataone.common == 2.0.0',
    ],
    ext_modules=[
      x509v3_certificate_extractor,
      x509v3_certificate_generator,
    ],
    setup_requires=[
      'setuptools_git >= 1.1'
    ],
  )


if __name__ == '__main__':
  main()
