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
"""Populate a Member Node with randomly generated objects
"""

import io
import logging
import optparse
import sys

from . import test_object_generator

import d1_common.types.exceptions

import d1_client.mnclient
import d1_client.mnclient_2_0

# Defaults
MN_BASE_URL = 'https://localhost/mn'
CERT_PUB_PEM_PATH = None
CERT_KEY_PEM_PATH = None
TIMEOUT_SEC = 60
NUM_OBJECTS = 1000
NUM_MIN_BYTES = 1024 * 10
NUM_MAX_BYTES = 1024 * 100


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  parser = optparse.OptionParser()

  parser.add_option(
    '--mn-base-url',
    action='store',
    type='string',
    default=MN_BASE_URL,
    help='The base URL for the Member Node to populate',
  )
  parser.add_option(
    '--cert-pub',
    dest='cert_pem_path',
    action='store',
    type='string',
    default=CERT_PUB_PEM_PATH,
    help='Path to PEM formatted public key of certificate',
  )
  parser.add_option(
    '--cert-key',
    dest='cert_key_path',
    action='store',
    type='string',
    default=CERT_KEY_PEM_PATH,
    help='Path to PEM formatted private key of certificate',
  )
  parser.add_option(
    '--timeout',
    dest='timeout_sec',
    action='store',
    type='float',
    default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
    help='Amount of time to wait for calls to complete (seconds)',
  )
  parser.add_option(
    '--num-objects',
    action='store',
    type='int',
    default=NUM_OBJECTS,
    help='Number of objects to create',
  )
  parser.add_option(
    '--num-min-bytes',
    action='store',
    type='int',
    default=NUM_MIN_BYTES,
    help='Minimum number of bytes in each object',
  )
  parser.add_option(
    '--num-max-bytes',
    action='store',
    type='int',
    default=NUM_MAX_BYTES,
    help='Maximum number of bytes in each object',
  )
  parser.add_option(
    '--disable-tls-validate',
    action='store_true',
    help='Disable validation of server side certificate',
  )
  parser.add_option(
    '--use-v1',
    action='store_true',
    help='Use the v1 API (v2 is default)',
  )
  parser.add_option(
    '--debug',
    action='store_true',
    help='Debug level logging',
  )

  (options, args) = parser.parse_args()

  logging.getLogger('').setLevel(
    logging.DEBUG if options.debug else logging.INFO
  )

  if options.use_v1:
    mn_client = d1_client.mnclient.MemberNodeClient(
      options.mn_base_url,
      cert_pem_path=options.cert_pem_path,
      cert_key_path=options.cert_key_path,
    )
  else:
    mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      options.mn_base_url,
      cert_pem_path=options.cert_pem_path,
      cert_key_path=options.cert_key_path,
    )

  for _ in range(options.num_objects):
    pid = test_object_generator.generate_random_ascii('pid')
    sysmeta_pyxb, sciobj_bytes = (
      test_object_generator.generate_science_object_with_sysmeta(
        pid,
        options.num_min_bytes,
        options.num_max_bytes,
        use_v1_bool=options.use_v1,
      )
    )
    try:
      mn_client.create(
        pid,
        io.BytesIO(sciobj_bytes),
        sysmeta_pyxb,
      )
    except d1_common.types.exceptions.DataONEException as e:
      logging.exception('MNStorage.create() failed with exception:')
      if e.traceInformation and len(e.traceInformation) >= 100:
        trace_path = 'traceInformation.out'
        with open(trace_path, 'wb') as f:
          f.write(e.traceInformation)
          logging.error(
            'Dumped traceInformation to file: {}'.format(trace_path)
          )
          sys.exit()


if __name__ == '__main__':
  sys.exit(main())
