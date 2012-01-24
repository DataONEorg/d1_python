#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`setup`
====================

:Synopsis: Create egg.
:Author: DataONE (Dahl)
"""

from setuptools import setup, find_packages

setup(
  name='GMN Test Client',
  #version=d1_client.__version__,
  description='Extends d1_client.mnclient.MemberNodeClient with GMN specific test functionality',
  author='DataONE (Dahl)',
  url='http://dataone.org',
  packages=find_packages(),
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  }
)
