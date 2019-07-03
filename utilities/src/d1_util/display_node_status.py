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
"""Display node status.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Retrieve a list of all DataONE Nodes
- Get and display key metrics for each of the Nodes.

Notes:

- See the description for the CERTIFICATE setting below for limitations in the
  information displayed by this script.

Operation:

- Configure the script in the Config section below

"""
import argparse
import logging
import sys

import d1_common.const
import d1_common.env
import d1_common.types.exceptions

import d1_client.cnclient
import d1_client.mnclient_2_0

# Config

# In addition to the default production environment, DataONE maintains several
# separate environments for use when developing and testing DataONE components.
# There are no connections between the environments. For instance, certificates,
# DataONE identities and science objects are exclusive to the environment in
# which they were created. This setting controls to which environment the CN
# client connects.

# Round-robin CN endpoints
DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT  # (recommended, production)
# DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-sandbox.dataone.org/cn'
# DATAONE_ROOT = 'https://cn-stage.dataone.org/cn/'
# DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'

# Paths to the certificate and key to use when querying the node. If the
# certificate has the key embedded, the _KEY setting should be set to None. MNs
# and CNs may restrict the information returned by some or all of the APIs
# called by this script to contain only information for which the caller has
# access. If the certificate is set to None, methods may either entirely deny
# access or return information only related to publicly accessible objects.
CERTIFICATE = None
CERTIFICATE_KEY = None


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

    logging.basicConfig()
    # Setting the default logger to level "DEBUG" causes the script to become
    # very verbose.
    logging.getLogger("").setLevel(logging.DEBUG)

    node_list = get_node_list_from_coordinating_node()
    for node in node_list.node:
        if is_member_node(node):
            get_mn_metrics(node)
        elif is_coordinating_node(node):
            get_cn_metrics(node)
        else:
            logging.error("Unknown node type")
            return
        print()


def get_node_list_from_coordinating_node():
    cn_client = d1_client.cnclient.CoordinatingNodeClient(base_url=DATAONE_ROOT)
    try:
        return cn_client.listNodes()
    except d1_common.types.exceptions.DataONEException:
        logging.exception("listNodes() failed with exception:")
        raise


def get_cn_metrics(cn):
    client = d1_client.cnclient.CoordinatingNodeClient(base_url=cn.baseURL)
    get_gen_metrics(client, cn)


def get_mn_metrics(mn):
    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(base_url=mn.baseURL)
    get_gen_metrics(client, mn)
    print_capabilities(client)


def print_capabilities(client):
    caps = client.getCapabilities()
    print("Identifier: {}".format(caps.identifier.value()))
    print("Name: {}".format(caps.name))
    print("Description: {}".format(caps.description))
    print("Member Node subject(s):")
    for s in caps.subject:
        print("  {}".format(s.value()))
    print("Contact(s):")
    for c in caps.contactSubject:
        print("  {}".format(c.value()))
    # print 'Contact subject: {0}'.format(caps.contactSubject)
    print("Services:")
    for s in caps.services.service:
        print("  Name: {}".format(s.name))
        print("  Version: {}".format(s.version))
        print("  Available: {}".format(s.available))
    print("Synchronization: ")
    print(
        (
            "  Schedule: hour={} mday={} min={} mon={} sec={} wday={} year={}".format(
                caps.synchronization.schedule.hour,
                caps.synchronization.schedule.mday,
                caps.synchronization.schedule.min,
                caps.synchronization.schedule.mon,
                caps.synchronization.schedule.sec,
                caps.synchronization.schedule.wday,
                caps.synchronization.schedule.year,
            )
        )
    )
    print("  Last harvested: {}".format(caps.synchronization.lastHarvested))
    print(
        ("  Last complete harvest: {}".format(caps.synchronization.lastCompleteHarvest))
    )


def get_gen_metrics(client, node):
    print("Node: {}".format(node.name))
    print("Base URL: {}".format(node.baseURL))
    print("Node Type: {}".format(node.type.upper()))
    print("Ping: {}".format(get_ping(client)))
    print("Total number of objects: {}".format(get_number_of_objects(client)))
    try:
        print(
            (
                "Total number of log records: {}".format(
                    get_number_of_log_records(client)
                )
            )
        )
    except d1_common.types.exceptions.NotAuthorized:
        print("Log records are restricted")


def get_ping(client):
    return client.ping()


def get_number_of_objects(client):
    try:
        return client.listObjects(start=0, count=0).total
    except d1_common.types.exceptions.DataONEException:
        logging.exception("listObjects() failed with exception:")
        raise


def get_number_of_log_records(client):
    return client.getLogRecords(start=0, count=0).total


def is_member_node(node):
    return node.type == "mn"


def is_coordinating_node(node):
    return node.type == "cn"


if __name__ == "__main__":
    sys.exit(main())
