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

"""Export a list of the objects that exist on the MN and, for each object, each
subject which has access to the object. The list is used by the DataONE Stress
Tester.
"""

# Stdlib.
import logging

# Django.
import django.core.management.base

# App.
import mn.models
import util


class Command(django.core.management.base.BaseCommand):
  help = 'Export all objects and their associated subjects'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )
    parser.add_argument(
      '--public',
      action='store_true',
      default=False,
      help='export only public subjects',
    )
    parser.add_argument(
      'path', type=str, help='path to export file'
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    self.create_object_list(options['path'], options['public'])
    print u'Exported object list to: {}'.format(object_list_path)

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
