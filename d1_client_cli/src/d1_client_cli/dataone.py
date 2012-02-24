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

:Synopsis: DataONE Command Line Interface
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import ast
import cmd
import csv
import datetime
import dateutil
import glob
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
from print_level import *
import cli_exceptions
import session

# D1
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


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def expand_path(filename):
  if filename:
    return os.path.expanduser(filename)
  return None

#===============================================================================


class CLIClient(object):
  def __init__(self, session, base_url):
    try:
      self.session = session
      self.base_url = base_url
      return super(CLIClient, self).__init__(
        self.base_url,
        cert_path=self._get_certificate(),
        key_path=self._get_certificate_private_key()
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
    cert_path = self.session.get('auth', 'certpath')
    if not cert_path:
      cert_path = self._get_cilogon_certificate_path()
    self._assert_certificate_present(cert_path)
    return cert_path

  def _get_certificate_private_key(self):
    if self.session.get('auth', 'anonymous'):
      return None
    key_path = self.session.get('auth', 'keypath')
    if key_path is not None:
      self._assert_certificate_present(key_path)
    return key_path

#===============================================================================


class CLIMNClient(CLIClient, d1_client.mnclient.MemberNodeClient):
  def __init__(self, session):
    base_url = session.get('node', 'mnurl')
    self._assert_base_url_set(base_url)
    return super(CLIMNClient, self).__init__(session, base_url)

  def _assert_base_url_set(self, base_url):
    if not base_url:
      raise cli_exceptions.CLIError('"mn_url" session parameter required')

#===============================================================================


class CLICNClient(CLIClient, d1_client.cnclient.CoordinatingNodeClient):
  def __init__(self, session):
    base_url = session.get('node', 'dataoneurl')
    self._assert_base_url_set(base_url)
    return super(CLICNClient, self).__init__(session, base_url)

  def _assert_base_url_set(self, base_url):
    if not base_url:
      raise cli_exceptions.CLIError('"dataone_url" session parameter required')

#===============================================================================


class DataONECLI():
  def __init__(self):
    self.session = session.session()
    self.session.load(suppress_error=True)

  def _get_file_size(self, path):
    with open(expand_path(path), 'r') as f:
      f.seek(0, os.SEEK_END)
      size = f.tell()
    return size

  def _get_file_checksum(self, path, algorithm='SHA-1', block_size=1024 * 1024):
    h = d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
    with open(expand_path(path), 'r') as f:
      while True:
        data = f.read(block_size)
        if not data:
          break
        h.update(data)
    return h.hexdigest()

  def _assert_file_exists(self, path):
    if not os.path.isfile(expand_path(path)):
      msg = 'Invalid file: {0}'.format(path)
      raise cli_exceptions.InvalidArguments(msg)

  def _set_invalid_checksum_to_default(self):
    algorithm = self.session.get('sysmeta', 'algorithm')
    try:
      d1_common.util.get_checksum_calculator_by_dataone_designator(algorithm)
    except ValueError, LookupError:
      self.session.set('sysmeta', 'algorithm', d1_common.const.DEFAULT_CHECKSUM_ALGORITHM)
      print_error(
        'Invalid checksum algorithm, "{0}", set to default, "{1}"'
        .format(algorithm, d1_common.const.DEFAULT_CHECKSUM_ALGORITHM)
      )

  def _create_system_metadata(self, pid, path):
    checksum = self._get_file_checksum(
      expand_path(path), self.session.get(
        'sysmeta', 'algorithm'
      )
    )
    size = self._get_file_size(expand_path(path))
    sysmeta = self.session.create_system_metadata(pid, checksum, size)
    return sysmeta

  def _create_system_metadata_xml(self, pid, path):
    sysmeta = self._create_system_metadata(pid, expand_path(path))
    return sysmeta.toxml()

  def _post_file_and_system_metadat_to_member_node(self, client, pid, path, sysmeta):
    with open(expand_path(path), 'r') as f:
      try:
        response = client.createResponse(pid, f, sysmeta)
        if response.status != 200:
          err = (response.status, response.reason)
          print_error("Couldn't create object.  Reason: (%d) %s" % err)
      except d1_common.types.exceptions.DataONEException as e:
        print_error('Unable to create Science Object on Member Node\n{0}'.format(e))

  def science_object_create(self, pid, path):
    '''Create a new Science Object on a Member Node
    '''
    path = expand_path(path)
    self._assert_file_exists(path)
    sysmeta = self._create_system_metadata(pid, path)
    client = CLIMNClient(self.session)
    self._post_file_and_system_metadat_to_member_node(client, pid, path, sysmeta)

  def _copy_file_like_object_to_file(self, file_like_object, path):
    try:
      file = open(expand_path(path), 'wb')
      shutil.copyfileobj(file_like_object, file)
      file.close()
    except EnvironmentError as (errno, strerror):
      error_message_lines = []
      error_message_lines.append('Could not write to file: {0}'.format(path))
      error_message_lines.append('I/O error({0}): {1}'.format(errno, strerror))
      error_message = '\n'.join(error_message_lines)
      raise cli_exceptions.CLIError(error_message)

  def output(self, file_like_object, path):
    '''Display or save file like object'''
    if not path:
      for line in file_like_object:
        print_info(line.rstrip())
    else:
      self._copy_file_like_object_to_file(file_like_object, expand_path(path))

  def _get_science_object_from_member_node(self, client, pid):
    try:
      return client.get(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get Science Object from Member Node\n{0}'.format(e)
      )

  def science_object_get(self, pid, path):
    client = CLIMNClient(self.session)
    response = self._get_science_object_from_member_node(client, pid)
    self.output(response, expand_path(path))

  def _get_system_metadata(self, client, pid):
    try:
      return client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to get System Metadata from Coordinating Node\n{0}'.format(e)
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
    self.output(StringIO.StringIO(self._pretty(sci_meta_xml)), expand_path(path))

  def related(self, pid):
    raise cli_exceptions.CLIError('not implemented')

  def resolve(self, pid):
    '''Get Object Locations for Object.
    '''
    client = CLICNClient(self.session)
    try:
      object_location_list = client.resolve(pid)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError('Unable to get resolve: {0}\n{1}'.format(pid, e))
    for location in object_location_list.objectLocation:
      print_info(location.url)

  def list(self, path):
    '''MN listObjects.
    '''
    client = CLIMNClient(self.session)
    object_list = client.listObjects(
      startTime=self.session.get('search', 'fromdate'),
      endTime=self.session.get('search', 'todate'),
      objectFormat=self.session.get('search', 'searchobjectformat'),
      start=self.session.get('slice', 'start'),
      count=self.session.get('slice', 'count')
    )
    object_list_xml = object_list.toxml()
    self.output(StringIO.StringIO(self._pretty(object_list_xml)), expand_path(path))

  def log(self, path):
    '''MN log.
    '''
    client = CLIMNClient(self.session)
    object_log = client.getLogRecords(
      fromDate=self.session.get('search', 'fromdate'),
      toDate=self.session.get('search', 'todate'),
      start=self.session.get('slice', 'start'),
      count=self.session.get('slice', 'count')
    )
    object_log_xml = object_log.toxml()
    self.output(StringIO.StringIO(self._pretty(object_log_xml)), expand_path(path))

  def set_access_policy(self, pid):
    access_policy = self.session.access_control_get_pyxb()
    client = CLICNClient(self.session)
    try:
      success = client.setAccessPolicy(pid, access_policy, 1)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to set access policy on: {0}\nError:\n{1}'.format(pid, e)
      )

  def set_replication_policy(self, pid):
    replication_policy = self.session.replication_control_get_pyxb()
    client = CLICNClient(self.session)
    try:
      success = client.setReplicationPolicy(pid, replication_policy, 1)
    except d1_common.types.exceptions.DataONEException as e:
      raise cli_exceptions.CLIError(
        'Unable to set replication policy on: {0}\nError:\n{1}'.format(pid, e)
      )

  #def getObjectFormats(self):
  #  '''List the format IDs from the CN
  #  '''
  #  pass
  #
  #
  #def objectformats(self):
  #  '''Get a list of object formats available on the target.
  #  :return: (object format, count) object formats.
  #
  #  TODO: May need to be completely
  #  removed (since clients should use CNs for object discovery).
  #  '''
  #
  #  if len(self.args) != 0:
  #    print_error('Invalid arguments')
  #    print_error('Usage: objectformats')
  #    return
  #  certpath = self.config['auth']['cert_path']
  #  keypath = self.config['auth']['key_path']
  #  if certpath is not None:
  #    if not os.path.exists(certpath):
  #      certpath = None
  #      keypath = None
  #
  #  client = d1_client.mnclient.MemberNodeClient(self.config['auth']['mn_url'],
  #                                               cert_path=certpath,
  #                                               key_path=keypath)
  #
  #  object_list = d1_client.objectlistiterator.ObjectListIterator(client)
  #
  #  unique_objects = {}
  #  for info in object_list:
  #    print_debug("ID:%s | FMT: %s" % (info.identifier, info.objectFormat) )
  #    try:
  #      unique_objects[info.objectFormat] += 1
  #    except KeyError:
  #      unique_objects[info.objectFormat] = 1
  #
  #  self.output(StringIO.StringIO('\n'.join(unique_objects) + '\n'))

  # ----------------------------------------------------------------------------
  # Search
  # ----------------------------------------------------------------------------

  def search(self):
    '''CN search.
    '''
    client = CLICNClient(self.session)
    kwargs = {
      'start': self.session.get('slice', 'start'),
      'count': self.session.get('slice', 'count')
    }
    print_info('**aBp_ DEBUG**')
    print_info(kwargs)
    if self.session.get('search', 'fields') is not None:
      kwargs['fields'] = self.session.get('search', 'fields')
    res = client.search(self.session.get('search', 'query'), **kwargs)
    print_info('Num found = %d' % res['numFound'])
    for doc in res['docs']:
      for k in doc.keys():
        print_info('%s: %s' % (k, doc[k]))
      print_info('========')

  def fields(self):
    '''List the CN search fields - enumerates the SOLR index fields.
    '''
    client = d1_client.cnclient.CoordinatingNodeClient(
      self.session.get(
        'node', 'dataoneurl'
      )
    )
    res = client.getSearchFields()
    print_info('%-25s %-12s %-12s %-12s' % ('Name', 'Type', 'Unique', 'Records'))
    keys = res.keys()
    keys.sort()
    for f in keys:
      try:
        print_info(
          '%-25s %-12s %-12s %-12s' % (
            f, res[f]['type'], str(res[f]['distinct']), str(res[f]['docs'])
          )
        )
      except:
        print_info(
          '%-25s %-12s %-12s %-12s' % (
            f, res[f]['type'], '?', str(res[f]['docs'])
          )
        )

  # ----------------------------------------------------------------------------
  # Session parameters
  # ----------------------------------------------------------------------------

  def reset(self):
    return self.session.reset()

  def session_load(self, suppress_error=False, pickle_file_path=None):
    return self.session.load(suppress_error, expand_path(pickle_file_path))

  def session_save(self, pickle_file_path=None):
    return self.session.save(expand_path(pickle_file_path))

  def session_print_parameter(self, name):
    return self.session.print_parameter(name)

  def session_set_parameter(self, name, value):
    return self.session.set_with_conversion_implicit_section(name, value)

  def session_clear_parameter(self, name):
    return self.session.set_with_implicit_section(name, None)

  # ----------------------------------------------------------------------------
  # Access control
  # ----------------------------------------------------------------------------

  def access_control_add_allowed_subject(self, subject, permission):
    return self.session.access_control_add_allowed_subject(subject, permission)

  def access_control_remove_allowed_subject(self, subject):
    return self.session.access_control_remove_allowed_subject(subject)

  def access_control_allow_public(self, allow):
    self.session.access_control_allow_public(allow)

  def access_control_remove_all_allowed_subjects(self):
    self.session.access_control_remove_all_allowed_subjects()

  # ----------------------------------------------------------------------------
  # Replication policy
  # ----------------------------------------------------------------------------

  def replication_policy_clear(self):
    return self.session.replication_policy_clear()

  def replication_policy_add_preferred(self, mn):
    return self.session.replication_policy_add_preferred(mn)

  def replication_policy_add_blocked(self, mn):
    return self.session.replication_policy_add_blocked(mn)

  def replication_policy_remove(self, mn):
    return self.session.replication_policy_remove(mn)

  def replication_policy_set_replication_allowed(self, replication_allowed):
    return self.session.replication_policy_set_replication_allowed(replication_allowed)

  def replication_policy_set_number_of_replicas(self, number_of_replicas):
    return self.session.replication_policy_set_number_of_replicas(number_of_replicas)

  def replication_policy_print(self):
    return self.session.replication_policy_print()

#===============================================================================


class CLI(cmd.Cmd):
  def __init__(self):
    self.d1 = DataONECLI()
    cmd.Cmd.__init__(self)
    self.prompt = '> '
    self.intro = 'DataONE Command Line Interface'

  def _split_args(self, line, n_required, n_optional):
    args = shlex.split(line)
    if len(args) < n_required or len(args) > n_required + n_optional:
      msg = 'Need {0} required and {1} optional parameters'.format(
        n_required if n_required else 'no', n_optional if n_optional else 'no'
      )
      raise cli_exceptions.InvalidArguments(msg)
    # Pad the list out with None for any optional parameters that were not
    # provided.
    args += [None] * (n_required + n_optional - len(args))
    if len(args) == 1:
      return args[0]
    return args

  def _update_verbose(self):
    if self.d1.session.get('cli', 'verbose'):
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)

  #-----------------------------------------------------------------------------
  # Session.
  #-----------------------------------------------------------------------------

  def do_reset(self, line):
    '''reset
    Set all session parameters to their default values
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.reset()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_load(self, line):
    '''load [file]
    Load session parameters from file
    '''
    try:
      file = self._split_args(line, 0, 1)
      self.d1.session_load(pickle_file_path=expand_path(file))
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_save(self, line):
    '''save [file]
    Save session parameters to file
    '''
    try:
      file = self._split_args(line, 0, 1)
      self.d1.session_save(pickle_file_path=expand_path(file))
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_show(self, line):
    '''show [session parameter]
    Display the value of a session parameter. Display all parameters if [session parameter] is omitted.
    '''
    try:
      session_parameter = self._split_args(line, 0, 1)
      self.d1.session_print_parameter(session_parameter)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_set(self, line):
    '''set <session parameter> <value>
    Set the value of a session parameter
    '''
    if len(shlex.split(line)) == 0:
      self.do_show(line)
    else:
      try:
        session_parameter, value = self._split_args(line, 2, 0)
        self.d1.session_set_parameter(session_parameter, value)
      except cli_exceptions.InvalidArguments as e:
        print_error(e)

  # TODO: add complete_show and complete_set method to display possibilities. - aBp_

  def do_clear(self, line):
    '''clear <session parameter>
    Clear the value of a session parameter.
    '''
    try:
      session_parameter = self._split_args(line, 1, 0)
      self.d1.session_clear_parameter(session_parameter)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  #-----------------------------------------------------------------------------
  # Access control.
  #-----------------------------------------------------------------------------

  def do_allow(self, line):
    '''allow <subject> [access level]
    Allow access to subject
    '''
    try:
      subject, permission = self._split_args(line, 1, 1)
      self.d1.access_control_add_allowed_subject(subject, permission)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_deny(self, line):
    '''deny <subject>
    Remove subject from access policy
    '''
    try:
      subject = self._split_args(line, 1, 0)
      self.d1.access_control_remove_allowed_subject(subject)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_allowpublic(self, line):
    '''allowpublic
    Allow public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_allow_public(True)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_denypublic(self, line):
    '''denypublic
    Deny public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_allow_public(False)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_denyall(self, line):
    '''denyall
    Remove all subjects from access policy and deny public read
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.access_control_remove_all_allowed_subjects()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  #-----------------------------------------------------------------------------
  # Replication policy.
  #-----------------------------------------------------------------------------

  def do_clearreplication(self, line):
    '''clearreplication
    Clear replication policy
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_clear()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_addpreferred(self, line):
    '''addpreferred <member node>
    Add Member Node to list of preferred replication targets
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_add_preferred(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_addblocked(self, line):
    '''addblocked <member node>
    Add blocked Member Node to access policy
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_add_blocked(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_remove(self, line):
    '''remove <member node>
    Remove Member Node from access policy
    '''
    try:
      mn = self._split_args(line, 1, 0)
      return self.d1.replication_policy_remove(mn)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_allowreplication(self, line):
    '''allowreplication
    Allow object to be replicated
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_set_replication_allowed(True)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_disallowreplication(self, line):
    '''disallowreplication
    Prevent object from being replicated
    '''
    try:
      self._split_args(line, 0, 0)
      return self.d1.replication_policy_set_replication_allowed(False)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_setreplicas(self, line):
    '''setreplicas <number of replicas>
    Set preferred number of replicas
    '''
    try:
      n_replicas = self._split_args(line, 1, 0)
      return self.d1.replication_policy_get_number_of_replicas(n_replicas)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  #-----------------------------------------------------------------------------
  # Search
  #-----------------------------------------------------------------------------

  def do_search(self, line):
    '''search
    Comprehensive search for Science Data Objects across all available MNs
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.search()
    except (
      cli_exceptions.InvalidArguments, cli_exceptions.CLIError,
      d1_client.solrclient.SolrException
    ) as e:
      print_error(e)

  def do_fields(self, line):
    '''fields
    List the SOLR index fields that are available for use in the search command
    '''
    try:
      self._split_args(line, 0, 0)
      self.d1.fields()
    except (
      cli_exceptions.InvalidArguments, cli_exceptions.CLIError,
      d1_client.solrclient.SolrException
    ) as e:
      print_error(e)

  #-----------------------------------------------------------------------------
  # Science Object Operations
  #-----------------------------------------------------------------------------

  def do_data(self, line):
    '''data <pid> <file>
    Get a Science Data Object from a Member Node
    '''
    try:
      pid, file = self._split_args(line, 2, 0)
      self.d1.science_object_get(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_meta(self, line):
    '''meta <pid> [file]
    Get System Metdata from a Coordinating Node
    '''
    try:
      pid, file = self._split_args(line, 1, 1)
      self.d1.system_metadata_get(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(str(e))

  def do_create(self, line):
    '''create <pid> <file>
    Create a new Science Object on a Member Node
    '''
    try:
      pid, file = self._split_args(line, 2, 0)
      self.d1.science_object_create(pid, file)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_related(self, line):
    '''related <pid>
    Given the PID for a Science Data Object, find it's Science Metadata and vice versa
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.related(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_resolve(self, line):
    '''resolve <pid>
    Given the PID for a Science Object, find all locations from which the Science Object can be downloaded
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.resolve(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_list(self, line):
    '''list
    Retrieve a list of available Science Data Objects from a single MN with basic filtering
    '''
    try:
      path = self._split_args(line, 0, 1)
      self.d1.list(path)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_log(self, line):
    '''log
    Retrieve event log
    '''
    try:
      path = self._split_args(line, 0, 1)
      self.d1.log(path)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_setaccess(self, line):
    '''setaccess <pid>
    Update the Access Policy on an existing Science Data Object
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.set_access_policy(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  def do_setreplication(self, line):
    '''setreplication <pid>
    Update the Replication Policy on an existing Science Data Object
    '''
    try:
      pid = self._split_args(line, 1, 0)
      self.d1.set_replication_policy(pid)
    except (cli_exceptions.InvalidArguments, cli_exceptions.CLIError) as e:
      print_error(e)

  #-----------------------------------------------------------------------------
  # CLI
  #-----------------------------------------------------------------------------

  def do_history(self, line):
    '''history
    Display a list of commands that have been entered
    '''
    try:
      self._split_args(line, 0, 0)
      print_info(self._history)
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_exit(self, line):
    '''exit
    Exit from the CLI
    '''
    try:
      self._split_args(line, 0, 0)
      sys.exit()
    except cli_exceptions.InvalidArguments as e:
      print_error(e)

  def do_EOF(self, line):
    '''Exit on system EOF character'''
    return self.do_exit(line)

  def do_help(self, line):
    '''Get help on commands
    'help' or '?' with no arguments displays a list of commands for which help is available
    'help <command>' or '? <command>' gives help on <command>
    '''
    # The only reason to define this method is for the help text in the doc
    # string
    cmd.Cmd.do_help(self, line)

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
    print_info('Exiting...')

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
    self._update_verbose()
    self.d1._set_invalid_checksum_to_default()
    return stop

  def emptyline(self):
    '''Do nothing on empty input line'''
    pass

  def default(self, line):
    '''Called on an input line when the command prefix is not recognized.
    '''
    print_error('Unknown command')

  def run_command_line_arguments(self, commands):
    for command in commands:
      self.onecmd(command)
      self._update_verbose()
      self.d1._set_invalid_checksum_to_default()


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
  #      opts.__dict__[date_opt] = d1_common.date_time.from_iso8601(opts_dict[date_opt])
  #    except (TypeError, d1_common.date_time.iso8601.ParseError):
  #      print_error('Invalid date option {0}: {1}'.format(date_opt, opts_dict[date_opt]))
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
