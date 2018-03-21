#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
"""
- Generic boiler plate for Python CLI apps.
- Simple command tokenizing and validation.
"""

import cmd
import platform
import shlex
import sys

import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.command_processor as command_processor
import d1_cli.impl.session as session


class CLI(cmd.Cmd):
  def __init__(self):
    self._command_processor = command_processor.CommandProcessor()
    cmd.Cmd.__init__(self)
    self.prefix = ''
    self.prompt = '> '
    #self.intro = u'DataONE Command Line Interface'
    self.keep_looping = False
    self.interactive = False

  #-----------------------------------------------------------------------------
  # Command processing.
  #-----------------------------------------------------------------------------

  # Override methods in Cmd object.
  def preloop(self):
    """Initialization before prompting user for commands.
    Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
    """
    # Set up command completion.
    cmd.Cmd.preloop(self)
    self._history = []

  def postloop(self):
    """Take care of any unfinished business.
    Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    """
    cmd.Cmd.postloop(self) # Clean up command completion
    cli_util.print_info('Exiting...')

  def precmd(self, line):
    """This method is called after the line has been input but before
    it has been interpreted. If you want to modify the input line
    before execution (for example, variable substitution) do it here.
    """
    line = self.prefix + line
    self._history += [line.strip()]
    return line

  def postcmd(self, stop, line):
    """If you want to stop the console, return something that evaluates to true.
    If you want to do some post command processing, do it here.
    """
    return stop

  def emptyline(self):
    """Do nothing on empty input line"""
    pass

  def default(self, line):
    """Called on an input line when the command prefix is not recognized.
    """
    args = self._split_args(line, 0, 99)
    cli_util.print_error('Unknown command: {}'.format(args[0]))

  def run_command_line_arguments(self, cmd_line_list):
    for cmd_line_str in cmd_line_list:
      self.onecmd(cmd_line_str)

  #-----------------------------------------------------------------------------
  # CLI
  #-----------------------------------------------------------------------------

  def do_help(self, line):
    """Get help on commands
    "help" or "?" with no arguments displays a list_objects of commands for which help is available
    "help <command>" or "? <command>" gives help on <command>
    """
    command, = self._split_args(line, 0, 1)
    if command is None:
      return self._print_help()
    cmd.Cmd.do_help(self, line)

  def do_history(self, line):
    """history
    Display a list of commands that have been entered
    """
    self._split_args(line, 0, 0)
    for idx, item in enumerate(self._history):
      cli_util.print_info('{0: 3d} {1}'.format(idx, item))

  def do_exit(self, line):
    """exit
    Exit from the CLI
    """
    n_remaining_operations = len(self._command_processor.get_operation_queue())
    if n_remaining_operations:
      cli_util.print_warn(
        """There are {} unperformed operations in the write operation queue. These will
be lost if you exit.""".format(n_remaining_operations)
      )
      if not cli_util.confirm('Exit?', default='yes'):
        return
    sys.exit()

  def do_quit(self, line):
    """quit
    Exit from the CLI
    """
    self.do_exit(line)

  def do_eof(self, line):
    """Exit on system EOF character"""
    cli_util.print_info('')
    self.do_exit(line)

  #-----------------------------------------------------------------------------
  # Session, General
  #-----------------------------------------------------------------------------

  def do_set(self, line):
    """set [parameter [value]]
    set (without parameters): Display the value of all session variables.
    set <session variable>: Display the value of a single session variable.
    set <session variable> <value>: Set the value of a session variable.
    """
    session_parameter, value = self._split_args(line, 0, 2)
    if value is None:
      self._command_processor.get_session().print_variable(session_parameter)
    else:
      self._command_processor.get_session().set_with_conversion(
        session_parameter, value
      )
      self._print_info_if_verbose(
        'Set session variable {} to "{}"'.format(session_parameter, value)
      )

  def do_load(self, line):
    """load [file]
    Load session variables from file
    load (without parameters): Load session from default file ~/.dataone_cli.conf
    load <file>: Load session from specified file
    """
    config_file = self._split_args(line, 0, 1)[0]
    self._command_processor.get_session().load(config_file)
    if config_file is None:
      config_file = self._command_processor.get_session(
      ).get_default_pickle_file_path()
    self._print_info_if_verbose(
      'Loaded session from file: {}'.format(config_file)
    )

  def do_save(self, line):
    """save [config_file]
    Save session variables to file
    save (without parameters): Save session to default file ~/.dataone_cli.conf
    save <file>: Save session to specified file
    """
    config_file = self._split_args(line, 0, 1)[0]
    self._command_processor.get_session().save(config_file)
    if config_file is None:
      config_file = self._command_processor.get_session(
      ).get_default_pickle_file_path()
    self._print_info_if_verbose('Saved session to file: {}'.format(config_file))

  def do_reset(self, line):
    """reset
    Set all session variables to their default values
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_session().reset()
    self._print_info_if_verbose('Successfully reset session variables')

  #-----------------------------------------------------------------------------
  # Session, Access Control
  #-----------------------------------------------------------------------------

  def do_allowaccess(self, line):
    """allowaccess <subject> [access-level]
    Set the access level for subject
    Access level is "read", "write" or "changePermission".
    Access level defaults to "read" if not specified.
    Special subjects:
      public: Any subject, authenticated and not authenticated
      authenticatedUser: Any subject that has authenticated with CILogon
      verifiedUser: Any subject that has authenticated with CILogon and has been verified by DataONE
    """
    subject, permission = self._split_args(line, 1, 1)
    self._command_processor.get_session().get_access_control().add_allowed_subject(
      subject, permission
    )
    self._print_info_if_verbose(
      'Set {} access for subject "{}"'.format(permission, subject)
    )

  def do_denyaccess(self, line):
    """denyaccess <subject>
    Remove subject from access policy
    """
    subject, = self._split_args(line, 1, 0)
    self._command_processor.get_session().get_access_control(
    ).remove_allowed_subject(subject)
    self._print_info_if_verbose(
      'Removed subject "{}" from access policy'.format(subject)
    )

  def do_clearaccess(self, line):
    """clearaccess
    Remove all subjects from access policy
    Only the submitter will have access to the object.
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_session().get_access_control().clear()
    self._print_info_if_verbose('Removed all subjects from access policy')

  #-----------------------------------------------------------------------------
  # Session, Replication Policy
  #-----------------------------------------------------------------------------

  def do_allowrep(self, line):
    """allowrep
    Allow new objects to be replicated
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_session().get_replication_policy(
    ).set_replication_allowed(True)
    self._print_info_if_verbose('Set replication policy to allow replication')

  def do_denyrep(self, line):
    """denyrep
    Prevent new objects from being replicated
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_session().get_replication_policy(
    ).set_replication_allowed(False)
    self._print_info_if_verbose('Set replication policy to deny replication')

  def do_preferrep(self, line):
    """preferrep <member node> [member node ...]
    Add one or more preferred Member Nodes to replication policy
    """
    mns = self._split_args(line, 1, -1)
    self._command_processor.get_session().get_replication_policy(
    ).add_preferred(mns)
    self._print_info_if_verbose(
      'Set {} as preferred replication target(s)'.format(', '.join(mns))
    )

  def do_blockrep(self, line):
    """blockrep <member node> [member node ...]
    Add one or more blocked Member Node to replication policy
    """
    mns = self._split_args(line, 1, -1)
    self._command_processor.get_session().get_replication_policy(
    ).add_blocked(mns)
    self._print_info_if_verbose(
      'Set {} as blocked replication target(s)'.format(', '.join(mns))
    )

  def do_removerep(self, line):
    """removerep <member node> [member node ...]
    Remove one or more Member Nodes from replication policy
    """
    mns = self._split_args(line, 1, -1)
    self._command_processor.get_session().get_replication_policy(
    ).repremove(mns)
    self._print_info_if_verbose(
      'Removed {} from replication policy'.format(', '.join(mns))
    )

  def do_numberrep(self, line):
    """numberrep <number of replicas>
    Set preferred number of replicas for new objects
    If the preferred number of replicas is set to zero, replication is also disallowed.
    """
    n_replicas = self._split_args(line, 1, 0)[0]
    self._command_processor.get_session().get_replication_policy(
    ).set_number_of_replicas(n_replicas)
    self._print_info_if_verbose(
      'Set number of replicas to {}'.format(n_replicas)
    )

  def do_clearrep(self, line):
    """clearrep
    Set the replication policy to default

    The default replication policy has no preferred or blocked member nodes, allows
    replication and sets the preferred number of replicas to 3.
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_session().get_replication_policy().clear()
    self._print_info_if_verbose('Cleared the replication policy')

  #-----------------------------------------------------------------------------
  # Read Operations
  #-----------------------------------------------------------------------------

  def do_get(self, line):
    """get <identifier> <file>
    Get an object from a Member Node

    The object is saved to <file>.
    """
    pid, output_file = self._split_args(line, 2, 0)
    self._command_processor.science_object_get(pid, output_file)
    self._print_info_if_verbose(
      'Downloaded "{}" to file: {}'.format(pid, output_file)
    )

  def do_meta(self, line):
    """meta <identifier> [file]
    Get the System Metadata that is associated with a Science Object

    If the metadata is not on the Coordinating Node, the Member Node is checked.

    Provide ``file`` to save the System Metada to disk instead of displaying it.
    """
    pid, output_file = self._split_args(line, 1, 1)
    self._command_processor.system_metadata_get(pid, output_file)
    if output_file is not None:
      self._print_info_if_verbose(
        'Downloaded system metadata for "{}" to file: {}'.
        format(pid, output_file)
      )

  def do_list(self, line):
    """list [path]
    Retrieve a list of available Science Data Objects from Member Node
    The response is filtered by the from-date, to-date, search, start and count
    session variables.

    See also: search
    """
    path = self._split_args(line, 0, 1, pad=False)
    if len(path):
      path = path[0]
    self._command_processor.list_objects(path)

  def do_log(self, line):
    """log [path]
    Retrieve event log from Member Node
    The response is filtered by the from-date, to-date, start and count session
    parameters.
    """
    path = self._split_args(line, 0, 1, pad=False)
    if len(path):
      path = path[0]
    self._command_processor.log(path)

  def do_resolve(self, line):
    """resolve <identifier>
    Find all locations from which the given Science Object can be downloaded
    """
    pid, = self._split_args(line, 1, 0)
    self._command_processor.resolve(pid)

  #-----------------------------------------------------------------------------
  # Write Operations
  #-----------------------------------------------------------------------------

  def do_create(self, line):
    """create <identifier> <file>
    Create a new Science Object on a Member Node

    The System Metadata that becomes associated with the new Science Object is
    generated from the session variables.
    """
    pid, sciobj_path = self._split_args(line, 2, 0)
    self._command_processor.science_object_create(pid, sciobj_path)
    self._print_info_if_verbose(
      'Added create operation for identifier "{}" to write queue'.format(pid)
    )

  def do_update(self, line):
    """update <old-pid> <new-pid> <file>
    Replace an existing Science Object in a :term:`MN` with another
    """
    curr_pid, pid_new, input_file = self._split_args(line, 3, 0)
    self._command_processor.science_object_update(curr_pid, input_file, pid_new)
    self._print_info_if_verbose(
      'Added update operation for identifier "{}" to write queue'.
      format(curr_pid)
    )

  def do_package(self, line):
    """package <package-pid> <science-metadata-pid> <science-pid> [science-pid ...]
    Create a simple OAI-ORE Resource Map on a Member Node
    """
    pids = self._split_args(line, 3, -1, pad=False)
    self._command_processor.create_package(pids)
    self._print_info_if_verbose(
      'Added package create operation for identifier "{}" to write queue'.
      format(pids[0])
    )

  def do_archive(self, line):
    """archive <identifier> [identifier ...]
    Mark one or more existing Science Objects as archived
    """
    pids = self._split_args(line, 1, -1)
    self._command_processor.science_object_archive(pids)
    self._print_info_if_verbose(
      'Added archive operation for identifier(s) {} to write queue'.
      format(', '.join(pids))
    )

  def do_updateaccess(self, line):
    """updateaccess <identifier> [identifier ...]
    Update the Access Policy on one or more existing Science Data Objects
    """
    pids = self._split_args(line, 1, -1)
    self._command_processor.update_access_policy(pids)
    self._print_info_if_verbose(
      'Added access policy update operation for identifiers {} to write queue'.
      format(', '.join(pids))
    )

  def do_updatereplication(self, line):
    """updatereplication <identifier> [identifier ...]
    Update the Replication Policy on one or more existing Science Data Objects
    """
    pids = self._split_args(line, 1, -1)
    self._command_processor.update_replication_policy(pids)
    self._print_info_if_verbose(
      'Added replication policy update operation for identifiers {} to write queue'.
      format(', '.join(pids))
    )

  #-----------------------------------------------------------------------------
  # Utilities
  #-----------------------------------------------------------------------------

  def do_listformats(self, line):
    """listformats
    Display all known Object Format IDs
    """
    self._split_args(line, 0, 0)
    self._command_processor.list_format_ids()

  def do_listnodes(self, line):
    """listnodes
    Display all known DataONE Nodes
    """
    self._split_args(line, 0, 0)
    self._command_processor.list_nodes()

  def do_search(self, line):
    """search [query]
    Comprehensive search for Science Data Objects across all available MNs

    See https://releases.dataone.org/online/api-documentation-v2.0.1/design/SearchMetadata.html
    for the available search terms.
    """
    args = self._split_args(line, 0, -1)
    query = ' '.join([_f for _f in args if _f])
    self._command_processor.search(query)

  def do_ping(self, line):
    """ping [base-url ...]
    Check if a server responds to the DataONE ping() API method
    ping (no arguments): Ping the CN and MN that is specified in the session
    ping <base-url> [base-url ...]: Ping each CN or MN

    If an incomplete base-url is provided, default CN and MN base URLs at the
    given url are pinged.
    """
    hosts = self._split_args(line, 0, 99, pad=False)
    self._command_processor.ping(hosts)

  #-----------------------------------------------------------------------------
  # Write Operation Queue
  #-----------------------------------------------------------------------------

  def do_queue(self, line):
    """queue
    Print the queue of write operations
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_operation_queue().display()

  def do_run(self, line):
    """run
    Perform each operation in the queue of write operations
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_operation_queue().execute()
    self._print_info_if_verbose(
      'All operations in the write queue were successfully executed'
    )

  def do_edit(self, line):
    """edit
    Edit the queue of write operations
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_operation_queue().edit()
    self._print_info_if_verbose(
      'The write operation queue was successfully edited'
    )

  def do_clearqueue(self, line):
    """clearqueue
    Remove the operations in the queue of write operations without performing them
    """
    self._split_args(line, 0, 0)
    self._command_processor.get_operation_queue().clear()
    self._print_info_if_verbose(
      'All operations in the write queue were cleared'
    )

  #
  # Private.
  #

  def _split_args(self, line, n_required, n_optional, pad=True):
    # args = [a.decode('utf-8') for a in shlex.split(line.encode('utf-8'))]
    args = shlex.split(line)
    n_optional_max = 1000 if n_optional == -1 else n_optional
    if len(args) < n_required or len(args) > n_required + n_optional_max:
      msg = self._text_description_of_required_and_optional(
        n_required, n_optional
      )
      raise cli_exceptions.InvalidArguments(msg)
    if pad:
      # Pad the list_objects out with None for any optional parameters that were
      # not provided.
      args += [None] * (n_required + n_optional - len(args))
    #if len(args) == 1:
    #  return args[0]
    return args

  def _text_description_of_required_and_optional(self, n_required, n_optional):
    if n_required == 0:
      if n_optional == 0:
        req = 'no parameters'
      else:
        req = 'no required parameters'
    elif n_required == 1:
      req = 'one required parameter'
    else:
      req = '{} required parameters'.format(n_required)
    if n_optional == 0:
      opt = ''
    elif n_optional == 1:
      opt = ' and one optional parameter'
    elif n_optional < 0:
      opt = ' and an unlimited number of optional parameters'
    else:
      opt = ' and {} optional parameters'.format(n_optional)
    return 'Command takes {}'.format(req + opt)

  def _print_info_if_verbose(self, msg):
    if self._command_processor.get_session().get(session.VERBOSE_NAME):
      cli_util.print_info(msg)

  def _print_help(self):
    """Custom help message to group commands by functionality"""
    msg = """Commands (type help <command> for details)

CLI:                     help history exit quit
Session, General:        set load save reset
Session, Access Control: allowaccess denyaccess clearaccess
Session, Replication:    allowrep denyrep preferrep blockrep
                         removerep numberrep clearrep
Read Operations:         get meta list log resolve
Write Operations:        update create package archive
                         updateaccess updatereplication
Utilities:               listformats listnodes search ping
Write Operation Queue:   queue run edit clearqueue

Command History:         Arrow Up, Arrow Down
Command Editing:         Arrow Left, Arrow Right, Delete
"""
    if platform.system() != 'Windows':
      msg += """Command Completion:      Single Tab: Complete unique command
                         Double Tab: Display possible commands
"""
    cli_util.print_info(msg)
