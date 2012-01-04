#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`mk_fixtures`
==================

:Synopsis: Create fixtures used by unit tests.
:Author: DataONE (Dahl)
"""

import sys
import os
import re

import settings

# Populate db with information about filesystem objects.
if 'reset' in sys.argv:
  print os.system('rm test_db.sq3')
  print os.system('./manage.py syncdb')
  print os.system('./manage.py update_db')
  print os.system('./manage.py insert_test_log')

# Create fixtures.

for fixture_dir in settings.FIXTURE_DIRS:
  # Create empty fixtures.
  f = open(os.path.join(fixture_dir, 'empty.fixture.json'), 'w')
  f.write('[]')
  f.close()

  # Create populated fixtures to match current db contents.
  m = re.match(r'.*/(.*)/fixtures', fixture_dir)
  if m:
    app = m.group(1)
    cmd = './manage.py dumpdata {0} > \'{1}\''.format(
      app, os.path.join(
        fixture_dir, 'base.fixture.json'
      )
    )
    print cmd
    print os.system(cmd)
