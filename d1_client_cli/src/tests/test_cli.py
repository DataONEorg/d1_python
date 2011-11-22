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
:mod:`test_cli`
==============

:Synopsis:
  Unit tests for DataONE Command Line Interface
:Created: 2011-11-20
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import optparse
import os
import unittest
import uuid
import sys

# D1.
import d1_common

# App.
sys.path.append('../d1_client_cli/')
import dataone


class TestDataONECLI(unittest.TestCase):
  def test_create(self):
    # Generate PID.
    pid = '_invalid_test_object_{0}'.format(uuid.uuid4())

    args = []
    args.append('--sysmeta-object-format \'application/octet-stream\'')
    args.append('--sysmeta-rightsholder somerightsholder')
    args.append('--sysmeta-authoritative-member-node gmn-dev')

    #args.append('--sysmeta-access-policy \'<?xml version=\"1.0\" ?><ns1:accessPolicy xmlns:ns1=\"http://ns.dataone.org/service/types/v1\"><allow><subject>test_subject</subject><permission>read</permission></allow></ns1:accessPolicy>\'')

    args.append('--cert-path x509up_u1000')
    #args.append('--key-path x509up_u1000')
    #
    cli = dataone.DataONECLI(opts, args)
    #cmd = './dataone.py {0} create abc test.sciobj'.format(' '.join(args))
    #print cmd
    #os.system(cmd)


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option(
    '--dataone-url',
    dest='dataone_url',
    action='store',
    type='string',
    default=d1_common.const.URL_DATAONE_ROOT,
    help='URL to DataONE Root'
  )

  # https://demo1.test.dataone.org/knb/d1/mn/v1
  # https://localhost:443/mn/
  # https://knb-test-1.test.dataone.org/knb/d1/mn/v1
  parser.add_option(
    '--mn-url',
    dest='mn_url',
    action='store',
    type='string',
    default='http://localhost:8000/',
    help='URL to Member Node'
  )

  parser.add_option(
    '--cn-url',
    dest='cn_url',
    action='store',
    type='string',
    default='http://localhost:8000/cn/',
    help='URL to Coordinating Node'
  )
  parser.add_option(
    '--test', action='store',
    default='',
    dest='test',
    help='run a single test'
  )
  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')

  (opts, args) = parser.parse_args()

  if not opts.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  unittest.main(argv=sys.argv)


if __name__ == '__main__':
  main()
