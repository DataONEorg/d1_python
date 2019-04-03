#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Create an object on a Member Node based on a local file."""


import argparse
import logging
import os
import random
import string
import sys

import d1_common.checksum
import d1_common.types.dataoneTypes_v1
import d1_common.types.dataoneTypes_v2_0
import d1_common.types.exceptions

import d1_client.mnclient_1_2
import d1_client.mnclient_2_0

# App

# Defaults

# The timeout timer runs while the POST is occurring, so must be set to a value
# that covers the entire transfer time of the largest object plus safety margin.
# The timer resets whenever data arrives, which works well for a GET, but not
# for a POST, where all data is outgoing. None disables the timeout.
TIMEOUT_SEC = 30 * 60


def main():
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='Create object from file')

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
        # type='float',
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help='Amount of time to wait for calls to complete (seconds)',
    )
    parser.add_argument(
        '--disable-tls-validate',
        action='store_true',
        help='Disable validation of server side certificate',
    )
    parser.add_argument(
        '--use-v1', action='store_true', help='Use the v1 API (v2 is default)'
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    parser.add_argument(
        'mn_base_url',
        metavar='mn-base-url',
        action='store',
        help='The base URL for the Member Node',
    )
    parser.add_argument(
        'file_path',
        metavar='file-path',
        action='store',
        help='Path to the file to use for the create',
    )
    parser.add_argument('pid', action='store', help='PID')

    args = parser.parse_args()

    logging.getLogger('').setLevel(logging.DEBUG if args.debug else logging.INFO)

    if args.use_v1:
        mn_client = d1_client.mnclient.MemberNodeClient(
            args.mn_base_url,
            cert_pem_path=args.cert_pem_path,
            cert_key_path=args.cert_key_path,
        )
    else:
        mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
            args.mn_base_url,
            cert_pem_path=args.cert_pem_path,
            cert_key_path=args.cert_key_path,
        )

    try:
        _create(mn_client, args)
    except d1_common.types.exceptions.DataONEException as e:
        logging.exception('MNStorage.create() failed with exception:')
        if e.traceInformation and len(e.traceInformation) >= 100:
            trace_path = 'traceInformation.out'
            with open(trace_path, 'wb') as f:
                f.write(e.traceInformation)
                logging.error('Dumped traceInformation to file: {}'.format(trace_path))
                sys.exit()
    except Exception:
        logging.exception('MNStorage.create() failed with exception:')


def _create(mn_client, args):
    """Args:

    mn_client: args:

    """
    with open(args.file_path, 'rb') as f:
        sysmeta_pyxb = gen_sysmeta(
            pid=args.pid,
            f=f,
            size=os.path.getsize(args.file_path),
            format_id='application/octet-stream',
            include_revision_bool=False,
            use_v1_bool=args.use_v1,
        )

    with open(args.file_path, 'rb') as f:
        mn_client.createStream(
            args.pid,
            f,
            sysmeta_pyxb,
            cert_pem_path=args.cert_pem_path,
            cert_key_path=args.cert_key_path,
            timeout_sec=TIMEOUT_SEC,
        )


def gen_sysmeta(pid, f, size, format_id, include_revision_bool, use_v1_bool):
    """Args:

    pid: f: size: format_id: include_revision_bool: use_v1_bool:

    """
    now = d1_common.date_time.utc_now()
    if use_v1_bool:
        client = d1_common.types.dataoneTypes_v1
    else:
        client = d1_common.types.dataoneTypes_v2_0

    sysmeta_pyxb = client.pyxb_binding.systemMetadata()
    sysmeta_pyxb.accessPolicy = _generate_public_access_policy(client)
    sysmeta_pyxb.checksum = d1_common.checksum.create_checksum_object_from_stream(f)
    sysmeta_pyxb.dateSysMetadataModified = now
    sysmeta_pyxb.dateUploaded = now
    sysmeta_pyxb.formatId = format_id
    sysmeta_pyxb.identifier = pid
    sysmeta_pyxb.rightsHolder = _generate_random_ascii('rights_holder')
    sysmeta_pyxb.size = size
    sysmeta_pyxb.submitter = _generate_random_ascii('submitter')

    if include_revision_bool:
        sysmeta_pyxb.obsoletedBy = _generate_random_ascii('obsoleted_by_pid')
        sysmeta_pyxb.obsoletes = _generate_random_ascii('obsoletes_pid')

    sysmeta_pyxb.originMemberNode = _generate_random_ascii('origin_mn')
    sysmeta_pyxb.authoritativeMemberNode = _generate_random_ascii('auth_mn')

    return sysmeta_pyxb


def _generate_public_access_policy(client):
    """Args:

    client:

    """
    access_policy_pyxb = client.pyxb_binding.accessPolicy()
    access_rule_pyxb = client.pyxb_binding.AccessRule()
    access_rule_pyxb.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission_pyxb = client.pyxb_binding.Permission('read')
    access_rule_pyxb.permission.append(permission_pyxb)
    access_policy_pyxb.append(access_rule_pyxb)
    return access_policy_pyxb


def _generate_random_ascii(prefix, num_chars=10):
    """Args:

    prefix: num_chars:

    """
    return '{}_{}'.format(
        prefix,
        ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(num_chars)
        ),
    )


if __name__ == '__main__':
    sys.exit(main())
