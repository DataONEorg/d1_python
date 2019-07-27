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
"""Download and display Data Package (Resource Map) from Member Node.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Download a Data Package (Resource Map)
- Parse and display the Resource Map.

Operation:

- Configure the script in the Config section below

"""

import logging
import sys

import d1_common.resource_map


# Config
def main():

    logging.basicConfig()
    logging.getLogger("").setLevel(logging.DEBUG)

    # Create a Member Node client that can be used for running commands against
    # a specific Member Node.
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
        MN_BASE_URL,
        cert_pem_path=CERTIFICATE_FOR_CREATE,
        cert_key_path=CERTIFICATE_FOR_CREATE_KEY,
    )

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
