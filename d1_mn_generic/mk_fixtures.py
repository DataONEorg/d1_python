#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`mk_fixtures`
==================

:Synopsis:
  Create fixtures used by unit tests.

.. moduleauthor:: Roger Dahl
"""

import sys
import os

import settings

# Empty fixture.

f = open(os.path.join(settings.FIXTURE_DIRS, 'empty.fixture.json'), 'w')
f.write('[]')
f.close()

# Populated fixture.

# Populate db with information about filesystem objects.
if 'reset' in sys.argv:
  os.system('rm test_db.sq3')
  os.system('./manage.py syncdb')
  os.system('./manage.py update_db')
  os.system('./manage.py insert_test_log')

# Update the test fixture to match.
os.system(
  './manage.py dumpdata mn_service > {0}'.format(
    os.path.join(
      settings.FIXTURE_DIRS, 'base.fixture.json'
    )
  )
)
