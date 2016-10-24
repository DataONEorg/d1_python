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

"""Update the CRUD whitelist

When running in production, GMN requires that subjects that wish to create,
update or delete science objects are registered in a whitelist. This command
manages the whitelist.
"""

# Stdlib.
import logging

# Django.
import django.core.management.base

# App.
import mn.models


class Command(django.core.management.base.BaseCommand):
  help = 'Set the whitelist for create, update and delete operations'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )
    parser.add_argument(
      'path', type=str, help='path to file containing subjects to whitelist'
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    num_subjects = self.set_whitelist(options['path'])
    print u'Whitelisted {} subjects'.format(num_subjects)

  def set_whitelist(self, whitelist_path):
    with open(whitelist_path) as f:
      mn.models.WhitelistForCreateUpdateDelete.objects.all().delete()
      cnt = 0
      for subject_str in f:
        subject_str = subject_str.strip()
        if subject_str == '' or subject_str.startswith('#'):
          continue
        mn.models.whitelist_for_create_update_delete(subject_str)
        cnt += 1

    return cnt
