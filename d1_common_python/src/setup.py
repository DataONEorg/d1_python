#!/usr/bin/python
#

import sys
from distutils.core import setup
import d1common

setup(
  name='D1 API Common',
  version=d1common.__version__,
  description='Common libraries for DataONE',
  author='Dave Vieglais',
  author_email='vieglais at ku edu',
  url='http://dataone.org',
  packages=['d1common', ],
)
