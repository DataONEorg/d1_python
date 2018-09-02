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
"""Create DataONE compliant certificate

The certificate can optionally include a SubjectInfo XML document in which
equivalent identities and group memberships are described. The certificate will
normally be signed with a test CA that is trusted by a test instance of a Member
Node. Test instances set up by DataONE will normally trust the DataONE Test CA.
"""

# Example: ./create_dataone_test_certificate.py --ca-path sample_files/ca_test.crt
# --ca-key-path sample_files/ca_test.key --ca-key-pw ca_test --public-key-path
# sample_files/new_cert_public_key.pem --subject-info-path
# sample_files/subject_info.xml 'CN=my name,O=mydomain,DC=com'

import logging
import optparse
import re
import sys

import d1_x509v3_certificate_generator


def split_dn(dn):
  dn_list = []
  for rdn in dn.split(','):
    k, v = rdn.split('=')
    dn_list.append((k, v))
  dn_list.reverse()
  return tuple(dn_list)


def make_base_name_from_dn(dn):
  for rdn in dn:
    if rdn[0] == 'CN':
      return re.sub('\W', '_', rdn[1])


def read_subject_info(subject_info_path):
  if subject_info_path is None:
    return ''
  try:
    with open(subject_info_path) as f:
      return f.read()
  except EnvironmentError as e:
    print('Error reading subject info from file: {}'.format(str(e)))
    exit()


def create_cert(options, args):
  subject_info = read_subject_info(options.subject_info_path)
  dn = split_dn(args[0])
  basename = make_base_name_from_dn(dn)
  crt_name = basename + '.crt'
  d1_x509v3_certificate_generator.generate(
    crt_name, options.ca_path, options.ca_cert_key_path, options.ca_key_pw,
    options.public_cert_key_path, subject_info, options.subject_alt_name, dn, 1
    if options.long_term else 0
  )


def main():
  parser = optparse.OptionParser()
  parser.add_option(
    '--subject-info-path',
    action='store',
    type='string',
  )
  parser.add_option(
    '--subject-alt-name', action='store', type='string',
    default='DNS:dataone.org'
  )
  parser.add_option(
    '--long-term', action='store_true',
    help='Create a certificate that is valid for 10 years'
  )

  parser.add_option(
    '--ca-path', action='store', type='string', default='ca.crt'
  )
  parser.add_option(
    '--ca-key-path', dest='ca_cert_key_path', action='store', type='string',
    default='ca.key'
  )
  parser.add_option(
    '--ca-key-pw', action='store', type='string', default='my_ca_pw'
  )

  parser.add_option(
    '--public-key-path', dest='public_cert_key_path', action='store',
    type='string', default='pubkey.pem'
  )

  parser.add_option('--verbose', action='store_true')

  (options, args) = parser.parse_args()

  if len(args) != 1:
    print('Need a single argument which must be the Subject DN. ')
    'Example: CN=My Name,O=Google,C=US,DC=cilogon,DC=org'
    parser.print_help()
    exit()

  if options.verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  create_cert(options, args)


if __name__ == '__main__':
  sys.exit(main())
