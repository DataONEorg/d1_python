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
import argparse

import django.conf

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2
DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20
DEFAULT_RETRY_COUNT = 3


def add_arguments(parser, docstr, add_base_url=True):
    """Add standard arguments for DataONE utilities to a command line parser."""
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument("--debug", action="store_true", help="Debug level logging")
    parser.add_argument(
        "--cert-pub",
        dest="cert_pem_path",
        action="store",
        default=django.conf.settings.CLIENT_CERT_PATH,
        help="Path to PEM formatted public key of certificate",
    )
    parser.add_argument(
        "--cert-key",
        dest="cert_key_path",
        action="store",
        default=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
        help="Path to PEM formatted private key of certificate",
    )
    parser.add_argument(
        "--public", action="store_true", help="Do not use certificate even if available"
    )
    parser.add_argument(
        "--disable-server-cert-validation",
        action="store_true",
        help="Do not validate the TLS/SSL server side certificate of the source node (insecure)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        action="store",
        default=DEFAULT_TIMEOUT_SEC,
        help="Timeout for DataONE API calls to the source MN",
    )
    parser.add_argument(
        "--retries",
        type=int,
        action="store",
        default=DEFAULT_RETRY_COUNT,
        help="Retry DataONE API calls that raise HTTP level exceptions",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        action="store",
        default=DEFAULT_PAGE_SIZE,
        help="Number of objects to retrieve in each list method API call to source MN",
    )
    parser.add_argument(
        "--major",
        type=int,
        action="store",
        help="Skip automatic detection of API major version and use the provided version",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        action="store",
        default=DEFAULT_MAX_CONCURRENT_TASK_COUNT,
        help="Max number of concurrent DataONE API",
    )
    if not add_base_url:
        parser.add_argument(
            "--baseurl",
            action="store",
            default=django.conf.settings.DATAONE_ROOT,
            help="Remote MN or CN BaseURL",
        )
    else:
        parser.add_argument("baseurl", help="Remote MN or CN BaseURL")
