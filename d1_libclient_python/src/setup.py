#!/usr/bin/python
#

import sys
from distutils.core import setup
import d1pythonitk

setup(
  name='Python DataONE Investigator Toolkit',
  version=pyd1.__version__,
  description='A client library for DataONE',
  author='Dave Vieglais',
  author_email='vieglais at ku edu',
  url='http://dataone.org',
  packages=['d1pythonitk', ],
)
