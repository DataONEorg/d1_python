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
"""Generate a Certificate Signing Request (CSR) for a Member Node Client Side
Certificate, suitable for submitting to DataONE.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Use the d1_common.cert.x509 module to create a local Certificate Signing Request
  (CSR).

"""
import argparse
import os

import d1_common.cert.x509
import d1_common.util
import d1_common.utils.ulog


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "node_urn", action="store", help="Node URN. E.g., 'urn:node:XYZ'"
    )
    parser.add_argument(
        "csr_path", action="store", help="Save path for PEM formatted CSR"
    )
    args = parser.parse_args()
    d1_common.utils.ulog.setup(is_debug=args.debug)
    try:
        create_csr(args)
    except CSRCreateError as e:
        print("Error: {}".format((str(e))))
    except KeyboardInterrupt:
        print("Interrupted")


def create_csr(args):
    csr_private_key_bytes = d1_common.cert.x509.generate_private_key()
    csr_cert = d1_common.cert.x509.generate_csr(
        csr_private_key_bytes, d1_common.cert.x509.create_mn_dn(args.node_urn)
    )

    pem_path = (
        args.csr_path
        if args.csr_path.lower().endswith(".pem")
        else args.csr_path + ".pem"
    )
    d1_common.cert.x509.save_pem(
        pem_path, d1_common.cert.x509.serialize_cert_to_pem(csr_cert)
    )
    print("Wrote CSR with public key to: {}".format(pem_path))

    key_path = os.path.splitext(pem_path)[0] + ".key.pem"
    ca_pw_bytes = d1_common.cert.x509.input_key_passphrase("CSR private key")
    d1_common.cert.x509.save_pem(
        key_path,
        d1_common.cert.x509.serialize_private_key_to_pem(
            csr_private_key_bytes, ca_pw_bytes
        ),
    )
    print("Wrote CSR private key to: {}".format(key_path))


class CSRCreateError(Exception):
    pass


if __name__ == "__main__":
    main()
