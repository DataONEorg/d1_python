#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`dataone`
==============

:Synopsis:
  DataONE Command Line Client
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import ast
import cmd
import csv
import datetime
import dateutil
import glob
import hashlib
import httplib
import json
import logging
import optparse
import os
import pprint
import random
import re
import readline
import shlex
import shutil
import stat
import StringIO
import sys
import time
import unittest
import urllib
import urlparse
import uuid
import xml.dom.minidom

# 3rd party.
import pyxb

# App.
import cli_exceptions
import session

# If this was checked out as part of the MN service, the libraries can be found here.
sys.path.append(
  os.path.abspath(
    os.path.join(
      os.path.dirname(
        __file__
      ), '../../../mn_service/mn_prototype/'
    )
  )
)

# MN API.
try:
  import d1_common.mime_multipart
  import d1_common.types.exceptions
  import d1_common.types.generated.dataoneTypes as dataoneTypes
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.mnclient
  import d1_client.cnclient
  import d1_client.systemmetadata
  import d1_client.objectlistiterator
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

try:
  import iso8601
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write(
    '     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n'
  )
  raise


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)

#===============================================================================


class CLIClient(d1_client.mnclient.MemberNodeClient):
  def __init__(self, session, base_url):
    try:
      self.session = session
      self.base_url = base_url
      return super(CLIClient, self).__init__(
        self.base_url,
        certfile=self._get_certificate(),
        keyfile=self._get_certificate_private_key()
      )
    except d1_common.types.exceptions.DataONEException as e:
      err_msg = []
      err_msg.append('Unable to connect to: {0}'.format(node_base_url))
      err_msg.append('{0}'.format(str(e)))
      raise cli_exceptions.CLIError('\n'.join(err_msg))

  def _get_cilogon_certificate_path(self):
    return '/tmp/x509up_u{0}'.format(os.getuid())

  def _assert_certificate_present(self, path):
    if not os.path.exists(path):
      raise cli_exceptions.CLIError('Certificate not found')

  def _get_certificate(self):
    if self.session.get('auth', 'anonymous'):
      return None
    cert_path = self.session.get('auth', 'cert_path')
    if not cert_path:
      cert_path = self._get_cilogon_certificate_path()
    self._assert_certificate_present(cert_path)
    return cert_path

  def _get_certificate_private_key(self):
    if self.session.get('auth', 'anonymous'):
      return None
    key_path = self.session.get('auth', 'key_path')
    self._assert_certificate_present(key_path)
    return key_path

#===============================================================================


class CLIMNClient(CLIClient):
  def __init__(self, session):
    base_url = session.get('node', 'mn_url')
    self._assert_base_url_set(base_url)
    return super(CLIMNClient, self).__init__(session, base_url)

  def _assert_base_url_set(self, base_url):
    if not base_url:
      raise cli_exceptions.CLIError('"mn_url" session parameter required')

#===============================================================================


class CLICNClient(CLIClient):
  def __init__(self, session):
    base_url = session.get('node', 'dataone_url')
    self._assert_base_url_set(base_url)
    return super(CLICNClient, self).__init__(session, base_url)

  def _assert_base_url_set(self, base_url):
    if not base_url:
      raise cli_exceptions.CLIError('"dataone_url" session parameter required')

#===============================================================================


class DataONECLI():
  def __init__(self):
    self.session = session.session()
    self.session.load_session_from_ini_file(suppress_error=True)

  def _get_file_size(self, path):
    with open(path, 'r') as f:
      f.seek(0, os.SEEK_END)
      size = f.tell()
    return size

  def _get_file_checksum(self, path, algorithm='SHA1', block_size=1024 * 1024):
    h = hashlib.new(algorithm)
    with open(path, 'r') as f:
      while True:
        data = f.read()
        if not data:
          break
        h.update(data)
    return h.hexdigest()

  def _assert_file_exists(self, path):
    if not os.path.isfile(path):
      msg = 'Invalid file: {0}'.format(path)
      raise cli_exceptions.InvalidArguments(msg)

  def _set_invalid_checksum_to_default(self):
    algorithm = self.session.get('sysmeta', 'algorithm')
    try:
      hashlib.new(algorithm)
    except ValueError:
      self.config['sysmeta']['algorithm'] = (
        d1_common.const.DEFAULT_CHECKSUM_ALGORITHM, str
      )
      logging.error(
        'Invalid checksum algorithm, "{0}", set to default, "{1}"'
        .format(algorithm, d1_common.const.DEFAULT_CHECKSUM_ALGORITHM)
      )

  def _create_system_metadata(self, pid, path):
    checksum = self._get_file_checksum(path)
    size = self._get_file_size(path)
    sysmeta = self.session.create_system_metadata(pid, checksum, size)
    return sysmeta

  def _create_system_metadata_xml(self, pid, path):
    sysmeta = self._create_system_metadata(pid, path)
    return sysmeta.toxml()

  def _post_file_and_system_metadat_to_member_node(self, client, pid, path, sysmeta):
    with open(path, 'r') as f:
      try:
        response = client.createResponse(pid, f, sysmeta)
      except d1_common.types.exceptions.DataONEException as e:
        logging.error('Unable to create Science Object on Member Node.\n{0}'.format(e))

  def science_object_create(self, pid, path):
    '''Create a new Science Object on a Member Node
    '''
    self._assert_file_exists(path)
    sysmeta = self._create_system_metadata(pid, path)
    client = CLIMNClient(self.session)
    self._post_file_and_system_metadat_to_member_node(client, pid, path, sysmeta)

  def _copy_file_like_object_to_file(self, response, path):
    try:
      file = open(path, 'wb')
      shutil.copyfileobj(response, file)
      file.close()
    except EnvironmentError as (errno, strerror):
      error_message_lines = []
      error_message_lines.append('Could not write to file: {0}'.format(path))
      error_message_lines.append('I/O error({0}): {1}'.format(errno, strerror))
      error_message = '\n'.join(error_message_lines)
      raise cli_exceptions.CLIError(error_message)

  def _get_science_object_from_member_node(self, client, pid):
    try:
      return client.get(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get Science Object from Member Node.\n{0}'.format(e)
      )

  def science_object_get(self, pid, path):
    client = CLIMNClient(self.session)
    response = self._get_science_object_from_member_node(client, pid)
    self._copy_file_like_object_to_file(response, path)

  def _get_system_metadata(self, client, pid):
    try:
      return client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get System Metadata from Coordinating Node.\n{0}'.format(e)
      )

  def _pretty(self, xml_doc):
    if self.session.get('cli', 'pretty'):
      dom = xml.dom.minidom.parseString(xml_doc)
      return dom.toprettyxml(indent='  ')
    return xml_doc

  def system_metadata_get(self, pid, path):
    client = CLICNClient(self.session)
    metadata = self._get_system_metadata(client, pid)
    sci_meta_xml = metadata.toxml()
    self._copy_file_like_object_to_file(
      StringIO.StringIO(self._pretty(sci_meta_xml())), path
    )

  def update_access_policy(self, pid):
    client = CLICNClient(self.session)
    metadata = self._get_system_metadata(client, pid)
    sci_meta_xml = metadata.toxml()
    self._copy_file_like_object_to_file(
      StringIO.StringIO(self._pretty(sci_meta_xml())), path
    )

  def related(self, pid):
    client = CLICNClient(self.session)
    metadata = self._get_system_metadata(client, pid)
    print 'Describes:'
    if len(metadata.describes) > 0:
      for describes in metadata.describes:
        print '  {0}'.format(describes)
    else:
      print '  <none>'
    print 'Described By:'
    if len(metadata.describedBy) > 0:
      for describedBy in metadata.describedBy:
        print '  {0}'.format(describedBy)
    else:
      print '  <none>'

  # ----------------------------------------------------------------------------
  # Misc
  # ----------------------------------------------------------------------------

  def resolve(self, pid):
    '''Get Object Locations for Object.
    '''
    client = CLIMNClient(self.session)
    object_location_list = client.resolve(pid)
    print StringIO.StringIO(self._pretty(object_location_list)).getvalue()

  def list(self):
    '''MN listObjects.
    '''
    client = CLIMNClient(self.session)
    object_list = client.listObjects(
      startTime=self.session.get('search', 'start_time'),
      endTime=self.session.get('search', 'end_time'),
      objectFormat=self.session.get('search', 'search_object_format'),
      start=self.session.get('slice', 'start'),
      count=self.session.get('slice', 'count')
    )
    object_list_xml = object_list.toxml()
    print StringIO.StringIO(self._pretty(object_list_xml)).getvalue()

  def log(self):
    '''MN log.
    '''
    client = CLIMNClient(self.session)
    object_list = client.getLogRecords(
      startTime=self.session.get('search', 'start_time'),
      toDate=self.session.get('search', 'end_time'),
      start=self.session.get('slice', 'start'),
      count=self.session.get('slice', 'count')
    )
    object_list_xml = object_list.toxml()
    print StringIO.StringIO(self._pretty(object_list_xml)).getvalue()

  def getObjectFormats(self):
    '''List the format IDs from the CN
    '''
    pass

  def objectformats(self):
    '''Get a list of object formats available on the target.
    :return: (object format, count) object formats.

    TODO: May need to be completely
    removed (since clients should use CNs for object discovery).
    '''

    if len(self.args) != 0:
      logging.error('Invalid arguments')
      logging.error('Usage: objectformats')
      return
    certpath = self.config['auth']['cert_path']
    keypath = self.config['auth']['key_path']
    if certpath is not None:
      if not os.path.exists(certpath):
        certpath = None
        keypath = None

    client = d1_client.mnclient.MemberNodeClient(
      self.config['auth']['mn_url'], certfile=certpath, keyfile=keypath
    )

    object_list = d1_client.objectlistiterator.ObjectListIterator(client)

    unique_objects = {}
    for info in object_list:
      logging.debug("ID:%s | FMT: %s" % (info.identifier, info.objectFormat))
      try:
        unique_objects[info.objectFormat] += 1
      except KeyError:
        unique_objects[info.objectFormat] = 1

    self.output(StringIO.StringIO('\n'.join(unique_objects) + '\n'))

  # ----------------------------------------------------------------------------
  # Search
  # ----------------------------------------------------------------------------

  def search(self):
    '''CN search.
    '''
    print self.session.get('node', 'dataone_url')
    client = d1_client.cnclient.CoordinatingNodeClient(
      self.session.get(
        'node', 'dataone_url'
      )
    )
    kwargs = {
      'start': self.session.get('slice', 'start'),
      'count': self.session.get('slice', 'count')
    }
    if self.session.get('search', 'fields') is not None:
      kwargs['fields'] = self.session.session['fields']
    res = client.search(self.session.get('search', 'query'), **kwargs)
    print "Num found = %d" % res['numFound']
    for doc in res['docs']:
      for k in doc.keys():
        print "%s: %s" % (k, doc[k])
      print "========"

  def fields(self):
    '''List the CN search fields - enumerates the SOLR index fields.
    '''
    client = d1_client.cnclient.CoordinatingNodeClient(
      self.session.get(
        'node', 'dataone_url'
      )
    )
    res = client.getSearchFields()
    print "%-25s %-12s %-12s %-12s" % ('Name', 'Type', 'Unique', 'Records')
    keys = res.keys()
    keys.sort()
    for f in keys:
      try:
        print "%-25s %-12s %-12s %-12s" % (
          f, res[f]['type'], str(res[f]['distinct']), str(
            res[f]['docs']
          )
        )
      except:
        print "%-25s %-12s %-12s %-12s" % (f, res[f]['type'], '?', str(res[f]['docs']))

  # ----------------------------------------------------------------------------
  # Session Parameters
  # ----------------------------------------------------------------------------

  def reset(self):
    return self.session.reset()

  def load_session_from_ini_file(self, suppress_error=False, ini_file_path=None):
    return self.session.load_session_from_ini_file(suppress_error, ini_file_path)

  def save_session_to_ini_file(self, ini_file_path=None):
    return self.session.save_session_to_ini_file(ini_file_path)

  def print_session_parameter(self, name):
    return self.session.print_parameter(name)

  def set_session_parameter(self, name, value):
    return self.session.set_with_conversion_implicit_section(name, value)

  def clear_session_parameter(self, name):
    return self.session.set_with_implicit_section(name, None)

  def access_control_add_allowed_subject(self, subject, permission):
    return self.session.access_control_add_allowed_subject(subject, permission)

  def access_control_remove_allowed_subject(self, subject):
    return self.session.access_control_remove_allowed_subject(subject)

  def access_control_allow_public(self, allow):
    self.session.access_control_allow_public(allow)

  def access_control_remove_all_allowed_subjects(self, line):
    self.session.access_control_remove_all_allowed_subjects(line)

  #=============================================================================

  def update_verbose(self):
    if self.session.get('cli', 'verbose'):
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)

#===============================================================================


class CLI(cmd.Cmd):
  def __init__(self):
    self.d1 = DataONECLI()
    cmd.Cmd.__init__(self)
    self.prompt = '> '
    self.intro = 'DataONE Command Line Interface'

  def _split_key_value(self, line):
    try:
      k, v = shlex.split(line)
    except ValueError:
      raise cli_exceptions.InvalidArguments('Need two arguments')
    else:
      return k, v

  def _split_key_optional_value(self, line):
    try:
      return self._split_key_value(line)
    except cli_exceptions.InvalidArguments:
      try:
        k, = shlex.split(line)
      except ValueError:
        raise cli_exceptions.InvalidArguments('Need one or two arguments')
      else:
        return k, None

  #-----------------------------------------------------------------------------
  # Session.
  #-----------------------------------------------------------------------------

  def do_reset(self, line):
    '''reset
    Set all session parameters to their default values
    '''
    try:
      self.d1.reset()
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_load(self, line):
    '''load [file]
    Load session parameters from file
    '''
    if line.strip() == '':
      line = None
    try:
      self.d1.load_session_from_ini_file(ini_file_path=line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_save(self, line):
    '''load [file]
    Load session parameters from file
    '''
    if line.strip() == '':
      line = None
    try:
      self.d1.save_session_to_ini_file(ini_file_path=line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_get(self, line):
    '''get [session parameter]
    Display the value of a session parameter. Display all parameters if [session parameter] is omitted.
    '''
    try:
      self.d1.print_session_parameter(line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

#section = self.find_section_containing_session_parameter(k)
#logging.info('{0}: {1}'.format(k, self.config[section][k][0]))

  def do_set(self, line):
    '''set <session parameter> <value>
    Set the value of a session parameter
    '''
    try:
      k, v = self._split_key_value(line)
      self.d1.set_session_parameter(k, v)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_clear(self, line):
    '''clear <session parameter>
    Clear the value of a session parameter.
    '''
    try:
      self.d1.clear_session_parameter(line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  #-----------------------------------------------------------------------------
  # Access control.
  #-----------------------------------------------------------------------------

  def do_allow(self, line):
    '''allow <subject> [access level]
    Allow access to subject
    '''
    try:
      subject, permission = self._split_key_optional_value(line)
      self.d1.access_control_add_allowed_subject(subject, permission)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_deny(self, line):
    '''deny <subject>
    Remove subject from access policy
    '''
    try:
      self.d1.access_control_remove_allowed_subject(line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_allowpublic(self, line):
    '''allowpublic
    Allow public read
    '''
    self.d1.access_control_allow_public(True)

  def do_denypublic(self, line):
    '''denypublic
    Deny public read
    '''
    self.d1.access_control_allow_public(False)

  def do_denyall(self, line):
    '''denyall
    Remove all subjects from access policy and deny public read
    '''
    try:
      self.d1.access_control_remove_all_allowed_subjects(line)
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  #-----------------------------------------------------------------------------
  # System Metadata
  #-----------------------------------------------------------------------------

  #def do_printsysmetaxml(self, line):
  #  try:
  #    self.d1.sysmeta_print(line)
  #  except cli_exceptions.InvalidArguments as e:
  #    logging.error(e)

  #-----------------------------------------------------------------------------
  # Science Object Operations
  #-----------------------------------------------------------------------------

  def do_create(self, line):
    '''create <pid> <file>
    Create a new Science Object on a Member Node
    '''
    try:
      pid, file = self._split_key_value(line)
      self.d1.science_object_create(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_getdata(self, line):
    '''getdata <pid> <file>
    Get a Science Data Object from a Member Node
    '''
    try:
      pid, file = self._split_key_value(line)
      self.d1.science_object_get(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_meta(self, line):
    '''meta <pid> [file]
    Get System Metdata from a Coordinating Node
    '''
    try:
      pid, file = self._split_key_optional_value(line)
      self.d1.system_metadata_get(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_setaccess(self, line):
    '''setaccess <pid>
    Update the Access Policy on an existing Science Data Object
    '''
    try:
      self.d1.update_access_policy(line)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_related(self, line):
    '''related <pid>
    Given the PID for a Science Data Object, find it's Science Metadata and vice versa
    '''
    try:
      self.d1.related(line)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_resolve(self, line):
    '''resolve <pid>
    Given the PID for a Science Object, find all locations from which the Science Object can be downloaded
    '''
    try:
      self.d1.resolve(line)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_list(self, line):
    '''list
    Retrieve a list of available Science Data Objects from a single MN with basic filtering
    '''
    try:
      self.d1.list()
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_log(self, line):
    '''log <pid>
    Retrieve event log for a Science Object
    '''
    try:
      self.d1.log(line)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  #-----------------------------------------------------------------------------
  # Search
  #-----------------------------------------------------------------------------

  def do_search(self, line):
    '''search
    Comprehensive search for Science Data Objects across all available MNs
    '''
    try:
      self.d1.search()
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  def do_fields(self, line):
    '''fields
    List the SOLR index fields that are available for use in the search command
    '''
    try:
      self.d1.fields()
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      logging.error(e)

  #-----------------------------------------------------------------------------
  # CLI
  #-----------------------------------------------------------------------------

  def do_history(self, args):
    '''history
    Display a list of commands that have been entered
    '''
    try:
      print self._history
    except cli_exceptions.InvalidArguments as e:
      logging.error(e)

  def do_exit(self, args):
    '''exit
    Exit from the CLI
    '''
    sys.exit()

  def do_EOF(self, args):
    '''Exit on system EOF character'''
    return self.do_exit(args)

  def do_help(self, args):
    '''Get help on commands
    'help' or '?' with no arguments displays a list of commands for which help is available
    'help <command>' or '? <command>' gives help on <command>
    '''
    # The only reason to define this method is for the help text in the doc
    # string
    cmd.Cmd.do_help(self, args)

  #-----------------------------------------------------------------------------
  # Command processing.
  #-----------------------------------------------------------------------------

  ## Override methods in Cmd object ##
  def preloop(self):
    '''Initialization before prompting user for commands.
       Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
    '''
    # Set up command completion.
    cmd.Cmd.preloop(self)
    self._history = []

  def postloop(self):
    '''Take care of any unfinished business.
       Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
    '''
    cmd.Cmd.postloop(self) ## Clean up command completion
    print "Exiting..."

  def precmd(self, line):
    ''' This method is called after the line has been input but before
      it has been interpreted. If you want to modify the input line
      before execution (for example, variable substitution) do it here.
    '''
    self._history += [line.strip()]
    return line

  def postcmd(self, stop, line):
    '''If you want to stop the console, return something that evaluates to true.
       If you want to do some post command processing, do it here.
    '''
    self.d1.update_verbose()
    self.d1._set_invalid_checksum_to_default()
    return stop

  def emptyline(self):
    '''Do nothing on empty input line'''
    pass

  def default(self, line):
    '''Called on an input line when the command prefix is not recognized.
    '''
    logging.error('Unknown command')

  def run_command_line_arguments(self, commands):
    for command in commands:
      self.onecmd(command)


def main():
  log_setup()

  parser = optparse.OptionParser('usage: %prog [command] ...')
  options, arguments = parser.parse_args()

  ## args[1] is not guaranteed to exist but the slice args[1:] would still be
  ## valid and evaluate to an empty list.
  #dataONECLI = DataONECLI(opts_dict,  args[1:])
  #
  ## Sanity.
  #if len(args) == 0 or args[0] not in dataONECLI.command_map.keys():
  #  parser.error('<command> is required and must be one of: {0}'
  #               .format(', '.join(dataONECLI.command_map.keys())))
  #
  #if opts.slice_count > d1_common.const.MAX_LISTOBJECTS:
  #  parser.error('--slice-count must be {0} or less'
  #               .format(parser.error('<command> is required and must be one of: {0}'
  #                                    .format(', '.join(dataONECLI.command_map.keys())))))
  #
  ## Check dates and convert them from ISO 8601 to datetime.
  #date_opts = ['start_time', 'end_time']
  #error = False
  #for date_opt in date_opts:
  #  if opts_dict[date_opt] != None:
  #    try:
  #      opts.__dict__[date_opt] = iso8601.parse_date(opts_dict[date_opt])
  #    except (TypeError, iso8601.iso8601.ParseError):
  #      logging.error('Invalid date option {0}: {1}'.format(date_opt, opts_dict[date_opt]))
  #      error = True
  #
  #if error == True:
  #  return

  cli = CLI()
  # Run any arguments passed on the command line.
  cli.run_command_line_arguments(arguments)
  # Start the command line interpreter loop.
  cli.cmdloop()


if __name__ == '__main__':
  main()
