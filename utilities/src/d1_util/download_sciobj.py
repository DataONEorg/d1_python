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
"""Download Science Objects from a Member Node or Coordinating Node.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Download a Science Object from a MN or CN.
"""

import logging
import sys

import d1_common.utils.filesystem
import d1_common.utils.ulog

import d1_client.cnclient_2_0
import d1_client.command_line

log = logging.getLogger(__name__)


def main():
    parser = d1_client.command_line.D1ClientArgParser(__doc__)
    parser.add_argument("pid", help="PID of object to download")
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        help=(
            "Optional save path for downloaded object. "
            "If not specified, saved in current directory "
            "with name derived from the PID"
        ),
    )
    args = parser.parse_args()
    d1_client.command_line.log_setup(args.debug)

    client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
        parser.get_method_args(args)
    )

    path = args.path or d1_common.utils.filesystem.gen_safe_path_element(args.pid)
    try:
        with open(path, "wb") as f:
            client.get_and_save(args.pid, f)
    except Exception as e:
        log.error("Download failed: {}".format(str(e)))
        return 1

    log.info("Downloaded successfully to: {}".format(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
