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
import argparse
import logging
import logging.config

import d1_common
import d1_common.const
import d1_common.env


def get_standard_arg_parser(
    description_str=None,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    # formatter_class=argparse.RawDescriptionHelpFormatter,
    add_base_url=False,
):
    """Return an argparse.ArgumentParser populated with a standard set of command line
    arguments.

    Command line tools that interact with the DataONE infrastructure typically
    instantiate a DataONE Client with all arguments either set to their defaults or
    specified as command line arguments by the user.

    This module makes it convenient for scripts to add a standardized set of command
    line arguments that allow the user to override the default settings in the DataONE
    Client as needed.

    The script that calls this function will typically add its own specific arguments by
    making additional ``parser.add_argument()`` calls before extracting the command line
    arguments with ``args = parser.parse_args()``.

    When creating the DataONE Client, simply pass the command line arguments to the client
    via the ``command_line_adapter()``.

    Args:
        description_str: Description of the command
            The description is included in the automatically generated help message.

        formatter_class:
            Modify the help message format. See the `argparse` module for available
            Formatter classes.

        add_base_url:
            Require a BaseURL to be provided as a positional command line argument.

            If the script will be creating a CN Client, leave this set to False to
            enable automatically connecting to the CN in the environment specified by
            ``--env``, which is the Production environment by default.

            If the script will be creating a MN Client, set this to True to require a MN
            BaseURL to be specified on the command line.

    Returns:
        argparse.ArgumentParser(): Prepulated with command line arguments that allow overriding
            DataONEClient defaults.

    Example:

        def main():
            parser = d1_client.command_line.get_standard_d1_client_arg_parser(
                __doc__, add_base_url=True
            )
            parser.add_argument(
                "--my-additional-arg",
                ...
            )
            ...
            args = parser.parse_args()
            ...
            client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
                d1_client.command_line.args_adapter(args)
            )
            ...

    """
    parser = argparse.ArgumentParser(
        description=description_str, formatter_class=formatter_class
    )
    group = parser.add_argument_group("DataONE Client")
    group.add_argument(
        "--env",
        dest="env",
        metavar="d1env",
        default=d1_common.env.get_d1_env_keys()[0],
        choices=d1_common.env.get_d1_env_keys(),
        help="DataONE environment to use",
    )
    group.add_argument(
        "--cert-pub",
        dest="d1client__cert_pem_path",
        metavar="path",
        action="store",
        help="Path to PEM formatted public key of certificate",
    )
    group.add_argument(
        "--cert-key",
        dest="d1client__cert_key_path",
        metavar="path",
        action="store",
        help="Path to PEM formatted private key of certificate",
    )
    group.add_argument(
        "--jwt-token",
        dest="d1client__jwt_token",
        metavar="string",
        action="store",
        help="JSON Web Token (JWT) to pass to the remote node",
    )
    group.add_argument(
        "--disable-cert-validation",
        dest="d1client__verify_tls",
        action="store_false",
        help="Do not validate the TLS/SSL server side certificate of the remote node (insecure)",
    )
    group.add_argument(
        "--timeout",
        type=float,
        dest="d1client__timeout_sec",
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        metavar="sec",
        action="store",
        help="Timeout for API calls to the remote node",
    )
    group.add_argument(
        "--tries",
        dest="d1client__retries",
        type=int,
        default=3,
        metavar="num",
        action="store",
        help="Number of times to try an API call that returns an HTTP error code",
    )
    group.add_argument(
        "--major",
        type=int,
        dest="d1client__major",
        metavar="num",
        action="store",
        help="Use API major version instead of finding by querrying a CN",
    )
    group.add_argument(
        "--user-agent",
        dest="d1client__user_agent",
        default=d1_common.const.USER_AGENT,
        action="store",
        metavar="string",
        help="Override the default User-Agent header",
    )
    group.add_argument(
        "--encoding",
        dest="d1client__charset",
        default=d1_common.const.DEFAULT_CHARSET,
        action="store",
        metavar="string",
        help="Specify character encoding for HTTP message body",
    )
    # General, not passed to DataONEClient
    group.add_argument(
        "--page-size",
        type=int,
        dest="page_size",
        default=d1_common.const.DEFAULT_SLICE_SIZE,
        metavar="items",
        action="store",
        help="Number of objects to request per page when calling APIs that support paging",
    )
    group.add_argument(
        "--debug",
        action="store_true",
        dest="debug",
        help="Set debug level logging in D1Client",
    )
    if add_base_url:
        group.add_argument("base_url", help="Member Node BaseURL")

    parser.add_argument_group("Command")

    return parser


def args_adapter(args):
    """Convert a command line arguments object to a dict suitable for passing to a
    D1Client create call via argument unpacking.

    Args:
        args: Object returned from `parser.parse_args()`

    Returns:
        dict: Arguments valid for passing to a D1Client create call.

    Example:

        args = parser.parse_args()
        ...
        client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
            **d1_client.command_line.args_adapter(args)
        )

    """
    arg_dict = {
        k.replace("d1client__", ""): v
        for k, v in vars(args).items()
        if k.startswith("d1client__") and v is not None
    }
    if "base_url" not in arg_dict:
        arg_dict["base_url"] = d1_common.env.get_d1_env(args.env)["base_url"]
        # arg_dict.setdefault('base_url', d1_common.env.get_d1_env(args.env)['base_url'])
    return arg_dict


def log_setup(is_debug):
    """Set up a log format that is suitable for writing to the console by command line
    tools."""
    level = logging.DEBUG if is_debug else logging.INFO
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "%(levelname)-8s %(message)s",
                    "datefmt": None,
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "level": level,
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": level,
                    "class": "logging.StreamHandler",
                }
            },
        }
    )
