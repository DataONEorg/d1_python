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
"""Generate a self signed root Certificate Authority (CA) certificate.

The certificate can be used for issuing certificates and sign CSRs that are locally
trusted.
"""
import argparse
import logging
import os

import d1_common.cert.x509
import d1_common.env


def main():
    logging.basicConfig(level=logging.WARN)
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "ca_path", action="store", help="Save path for PEM formatted CA certificate"
    )
    args = parser.parse_args()
    try:
        create_ca(args)
    except CACreateError as e:
        print("Error: {}".format((str(e))))
    except KeyboardInterrupt:
        print("Exit")


def create_ca(args):
    ca_private_key = d1_common.cert.x509.generate_private_key()
    ca_cert = d1_common.cert.x509.generate_ca_cert("dataone.org", ca_private_key)

    ca_pw_bytes = d1_common.cert.x509.input_key_passphrase("CA private key")

    pem_path = (
        args.ca_path if args.ca_path.lower().endswith(".pem") else args.ca_path + ".pem"
    )
    d1_common.cert.x509.save_pem(
        pem_path, d1_common.cert.x509.serialize_cert_to_pem(ca_cert)
    )
    print("Wrote CA certificate to: {}".format(pem_path))

    key_path = os.path.splitext(pem_path)[0] + ".key.pem"
    d1_common.cert.x509.save_pem(
        key_path,
        d1_common.cert.x509.serialize_private_key_to_pem(ca_private_key, ca_pw_bytes),
    )
    print("Wrote CA private key to: {}".format(key_path))


class CACreateError(Exception):
    pass


if __name__ == "__main__":
    main()
