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
"""Export objects identifiers and related subjects strings to CSV

The CSV file can be analyzed to determine if objects have the expected
permissions.

Permissions are cumulative, so if a subject has, e.g., 'write' permissions on
an object, 'read' access is implied. So if multiple permissions have been given
to a subject for an object, only the highest permission is included in the list.
"""

from __future__ import absolute_import

import argparse
import logging

import d1_gmn.app.auth
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.sysmeta

import d1_common.types.exceptions
import d1_common.util
import d1_common.xml

import django.core.management.base


# noinspection PyClassHasNoInit,PyProtectedMember
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='debug level logging'
    )
    parser.add_argument(
      '--limit', type=int, default=0,
      help='limit number of objects exported. 0 (default) is no limit'
    )
    parser.add_argument('path', type=str, help='path to export file')

  def handle(self, *args, **opt):
    assert not args
    util.log_setup(opt['debug'])
    logging.info(
      u'Running management command: {}'.format(__name__) # util.get_command_name())
    )
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    logging.info(u'Exported object list to: {}'.format(opt['path']))
    with open(opt['path'], 'w') as f:
      for i, sciobj_model in enumerate(
          d1_gmn.app.models.ScienceObject.objects.order_by('pid__did')
      ):
        f.write(
          '{}\t{}\n'.format(
            sciobj_model.pid.did, ','.join([
              '{}={}'.format(subj, d1_gmn.app.auth.level_to_action(level))
              for (subj, level) in self.get_object_permissions(sciobj_model)
            ])
          )
        )
        if i + 1 == opt['limit']:
          break

  def get_object_permissions(self, sciobj_model):
    return [
      (p.subject.subject, p.level)
      for p in d1_gmn.app.models.Permission.objects.filter(sciobj=sciobj_model)
      .order_by('subject__subject')
    ]
