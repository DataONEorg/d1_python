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
Metadata object.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Submit a science object to CNDiagnostic.echoIndexedObject() and print the result.

API:

CNDiagnostic.echoIndexedObject(session, queryEngine, sysmeta, object) → OctetStream
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html
#CNDiagnostic.echoIndexedObject

"""

import sys

import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.command_line

import d1_test.instance_generator.system_metadata

DEFAULT_FORMAT_ID = "http://www.isotc211.org/2005/gmd"



def main():
    parser = d1_client.command_line.D1ClientArgParser(__doc__)
    parser.add_argument("path", help="Path to science metadata file")
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT_ID,
        help="Set the formatId of the submitted Science Metadata",
    )
    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)

    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        **parser.get_method_args(args)
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

    with open(args.path, "rb") as scimeta_file:
        response = client.echoIndexedObject("solr", sysmeta_pyxb, scimeta_file)

    print(d1_common.xml.reformat_to_pretty_xml(response.text))


if __name__ == "__main__":
    sys.exit(main())
