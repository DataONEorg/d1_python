#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Solr query.

This is an example on how to use the DataONE Client Library for Python. It
shows how to:

- Query DataONE's Solr index
- Display the results

"""
import argparse
import logging
import pprint
import sys

import d1_common.env

import d1_client.solr_client


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

    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)

    # Connect to the DataONE Coordinating Nodes in the default (production) environment.
    c = d1_client.solr_client.SolrConnection()

    search_result = c.search(
        {
            'q': 'id:[* TO *]',  # Filter for search
            'rows': 10,  # Number of results to return
            'fl': 'formatId',  # List of fields to return for each result
        }
    )

    pprint.pprint(search_result)


if __name__ == '__main__':
    sys.exit(main())
