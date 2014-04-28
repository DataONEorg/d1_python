#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2014 DataONE
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
:mod:`get_certificate_primary_subject`
======================================

:Synopsis: Get DataONE compliant serialization of DN in PEM encoded X.509 certificate.
:Created: 2014-04-23
:Author: DataONE (Dahl)
'''

import sys

import d1_x509v3_certificate_extractor


def main():
  if len(sys.argv) != 2:
    print 'Usage: {0} <PEM encoded X.509 certificate file>'.format(sys.argv[0])
    exit(1)

  list_subjects(sys.argv[1])


def list_subjects(certificate_path):
  try:
    with open(certificate_path, 'rb') as f:
      subject, subject_info = d1_x509v3_certificate_extractor.extract(f.read())
  except IOError:
    print 'Error: Could not open file'
  print subject


if __name__ == '__main__':
  main()
