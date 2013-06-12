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
'''
:mod:`print_level`
==================

:Synopsis: Create a data package
:Created: 2011-12-02
:Author: DataONE (Dahl)
'''


def print_level(level, msg):
  ''' Print the information in as Unicode safe manner as possible.
  '''
  for l in unicode(msg).split(u'\n'):
    msg = u'%s%s' % (u'{0: <8s}'.format(level), unicode(l))
    print msg.encode('utf-8')


def print_debug(msg):
  print_level(u'DEBUG', unicode(msg))


def print_error(msg):
  print_level(u'ERROR', unicode(msg))


def print_warn(msg):
  print_level(u'WARN', unicode(msg))


def print_info(msg):
  print_level(u'', unicode(msg))
