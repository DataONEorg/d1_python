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
''':mod:`fs`
============

:Synopsis:
 - Filesystem mockups.
:Author: DataONE (Dahl)
'''

import datetime

#d = datetime.datetime.now()
d = datetime.datetime(2005, 5, 23, 11, 12, 13)

fs = (
  ('fa', 50, d), ('fb', 51, d), (
    'd', (
      ('f2a', 52, d), ('f2b', 53, d), ('f2c', 54, d), ('d2', (('f3a', 55, d),
                                                              ('f3b', 56, d), ), d)
    ), d
  )
)
