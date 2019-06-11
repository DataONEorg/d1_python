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
"""Download the issuer CA X.509 certificates for all DataONE nodes.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Downloads server side certificate from a DataONE nodes
- Parse certificates to find the issuer CA certificate URLs
- Downloads the CA certs

Operation:

This process downloads the server side certificates from the DataONE nodes and parses
them to find the issuer CA certificate URLs. It then downloads the CA certs.

The CA certs can then be installed as trusted CAs in the local environment in order to
ensure that the DataONE client library trusts all server side certs currently in use in
DataONE.

To install the CA bundles on Ubuntu and derived distributions, move the files to:

/usr/local/share/ca-certificates

Then run:

update-ca-certificates

update-ca-certificates only processes ".crt" files, so this script saves the
certificates with that extension.

"""
import argparse
import logging
import os
import re
import ssl
import sys

import requests

import d1_common.cert.x509
import d1_common.env
import d1_common.util
import d1_common.xml

import d1_client.iter.node


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--env",
        type=str,
        default="prod",
        help="Environment, one of {}".format(", ".join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        "--cert-pub",
        dest="cert_pem_path",
        action="store",
        help="Path to PEM formatted public key of certificate",
    )
    parser.add_argument(
        "--cert-key",
        dest="cert_key_path",
        action="store",
        help="Path to PEM formatted private key of certificate",
    )
    parser.add_argument(
        "--timeout",
        action="store",
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help="Amount of time to wait for calls to complete (seconds)",
    )

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("dir", help="Path to download directory")
    parser.add_argument(
        "--env",
        type=str,
        default="prod",
        help="Environment, one of {}".format(", ".join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    args = parser.parse_args()

    d1_common.util.log_setup(args.debug)

    if not os.path.isdir(args.dir):
        raise ValueError("Directory does not exist: {}".format(args.dir))

    if args.env not in d1_common.env.D1_ENV_DICT:
        raise ValueError(
            "Environment must be one of {}".format(", ".join(d1_common.env.D1_ENV_DICT))
        )

    env_dict = d1_common.env.get_d1_env(args.env)
    cn_base_url = env_dict["base_url"]

    node_iterator = d1_client.iter.node.NodeListIterator(cn_base_url)

    for node_pyxb in node_iterator:
        logging.debug(d1_common.xml.serialize_to_xml_str(node_pyxb))
        try:
            download_server_cert(
                node_pyxb.baseURL, node_pyxb.identifier.value(), args.dir
            )
        except Exception as e:
            logging.info("{}".format(str(e)))


def download_server_cert(base_url, node_id, download_dir_path):
    logging.info("-" * 100)
    logging.info("{} - {}".format(base_url, node_id))

    logging.info("Downloading server side cert: {}".format(base_url))
    server_der = d1_common.cert.x509.download_as_der(base_url)
    server_cert = d1_common.cert.x509.decode_der(server_der)
    issuer_cert_url = d1_common.cert.x509.extract_issuer_ca_cert_url(server_cert)

    logging.info("Downloading CA issuer cert: {}".format(issuer_cert_url))
    issuer_der = requests.get(issuer_cert_url).content
    issuer_pem = ssl.DER_cert_to_PEM_cert(issuer_der)
    issuer_cert = d1_common.cert.x509.decode_der(issuer_der)

    for n in issuer_cert.issuer:
        if n.oid.dotted_string == "2.5.4.3":
            issuer_name = n.value
            break
    else:
        issuer_name = issuer_cert_url

    logging.info("Issuer: {}".format(issuer_name))

    pem_file_name = "{}.crt".format(re.sub(r"\W+", "_", issuer_name).lower())
    pem_file_path = os.path.join(download_dir_path, pem_file_name)
    with open(pem_file_path, "wb") as f:
        f.write(issuer_pem)


if __name__ == "__main__":
    sys.exit(main())
