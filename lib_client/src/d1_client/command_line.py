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
import logging
import logging.config

import d1_common
import d1_common.const
import d1_common.env
import d1_common.utils.arg_parse
import d1_common.utils.ulog


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
    argparse.ArgumentParser(): Prepopulated with command line arguments that allow overriding
        DataONEClient defaults.

Example:

    def main():
        parser = d1_client.command_line.D1ClientArgParser(
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
            parser.get_method_args(args)
        )
        ...

"""


class D1ClientArgParser(d1_common.utils.arg_parse.ArgParserBase):
    """An argparse.ArgumentParser populated with a standard set of command line
    arguments for controlling the path generator from the command line.

    The script that calls this function will typically add its own specific arguments by
    making additional ``parser.add_argument()`` calls.

    When creating the path_generator, simply pass ``parser.get_method_args`` to
    `path_generator()`.

    Example:
        import d1_common.iter.path

        parser = d1_common.iter.path.ArgParser(
            __doc__,
            # Set non-configurable values
            include_glob_list=['*.py'],
            return_entered_dir_paths=True,
        )
        # Add command specific arguments
        parser.add_argument(...)
        # Create the path_generator and iterate over the resulting paths
        for p in d1_common.iter.path.path_generator(parser.get_method_args):
            print(p)
    """

    def __init__(self, *args, **kwargs):
        """Create a ArgumentParser populated with a standard set of command line
        arguments for controlling the path generator from the command line.

        Args:
            description_str: Description of the command
                The description is included in the automatically generated help message.

            formatter_class:
                Modify the help message format. See the `argparse` module for available
                Formatter classes.

            fixed value overrides:
                Passing any of these arguments causes provided value to be used when
                instantiating the path generator, and the corresponding command line
                argument to become hidden and unavailable.

            default value overrides:
                Passing any of these arguments causes the provided value to be used
                as the default. The corresponding command line argument is still
                available and can be used to override the default value

        """
        self.parser_name = "DataONE Client"
        self.parser_dict = {
            "env": (
                "--env",
                dict(
                    metavar="d1env",
                    default=d1_common.env.get_d1_env_keys()[0],
                    choices=d1_common.env.get_d1_env_keys(),
                    help="DataONE environment to use",
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
            "jwt_token": (
                "--jwt-token",
                dict(
                    metavar="string",
                    action="store",
                    help="JSON Web Token (JWT) to pass to the remote node",
                ),
            ),
            "verify_tls": (
                "--disable-cert-validation",
                dict(
                    action="store_false",
                    help="Do not validate the TLS/SSL server side certificate of the remote node (insecure)",
                ),
            ),
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
            "try_count": (
                "--try-count",
                dict(
                    type=int,
                    default=3,
                    metavar="N",
                    action="store",
                    help="Number of times to try an API call that returns an HTTP error code",
                ),
            ),
            "major": (
                "--major",
                dict(
                    type=int,
                    metavar="N",
                    action="store",
                    help="Use API major version instead of finding by querying a CN",
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
            "charset": (
                "--encoding",
                dict(
                    default=d1_common.const.DEFAULT_CHARSET,
                    action="store",
                    metavar="string",
                    help="Specify character encoding for HTTP message body",
                ),
            ),
            # General, not passed to DataONEClient
            "page_size": (
                "--page-size",
                dict(
                    type=int,
                    default=d1_common.const.DEFAULT_SLICE_SIZE,
                    metavar="items",
                    action="store",
                    help="Number of objects to request per page when calling APIs that support paging",
                ),
            ),
        }
        super().__init__(*args, **kwargs)
        # if add_base_url:
        #     group.add_argument("base_url", help="Member Node BaseURL")
        #
        # parser.add_argument_group("Command")
        #
        # return parser
        #
        # super().__init__(self, *args, **kwargs)


def log_setup(is_debug, disable_existing_loggers=False):
    """Set up a log format that is suitable for writing to the console by command line
    tools."""
    level = logging.DEBUG if is_debug else logging.INFO
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": disable_existing_loggers,
            "formatters": {
                "verbose": {"format": "%(levelname)-8s %(message)s", "datefmt": None}
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "level": level,
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["stdout"],
                    "level": level,
                    "class": "logging.StreamHandler",
                }
            },
        }
    )
