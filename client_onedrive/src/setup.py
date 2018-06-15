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
"""DataONE ONEDrive Client package
"""

import sys

import setuptools

# yapf: disable


def main():
  setuptools.setup(
    name='dataone.onedrive',
    version='3.0.4',
    description='Filesystem access to the DataONE Workspace',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='https://github.com/DataONEorg/d1_python',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'dataone.common >= 3.0.4',
      'dataone.libclient >= 3.0.4',
      #
      'fusepy >= 2.0.4',
      'pyxb >= 1.2.6',
      'pyzotero >= 1.3.2',
      'rdflib >= 4.2.2',
      'requests >= 2.18.4',
    ],
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
    ],
    keywords='DataONE client upload download member-node coordinating-node',
    # Options for py2exe and py2app.
    options=opts,
    **extra_opts
  )


# Windows executable setup
if sys.platform == 'win32':
  opts = {
    'py2exe': {
      'packages': [
        'd1_client_onedrive',
        'd1_client_onedrive.impl',
        'd1_client_onedrive.impl.drivers',
        'd1_client_onedrive.impl.drivers.dokan',
        'd1_client_onedrive.impl.drivers.fuse',
        'd1_client_onedrive.impl.resolver',
        'rdflib.plugins',
      ],
      'skip_archive': True,
    },
  },
  extra_opts = dict(
    console=['d1_client_onedrive/onedrive.py'],
  ),

elif sys.platform == 'darwin':
  # Mac App setup
  opts = dict(
    py2app=dict(
      argv_emulation=True,
      iconfile='mac/mac_dataone.icns',
      packages=[
        'rdflib',
      ],
      site_packages=False,
      resources=[
        'd1_client_onedrive/impl/d1.icon',
      ],
      plist=dict(
        LSBackgroundOnly=True,
      ),
    ),
  ),
  extra_opts = dict(
    #app = ['d1_client_onedrive/onedrive.py'],
    app=[
      'mac/start_app.py',
    ],
    setup_requires=[
      'py2app',
    ],
  )
else:
  # Normal setup
  opts = dict()
  extra_opts = dict()


if __name__ == '__main__':
  main()
