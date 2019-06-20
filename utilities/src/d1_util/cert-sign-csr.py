#!/usr/bin/env python

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
"""Sign a Certificate Signing Request (CSR).

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Use the d1_common.cert.x509 module to sign a Certificate Signing Request (CSR) using a
local CA.

"""
import argparse
import logging
import os




import d1_common.cert.x509


def main():
    logging.basicConfig(level=logging.WARN)
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "csr_path", action="store", help="Load path for PEM formatted CSR"
    )
    parser.add_argument("ca_path", action="store", help="Load path for CA certificate")
    parser.add_argument(
        "ca_key_path", action="store", help="Load path for CA certificate private key"
    )
    args = parser.parse_args()
    try:
        sign_csr(args)
    except CSRSignError as e:
        print("Error: {}".format((str(e))))
    except KeyboardInterrupt:
        print("Interrupted")


def sign_csr(args):
    assert_valid_path(args.csr_path)
    assert_valid_path(args.ca_path)
    assert_valid_path(args.ca_key_path)

    csr_cert = d1_common.cert.x509.load_csr(args.csr_path)

    ca_pw_bytes = d1_common.cert.x509.input_key_passphrase("CA private key")
    ca_private_key = d1_common.cert.x509.load_private_key(args.ca_key_path, ca_pw_bytes)

    ca_cert = d1_common.cert.x509.deserialize_pem_file(args.ca_path)

    signed_cert = d1_common.cert.x509.generate_cert(
        ca_issuer=ca_cert.issuer,
        ca_key=ca_private_key,
        csr_subject=csr_cert.subject,
        csr_pub_key=csr_cert.public_key(),
    )

    csr_base_path = os.path.splitext(args.csr_path)[0]
    cert_path = csr_base_path + ".signed.cert.pem"
    d1_common.cert.x509.save_pem(
        cert_path, d1_common.cert.x509.serialize_cert_to_pem(signed_cert)
    )
    print("Wrote signed certificate to: {}".format(cert_path))


def assert_valid_path(p):
    if not os.path.isfile(p):
        raise CSRSignError("Path does not exist or is not a file: {}".format(p))


class CSRSignError(Exception):
    pass


if __name__ == "__main__":
    main()
