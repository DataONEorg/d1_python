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

"""Base for all GMN Management Commands.
"""
import argparse
import asyncio
import fcntl
import functools
import logging
import logging.config
import os
import random
import re
import sys
import tempfile

import psycopg2
import psycopg2.extensions
import psycopg2.extras

import d1_common.cert
import d1_common.cert.jwt
import d1_common.const
import d1_common.types.exceptions
import d1_common.typing as t
import d1_common.util
import d1_common.utils.arg_parse
import d1_common.utils.progress_tracker
import d1_common.utils.ulog

import d1_client.aio.async_client
import d1_client.aio.command_line
import d1_client.aio.iter.eventlog_async
import d1_client.aio.iter.eventlog_cmd
import d1_client.aio.iter.objectlist_async
import d1_client.aio.iter.objectlist_cmd
import d1_client.command_line
import d1_client.d1client

import django.conf
import django.core
import django.core.exceptions
import django.core.management.base
import django.db

import d1_gmn.app.middleware.session_cert
import d1_gmn.app.model_util
import d1_gmn.app.models

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2
DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20
DEFAULT_TRY_COUNT = 3

# log = logging.getLogger('view-cert')


class GMNCommandBase(django.core.management.base.BaseCommand):
    """All GMN commands derive from this base instead of BaseCommand.
    """

    async_d1_client: t.AsyncD1Client

    def __init__(self, doc_rst, name_str, *args, **kwargs):
        """Initialize the context in which the GMN command will run.

        Args:
            doc_rst: str
                ``__doc__`` from the module of the GMN command.
            name_str:
                ``__name__`` from the module of the GMN command.
            *args and **kwargs:
                Anything ``manage.py`` wants to pass to the Django ``BaseCommand``
                class.
        """
        super().__init__(*args, **kwargs)
        self.CommandError = django.core.management.base.CommandError
        self.command_name = name_str.split(".")[-1]
        self.log = self.setup_logging()
        self.is_help = "--help" in sys.argv or "-h" in sys.argv
        self.doc_str = self._strip_rst_markup(doc_rst)
        self.tracker = None
        self.opt_dict = None
        self.single_instance_lock_file = None
        # Components available via add_components()
        self.async_d1_client = None
        self.async_d1_client_arg_parser = None
        self.async_event_log_iter = None
        self.async_event_log_iter_arg_parser = None
        self.async_object_list_iter = None
        self.async_object_list_iter_arg_parser = None
        self.d1_client = None
        self.d1_client_arg_parser = None
        #
        self.task_set = set()
        self.pid_set = set()
        self.main_task_name = "Running GMN command: {}".format(self.command_name)

    def run_from_argv(self, argv):
        """Override the entry point through which management commands are called with a
        wrapper that does some initialization and cleanup.

        - Add a message saying to use --help for more information when erroring out.
        Without `--help`, Django prints a shorter usage message, and it is not obvious
        that there is more information available in the full help message.

        - Add a blank line after help message.

        Text written to stderr is colored red when Django detects that stdout is a
        console.
        """
        try:
            with d1_common.utils.progress_tracker.ProgressTracker(self.log) as tracker:
                self.tracker = tracker

                super().run_from_argv(argv)
        except KeyboardInterrupt:
            logging.disable()
        except SystemExit:
            if not self.is_help:
                self.stderr.write("\nUse --help for more information\n")
            raise
        except d1_common.cert.jwt.JwtException as e:
            self.stderr.write(str(e))
        except d1_common.types.exceptions.DataONEException as e:
            self.stderr.write(e.friendly_format() + "\n")
        finally:
            if self.d1_client:
                self.d1_client.close()
            if "--help" in argv or "-h" in argv:
                self.stderr.write("\n")

    # Command line options and arguments

    def setup_logging(self):
        # Logging
        d1_common.utils.ulog.setup(is_debug=True, disable_existing_loggers=False)
        # d1_common.utils.ulog.setup(True, False)
        logging.setLoggerClass(d1_common.utils.ulog.ULogger)
        return logging.getLogger(self.command_name)
        # self.log.setLevel(logging.DEBUG)
        # logging.basicConfig(level=logging.DEBUG)
        # self.log.error('111111111111111111111')
        # self.log = d1_common.utils.ulog.getLogger(self.command_name)
        # self.log = logging.getLogger(self.command_name)
        # logging.getLogger(d1_gmn.app.node_registry.__name__).setLevel(logging.ERROR)

        #! d1_common.utils.ulog.debug_logging_tree()
        #! print('-------------------')
        #! print(self.log.level)
        #! self.log.debug('\nDEBUG\n')
        #! self.log.info('\nINFO\n')
        #! self.log.error('\nERROR\n')
        #! self.log = logging.getLogger('view-cert')#!'(self.command_name)
        #! self.log_writer = d1_common.utils.ulog.LogWriter(self.log.info)
        #! logging.basicConfig(level=logging.DEBUG)
        #! print('aaaaaaaaaaaaa')
        #! self.log.info('111111111111111')
        #! self.log_writer = self.log.info
        #! self.log_writer('log writer 22222222222222')
        #! d1_common.utils.ulog.debug_logging_tree()
        #! print(self.command_name)
        #! print('stdout')
        #! self.stdout.write('w stdout')
        #! sys.stdout.write('sys stdout')
        #! print(self.stdout)
        #! print('stderr')
        #! self.stderr.write('w stderr')
        #! sys.stderr.write('sys stderr')
        #! print(self.stderr)
        #! sys.exit()
        #!

    def create_parser(self, prog_name, subcommand, **kwargs):
        """Override and slightly tweak the argparse.ArgumentParser created automatically
        for management commands. Add arguments shared by all GMN commands.

        """
        parser = django.core.management.base.CommandParser(
            prog=f"d1-gmn {subcommand}",
            description=self.doc_str,
            formatter_class=GMNHelpFormatter.factory(self.is_help),
            called_from_command_line=getattr(self, "_called_from_command_line", None),
            **kwargs,
        )

        # Add standard Django commands.
        parser.add_argument(
            "-v",
            "--verbosity",
            default=1,
            type=int,
            choices=[0, 1, 2, 3],
            help="Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output",
        )
        parser.add_argument(
            "--settings",
            help=(
                "The Python path to a settings module, e.g. "
                '"myproject.settings.main". If this isn\'t provided, the '
                "DJANGO_SETTINGS_MODULE environment variable will be used."
            ),
        )
        parser.add_argument(
            "--pythonpath",
            help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".',
        )
        parser.add_argument(
            "--traceback", action="store_true", help="Raise on CommandError exceptions"
        )
        parser.add_argument(
            "--no-color", action="store_true", help="Don't colorize the command output."
        )
        parser.add_argument(
            "--force-color",
            action="store_true",
            help="Force colorization of the command output.",
        )

        # Add arguments that are shared by all GMN commands.
        parser.add_argument("--debug", action="store_true", help="Debug level logging")

        self.add_components(parser)

        group = parser.add_argument_group(self.command_name)
        self.add_arguments(group)

        return parser

    def add_components(self, parser):
        """Override to add components that the command will use.

        Command line options are automatically added to allow adjusting parameters
        for the components, after which the components are automatically created and
        available for use. Currently supported:

        - self.using_d1_client(parser):
            - Traditional DataONE Client.

        - self.using_async_d1_client(parser):
            - Async DataONE Client.

        - using_async_object_list_iter(parser, list_objects_arg_dict):
            - Async ObjectList Iterator.

        - using_async_event_log_iter(parser, list_objects_arg_dict):
            - Async EventLog Iterator.

        - self.using_force_for_production(parser):
            - Require that user pass --force if running in production mode.

        - self.using_pid_path(parser):
            - Give user option to load a list of PIDs from a file.
            - If used, PIDs are in self.pid_file_set

        - self.using_single_instance(parser):
            - Allow only a single instance of the command to run at a time.
        """
        pass

    def add_arguments(self, parser):
        """Override to add command line arguments that are specific to this command."""
        pass

    # Setup and call handle for serial or async command

    def handle(self, *args, **opt_dict):
        """Do not override in the main module.
        """
        # args is a copy of positional args to mimic the old optparse module. This module
        # just ignores it, and Django should just drop it in a major release.
        self.opt_dict = opt_dict
        self._assert_force_arg()
        self._create_d1_client()
        self._create_async_d1_client()
        self._create_async_object_list_iter()
        self._create_async_event_log_iter()
        self._load_pid_file()

        # if self.opt_dict["debug"]:
        #     logging.disable(logging.NOTSET)
        # else:
        #     logging.disable(logging.DEBUG)

        try:
            return self._call_serial()
        except NotHandledError:
            pass
        try:
            return self._call_async()
        except NotHandledError:
            pass
        raise django.core.management.base.CommandError(
            "Command must supply handle_serial() or handle_async()"
        )

    def _call_serial(self):
        self.handle_serial()

    def handle_serial(self):
        """Override for all commands that do not use async IO."""
        raise NotHandledError

    def _call_async(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._async_interface())
        finally:
            loop.close()

    async def _async_interface(self):
        """Transition point where the command starts running in async (event loop)
        mode."""
        try:
            return await self.handle_async()
        except Exception as e:
            self.log.exception("GMN command failed with exception")
            raise django.core.management.base.CommandError(str(e))
        finally:
            if self.async_d1_client:
                await self.async_d1_client.close()

    async def handle_async(self):
        """Override for all commands that use async IO.

        Enables access to the Async DataONE Client and other async components.
        """
        raise NotHandledError

    # Clients

    # Automatically add command line options for DataONE clients and iterators required
    # by the command, and flag them for later automatic creation.

    def using_d1_client(self, parser, **arg_parser_dict):
        """Prepare the traditional DataONE Client for use.
        """
        if self.d1_client_arg_parser is None:
            self.log.debug("Using traditional DataONE Client")
            self.d1_client_arg_parser = d1_client.command_line.D1ClientArgParser(
                argument_parser=parser, **arg_parser_dict
            )
        parser.add_argument(
            "--public",
            action="store_true",
            help=(
                "Make outgoing connections only as the public user. Normally, "
                "outgoing connections will be made using the client side certificate, "
                "if available."
            ),
        )

    def using_async_d1_client(self, parser, **arg_parser_dict):
        """Prepare the Async DataONE Client for use.

        Adds command line arguments for controlling the client and flags the client for
        automatic creation after the command line has been parsed.

        """
        if self.async_d1_client_arg_parser is None:
            self.log.debug("Using Async DataONE Client")
            self.async_d1_client_arg_parser = d1_client.aio.command_line.AsyncArgParser(
                argument_parser=parser, **arg_parser_dict
            )
            parser.add_argument(
                "--public",
                action="store_true",
                help=(
                    "Make outgoing connections only as the public user. Normally, "
                    "outgoing connections will be made using the client side certificate, "
                    "if available."
                ),
            )

    def using_async_object_list_iter(self, parser, **list_objects_arg_dict):
        """Prepare the Async ObjectList Iterator for use.

        Also prepare the AsyncDataONEClient if it has not been prepared yet, as it's
        required by the iterator.

        Adds command line arguments for controlling the client and flags the client for
        automatic creation after the command line has been parsed.
        """
        self.using_async_d1_client(parser)
        if self.async_object_list_iter_arg_parser is None:
            self.log.debug("Using Async ObjectList Iterator")
            self.async_object_list_iter_arg_parser = d1_client.aio.iter.objectlist_cmd.AsyncArgParser(
                argument_parser=parser,
                fixed_list_objects_arg_dict=list_objects_arg_dict,
            )

    def using_async_event_log_iter(self, parser, **list_objects_arg_dict):
        """Prepare the Async EventLog Iterator for use.

        Also prepare the AsyncDataONEClient if it has not been prepared yet, as it's
        required by the iterator.

        Adds command line arguments for controlling the client and flags the client for
        automatic creation after the command line has been parsed.
        """
        self.using_async_d1_client(parser)
        if self.async_event_log_iter_arg_parser is None:
            self.log.debug("Using Async ObjectList Iterator")
            self.async_event_log_iter_arg_parser = d1_client.aio.iter.eventlog_cmd.AsyncArgParser(
                argument_parser=parser, fixed_log_records_arg_dict=list_objects_arg_dict
            )

    def using_force_for_production(self, parser):
        """Requre that user pass a --force argument if GMN appears to be running in a
        production environment.
        """
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force command to run even if GMN appears to be running in a production environment",
        )

    def using_pid_file(self, parser):
        """Add a --pid-path switch that can be used for specifying a file containing a
        list of PIDs to load. If thefile is provided, the PIDs are available in
        self.pid_set.
        """
        parser.add_argument(
            "--pid-path",
            action="store",
            help="Provide a file containing a list of PIDs to process. The file "
            "must be UTF-8 encoded and contain one PID per line",
        )

    def using_single_instance(self, _parser):
        """Add a requirement that only a single instance of this GMN command runs at a
        time. If another instance is already running, the command will exit with an
        error message indicating the reason.
        """
        single_path = os.path.join(tempfile.gettempdir(), self.command_name + ".single")
        self.single_instance_lock_file = open(single_path, "w")
        try:
            fcntl.lockf(self.single_instance_lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise django.core.management.base.CommandError(
                f"Aborted: Another instance of {self.command_name} is still running"
            )

    # Automatically create clients that have been flagged for use using parameters that
    # the user had the option of overriding on the command line, or were fixed to
    # specific values by the GMN command.

    # Private

    def _assert_force_arg(self):
        """If the --force argument has been required for GMN running in production,
        assert that it was passed on the command line.
        """
        if (
            "force" in self.opt_dict
            and self.is_in_production()
            and not self.opt_dict["force"]
        ):
            raise django.core.management.base.CommandError(
                "This GMN instance appears to be running in DataONE's production environment. "
                "This command ({}) is not intended to be used on a GMN instance in production "
                "as it may change or delete data that is immutable in production. "
                "To force the command to run anyway, use the --force command line switch.".format(
                    self.command_name
                )
            )

    def _create_d1_client(self):
        if self.d1_client_arg_parser is not None and self.d1_client is not None:
            self.log.debug("Creating regular DataONEClient")
            client_opt_dict = self.d1_client_arg_parser.get_method_args(self.opt_dict)
            self._set_client_cert_options(client_opt_dict)
            self.d1_client = d1_client.d1client.get_client_class(
                self.opt_dict["major"]
            )(**client_opt_dict)

    def _create_async_d1_client(self):
        if self.async_d1_client_arg_parser is not None and self.async_d1_client is None:
            self.log.debug("Creating AsyncDataONEClient")
            client_opt_dict = self.async_d1_client_arg_parser.get_method_args(
                self.opt_dict
            )
            self._set_client_cert_options(client_opt_dict)
            self.async_d1_client = d1_client.aio.async_client.AsyncDataONEClient(
                **client_opt_dict
            )

    def _set_client_cert_options(self, client_opt_dict):
        # Any cert paths set on the command line take precedence
        if client_opt_dict.get("cert_pem_path", None) or client_opt_dict.get(
            "cert_key_path", None
        ):
            pass
        # Else if --public was set, certs are not set
        elif self.opt_dict.get("public", False):
            pass
        # Else fall back to using GMN's client side cert.
        else:
            if os.path.exists(django.conf.settings.CLIENT_CERT_PATH):
                client_opt_dict["cert_pem_path"] = django.conf.settings.CLIENT_CERT_PATH
            if os.path.exists(django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH):
                client_opt_dict[
                    "cert_key_path"
                ] = django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH

    def _create_async_object_list_iter(self):
        if (
            self.async_object_list_iter_arg_parser is not None
            and self.async_object_list_iter is None
        ):
            self.log.debug("Creating AsyncObjectListIterator")
            # The async obj iterator requires the async_d1_client.
            assert self.async_d1_client_arg_parser
            self._create_async_d1_client()
            if self.async_object_list_iter is None:
                self.async_object_list_iter = d1_client.aio.iter.objectlist_async.ObjectListIteratorAsync(
                    async_client=self.async_d1_client
                )

    def _create_async_event_log_iter(self):
        if (
            self.async_event_log_iter_arg_parser is not None
            and self.async_event_log_iter is None
        ):
            self.log.debug("Creating AsyncObjectListIterator")
            # The async obj iterator requires the async_d1_client.
            assert self.async_d1_client_arg_parser
            self._create_async_d1_client()
            if self.async_event_log_iter is None:
                self.async_event_log_iter = d1_client.aio.iter.eventlog_async.EventLogIteratorAsync(
                    async_client=self.async_d1_client
                )

    def _load_pid_file(self):
        """If the --pid-path argument was provided and has been set, load a set of
        strings from a UTF-8 encoded file.

        - The file must contain one string, such as a PID or a subject, on each line.
        - Blank lines or lines with only whitespace are ignored.
        - Any duplicated strings in the file are returned as one string.
        - In >Py3.7, the set insertion order is preserved on iteration.
        """
        pid_path = self.opt_dict.get("pid_path", None)
        if pid_path:
            try:
                with open(pid_path, encoding="utf-8") as f:
                    self.pid_set = {st for st in [s.strip() for s in f] if st != ""}
            except EnvironmentError as e:
                raise self.CommandError(
                    'Unable to load list from file. error="{}"'.format(str(e))
                )

    # Async tasks

    async def add_task(self, task_func):
        if len(self.task_set) >= self.opt_dict["max_concurrent"]:
            await self.await_task()
        self.task_set.add(task_func)

    async def await_task(self):
        task_set = self.task_set.copy()
        self.task_set.clear()
        result_set, new_task_set = await asyncio.wait(
            task_set, return_when=asyncio.FIRST_COMPLETED
        )
        self.task_set.update(new_task_set)
        # Exceptions from awaited tasks trigger here.
        try:
            result_set.pop().result()
        except Exception:
            self.tracker.event("Continued after error. Check log")
            self.log.exception("Import failed with error:")
            raise
        self.tracker.progress()

    async def await_all(self):
        while self.task_set:
            await self.await_task()

    # Utilities

    def abort_if_not_debug_mode(self):
        if not django.conf.settings.DEBUG_GMN:
            raise django.core.management.base.CommandError(
                "This command is only available when DEBUG_GMN is True in "
                "settings.py"
            )

    def is_db_empty(self):
        return not d1_gmn.app.models.IdNamespace.objects.exists()

    def assert_path_is_dir(self, dir_path):
        if not os.path.isdir(dir_path):
            raise django.core.management.base.CommandError(
                'Invalid dir path. path="{}"'.format(dir_path)
            )

    def find_api_major(self, base_url, client_arg_dict):
        return d1_client.d1client.get_api_major_by_base_url(base_url, **client_arg_dict)

    def is_in_production(self):
        """Return True if GMN appears to be active in DataONE's production environment.
        """
        return (
            django.conf.settings.DATAONE_ROOT == d1_common.const.URL_DATAONE_ROOT
            and not django.conf.settings.STAND_ALONE
        )

    # Cert

    def extract_subj_from_cert_pem(self, cert_pem_path):
        try:
            return d1_gmn.app.middleware.session_cert.get_authenticated_subjects(
                cert_pem_path
            )[0]
        except ValueError as e:
            raise self.CommandError(
                'Unable to extract subject from certificate. error="{}"'.format(str(e))
            )

    def read_pem_cert(self, cert_pem_path):
        return self.load_utf8_to_str(cert_pem_path)

    # Whitelist

    def get_whitelist_list(self):
        return sorted(self.get_whitelist_set())

    def get_whitelist_set(self):
        return {
            s.subject.subject
            for s in d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.all()
        }

    def is_subject_in_whitelist(self, subject_str):
        return subject_str in self.get_whitelist_set()

    def add_subj_to_whitelist(self, subj_str):
        if self.is_subject_in_whitelist(subj_str):
            raise self.CommandError("Subject already in whitelist: {}".format(subj_str))
        d1_gmn.app.models.whitelist_for_create_update_delete(subj_str)
        self.log.info("Added subject to whitelist: {}".format(subj_str))

    def log_and_remove_subj_from_whitelist(self, subj_str):
        if not self.is_subject_in_whitelist(subj_str):
            raise self.CommandError("Subject is not in whitelist: {}".format(subj_str))
        d1_gmn.app.models.WhitelistForCreateUpdateDelete.objects.filter(
            subject=d1_gmn.app.models.subject(subj_str)
        ).delete()
        self.log.info("Removed subject to whitelist: {}".format(subj_str))

    # JWT

    def load_jwt_file(self, jwt_path):
        return self.load_binary_to_bytes(jwt_path)

    def get_jwt_subject(self, jwt_str_or_path):
        try:
            return d1_common.cert.jwt.get_subject_without_validation(
                self.get_jwt_bytes(jwt_str_or_path)
            )
        except (d1_common.cert.jwt.JwtException, UnicodeDecodeError) as e:
            raise self.CommandError(
                'Unable to extract subject from JWT. error="{}"'.format(str(e))
            )

    def get_jwt_bytes(self, jwt):
        try:
            with open(jwt, "r", encoding="ascii") as f:
                jwt_bytes = f.read().strip().encode("ascii")
        except UnicodeDecodeError as e:
            raise self.CommandError(
                'JWT file must be Base64 encoded. error="{}". path="{}"'.format(
                    str(e), jwt
                )
            )
        except EnvironmentError:
            self.log.debug("JWT passed directly as command line argument")
            try:
                return jwt.encode("ascii")
            except UnicodeDecodeError as e:
                raise self.CommandError(
                    'JWT command line argument must be Base64 encoded. error="{}"'.format(
                        str(e)
                    )
                )
        else:
            self.log.debug('JWT loaded from file. path="{}"'.format(jwt))
            return jwt_bytes

    # Files

    def load_binary_to_bytes(self, binary_path):
        try:
            with open(binary_path, "rb") as f:
                return f.read()
        except EnvironmentError as e:
            raise django.core.management.base.CommandError(
                'Unable to load binary file. error="{}"'.format(str(e))
            )

    def load_utf8_to_str(self, utf8_path):
        try:
            with open(utf8_path, "r") as f:
                return f.read()
        except EnvironmentError as e:
            raise django.core.management.base.CommandError(
                'Unable to load UTF-8 file. error="{}"'.format(str(e))
            )

    # Database

    def query_sciobj_with_pid_filter(self):
        """Generator returning sciobj_model objects.

        If `using_pid_file()` and user provided a valid path to a list of PIDs, the
        returned list is filtered to include only objects that are both in the database
        and in the PID list.
        """
        return d1_gmn.app.model_util.query_sciobj(
            {"pid__did__in": self.pid_set} if self.pid_set else None
        )

    def query_sciobj_count(self):
        """Generator returning sciobj_model objects.

        Get count of sciobj_model that will be returned by
        `query_sciobj_with_pid_filter()`.
        """
        return self.query_sciobj_with_pid_filter().count()

    # Testing

    def create_test_subj(self):
        # for subj_model in d1_gmn.app.models.Subject.objects.filter():
        #     subj_model.subject = re.sub(
        #         "(uid).*?,",
        #         f"uid={d1_test.instance_generator.random_data.random_lower_ascii(fixed_len=6)}",
        #         subj_model.subject,
        #     )
        #     subj_model.save()
        #
        # rnd_set = set(
        #     re.sub(
        #         "(uid).*?,",
        #         f"uid={d1_test.instance_generator.random_data.random_lower_ascii(fixed_len=6)}",
        #         s,
        #     )
        #     for s in rnd_set
        # )
        all_existing_subj_list = [
            o.subject for o in d1_gmn.app.models.Subject.objects.all()
        ]
        rnd_set = set(random.sample(all_existing_subj_list, 3))
        rnd_set |= {"unknown_subj_1", "unknown_subj_2"}
        primary_str = random.choice(all_existing_subj_list)
        return primary_str, rnd_set

    # Private

    def _strip_rst_markup(self, doc_rst):
        """The docstring (__doc__) of the main module for GMN commands doubles as text
        for the --help command and as docs for the command in the online GMN docs. Help
        needs plain text while the docstrings use basic reST markup. So the markup we
        use is stripped out here.

        """
        doc_list = [self.command_name, "-" * len(self.command_name), ""]
        doc_rst = re.sub(r"`_|``|`|::|\n\s*\.\. .*", "", doc_rst)
        # Strip out whitespace created by the first regex.
        doc_rst = re.sub(r"\n\s*\n", "\n\n", doc_rst)
        doc_rst = re.sub(r":doc:[^\s]*", "the online documentation", doc_rst)
        doc_rst = re.sub(r"^", "XXXXXXXXXXXXXXXXXXXXXXXXXXX", doc_rst, re.MULTILINE)
        # import textwrap
        # textwrap.dedent()
        return "\n".join(doc_list) + "\n" + (doc_rst or "")


class GMNHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Django tried to improve the default help text formatting in argparse but they
    broke it instead. This fixes things.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    option_order = {
        v: i
        for i, v in enumerate(
            (
                ("-h", "--help"),
                ("-v", "--verbosity"),
                ("--traceback",),
                ("--pythonpath",),
                ("--settings",),
                ("--no-color",),
                ("--force-color",),
                ("--debug",),
                ("--pid-path",),
            )
        )
    }

    @classmethod
    def factory(cls, is_help_):
        """Create a class that has an added is_help member which selects if usage
        information should be included when argparse later calls the overridden
        methods."""

        class ClassWithHelpFlag(cls):
            is_help = is_help_

        return ClassWithHelpFlag

    def _reorder_actions(self, actions):
        return sorted(
            actions,
            key=lambda v: (
                self.option_order.get(tuple(v.option_strings), 100),
                v.option_strings,
            ),
        )

    def add_usage(self, usage, actions, *args, **kwargs):
        """Suppress the usage information when the full help text is being displayed."""
        # noinspection PyUnresolvedReferences
        if not self.is_help:
            super().add_usage(usage, self._reorder_actions(actions), *args, **kwargs)

    def add_arguments(self, actions):
        super().add_arguments(self._reorder_actions(actions))


class NotHandledError(Exception):
    pass


# # noinspection PyAttributeOutsideInit
# class Db(object):
#     def __init__(self):
#         pass
#
#     def connect(self, dsn):
#         """Connect to DB.
#
#         dbname: the database name user: user name used to authenticate password:
#         password used to authenticate host: database host address (defaults to UNIX
#         socket if not provided) port: connection port number (defaults to 5432 if not
#         provided)
#
#         """
#         self.con = psycopg2.connect(dsn)
#         self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         # autocommit: Disable automatic transactions
#         self.con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
#
#     def close(self):
#         self.cur.close()
#
#     # noinspection PyUnresolvedReferences
#     def run(self, sql_str, *args, **kwargs):
#         try:
#             self.cur.execute(sql_str, args, **kwargs)
#         except psycopg2.DatabaseError as e:
#             logging.debug("SQL query result: {}".format(str(e)))
#             raise
#         try:
#             return self.cur.fetchall()
#         except psycopg2.DatabaseError:
#             return None
