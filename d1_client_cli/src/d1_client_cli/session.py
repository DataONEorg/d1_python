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
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: easy_install DataONE_Common\n')
  raise

# App.
import access_control
import cli_exceptions
import cli_util
from print_level import * #@UnusedWildImport
import replication_policy
import system_metadata

# Identifiers for names, in case they change again (i.e. object-format to format-id).
SECTION_cli = 'cli'
SECTION_node = 'node'
SECTION_slice = 'slice'
SECTION_auth = 'auth'
SECTION_sysmeta = 'sysmeta'
SECTION_search = 'search'

PRETTY = (SECTION_cli, 'pretty')
VERBOSE = (SECTION_cli, 'verbose')
CN_URL = (SECTION_node, 'dataone-url')
MN_URL = (SECTION_node, 'mn-url')
START = (SECTION_slice, 'start')
COUNT = (SECTION_slice, 'count')
ANONYMOUS = (SECTION_auth, 'anonymous')
CERT_FILENAME = (SECTION_auth, 'cert-file')
KEY_FILENAME = (SECTION_auth, 'key-file')
FORMAT = (SECTION_sysmeta, 'format-id')
SUBMITTER = (SECTION_sysmeta, 'submitter')
OWNER = (SECTION_sysmeta, 'rights-holder')
ORIG_MN = (SECTION_sysmeta, 'origin-mn')
AUTH_MN = (SECTION_sysmeta, 'authoritative-mn')
CHECKSUM = (SECTION_sysmeta, 'algorithm')
FROM_DATE = (SECTION_search, 'from-date')
TO_DATE = (SECTION_search, 'to-date')
SEARCH_FORMAT = (SECTION_search, 'search-format-id')
QUERY_ENGINE = (SECTION_search, 'query-type')
QUERY_STRING = (SECTION_search, 'query')

# Session variable mapping.
#
session_variable_dict = {
  'dataoneurl': (CN_URL[1], str),
  'mnurl': (MN_URL[1], str),
  'certpath': (CERT_FILENAME[1], str),
  'keypath': (KEY_FILENAME[1], str),
  'object-format': (FORMAT[1], str),
  'objectformat': (FORMAT[1], str),
  'rightsholder': (OWNER[1], str),
  'originmn': (ORIG_MN[1], str),
  'authoritativemn': (AUTH_MN[1], str),
  'fromdate': (FROM_DATE[1], str),
  'todate': (TO_DATE[1], str),
  'search-object-format': (SEARCH_FORMAT[1], str),
  'searchobjectformat': (SEARCH_FORMAT[1], str),
  'querytype': (QUERY_ENGINE[1], str),
}


class session(object):
  def __init__(self):
    self.session = self.get_default_session()
    self.access_control = access_control.access_control()
    self.replication_policy = replication_policy.replication_policy()

  def reset(self):
    self.__init__()

  def get_default_session(self):
    return copy.deepcopy({
      SECTION_cli: {
        PRETTY[1]: (True, bool),
        VERBOSE[1]: (False, bool),
      },
      SECTION_node: {
        CN_URL[1]: (d1_common.const.URL_DATAONE_ROOT, str),
        MN_URL[1]: ('https://localhost/mn/', str),
      },
      SECTION_slice: {
        START[1]: (0, int),
        COUNT[1]: (d1_common.const.MAX_LISTOBJECTS, int),
      },
      SECTION_auth: {
        ANONYMOUS[1]: (True, bool),
        CERT_FILENAME[1]: (None, str),
        KEY_FILENAME[1]: (None, str),
      },
      SECTION_sysmeta: {
        FORMAT[1]: (None, str),
        SUBMITTER[1]: (None, str),
        OWNER[1]: (None, str),
        ORIG_MN[1]: (None, str),
        AUTH_MN[1]: (None, str),
        CHECKSUM[1]: (d1_common.const.DEFAULT_CHECKSUM_ALGORITHM, str),
      },
      SECTION_search: {
        FROM_DATE[1]: (None, str),
        TO_DATE: (None, str),
        SEARCH_FORMAT[1]: (None, str),
        QUERY_ENGINE[1]: (d1_common.const.DEFAULT_SEARCH_ENGINE, str),
        QUERY_STRING[1]: ('*:*', str),
      },
    })

  def get_session_section_ordering(self):
    return (
      SECTION_cli, SECTION_node, SECTION_slice, SECTION_auth, SECTION_sysmeta,
      SECTION_search
    )

  def get_default_pickle_file_path(self):
    return os.path.join(os.environ['HOME'], '.d1client.conf')

  def _find_section_containing_session_parameter(self, name):
    '''Find the section containing a session parameter.'''
    # Because the session parameters are split into sections and the user does
    # not specify the section when setting a parameter, it is necessary to
    # search for the parameter.
    for section in self.session:
      if name in self.session[section]:
        return section
    raise cli_exceptions.InvalidArguments('Invalid session parameter: {0}'.format(name))

  def _assert_valid_session_parameter(self, section, name):
    try:
      self.session[section][name]
    except LookupError:
      raise cli_exceptions.InvalidArguments(
        'Invalid session parameter: {0} / {1}'.format(section, name)
      )

  def is_pretty(self):
    pretty = self.session[SECTION_cli][PRETTY][0]
    return (pretty is not None) and pretty

  def is_verbose(self):
    verbose = self.session[SECTION_cli][VERBOSE][0]
    return (verbose is not None) and verbose

  #=============================================================================
  # Public.
  #=============================================================================

  def get(self, section, name=None):
    self._assert_valid_session_parameter(section, name)
    return self.session[section][name][0]

  def get_with_implicit_section(self, name):
    section = self._find_section_containing_session_parameter(name)
    return self.get(section, name)

  def set(self, section, name, value): #@ReservedAssignment
    self._assert_valid_session_parameter(section, name)
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
        self.set(section, name, type_converter(v))
      except ValueError as e:
        raise cli_exceptions.InvalidArguments(
          'Invalid value for {0} / {1}: {2}'.format(section, name, value_string)
        )

  def validate_value_type(self, value_string, type_converter):
    # Make sure booleans are "sane"
    if type_converter is BooleanType:
      if value_string in ('true', 'True', 't', 'T', 1, '1', 'yes', 'Yes'):
        return 'True'
      elif value_string in ('false', 'False', 'f', 'F', 0, '0', 'no', 'No'):
        return 'False'
      else:
        raise ValueError('"%s": Invalid boolean value' % value_string)

  def set_with_conversion_implicit_section(self, name, value_string):
    section = self._find_section_containing_session_parameter(name)
    self.set_with_conversion(section, name, value_string)

  #=============================================================================
  # Access control.
  #=============================================================================

  def access_control_add_allowed_subject(self, subject, permission):
    self.access_control.add_allowed_subject(subject, permission)

  def access_control_remove_allowed_subject(self, subject):
    self.access_control.remove_allowed_subject(subject)

  def access_control_allow_public(self, allow):
    self.access_control.allow_public(allow)

  def access_control_remove_all_allowed_subjects(self):
    self.access_control.remove_all_allowed_subjects()

  def access_control_get_pyxb(self):
    return self.access_control.to_pyxb()

  # ============================================================================
  # Replication policy.
  # ============================================================================

  def replication_policy_clear(self):
    return self.replication_policy.clear()

  def replication_policy_add_preferred(self, mn):
    return self.replication_policy.add_preferred(mn)

  def replication_policy_add_blocked(self, mn):
    return self.replication_policy.add_blocked(mn)

  def replication_policy_remove(self, mn):
    return self.replication_policy.remove(mn)

  def replication_policy_set_replication_allowed(self, replication_allowed):
    return self.replication_policy.set_replication_allowed(replication_allowed)

  def replication_policy_set_number_of_replicas(self, number_of_replicas):
    return self.replication_policy.set_number_of_replicas(number_of_replicas)

  def replication_policy_print(self):
    return self.replication_policy.print_replication_policy()

  def replication_control_get_pyxb(self):
    return self.replication_policy.to_pyxb()

  # ============================================================================
  # Session.
  # ============================================================================

  def print_single_parameter(self, name):
    section = self._find_section_containing_session_parameter(name)
    print_info('{0: <30s}{1}'.format(name, self.get(section, name)))

  def print_all_parameters(self):
    # Debug: Print types.
    #pprint.pprint(self.session)
    #return
    sections = self.get_session_section_ordering()
    for section in sections:
      print_info('{0}:'.format(section))
      for k in sorted(self.session[section].keys()):
        print_info('  {0: <30s}{1}'.format(k, self.session[section][k][0]))
    print_info(str(self.access_control))
    print_info(str(self.replication_policy))
    print_info('\n')

  def print_parameter(self, name):
    if not name:
      self.print_all_parameters()
    else:
      self.print_single_parameter(name)

  def load(self, suppress_error=False, pickle_file_path=None):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(pickle_file_path, 'rb') as f:
        self.__dict__.update(pickle.load(f))
      self.verify_session_variables()
    except (NameError, IOError, ImportError) as e:
      if not suppress_error:
        print_error(
          'Unable to load session from file: {0}\n{1}'.format(
            pickle_file_path, str(e)
          )
        )
    except:
      cli_util._handle_unexpected_exception()

  #   Go through the session variables and make sure that all the new names
  # are there and any missing variable is there added.
  #
  def verify_session_variables(self):
    dflt = self.get_default_session()
    curr = self.session
    changed = False
    #
    for section in dflt.keys():
      curr_section = curr.get(section)
      dflt_section = dflt.get(section)
      #
      # Replace old names with new names.
      for old_name in curr_section.keys():
        new_value = session_variable_dict.get(old_name)
        if new_value is not None:
          curr_value = curr_section[old_name]
          print_info(
            'Replacing session variable "{0}" with "{1}" (value "{2}")'
            .format(old_name, new_value[0], str(curr_value[0]))
          )
          curr_section[new_value[0]] = (curr_value[0], new_value[0])
          del (curr_section[old_name])
          changed = True
      #
      # Add new values.
      for v in dflt_section.keys():
        if curr_section.get(v) is None:
          add_value = dflt_section[v][0]
          print_info('Adding missing value: "{0}" = "{1}"'.format(v, str(add_value)))
          curr_section[v] = (dflt_section[v][0], dflt_section[v][1])
          changed = True
    #
    if (changed is not None) and changed:
      print_info(
        '\nThis session has been updated.  Please save the new values.\n\
    (see "save" command)\n'
      )

  def save(self, pickle_file_path=None):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(pickle_file_path, 'wb') as f:
        pickle.dump(self.__dict__, f, 2)
    except (NameError, IOError) as e:
      if not self.suppress_error:
        print_error(
          'Unable to save session to file: {0}\n{1}'.format(
            pickle_file_path, str(e)
          )
        )

  def create_system_metadata(self, pid, checksum, size):
    access_policy = self.access_control.to_pyxb()
    replication_policy = self.replication_policy.to_pyxb()
    sysmeta_creator = system_metadata.system_metadata()
    self._create_missing_sysmeta_session_parameters()
    sysmeta = sysmeta_creator.create_pyxb_object(
      self, pid, size, checksum, access_policy, replication_policy
    )
    return sysmeta

  def _create_missing_sysmeta_session_parameters(self):
    ''' Make sure all the session values that are:
          necessary to create the sysmeta data
          can be determined from other values
        are there.
        * authoritative-mn, origin-mn, rights-holder
    '''
    save_data = False
    if self.get(AUTH_MN[0], AUTH_MN[1]) is None:
      mn = self.get(MN_URL[0], MN_URL[1])
      mn_host = self._get_host_from_url(mn)
      if mn_host is not None:
        self.set(AUTH_MN[0], AUTH_MN[1], mn_host)
        print_info('Setting %s to "%s"' % (AUTH_MN[1], mn_host))
        save_data = True
    #
    if self.get(ORIG_MN[0], ORIG_MN[1]) is None:
      mn = self.get(MN_URL[0], MN_URL[1])
      mn_host = self._get_host_from_url(mn)
      if mn_host is not None:
        self.set(ORIG_MN[0], ORIG_MN[1], mn_host)
        print_info('Setting %s to "%s"' % (ORIG_MN[1], mn_host))
        save_data = True
    #
    if self.get(OWNER[0], OWNER[1]) is None:
      submitter = self.get(SUBMITTER[0], SUBMITTER[1])
      if submitter is not None:
        self.set(OWNER[0], OWNER[1], submitter)
        print_info('Setting %s to "%s"' % (OWNER[1], submitter))
        save_data = True
    if save_data:
      print_info('  *  Session values were changed, please "save" them!\n')

  def _get_host_from_url(self, url):
    if url is not None:
      url_dict = urlparse.urlparse(url)
      if url_dict.netloc is not None:
        host = url_dict.netloc
        ndx = host.find(":")
        if ndx > 0:
          host = host[:ndx]
        return host
    return None

  def assert_required_parameters_present(self, names):
    missing_parameters = []
    for name in names:
      value = self.get_with_implicit_section(name)
      if value is None:
        missing_parameters.append(name)
    if len(missing_parameters):
      msg_missing = 'Missing session parameters: {0}'.format(
        ', '.join(missing_parameters)
      )
      raise cli_exceptions.InvalidArguments(msg_missing)
