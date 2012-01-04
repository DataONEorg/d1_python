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
''':mod:`register`
==================

:Synopsis: Register a new Member Node with DataONE.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import optparse
import os
import sys

# D1.
import d1_client.cnclient

import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def update_verbose(verbose):
  if verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)


def load_node_doc(node_xml_path):
  try:
    with open(node_xml_path, 'rb') as f:
      return dataoneTypes.CreateFromDocument(f.read())
  except IOError:
    logging.error('Unable to read node document file: {0}'.format(node_xml_path))
    raise


def register(options, arguments):
  try:
    node = load_node_doc(arguments[0])
  except IOError:
    return

  client = d1_client.cnclient.CoordinatingNodeClient(
    options.dataone_url,
    certfile=options.cert_path,
    keyfile=options.key_path
  )

  response = client.registerResponse(node)

  logging.info('Server response:\n{0}'.format(response.read()))


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser(
    'usage: %prog [options] <node registration xml document>'
  )
  parser.add_option('--verbose', dest='verbose', action='store_true', default=False)
  parser.add_option('--node', dest='node', action='store', type='string')
  parser.add_option(
    '--cert-path',
    dest='cert_path',
    action='store',
    type='string',
    default='./cert.pem'
  )
  parser.add_option(
    '--key-path',
    dest='key_path',
    action='store',
    type='string',
    default=None
  )
  parser.add_option(
    '--dataone-url',
    dest='dataone_url',
    action='store',
    type='string',
    default='https://cn-dev-2.dataone.org/cn/v1/'
  )
  #parser.add_option('--dataone-url', dest='dataone_url', action='store', type='string', default=d1_common.const.URL_DATAONE_ROOT)
  (options, arguments) = parser.parse_args()

  update_verbose(options.verbose)

  if len(arguments) != 1:
    logging.error('Must provide a valid node registration xml document')
    sys.exit()

  register(options, arguments)


if __name__ == '__main__':
  main()
