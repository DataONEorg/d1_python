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
"""View and manipulate object event records
"""

import argparse

import d1_common.types.exceptions
import d1_common.util

import django.core.management.base


# noinspection PyClassHasNoInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument('command', choices=['view'], help='Action')

  def handle(self, *args, **opt):
    assert not args
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    if opt['command'] == 'view':
      self._view()
    else:
      assert False

  def _view(self):
    # TODO: Implement
    assert NotImplementedError()
