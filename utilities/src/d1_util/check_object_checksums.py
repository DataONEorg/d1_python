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
- Compare the checksums to audit that replicas are valid

"""
import argparse
import json
import logging
import os
import re
import sys

import requests
import requests.packages.urllib3

import d1_common.checksum
import d1_common.const
import d1_common.env
import d1_common.types.dataoneTypes_v1_2
import d1_common.url
import d1_common.util

import d1_client.mnclient_1_2


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

    # parser.add_argument(
    #   '--fin', default=DEFAULT_OBJ_STATS_PATH,
    #   help='Path to input JSON file with object size statistics'
    # )
    # parser.add_argument(
    #   '--fout', default=DEFAULT_CHECKSUM_PATH,
    #   help='Path to output JSON file with checksum results'
    # )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    args = parser.parse_args()

    d1_common.util.log_setup(args.debug)

    if not os.path.exists(args.fin):
        raise ValueError("No such file: {}".format(args.fin))

    requests.packages.urllib3.disable_warnings()

    with open(args.fin, "r") as f:
        stats_struct = json.load(f)

    # env_dict = stats_struct['env']
    stats_list = stats_struct["stats_list"]

    make_checksum_validation_script(stats_list)
    return

    checksum_validation_list = validate_checksums_all(stats_list)

    with open(args.fout, "w") as f:
        json.dump({"checksum_validation_list": checksum_validation_list}, f, indent=2)

    logging.info('Wrote result to JSON file. path="{}"'.format(args.fout))


def make_checksum_validation_script(stats_list):
    """Make batch files required for checking checksums from another machine."""
    if not os.path.exists("./hash_check"):
        os.mkdir("./hash_check")

    with open("./hash_check/curl.sh", "w") as curl_f, open(
        "./hash_check/md5.txt", "w"
    ) as md5_f, open("./hash_check/sha1.txt", "w") as sha1_f:

        curl_f.write("#!/usr/bin/env bash\n\n")

        for stats_dict in stats_list:
            for sysmeta_xml in stats_dict["largest_sysmeta_xml"]:
                print(sysmeta_xml)
                sysmeta_pyxb = d1_common.types.dataoneTypes_v1_2.CreateFromDocument(
                    sysmeta_xml
                )

                pid = sysmeta_pyxb.identifier.value().encode("utf-8")
                file_name = re.sub("\W+", "_", pid)
                size = sysmeta_pyxb.size
                base_url = stats_dict["gmn_dict"]["base_url"]

                if size > 100 * 1024 * 1024:
                    logging.info("Ignored large object. size={} pid={}")

                curl_f.write("# {} {}\n".format(size, pid))
                curl_f.write(
                    "curl -o obj/{} {}/v1/object/{}\n".format(
                        file_name, base_url, d1_common.url.encodePathElement(pid)
                    )
                )

                if sysmeta_pyxb.checksum.algorithm == "MD5":
                    md5_f.write(
                        "{} obj/{}\n".format(sysmeta_pyxb.checksum.value(), file_name)
                    )
                else:
                    sha1_f.write(
                        "{} obj/{}\n".format(sysmeta_pyxb.checksum.value(), file_name)
                    )

    with open("./hash_check/check.sh", "w") as f:
        f.write("#!/usr/bin/env bash\n\n")
        f.write("mkdir -p obj\n")
        f.write("./curl.sh\n")
        f.write("sha1sum -c sha1.txt\n")
        f.write("md5sum -c md5.txt\n")


def validate_checksums_all(stats_list):
    validation_list = []
    for stats_dict in stats_list:
        if stats_dict["gmn_dict"]["node_id"] != "urn:node:NCEI":
            continue
        log_dict(stats_dict)
        validation_dict = validate_checksums(stats_dict)
        validation_list.append(validation_dict)
        break

    return validation_list


def validate_checksums(stats_dict):
    sysmeta_pyxb = d1_common.types.dataoneTypes_v1_2.CreateFromDocument(
        stats_dict["largest_sysmeta_xml"]
    )
    client = d1_client.mnclient_1_2.MemberNodeClient_1_2(
        base_url=stats_dict["gmn_dict"]["base_url"]
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
