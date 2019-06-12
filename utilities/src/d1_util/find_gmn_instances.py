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
"""Find and examine GMN based Member Nodes in a DataONE environment.

This is an example on how to use the DataONE Client and Common libraries for
Python. It shows how to:

- Retrieve a list of Member Nodes in a DataONE environment
- Iterate over the list, connect to the MNs and examine them
- Find software version and object count for GMN based Member Nodes

Operation:

- Configure the script in the Config section below

"""
import argparse
import json
import logging
import sys

import bs4
import requests

import d1_common.env
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

import d1_client.iter.node
import d1_client.mnclient

# Config

# Failing nodes
SKIP_NODE_LIST = [
    "urn:node:DRYAD",  # fails
    "urn:node:EDACGSTORE",  # fails
    "urn:node:LTER",  # times out
]

DEFAULT_JSON_FILE_PATH = "gmn_node_list.json"


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
    parser.add_argument(
        "--json",
        default=DEFAULT_JSON_FILE_PATH,
        help="Path to write JSON result file (any existing is overwritten)",
    )
    parser.add_argument(
        "--env",
        type=str,
        default="prod",
        help="Environment, one of {}".format(", ".join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    args = parser.parse_args()

    d1_common.util.log_setup(args.debug)

    requests.packages.urllib3.disable_warnings()

    env_dict = d1_common.env.get_d1_env(args.env)
    cn_base_url = env_dict["base_url"]

    node_iterator = d1_client.iter.node.NodeListIterator(cn_base_url)

    gmn_node_list = find_gmn_instances(node_iterator)

    with open(args.json, "w") as f:
        json.dump({"env": env_dict, "gmn_nodes": gmn_node_list}, f, indent=2)

    logging.info('Wrote result to JSON file. path="{}"'.format(args.json))


def find_gmn_instances(node_iterator):
    gmn_node_list = []
    for node_pyxb in node_iterator:
        base_url = node_pyxb.baseURL
        node_id = node_pyxb.identifier.value()

        object_count_str, gmn_version_str, is_gmn = check_node(base_url, node_id)

        logging.info(
            'object_count="{}" gmn_version_str="{}", is_gmn="{}"'.format(
                object_count_str, gmn_version_str, is_gmn
            )
        )

        if is_gmn:
            gmn_node_list.append(
                {
                    "base_url": base_url,
                    "node_id": node_id,
                    "object_count_str": object_count_str,
                    "gmn_version_str": gmn_version_str,
                }
            )

    return gmn_node_list


def check_node(base_url, node_id):
    logging.info("-" * 100)
    logging.info("{} - {}".format(base_url, node_id))

    if node_id in SKIP_NODE_LIST:
        logging.info("Skipping due to being ")
        return "in SKIP_NODE_LIST", None, False

    logging.info(base_url)
    object_count_str = get_object_count(base_url)
    is_gmn, gmn_version_str = get_gmn_version(base_url)
    return object_count_str, gmn_version_str, is_gmn


def get_object_count(base_url):
    c = d1_client.mnclient.MemberNodeClient(
        base_url, verify_tls=False, suppress_verify_warnings=True
    )
    try:
        return "{}".format(c.listObjects(count=1).total)
    except Exception as e:
        if isinstance(e, d1_common.types.exceptions.NotAuthorized):
            return e.name
        return str(e)


def get_gmn_version(base_url):
    """Return the version currently running on a GMN instance.

    (is_gmn, version_or_error)

    """
    home_url = d1_common.url.joinPathElements(base_url, "home")
    try:
        response = requests.get(home_url, verify=False)
    except requests.exceptions.ConnectionError as e:
        return False, str(e)

    if not response.ok:
        return False, "invalid /home. status={}".format(response.status_code)

    soup = bs4.BeautifulSoup(response.content, "html.parser")
    version_str = soup.find(string="GMN version:").find_next("td").string
    if version_str is None:
        return False, "Parse failed"

    return True, version_str


if __name__ == "__main__":
    sys.exit(main())
