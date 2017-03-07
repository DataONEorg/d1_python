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
subject which has access to the object.
"""

from __future__ import absolute_import

# Stdlib.
import logging

# Django.
import django.core.management.base

# App.
import app.management.commands.util
import app.models


# noinspection PyClassHasNoInit
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
    parser.add_argument('path', type=str, help='path to export file')

  def handle(self, *args, **options):
    app.management.commands.util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.
      format(app.management.commands.util.get_command_name())
    )
    app.management.commands.util.abort_if_other_instance_is_running()
    self.export_object_list(options['path'], options['public'])
    logging.info(u'Exported object list to: {}'.format(options['path']))

  def export_object_list(self, path, public_only):
    with open(path, 'w') as f:
      for sciobj_model in app.models.ScienceObject.objects.all():
        # Permissions are cumulative, so if a subject has permissions for an
        # object, that permissions are guaranteed to include "read", the
        # lowest level permission.
        for permission_model in app.models.Permission.objects.filter(
            sciobj=sciobj_model
        ):
          if public_only:
            if permission_model.subject.subject == 'public':
              f.write('{}\n'.format(sciobj_model.pid.did))
          else:
            f.write(
              '{}\t{}\n'.
              format(sciobj_model.pid.did, permission_model.subject.subject)
            )
