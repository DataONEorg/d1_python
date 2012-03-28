#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`cli_util`
===============

:Synopsis: Utilities shared between components of the DataONE Command Line
  Interface
:Created: 2012-03-07
:Author: DataONE (Dahl)
'''

# Stdlib.
from print_level import * #@UnusedWildImport
import sys
import traceback


def _handle_unexpected_exception(max_traceback_levels=5):
  exc_type, exc_msgs = sys.exc_info()[:2] # ignore the traceback.
  #
  if exc_type.__name__ == 'SSLError':
    print_error('There was a problem with SSL, did you update your key?')
  elif exc_type.__name__ == 'MissingSysmetaParameters':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'InvalidArguments':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'NotFound':
    print_error(exc_msgs.__dict__['value'])
  elif exc_type.__name__ == 'ServiceFailure':
    print_error(
      'There was a problem with the response from the DataONE node. (error %d:%d)' %
      (exc_msgs.__dict__['errorCode'], exc_msgs.__dict__['detailCode'])
    )
  else:
    _print_unexpected_exception(max_traceback_levels)


def _print_unexpected_exception(max_traceback_levels=5):
  exc_class, exc_msgs, exc_traceback = sys.exc_info()
  print_error(u'Unexpected error:')
  print_error(u'  Name: {0}'.format(exc_class.__name__))
  print_error(u'  Value: {0}'.format(exc_msgs))
  try:
    exc_args = exc_msgs.__dict__["args"]
  except KeyError:
    exc_args = "<no args>"
  print_error('  Args: {0}'.format(exc_args))
  print_error('  Traceback:')
  for tb in traceback.format_tb(exc_traceback, max_traceback_levels):
    print_error('    {0}'.format(tb))
