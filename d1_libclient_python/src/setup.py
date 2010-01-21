#!/usr/bin/python
#

import sys
from distutils.core import setup
import pyd1

setup(
  name='PyD1',
  version=pyd1.__version__,
  description='A client for DataONE',
  author='Dave Vieglais',
  author_email='vieglais at ku edu',
  url='http://dataone.org',
  packages=['pyd1', ],
)
