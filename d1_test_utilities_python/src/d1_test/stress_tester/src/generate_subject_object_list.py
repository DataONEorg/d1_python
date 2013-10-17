#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
''':mod:`generate_list_for_get`
===============================

:Synopsis: Get from the GMN database: List of valid subjects and the objects
  that each subjec that permissions for.
:Author: DataONE (Dahl)
'''
# Stdlib.
import logging
import optparse
import os
import re
import sys
import unittest

# 3rd party.
import psycopg2

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_instance_generator.subject
import d1_instance_generator.random_data

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('./shared/'))
import settings
import subject_dn

# Get an instance of a logger.
logger = logging.getLogger()

q = '''
select s.pid, u.subject from mn_scienceobject s
join mn_permission p on p.object_id = s.id
join mn_permissionsubject u on u.id = p.subject_id
'''


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser('usage: %prog [options]')
  parser.add_option('--verbose', dest='verbose', action='store_true', default=False)
  (options, arguments) = parser.parse_args()

  if len(arguments) != 0:
    logging.error('No arguments are required')
    exit()

  get_subjects_and_objects()


def get_subjects_and_objects():
  # get a connection, if a connect cannot be made an exception will be raised here
  conn = psycopg2.connect(settings.GMN_CONNECTION_STRING)
  cursor = conn.cursor()
  cursor.execute(q)
  records = cursor.fetchall()

  with open(settings.SUBJECTS_AND_OBJECTS_PATH, 'wb') as f:
    for r in records:
      f.write(r[0] + '\t' + r[1] + '\n')


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  main()
