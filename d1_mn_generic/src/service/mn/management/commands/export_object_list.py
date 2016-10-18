#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
""":mod:`generate_object_list`
==============================

:Synopsis:
  Create a list of the objects that exist on the MN and, for each object,
  each subject which has read access to the object. The list is used by the
  DataONE Stress Tester.
:Author: DataONE (Dahl)
"""

# Stdlib.
import logging
import os
import sys

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
import mn.models

# Django.
import django.core.management.base
from optparse import make_option

# Get an instance of a logger.
logger = logging.getLogger()


class Command(django.core.management.base.BaseCommand):
  args = '<file name>'
  option_list = BaseCommand.option_list + (
    make_option(
      '--public',
      action='store_true',
      dest='public_only',
      default=False,
      help='Create list containing only public subjects'
    ),
  )
  help = 'Create list of all objects and their associated subjects'

  def handle(self, *args, **options):
    if len(args) != 1:
      print('Must specify the path to a file in which to store the object list')
      exit()

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    object_list_path = args[0]

    self.create_object_list(object_list_path, options['public_only'])

    print 'Saved object list to: {}'.format(object_list_path)

  def create_object_list(self, path, public_only):
    with open(path, 'w') as f:
      for o in mn.models.ScienceObject.objects.all():
        # Permissions are cumulative, so if a subject has permissions for an
        # object, that permissions are guaranteed to include "read", the
        # lowest level permission.
        for p in mn.models.Permission.objects.filter(object=o):
          if public_only:
            if p.subject.subject == 'public':
              f.write('{}\n'.format(o.pid))
          else:
            f.write('{}\t{}\n'.format(o.pid, p.subject.subject))
