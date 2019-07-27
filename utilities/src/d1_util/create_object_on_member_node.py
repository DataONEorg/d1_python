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

"""Create Science Object on Member Node.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Upload a local file to a Member Node as a Science Object

Operation:

- The first time the script is run, a message indicating that the object was
  successfully created should be displayed, and the object should become available on
  the Member Node.

- If the script is then launched again without changing the identifier (PID), an
  IdentifierNotUnique exception should be returned. This indicates that the identifier
  is now in use by the previously created object.

- Any other errors will also be returned as DataONE exceptions.

"""

import logging
import pathlib
import sys

import d1_scimeta.util

import d1_common.const
import d1_common.types.exceptions

import d1_client.command_line
import d1_client.d1client

log = logging.getLogger(__name__)


def main():
    parser = d1_client.command_line.D1ClientArgParser(__doc__, add_base_url=True)
    parser.add_argument("--formats", action="store_true", help="List valid formatIds")
    # parser.add_argument(
    #     "node_id", help="URN of target node (e.g.: urn:node:ABC)"
    # )
    parser.add_argument("pid", help="Persistent Identifiers for Science Object")
    parser.add_argument("format_id", help="formatId for Science Object")
    parser.add_argument("path", help="Path to Science Object file")
    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)

    if args.formats:
        d1_scimeta.util.get_supported_format_id_list()
        return 0

    client = d1_client.d1client.DataONEClient(parser.get_method_args(args))

    if client.auth_subj_tup[0] == d1_common.const.SUBJECT_PUBLIC:
        log.error(
            "Must provide a certificate in order to gain access to create objects on MN"
        )
        return 1

    try:
        client.create_sciobj(args.pid, args.format_id, pathlib.Path(args.path))
    except d1_common.types.exceptions.DataONEException as e:
        log.error("Create failed. Error: {}".format(str(e)))
        return 1

    log.error("Create successful")
    return 0


if __name__ == "__main__":
    sys.exit(main())
