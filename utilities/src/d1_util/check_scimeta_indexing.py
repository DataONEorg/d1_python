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
"""Check if a science metadata object can be successfully indexed by the CN.

This will submit a science metadata object, such as an EML or ISO XML document to the CN
and retrieve the indexing result for that object.

As values from the associated System Metadata document are also indexed, this example
generates a randomized System Metadata document that is included with the Science
Metdata object.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Submit a science object to CNDiagnostic.echoIndexedObject() and print the result.

API:

CNDiagnostic.echoIndexedObject(session, queryEngine, sysmeta, object) → OctetStream
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html
  #CNDiagnostic.echoIndexedObject

"""

import sys

import d1_common.const
import d1_common.env
import d1_common.util
import d1_common.xml

import d1_test.instance_generator.system_metadata

import d1_client.cnclient_2_0

DEFAULT_FORMAT_ID = "http://www.isotc211.org/2005/gmd"

import d1_client.command_line


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
    parser.add_argument("path", help="Path to science metadata file")
    parser.add_argument("--debug", action="store_true", help="Debug level logging")

    args = parser.parse_args()
    d1_client.command_line.log_setup(args)

    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        **d1_client.command_line.args_adapter(args)
    )

    sysmeta_pyxb = d1_test.instance_generator.system_metadata.generate_from_file_path(
        client,
        args.path,
        {
            "identifier": "test_pid",
            "formatId": args.format,
            "accessPolicy": None,
            "replicationPolicy": None,
            "obsoletes": None,
            "obsoletedBy": None,
            "archived": None,
            "replica": None,
            "mediaType": None,
        },
    )

    with open(args.path, "rb") as f:
        sciobj_bytes = f.read()

    response = cn_client.echoIndexedObject(
        "solr", sysmeta_pyxb, io.BytesIO(sciobj_bytes)
    )

    print(d1_common.xml.reformat_to_pretty_xml(response.text))


if __name__ == "__main__":
    sys.exit(main())
