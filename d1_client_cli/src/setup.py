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
  name='Python DataONE CLI',
  version=d1_client_cli.__version__,
  author='Andy Pippin',
  author_email='pippin at nceas dot ucsb dot edu',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  description='A DataONE Command-line interface',
  packages=find_packages(),

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    'pyxb >= 1.1.3',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  }
)
