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
"""DataONE Command Line Interface."""

import logging
import optparse
import sys
import traceback

import d1_cli.impl.check_dependencies
import d1_cli.impl.command_parser
import d1_cli.impl.exceptions
import d1_cli.impl.session
import d1_cli.impl.util
import d1_cli.version

import d1_common.types.exceptions

# def module_path():
#     """ This will get us the program's directory,
#     even if we are frozen using py2exe"""
#
#     if we_are_frozen():
#         return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
#
#     return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
#
# sys.path.append(os.path.join(module_path(), u'./impl'))


def main():
    if not d1_cli.impl.check_dependencies.are_modules_importable():
        raise Exception("Dependency check failed")

    print("DataONE Command Line Interface ({})".format(d1_cli.version.__version__))

    parser = optparse.OptionParser(
        usage="usage: %prog [command] ...", option_list=option_list
    )
    options, commands = parser.parse_args()

    command_parser = d1_cli.impl.command_parser.CLI()
    handle_options(command_parser, options)

    d1_common.util.log_setup(options.debug)

    # If the user passed commands on the command line, run them.
    for command in commands:
        try:
            command_parser.onecmd(command)
        except (
            d1_cli.impl.exceptions.InvalidArguments,
            d1_cli.impl.exceptions.CLIError,
        ) as e:
            d1_cli.impl.util.print_error(e)
        except d1_common.types.exceptions.DataONEException as e:
            d1_cli.impl.util.print_error("DataONE Node returned error:")
            d1_cli.impl.util.print_error(e)
        # except RuntimeError:
        #     if options.debug:
        #         raise
        #     handle_unexpected_exception()

    # Enter the main processing loop.
    while True:
        try:
            command_parser.cmdloop()
        except KeyboardInterrupt:
            command_parser.do_exit("")
        except SystemExit:
            break
        except (
            d1_cli.impl.exceptions.InvalidArguments,
            d1_cli.impl.exceptions.CLIError,
        ) as e:
            d1_cli.impl.util.print_error(e)
            # raise
        except d1_common.types.exceptions.DataONEException as e:
            # Suppress trace information in DataONEExceptions if not in debug mode.
            if not options.debug:
                e.traceInformation = None
            d1_cli.impl.util.print_error("DataONE Node returned error:")
            d1_cli.impl.util.print_error(e)
        # except RuntimeError:
        #     if options.debug:
        #         raise
        #     handle_unexpected_exception()


def log_setup(debug):
    if debug:
        logging.getLogger("").setLevel(logging.DEBUG)
    else:
        logging.getLogger("").setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger("").addHandler(console_logger)


# Command-line options.
option_list = [
    optparse.make_option(
        "--" + d1_cli.impl.session.CHECKSUM_NAME,
        action="store",
        dest="algorithm",
        help="Checksum algorithm used for a Science Data Object.",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.ANONYMOUS_NAME,
        action="store_true",
        dest="anonymous",
        help="Ignore any installed certificates and connect anonymously",
    ),
    optparse.make_option(
        "--no-" + d1_cli.impl.session.ANONYMOUS_NAME,
        action="store_false",
        dest="anonymous",
        help="Use the installed certificates and do not connect anonymously",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.AUTH_MN_NAME,
        action="store",
        dest="authoritative_mn",
        metavar="MN-URI",
        help="Authoritative Member Node for generating System Metadata.",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.CERT_FILENAME_NAME,
        action="store",
        dest="cert_file",
        metavar="FILE",
        help="Path to client certificate",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.COUNT_NAME,
        action="store",
        dest="count",
        type="int",
        help="Maximum number of items to display",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.CN_URL_NAME,
        action="store",
        dest="cn_url",
        metavar="URI",
        help="URI to use for the Coordinating Node",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.FROM_DATE_NAME,
        action="store",
        dest="from_date",
        metavar="DATE",
        help="Start time used by operations that accept a date range",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.KEY_FILENAME_NAME,
        action="store",
        dest="key_file",
        metavar="FILE",
        help="File of client private key (not required if key is in cert-file",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.MN_URL_NAME,
        action="store",
        dest="mn_url",
        metavar="URI",
        help="Member Node URL",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.FORMAT_NAME,
        action="store",
        dest="object_format",
        metavar="OBJECT-FORMAT",
        help="ID for the Object Format to use when generating System Metadata",
    ),
    optparse.make_option(
        "--formatId",
        action="store",
        dest="object_format",
        metavar="OBJECT-FORMAT",
        help="ID for the Object Format to use when generating System Metadata",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.QUERY_STRING_NAME,
        action="store",
        dest="query_string",
        metavar="QUERY",
        help="Query string (SOLR or Lucene query syntax) for searches",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.OWNER_NAME,
        action="store",
        dest="rights_holder",
        metavar="SUBJECT",
        help="Subject of the rights holder to use when generating System Metadata",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.SEARCH_FORMAT_NAME,
        action="store",
        dest="search_object_format",
        metavar="OBJECT-FORMAT",
        help="Include only objects of this format when searching",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.START_NAME,
        action="store",
        dest="start",
        type="int",
        help="First item to display for operations that display a list_objects of items",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.TO_DATE_NAME,
        action="store",
        dest="to_date",
        metavar="DATE",
        help="End time used by operations that accept a date range",
    ),
    optparse.make_option(
        "-v",
        "--" + d1_cli.impl.session.VERBOSE_NAME,
        action="store_true",
        dest="verbose",
        help="Display more information",
    ),
    optparse.make_option(
        "--no-" + d1_cli.impl.session.VERBOSE_NAME,
        action="store_false",
        dest="verbose",
        help="Display less information",
    ),
    optparse.make_option(
        "--" + d1_cli.impl.session.EDITOR_NAME,
        action="store_true",
        dest="editor",
        help="Editor to use for editing operation queue",
    ),
    optparse.make_option(
        "--no-" + d1_cli.impl.session.EDITOR_NAME,
        action="store_false",
        dest="editor",
        help="Use editor specified in EDITOR environment variable",
    ),
    optparse.make_option(
        "--allow-replication",
        action="store_true",
        dest="action_allowReplication",
        help="Allow objects to be replicated.",
    ),
    optparse.make_option(
        "--disallow-replication",
        action="store_false",
        dest="action_allowReplication",
        help="Do not allow objects to be replicated.",
    ),
    optparse.make_option(
        "--replicas",
        action="store",
        dest="action_numReplicas",
        metavar="#replicas",
        help="Set the preferred number of replicas.",
    ),
    optparse.make_option(
        "--add_blocked",
        action="store",
        dest="action_blockNode",
        metavar="MN",
        help="Add blocked Member Node to access policy.",
    ),
    optparse.make_option(
        "--add_preferred",
        action="store",
        dest="action_preferNode",
        metavar="MN",
        help="Add Member Node to list_objects of preferred replication targets.",
    ),
    #  optparse.make_option('--configure', action='store_true', dest='action_configure',
    #              help='Perform initial configuration'),
    optparse.make_option(
        "--cn",
        action="store",
        dest="cn_host",
        metavar="HOST",
        help="Name of the host to use for the Coordinating Node",
    ),
    optparse.make_option(
        "--mn",
        action="store",
        dest="mn_host",
        metavar="HOST",
        help="Name of the host to use for the Member Node",
    ),
    optparse.make_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        help="Display less information",
    ),
    optparse.make_option(
        "--debug", action="store_true", help="Print full stack trace and exit on errors"
    ),
]


def handle_options(cli, options):
    try:
        if options.algorithm:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.CHECKSUM_NAME, options.algorithm
            )
        if options.anonymous:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.ANONYMOUS_NAME, options.anonymous
            )
        if options.authoritative_mn:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.AUTH_MN_NAME, options.authoritative_mn
            )
        if options.cert_file:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.CERT_FILENAME_NAME, options.cert_file
            )
        if options.count:
            cli.d1.session_set_parameter(d1_cli.impl.session.COUNT_NAME, options.count)
        if options.cn_url:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.CN_URL_NAME, options.cn_url
            )
        if options.cn_host:
            url = "".join(
                (
                    d1_common.const.DEFAULT_CN_PROTOCOL,
                    "://",
                    options.cn_host,
                    d1_common.const.DEFAULT_CN_PATH,
                )
            )
            cli.d1.session_set_parameter(d1_cli.impl.session.CN_URL_NAME, url)
        if options.from_date:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.FROM_DATE_NAME, options.from_date
            )
        if options.key_file:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.KEY_FILENAME_NAME, options.key_file
            )
        if options.mn_url:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.MN_URL_NAME, options.mn_url
            )
        if options.mn_host:
            url = "".join(
                (
                    d1_common.const.DEFAULT_MN_PROTOCOL,
                    "://",
                    options.mn_host,
                    d1_common.const.DEFAULT_MN_PATH,
                )
            )
            cli.d1.session_set_parameter(d1_cli.impl.session.MN_URL_NAME, url)
        if options.object_format:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.FORMAT_NAME, options.object_format
            )
        if options.query_string:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.QUERY_STRING_NAME, options.query_string
            )
        if options.rights_holder:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.OWNER_NAME, options.rights_holder
            )
        if options.search_object_format:
            try:
                cli.d1.session_set_parameter(
                    d1_cli.impl.session.SEARCH_FORMAT_NAME, options.search_object_format
                )
            except ValueError as e:
                d1_cli.impl.util.print_error(e.args[0])
        if options.start:
            cli.d1.session_set_parameter(d1_cli.impl.session.START_NAME, options.start)
        if options.to_date:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.TO_DATE_NAME, options.to_date
            )
        if options.verbose:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.VERBOSE_NAME, options.verbose
            )
        if options.editor:
            cli.d1.session_set_parameter(
                d1_cli.impl.session.EDITOR_NAME, options.editor
            )
        # Replication.
        if options.action_allowReplication is not None:
            if options.action_allowReplication:
                cli.d1.replication_policy_set_replication_allowed(True)
            else:
                cli.d1.replication_policy_set_replication_allowed(False)
        if options.action_numReplicas:
            cli.d1.replication_policy_set_number_of_replicas(options.action_numReplicas)
        if options.action_blockNode:
            cli.d1.get_replication_policy().add_blocked(options.action_blockNode)
        if options.action_preferNode:
            cli.d1.get_replication_policy().add_preferred(options.action_preferNode)
    except d1_cli.impl.exceptions.InvalidArguments as e:
        d1_cli.impl.util.print_error(e)
    # except RuntimeError:
    #     d1_cli.impl.util._handle_unexpected_exception()


def handle_unexpected_exception(max_traceback_levels=100):
    """Suppress stack traces for common errors and provide hints for how to resolve
    them."""
    exc_type, exc_msgs = sys.exc_info()[:2]
    if exc_type.__name__ == "SSLError":
        d1_cli.impl.util.print_error(
            """HTTPS / TLS / SSL / X.509v3 Certificate Error:
  An HTTPS connection could not be established. Verify that a DataONE node
  responds at the URL provided in the cn-url or mn-url session variable. If the
  URL is valid and if you intended to connect without authentication, make sure
  that the session variable, "anonymous", is set to True. If you intended to
  connect with authentication, make sure that the parameter, "cert-file", points
  to a valid certificate from CILogon. If the certificate has the private
  key in a separate file, also set "key-file" to the private key file.
  Otherwise, set "key-file" to None. Note that CILogon certificates must be
  renewed after 18 hours.
            """
        )
    elif exc_type.__name__ == "timeout":
        d1_cli.impl.util.print_error(
            """Timeout error:
  A connection to a DataONE node timed out. Verify that a DataONE node responds
  at the URL provided in the cn-url or mn-url session variable.
            """
        )
    else:
        _print_unexpected_exception(max_traceback_levels)


def _print_unexpected_exception(max_traceback_levels=100):
    exc_class, exc_msgs, exc_traceback = sys.exc_info()
    d1_cli.impl.util.print_error("Error:")
    d1_cli.impl.util.print_error("  Name: {}".format(exc_class.__name__))
    d1_cli.impl.util.print_error("  Value: {}".format(exc_msgs))
    try:
        exc_args = exc_msgs.__dict__["args"]
    except KeyError:
        exc_args = "<no args>"
    d1_cli.impl.util.print_error("  Args: {}".format(exc_args))
    d1_cli.impl.util.print_error("  Traceback:")
    for tb in traceback.format_tb(exc_traceback, max_traceback_levels):
        d1_cli.impl.util.print_error("    {}".format(tb))


if __name__ == "__main__":
    sys.exit(main())
