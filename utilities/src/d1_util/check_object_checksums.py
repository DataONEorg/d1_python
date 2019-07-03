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
"""Compare Science Object checksums for replicas on CNs and MNs.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Download Science Object checksums from CNs and MNs
"""
import logging
import sys

import d1_common.checksum


import d1_client.mnclient_1_2

import d1_client.command_line


def main():
    parser = d1_client.command_line.get_standard_arg_parser(__doc__, add_base_url=True)
    args = parser.parse_args()
    d1_client.command_line.log_setup(args)

    client = d1_client.mnclient_1_2.MemberNodeClient_1_2(
        **d1_client.command_line.args_adapter(args)
    )

    response = client.get(sysmeta_pyxb.identifier.value())
    checksum_pyxb = d1_common.checksum.create_checksum_object_from_iterator(
        response.iter_content(), sysmeta_pyxb.checksum.algorithm
    )
    is_valid = d1_common.checksum.are_checksums_equal(
        sysmeta_pyxb.checksum, checksum_pyxb
    )
    return {"is_valid": is_valid}


def log_dict(d):
    logging.info(
        ", ".join(
            ['{}="{}"'.format(k, d[k]) for k in sorted(d) if k is not "sysmeta_xml"]
        )
    )


if __name__ == "__main__":
    sys.exit(main())
