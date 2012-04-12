#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`setup`
====================

:Synopsis: Create egg.
:Author: DataONE (Pippin)
"""

from setuptools import setup, find_packages
import d1_client_cli

setup(
  name='DataONE_CLI',
  version=d1_client_cli.__version__,
  author='Roger Dahl, and the DataONE Development Team',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  description='A DataONE Command-line interface',
  packages=find_packages(),

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    'DataONE_Common >= 1.0.0c5',
    'DataONE_ClientLib >= 1.0.0c5',
    'rdflib >= 2.4.2',
    'python-dateutil',
    'iso8601',
  ],
  dependency_links=[
    'http://foresite-toolkit.googlecode.com/files/foresite-1.2.tgz',
    #    'http://downloads.sourceforge.net/project/pyxb/pyxb/1.1.3/PyXB-full-1.1.3.tar.gz',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  },
  entry_points={
    'console_scripts': ['dataone = d1_client_cli.dataone:main', ]
  },
)
