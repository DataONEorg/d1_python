#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2013 DataONE
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
:mod:`session`
==============

:Synopsis: Hold and manipulate session parameters.
:Created: 2011-11-20
:Author: DataONE (Dahl)
'''

# Stdlib.
import ast
import copy
import os
import pickle
from types import * #@UnusedWildImport
import urlparse

# D1.
try:
  import d1_common.const
except ImportError as e:
  sys.stderr.write(u'Import error: {0}\n'.format(str(e)))
  sys.stderr.write(u'Try: easy_install DataONE_Common\n')
  raise

# App.
import access_control
import cli_exceptions
import cli_util
from const import * #@UnusedWildImport
import replication_policy
import system_metadata

# Identifiers for names.

SECTION_CLI = u'cli'
SECTION_NODE = u'node'
SECTION_SLICE = u'slice'
SECTION_AUTH = u'auth'
SECTION_SYSMETA = u'sys-meta'
SECTION_SEARCH = u'search'

VERBOSE_SECT = SECTION_CLI
VERBOSE_NAME = u'verbose'
EDITOR_SECT = SECTION_CLI
EDITOR_NAME = u'editor'
CN_URL_SECT = SECTION_NODE
CN_URL_NAME = u'dataone-url'
MN_URL_SECT = SECTION_NODE
MN_URL_NAME = u'mn-url'
START_SECT = SECTION_SLICE
START_NAME = u'start'
COUNT_SECT = SECTION_SLICE
COUNT_NAME = u'count'
ANONYMOUS_SECT = SECTION_AUTH
ANONYMOUS_NAME = u'anonymous'
CERT_FILENAME_SECT = SECTION_AUTH
CERT_FILENAME_NAME = u'cert-file'
KEY_FILENAME_SECT = SECTION_AUTH
KEY_FILENAME_NAME = u'key-file'
FORMAT_SECT = SECTION_SYSMETA
FORMAT_NAME = u'format-id'
SUBMITTER_SECT = SECTION_SYSMETA
SUBMITTER_NAME = u'submitter'
OWNER_SECT = SECTION_SYSMETA
OWNER_NAME = u'rights-holder'
ORIG_MN_SECT = SECTION_SYSMETA
ORIG_MN_NAME = u'origin-mn'
AUTH_MN_SECT = SECTION_SYSMETA
AUTH_MN_NAME = u'authoritative-mn'
CHECKSUM_SECT = SECTION_SYSMETA
CHECKSUM_NAME = u'algorithm'
FROM_DATE_SECT = SECTION_SEARCH
FROM_DATE_NAME = u'from-date'
TO_DATE_SECT = SECTION_SEARCH
TO_DATE_NAME = u'to-date'
SEARCH_FORMAT_SECT = SECTION_SEARCH
SEARCH_FORMAT_NAME = u'search-format-id'
QUERY_ENGINE_SECT = SECTION_SEARCH
QUERY_ENGINE_NAME = u'query-type'
QUERY_STRING_SECT = SECTION_SEARCH
QUERY_STRING_NAME = u'query'

# Session variable map.

session_variable_dict = {
  u'dataoneurl': (CN_URL_NAME, unicode),
  u'mnurl': (MN_URL_NAME, unicode),
  u'certpath': (CERT_FILENAME_NAME, unicode),
  u'keypath': (KEY_FILENAME_NAME, unicode),
  u'object-format': (FORMAT_NAME, unicode),
  u'objectformat': (FORMAT_NAME, unicode),
  u'rightsholder': (OWNER_NAME, unicode),
  u'originmn': (ORIG_MN_NAME, unicode),
  u'authoritativemn': (AUTH_MN_NAME, unicode),
  u'fromdate': (FROM_DATE_NAME, unicode),
  u'todate': (TO_DATE_NAME, unicode),
  u'search-object-format': (SEARCH_FORMAT_NAME, unicode),
  u'searchobjectformat': (SEARCH_FORMAT_NAME, unicode),
  u'querytype': (QUERY_ENGINE_NAME, unicode),
}


class session(object):
  def __init__(self, nodes, format_ids):
    self._nodes = nodes
    self._format_ids = format_ids
    self.session = self._create_default_session()
    self.access_control = access_control.AccessControl()
    self.replication_policy = replication_policy.ReplicationPolicy()

  def reset(self):
    self.session = self._create_default_session()
    self.access_control = access_control.AccessControl()
    self.replication_policy = replication_policy.ReplicationPolicy()

  def get_access_control(self):
    return self.access_control

  def get_replication_policy(self):
    return self.replication_policy

  def get(self, section, name=None):
    self._assert_valid_session_parameter(section, name)
    return self.session[section][name][0]

  def get_with_implicit_section(self, name):
    section = self._find_section_containing_session_parameter(name)
    return self.get(section, name)

  def set(self, section, name, value):
    self._assert_valid_session_parameter(section, name)
    self._assert_valid_session_parameter_value(section, name, value)
    name_type = self.session[section][name][1]
    self.session[section][name] = (value, name_type)

  def set_with_implicit_section(self, name, value):
    section = self._find_section_containing_session_parameter(name)
    self.set(section, name, value)

  def set_with_conversion(self, section, name, value_string):
    '''Convert user supplied string to Python type. Lets user use values such as
    True, False and integers. All parameters can be set to None, regardless of
    type. Handle the case where a string is typed by the user and is not quoted,
    as a string literal.
    '''
    self._assert_valid_session_parameter(section, name)
    try:
      v = ast.literal_eval(value_string)
    except (ValueError, SyntaxError):
      v = value_string
    if v is None:
      self.set(section, name, None)
    else:
      try:
        type_converter = self.session[section][name][1]
        value_string = self.validate_value_type(value_string, type_converter)
        value = type_converter(value_string)
        self.set(section, name, value)
      except ValueError as e:
        raise cli_exceptions.InvalidArguments(
          u'Invalid value for {0} / {1}: {2}'.format(section, name, value_string)
        )

  def validate_value_type(self, value, type_converter):
    # Make sure booleans are "sane"
    if type_converter is BooleanType:
      if value in (u'true', 'True', 't', 'T', 1, '1', 'yes', 'Yes'):
        return True
      elif value in (u'false', 'False', 'f', 'F', 0, '0', 'no', 'No'):
        return False
      else:
        raise ValueError(u'Invalid boolean value: {0}'.format(value))
    else:
      return value

  def set_with_conversion_implicit_section(self, name, value_string):
    section = self._find_section_containing_session_parameter(name)
    self.set_with_conversion(section, name, value_string)

  def print_single_parameter(self, name):
    section = self._find_section_containing_session_parameter(name)
    cli_util.print_info(u'{0: <30s}{1}'.format(name, self.get(section, name)))

  def print_all_parameters(self):
    # Debug: Print types.
    #pprint.pprint(self.session)
    #return
    sections = self._get_session_section_ordering()
    for section in sections:
      cli_util.print_info(u'{0}:'.format(section))
      for k in sorted(self.session[section].keys()):
        cli_util.print_info(u'  {0: <30s}{1}'.format(k, self.session[section][k][0]))
    cli_util.print_info(str(self.access_control))
    cli_util.print_info(str(self.replication_policy))
    cli_util.print_info(u'\n')

  def print_parameter(self, name):
    if not name:
      self.print_all_parameters()
    else:
      self.print_single_parameter(name)

  def load(self, pickle_file_path=None, suppress_error=False):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(cli_util.os.path.expanduser(pickle_file_path), u'rb') as f:
        self.__dict__.update(pickle.load(f))
      #self._verify_session_variables()
    except (NameError, IOError, ImportError) as e:
      if not suppress_error:
        cli_util.print_error(
          u'Unable to load session from file: {0}\n{1}'.format(
            pickle_file_path, str(e)
          )
        )

  def save(self, pickle_file_path=None, suppress_error=False):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(cli_util.os.path.expanduser(pickle_file_path), u'wb') as f:
        pickle.dump(self.__dict__, f, 2)
    except (NameError, IOError) as e:
      if not suppress_error:
        cli_util.print_error(
          u'Unable to save session to file: {0}\n{1}'.format(
            pickle_file_path, str(e)
          )
        )

  def is_verbose(self):
    verbose = self.session[VERBOSE_SECT][VERBOSE_NAME][0]
    return (verbose is not None) and verbose

  def get_default_pickle_file_path(self):
    return os.path.join(os.environ[u'HOME'], '.dataone_cli.conf')

  #
  # Private.
  #

  # Go through the session variables and make sure that all the new names
  # are there and any missing variable is there added.
  #def _verify_session_variables(self):
  #  dflt = self._create_default_session()
  #  curr = self.session
  #  changed = False
  #  #
  #  for section in dflt.keys():
  #    curr_section = curr.get(section)
  #    dflt_section = dflt.get(section)
  #    #
  #    # Replace old names with new names.
  #    for old_name in curr_section.keys():
  #      new_value = session_variable_dict.get(old_name)
  #      if new_value is not None:
  #        curr_value = curr_section[old_name]
  #        cli_util.print_info(u'Replacing session variable "{0}" with "{1}" (value "{2}")'
  #            .format(old_name, new_value[0], str(curr_value[0])))
  #        curr_section[new_value[0]] = (curr_value[0], new_value[0])
  #        del(curr_section[old_name])
  #        changed = True
  #    # Add new values.
  #    for v in dflt_section.keys():
  #      if curr_section.get(v) is None:
  #        add_value = dflt_section[v][0]
  #        cli_util.print_info(u'Adding missing value: "{0}" = "{1}"'
  #            .format(v, str(add_value)))
  #        curr_section[v] = (dflt_section[v][0], dflt_section[v][1])
  #        changed = True
  #  if (changed is not None) and changed:
  #    cli_util.print_info('\nThis session has been updated.  Please save the new values.\n\
  #  (see "save" operation)\n')

  #def session_validate_parameter(self, name, value):
  #  # Skip None.
  #  if value is None:
  #    return
  #  #
  #  # Validate the object format.
  #  if name == session.FORMAT_NAME or name == session.SEARCH_FORMAT_NAME:
  #    formats = self.get_known_object_format_ids()
  #    if len(formats) > 0 and value not in formats:
  #      raise ValueError(u'"%s": Invalid format' % value)

  def _create_default_session(self):
    return copy.deepcopy({
      SECTION_CLI: {
        VERBOSE_NAME: (True, bool),
        EDITOR_NAME: ('nano', unicode),
      },
      SECTION_NODE: {
        CN_URL_NAME: (d1_common.const.URL_DATAONE_ROOT, unicode),
        MN_URL_NAME: (u'https://localhost/mn/', unicode),
      },
      SECTION_SLICE: {
        START_NAME: (0, int),
        COUNT_NAME: (d1_common.const.MAX_LISTOBJECTS, int),
      },
      SECTION_AUTH: {
        ANONYMOUS_NAME: (True, bool),
        CERT_FILENAME_NAME: (None, unicode),
        KEY_FILENAME_NAME: (None, unicode),
      },
      SECTION_SEARCH: {
        FROM_DATE_NAME: (None, unicode),
        TO_DATE_NAME: (None, unicode),
        SEARCH_FORMAT_NAME: (None, unicode),
        QUERY_ENGINE_NAME: (d1_common.const.DEFAULT_SEARCH_ENGINE, unicode),
        QUERY_STRING_NAME: (u'*:*', unicode),
      },
      SECTION_SYSMETA: {
        FORMAT_NAME: (None, unicode),
        SUBMITTER_NAME: (None, unicode),
        OWNER_NAME: (None, unicode),
        ORIG_MN_NAME: (None, unicode),
        AUTH_MN_NAME: (None, unicode),
        CHECKSUM_NAME: (d1_common.const.DEFAULT_CHECKSUM_ALGORITHM, unicode),
      },
    })

  def _get_session_section_ordering(self):
    return (
      SECTION_CLI, SECTION_NODE, SECTION_SLICE, SECTION_AUTH, SECTION_SEARCH,
      SECTION_SYSMETA
    )

  def _find_section_containing_session_parameter(self, name):
    '''Find the section containing a session parameter.'''
    # Because the session parameters are split into sections and the user does
    # not specify the section when setting a parameter, it is necessary to
    # search for the parameter.
    for section in self.session:
      if name in self.session[section]:
        return section
    raise cli_exceptions.InvalidArguments(u'Invalid session parameter: {0}'.format(name))

  def _assert_valid_session_parameter(self, section, name):
    try:
      self.session[section][name]
    except LookupError:
      raise cli_exceptions.InvalidArguments(
        u'Invalid session parameter: {0} / {1}'.format(section, name)
      )

  def _assert_valid_session_parameter_value(self, section, name, value):
    if section == CHECKSUM_SECT and name == CHECKSUM_NAME:
      try:
        d1_common.util.get_checksum_calculator_by_dataone_designator(value)
      except LookupError:
        raise cli_exceptions.InvalidArguments(
          u'Invalid checksum algorithm: {0}'.format(value)
        )
    elif section == CN_URL_SECT and name == CN_URL_NAME:
      cn_base_url = self.get(CN_URL_SECT, CN_URL_NAME)
      if value not in [n[2] for n in self._nodes.get(cn_base_url) if n[0] == 'cn']:
        if not cli_util.confirm(
          '"{0}" is not a known DataONE Coordinating Node. Use anyway?'.format(
            value
          )
        ):
          raise cli_exceptions.InvalidArguments(u'Coordinating Node update cancelled')
    elif section == MN_URL_SECT and name == MN_URL_NAME:
      cn_base_url = self.get(CN_URL_SECT, CN_URL_NAME)
      if value not in [n[2] for n in self._nodes.get(cn_base_url) if n[0] == 'mn']:
        if not cli_util.confirm(
          '"{0}" is not a known DataONE Member Node. Use anyway?'.format(
            value
          )
        ):
          raise cli_exceptions.InvalidArguments(u'Member Node update cancelled')
    elif section == FORMAT_SECT and name == FORMAT_NAME:
      cn_base_url = self.get(CN_URL_SECT, CN_URL_NAME)
      if value not in self._format_ids.get(cn_base_url):
        raise cli_exceptions.InvalidArguments(
          u'Invalid Object Format ID: {0}'.format(value)
        )
