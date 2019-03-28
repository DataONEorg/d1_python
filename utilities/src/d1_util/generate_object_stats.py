#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""Generate statistics for Science Objects on a given set of Member Nodes.

This is an example on how to use the DataONE Client and Common libraries for
Python. It shows how to:

- Aggregate values from System Metadata on a set of Member Nodes

Operation:

- Configure the script in the Config section below

"""

import argparse
import json
import logging
import os
import sys

import requests

import d1_common.env
import d1_common.util

import d1_client.iter.sysmeta_multi

# Config

DEFAULT_GMN_LIST_PATH = 'gmn_node_list.json'
DEFAULT_OBJ_STATS_PATH = 'gmn_stats_list2.json'


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    parser.add_argument(
        '--env',
        type=str,
        default='prod',
        help='Environment, one of {}'.format(', '.join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        '--cert-pub',
        dest='cert_pem_path',
        action='store',
        help='Path to PEM formatted public key of certificate',
    )
    parser.add_argument(
        '--cert-key',
        dest='cert_key_path',
        action='store',
        help='Path to PEM formatted private key of certificate',
    )
    parser.add_argument(
        '--timeout',
        action='store',
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help='Amount of time to wait for calls to complete (seconds)',
    )

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--fin',
        default=DEFAULT_GMN_LIST_PATH,
        help='Path to input JSON file with GMN instances to examine',
    )
    parser.add_argument(
        '--fout',
        default=DEFAULT_OBJ_STATS_PATH,
        help='Path to output JSON file with object size statistics',
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    args = parser.parse_args()

    d1_common.util.log_setup(args.debug)

    if not os.path.exists(args.fin):
        raise ValueError('No such file: {}'.format(args.fin))

    requests.packages.urllib3.disable_warnings()

    with open(args.fin, 'r') as f:
        gmn_node_struct = json.load(f)

    gmn_node_list = gmn_node_struct['gmn_nodes']
    env_dict = gmn_node_struct['env']

    stats_list = find_object_size_stats_node_all(gmn_node_list)

    with open(args.fout, 'w') as f:
        json.dump({'env': env_dict, 'stats_list': stats_list}, f, indent=2)

    logging.info('Wrote result to JSON file. path="{}"'.format(args.fout))


def find_object_size_stats_node_all(gmn_node_list):
    stats_list = []
    for gmn_dict in gmn_node_list:
        try:
            int(gmn_dict['object_count_str'])
        except ValueError:
            continue

        stats_dict = find_object_size_stats_node(gmn_dict)
        stats_dict['gmn_dict'] = gmn_dict
        stats_list.append(stats_dict)

    return stats_list


def find_object_size_stats_node(gmn_dict):
    logging.info('-' * 100)
    logging.info('{} - {}'.format(gmn_dict['base_url'], gmn_dict['node_id']))

    sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
        gmn_dict['base_url'],
        api_major=1,
        client_dict={'verify_tls': False, 'suppress_verify_warnings': True},
    )

    stats_counter = d1_common.util.EventCounter()
    sysmeta_pyxb_list = []

    for i, sysmeta_pyxb in enumerate(sysmeta_iter):
        pid = sysmeta_pyxb.identifier.value()
        logging.info(
            '{:.2f} - {}'.format(
                float(i) / int(gmn_dict['object_count_str']) * 100, pid
            )
        )

        max_size_sysmeta_list(sysmeta_pyxb_list, sysmeta_pyxb)

        if sysmeta_pyxb.size > 1024 ** 2:
            stats_counter.count('small_obj')
        else:
            stats_counter.count('large_obj')

    return {
        'largest_sysmeta_xml': [s.toxml('utf-8') for s in sysmeta_pyxb_list],
        'stats_dict': stats_counter.event_dict,
    }


def max_size_sysmeta_list(sysmeta_pyxb_list, sysmeta_pyxb, max_size=10):
    sysmeta_pyxb_list.append(sysmeta_pyxb)
    sysmeta_pyxb_list.sort(key=lambda x: x.size, reverse=True)
    sysmeta_pyxb_list[:] = sysmeta_pyxb_list[:max_size]


def log_dict(d):
    logging.info(
        ', '.join(
            ['{}="{}"'.format(k, d[k]) for k in sorted(d) if k is not 'sysmeta_xml']
        )
    )


if __name__ == '__main__':
    sys.exit(main())
