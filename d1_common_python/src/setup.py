#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`setup`
====================

:Synopsis:
  Create egg.

.. moduleauthor:: Roger Dahl
"""

from setuptools import setup, find_packages

setup(
  name='Python DataONE Common',
  #version=d1_client.__version__,
  description='Contains functionality common to projects that interact with the DataONE infrastructure via Python',
  author='Dave Vieglais',
  author_email='vieglais at ku edu',
  url='http://dataone.org',
  packages=find_packages(),

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    # iso860
    'iso8601 >= 0.1',
    # PyXB
    'pyxb >= 1.1.2',
  ],
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst'],
  }
)
