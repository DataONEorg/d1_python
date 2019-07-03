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
"""Resolve an OAI-ORE Resource Map (data package) identifier to download URL for a BagIt
ZIP archive of the package.

This is an example on how to use the DataONE Client and Common libraries for Python.

"""
import d1_common.url
import d1_common.env
import d1_common.util
import d1_common.const
import d1_client.cnclient_2_0
import argparse
import logging
import sys

import d1_common.resource_map

# Config

# The identifier (PID) of the DataONE Data Package (Resource Map) to download
# and display. Data packages have Format ID
# http://www.openarchives.org/ore/terms.
SCIENCE_OBJECT_PID = "dakoop_test-PKG"

# BaseURL for the Member Node on which the science object resides. If the script
# is run on the same server as the Member Node, this can be localhost.
MN_BASE_URL = "https://mn-demo-6.test.dataone.org/knb/d1/mn"
# MN_BASE_URL = 'https://localhost/mn'

# Paths to the certificate and key to use when retrieving the object. This is
# required if the object is not publicly accessible. If the certificate has the
# key embedded, the _KEY setting should be set to None. If the objects have
# public access, these can both be set to None.
CERTIFICATE_FOR_CREATE = None
CERTIFICATE_FOR_CREATE_KEY = None

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--env",
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

    args = parser.parse_args()
    d1_common.util.log_setup(is_debug=args.debug)

    # TODO: Refactor to use module scope logger set to __name__.
    # logging.getLogger("").setLevel(logging.DEBUG)

    # Create a Coordinating Node (CN) client that can be used for running commands
    # against the CN in a specific DataONE environment.
    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        d1_common.env.get_d1_env(args.env)["base_url"],
        cert_pem_path=CERTIFICATE_FOR_CREATE,
        cert_key_path=CERTIFICATE_FOR_CREATE_KEY,
    )

    did = "10.24431_rw1k321_201955192852"
    object_location_list_pyxb = client.resolve(did)

    print("\nOAI-ORE Resource Map (data package) RDF locations:")
    for object_location in object_location_list_pyxb.objectLocation:
        # objectLocation.url = "https://{}.some.base.url/mn/v2/object/{}".format(
        print("  {}".format(object_location.url))

    # The first ObjectLocation in the ObjectLocationList references the object at the MN
    # that is registered as authoritative for the object. The other locations are
    # replicas.
    object_location = object_location_list_pyxb.objectLocation[0]

    # Check that the MN provides the
    latest_api_version = sorted(object_location.version)[-1]
    if latest_api_version != "v2":
        print("\nBagIt ZIP download is not supported by the authoritative Member Node")
        return 1

    print("\nBagIt ZIP location:")

    print(
        "  {}/v2/packages/{}".format(
            object_location.baseURL,
            latest_api_version,
            d1_common.url.encodePathElement(did),
        )
    )
    # objectLocation.nodeIdentifier = "urn:node:testResolve{}".format(i)
    # objectLocation.baseURL = "https://{}.some.base.url/mn".format(i)
    # objectLocation.version = "v2"
    #     i, pid_str
    # )
    # objectLocation.preference = i
    #
    # objectLocationList.objectLocation.append(objectLocation)

    exit()

    # Use the client to get a data package as a string (Format ID
    # http://www.openarchives.org/ore/terms).
    resource_map_xml = client.get(SCIENCE_OBJECT_PID).read()

    # Create a resource map parser.
    resource_map_parser = d1_common.resource_map.ResourceMapParser(resource_map_xml)

    # Use the resource map parser to parse the resource map. Then display it.

    print("\nResource Map PID:")
    print(resource_map_parser.get_resource_map_pid())

    print("\nTriples:")

    for s, p, o in resource_map_parser.get_all_triples():
        print("subject:   " + s)
        print("predicate: " + p)
        print("object:    " + o)
        print()

    print("\nAll PIDs in aggregation: ")

    for pid in resource_map_parser.get_aggregated_pids():
        print("PID: " + pid)

    print("\nScience Metadata PIDs in aggregation: ")

    for pid in resource_map_parser.get_aggregated_science_metadata_pids():
        print("PID: " + pid)

    print("\nScience Data PIDs in aggregation: ")

    for pid in resource_map_parser.get_aggregated_science_data_pids():
        print("PID: " + pid)


if __name__ == "__main__":
    sys.exit(main())
