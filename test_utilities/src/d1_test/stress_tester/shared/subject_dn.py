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
"""
:mod:`subject`
==============

:Created: 2012-07-12
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
"""

import re

# A DN is created by inserting a randomly generated string in the CN field
# in this tuple. It is typically not necessary to change the other fields
# from their defaults.
dn_tuple = (('DC', 'com'), ('DC', 'd1-stress-tester'), ('C', 'US'),
            ('O', 'd1-stress-tester'), ('CN', ''),)


def get_dn_by_subject(subject):
  return dn_tuple[:4] + (('CN', subject),)


def get_dataone_compliant_dn_serialization(dn):
  return ','.join(map('='.join, reversed(dn)))


def get_dataone_compliant_dn_serialization_by_subject(subject):
  return get_dataone_compliant_dn_serialization(get_dn_by_subject(subject))


def subject_to_filename(subject):
  return re.sub('\W', '_', subject)


def dataone_compliant_dn_serialization_to_dn_tuple(d1_dn_string):
  rdns = d1_dn_string.rsplit(',', 4)
  rdn_list = []
  for rdn in rdns:
    rdn_list.append(tuple(rdn.split('=')))
  return tuple(reversed(rdn_list))


if __name__ == '__main__':
  print((
    dataone_compliant_dn_serialization_to_dn_tuple(
      'CN=test1,test2,test3,O=d1-stress-tester,C=US,DC=d1-stress-tester,DC=com'
    )
  ))
