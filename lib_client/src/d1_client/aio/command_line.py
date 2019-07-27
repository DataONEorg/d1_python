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
"""Utilities for command line tools that instantiate `DataONEClient()`,
`CoordinatingNodeClient()`, or `MemberNodeClient()` objects.

The intention is to both reduce the amount of boilerplate code in command line tools
that interact with the DataONE infrastructure and to standardize the behavior of the
scripts.

"""
import d1_common
import d1_common.const
import d1_common.env
import d1_common.utils.arg_parse
import d1_common.utils.ulog

import d1_client.aio.async_client


class AsyncArgParser(d1_common.utils.arg_parse.ArgParserBase):
    def __init__(self, *args, **kwargs):
        self.parser_name = "DataONE Client"
        self.parser_dict = {
            "timeout_sec": (
                "--timeout",
                dict(
                    type=float,
                    default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
                    metavar="sec",
                    action="store",
                    help="Timeout for API calls to the remote node",
                ),
            ),
            "cert_pem_path": (
                "--cert-pub",
                dict(
                    metavar="path",
                    action="store",
                    help="Path to PEM formatted public key of certificate",
                ),
            ),
            "cert_key_path": (
                "--cert-key",
                dict(
                    metavar="path",
                    action="store",
                    help="Path to PEM formatted private key of certificate",
                ),
            ),
            "disable_server_cert_validation": (
                "--disable-cert-validation",
                dict(
                    action="store_true",
                    help="Do not validate the TLS/SSL server side certificate of the remote node (insecure)",
                ),
            ),
            "max_concurrent": (
                "--max-concurrent",
                dict(
                    type=int,
                    default=d1_client.aio.async_client.DEFAULT_MAX_CONCURRENT,
                    metavar="N",
                    action="store",
                    help="Max number of concurrent DataONE API calls",
                ),
            ),
            "try_count": (
                "--try-count",
                dict(
                    type=int,
                    default=d1_client.aio.async_client.DEFAULT_TRY_COUNT,
                    metavar="N",
                    action="store",
                    help="Number of times to try an API call that returns an HTTP error code",
                ),
            ),
            "user_agent": (
                "--user-agent",
                dict(
                    default=d1_common.const.USER_AGENT,
                    action="store",
                    metavar="string",
                    help="Override the default User-Agent header",
                ),
            ),
            # "charset": (
            #     "--encoding",
            #     dict(
            #         default=d1_common.const.DEFAULT_CHARSET,
            #         action="store",
            #         metavar="string",
            #         help="Specify character encoding for HTTP message body",
            #     ),
            # ),
            "base_url": (
                "base-url",
                dict(help="DataONE API BaseURL of remote Coordinating or Member Node"),
            ),
        }
        super().__init__(*args, **kwargs)
