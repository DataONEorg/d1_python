#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`setup`
====================

:Synopsis: Create egg.
:Author: DataONE (Dahl)
"""

from setuptools import setup, find_packages
import d1_common

setup(
  name='DataONE_Common',
  version=d1_common.__version__,
  author='DataONE Project',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  description='Contains functionality common to projects that interact with the DataONE infrastructure via Python',
  license='Apache License, Version 2.0',
  packages=find_packages(),

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    'iso8601 >= 0.1',
    'pyxb >= 1.1.2',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  }
)
