#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2018 DataONE
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
"""Submit a PEM (Base64) encoded X.509 v3 certificate to a CN for validation.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Submit a PEM (Base64) encoded X.509 v3 certificate, optionally containing a DataONE
  SubjectInfo extension, to a CN to check if it passes validation and to determine
  which DataONE subjects are authenticated by it.

Notes:

- This requires the private key of the certificate, and the CN validates the
  certificate.

- See `check_x509_certificate_local.py` for how to process the lists of equivalent
  identities and group memberships in a DataONE SubjectInfo extension into a list of
  authenticated DataONE subjects.

"""
import argparse
import os
import sys

import requests
import requests.packages.urllib3

import d1_common.env
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0

DEFAULT_BASE_URL = 'https://cn.dataone.org/cn/'


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    parser.add_argument(
        '--env',
        type=str,
        default='prod',
        help='Environment, one of {}'.format(', '.join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        '--cert-pub',
        dest='cert_pem_path',
        action='store',
        help='Path to PEM formatted public key of certificate',
    )
    parser.add_argument(
        '--cert-key',
        dest='cert_key_path',
        action='store',
        help='Path to PEM formatted private key of certificate',
    )
    parser.add_argument(
        '--timeout',
        action='store',
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help='Amount of time to wait for calls to complete (seconds)',
    )

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    parser.add_argument(
        '-b',
        '--base-url',
        default=DEFAULT_BASE_URL,
        help='The base URL for CN that will validate the certificate',
    )
    parser.add_argument(
        'cert_pem_path', help='Path to the .PEM certificate file to check'
    )
    parser.add_argument(
        'cert_key_path',
        help='Path to the .PEM private key file for the certificate to check',
    )

    args = parser.parse_args()

    d1_common.util.log_setup(args.debug)

    if not os.path.exists(args.cert_pem_path):
        raise ValueError('No such file: {}'.format(args.cert_pem_path))

    if not os.path.exists(args.cert_key_path):
        raise ValueError('No such file: {}'.format(args.cert_key_path))

    requests.packages.urllib3.disable_warnings()

    c = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        base_url=args.base_url,
        cert_pem_path=args.cert_pem_path,
        cert_key_path=args.cert_key_path,
    )
    subject_info_pyxb = c.echoCredentials()
    subject_info_pretty_xml = d1_common.xml.serialize_to_xml_str(subject_info_pyxb)

    print('CN extracted SubjectInfo:')

    print(subject_info_pretty_xml)


if __name__ == "__main__":
    sys.exit(main())
