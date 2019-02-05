#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""Perform various operations on Java Web Tokens (JWTs)

This is an example on how to use the DataONE Client and Common libraries
for Python.
"""
import argparse
import logging
import os
import re
import shutil
import subprocess
import sys

import cryptography.exceptions
import cryptography.hazmat
import cryptography.hazmat.primitives
import cryptography.hazmat.primitives.asymmetric
import cryptography.hazmat.primitives.asymmetric.padding
import cryptography.hazmat.primitives.hashes

import d1_common.cert.jwt
import d1_common.cert.x509
import d1_common.env
import d1_common.util


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

    d1_common.util.log_setup(True)
    # jwt_cleanup()
    # cert_cleanup()
    download_cn_certs()


def validate_and_decode(jwt_bu64, cert_obj):
    """Example for validating the signature of a JWT using only the
    cryptography library.

    Note that this does NOT validate the claims in the claim set.
    """
    public_key = cert_obj.public_key()
    message = '.'.join(d1_common.cert.jwt.get_bu64_tup(jwt_bu64)[:2])
    signature = d1_common.cert.jwt.get_jwt_tup(jwt_bu64)[2]
    try:
        public_key.verify(
            signature,
            message,
            cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15(),
            cryptography.hazmat.primitives.hashes.SHA256(),
        )
    except cryptography.exceptions.InvalidSignature as e:
        raise Exception('Signature is invalid. error="{}"'.format(str(e)))
    return d1_common.cert.jwt.get_jwt_dict(jwt_bu64)


def find_valid_combinations(cert_file_name_list, jwt_file_name_list):
    """Given a list of cert and JWT file names, print a list showing each
    combination along with indicators for combinations where the JWT signature
    was successfully validated with the cert."""
    for cert_file_name in cert_file_name_list:
        cert_pem = ''  # self.test_files.load_utf8_to_str(cert_file_name)
        cert_obj = d1_common.cert.x509.deserialize_pem(cert_pem)
        # d1_common.cert.x509.log_cert_info(logging.info, 'CERT', cert_obj)
        for jwt_file_name in jwt_file_name_list:
            jwt_bu64 = ''  # self.test_files.load_utf8_to_str(jwt_file_name)
            # d1_common.cert.jwt.log_jwt_bu64_info(logging.info, 'JWT', jwt_bu64)
            is_ok = False
            try:
                d1_common.cert.jwt.validate_and_decode(jwt_bu64, cert_obj)
            except d1_common.cert.jwt.JwtException as e:
                logging.info('Invalid. msg="{}"'.format(str(e)))
            else:
                is_ok = True
            logging.info(
                '{} {} {}'.format(
                    '***' if is_ok else '   ', cert_file_name, jwt_file_name
                )
            )


def download_cn_certs():
    def d(base_url):
        cert_obj = d1_common.cert.x509.download_as_obj(base_url)
        cert_file_name = filename_from_cert_obj(cert_obj)
        cert_pem = d1_common.cert.x509.serialize_cert_to_pem(cert_obj)
        cert_file_path = os.path.join('out', cert_file_name)
        with open(cert_file_path, 'wb') as f:
            f.write(cert_pem)

    d(d1_common.env.get_d1_env('prod')['base_url'])
    d(d1_common.env.get_d1_env('stage')['base_url'])


def jwt_cleanup():
    already_have_set = set()
    cmd_list = ['locate', '--regex', '.*(token|base64).*']
    jwt_path_list = subprocess.check_output(cmd_list).splitlines()
    for jwt_path in jwt_path_list:
        try:
            with open(jwt_path, 'rb') as f:
                jwt_bu64 = f.read().strip()
        except EnvironmentError:
            continue

        try:
            jwt_dict = d1_common.cert.jwt.get_jwt_dict(jwt_bu64)
        except (TypeError, ValueError) as e:
            logging.info(str(e))
            continue

        d1_common.cert.jwt.log_jwt_dict_info(logging.info, 'Found JWT', jwt_dict)

        if jwt_dict['_sig_sha1'] in already_have_set:
            os.unlink(jwt_path)
            logging.info('Deleted: {}'.format(jwt_path))
        else:
            already_have_set.add(jwt_dict['_sig_sha1'])
            d1_common.cert.jwt.ts_to_str(jwt_dict)
            new_path = 'jwt_token_{}.base64'.format(
                re.sub(r'[:-]', '', jwt_dict['iat']).replace(' ', '_')
            )
            shutil.move(jwt_path, new_path)
            logging.info('Moved {} -> {}'.format(jwt_path, new_path))


def cert_cleanup():
    already_have_set = set()
    cmd_list = ['locate', '--regex', '^/home/dahl/.*(pem|key|cert|crt|).*']
    cert_path_list = subprocess.check_output(cmd_list).splitlines()
    for cert_path in cert_path_list:
        if not os.path.isfile(cert_path) or os.path.getsize(cert_path) > 10 * 1024 ** 2:
            continue

        try:
            with open(cert_path, 'rb') as f:
                cert_pem = f.read().strip()
        except EnvironmentError:
            continue

        try:
            cert_obj = d1_common.cert.x509.deserialize_pem(cert_pem)
        except (TypeError, ValueError):
            continue

        d1_common.cert.x509.log_cert_info(logging.info, 'Found cert', cert_obj)

        new_name = filename_from_cert_obj(cert_obj)

        if new_name in already_have_set:
            logging.info('Already have: {}'.format(new_name))
            continue

        already_have_set.add(new_name)
        new_path = os.path.join('pem', new_name)
        shutil.copy(cert_path, new_path)
        logging.info('{} -> {}'.format(cert_path, new_path))


def filename_from_cert_obj(cert_obj):
    subject_str = d1_common.cert.x509.get_val_str(cert_obj, ['subject', 'value'])
    subject_str = re.sub(r'\W+', '_', subject_str.lower())
    not_valid_before_str = re.sub(
        r'[:-]', '', cert_obj.not_valid_before.isoformat().replace('T', '_')
    )
    # not_valid_after_str = re.sub(r'[:-]', '',
    # cert_obj.not_valid_after.isoformat().replace('T', '_'))
    new_name = 'cert_{}_{}.pem'.format(subject_str, not_valid_before_str)
    return new_name


if __name__ == '__main__':
    sys.exit(main())
