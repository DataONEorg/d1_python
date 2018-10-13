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
"""Hold and manipulate session variables.
"""

#> set
#         cli:
#           editor                        nano
#           verbose                       True
#         node:
#           cn-url                   https://cn.dataone.org/cn
#           mn-url                        http://127.0.0.1:8000
#         slice:
#           count                         1000
#           start                         0
#         auth:
#           anonymous                     False
#           cert-file                     /tmp/x509up_u1000
#           key-file                      None
#         search:
#           from-date                     None
#           query                         *:*
#           query-type                    solr
#           search-format-id              None
#           to-date                       None
#         sys-meta:
#           algorithm                     SHA-1
#           authoritative-mn              None
#           format-id                     text/xml
#           rights-holder                 public
#         access:
#           read                          "s1", "s2", "usera", "userb", "userc"
#         replication:
#           preferred member nodes        "p1", "p2", "p3"
#           blocked member nodes          "b1", "b2", "b3", "b4"
#           number of replicas            3
#           replication allowed           True
#

import ast
import copy
import os
import pickle
import platform

import d1_cli.impl.access_control as access_control
import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.operation_formatter as operation_formatter
import d1_cli.impl.replication_policy as replication_policy

import d1_common.checksum
import d1_common.const

# Names for variables.
VERBOSE_NAME = 'verbose'
EDITOR_NAME = 'editor'
CN_URL_NAME = 'cn-url'
MN_URL_NAME = 'mn-url'
START_NAME = 'start'
COUNT_NAME = 'count'
ANONYMOUS_NAME = 'anonymous'
CERT_FILENAME_NAME = 'cert-file'
KEY_FILENAME_NAME = 'key-file'
FORMAT_NAME = 'format-id'
OWNER_NAME = 'rights-holder'
AUTH_MN_NAME = 'authoritative-mn'
CHECKSUM_NAME = 'algorithm'
FROM_DATE_NAME = 'from-date'
TO_DATE_NAME = 'to-date'
SEARCH_FORMAT_NAME = 'search-format-id'
QUERY_ENGINE_NAME = 'query-type'
QUERY_STRING_NAME = 'query'

variable_type_map = {
  VERBOSE_NAME: bool,
  EDITOR_NAME: str,
  CN_URL_NAME: str,
  MN_URL_NAME: str,
  START_NAME: int,
  COUNT_NAME: int,
  ANONYMOUS_NAME: bool,
  CERT_FILENAME_NAME: str,
  KEY_FILENAME_NAME: str,
  FORMAT_NAME: str,
  OWNER_NAME: str,
  AUTH_MN_NAME: str,
  CHECKSUM_NAME: str,
  FROM_DATE_NAME: str,
  TO_DATE_NAME: str,
  SEARCH_FORMAT_NAME: str,
  QUERY_ENGINE_NAME: str,
  QUERY_STRING_NAME: str,
}

variable_defaults_map = {
  VERBOSE_NAME: True,
  EDITOR_NAME: 'notepad' if platform.system() == 'Windows' else 'nano',
  CN_URL_NAME: d1_common.const.URL_DATAONE_ROOT,
  MN_URL_NAME: d1_common.const.DEFAULT_MN_BASEURL,
  START_NAME: 0,
  COUNT_NAME: d1_common.const.DEFAULT_SLICE_SIZE,
  ANONYMOUS_NAME: True,
  CERT_FILENAME_NAME: None,
  KEY_FILENAME_NAME: None,
  FORMAT_NAME: None,
  OWNER_NAME: None,
  AUTH_MN_NAME: None,
  CHECKSUM_NAME: d1_common.const.DEFAULT_CHECKSUM_ALGORITHM,
  FROM_DATE_NAME: None,
  TO_DATE_NAME: None,
  SEARCH_FORMAT_NAME: None,
  QUERY_ENGINE_NAME: d1_common.const.DEFAULT_SEARCH_ENGINE,
  QUERY_STRING_NAME: '*:*',
}


class Session(object):
  def __init__(self, nodes, format_ids):
    self._nodes = nodes
    self._format_ids = format_ids
    self.reset()

  def reset(self):
    self._variables = self._create_default_variables()
    self._access_control = access_control.AccessControl()
    self._replication_policy = replication_policy.ReplicationPolicy()

  def get(self, variable):
    self._assert_valid_variable(variable)
    return self._variables[variable]

  def get_access_control(self):
    return self._access_control

  def get_replication_policy(self):
    return self._replication_policy

  def set(self, variable, value):
    self._assert_valid_variable(variable)
    self._assert_valid_variable_value(variable, value)
    self._variables[variable] = value

  def set_with_conversion(self, variable, value_string):
    """Convert user supplied string to Python type. Lets user use values such as
    True, False and integers. All variables can be set to None, regardless of
    type. Handle the case where a string is typed by the user and is not quoted,
    as a string literal.
    """
    self._assert_valid_variable(variable)
    try:
      v = ast.literal_eval(value_string)
    except (ValueError, SyntaxError):
      v = value_string
    if v is None or v == 'none':
      self._variables[variable] = None
    else:
      try:
        type_converter = variable_type_map[variable]
        value_string = self._validate_variable_type(
          value_string, type_converter
        )
        value = type_converter(value_string)
        self._variables[variable] = value
      except ValueError:
        raise cli_exceptions.InvalidArguments(
          'Invalid value for {}: {}'.format(variable, value_string)
        )

  def print_variable(self, variable):
    if not variable:
      self.print_all_variables()
    else:
      self.print_single_variable(variable)

  def print_single_variable(self, variable):
    self._assert_valid_variable(variable)
    cli_util.print_info('{}: {}'.format(variable, self.get(variable)))

  def print_all_variables(self):
    f = operation_formatter.OperationFormatter()
    d = copy.deepcopy(self._variables)
    d['replication'] = {
      'replication-allowed':
        self._replication_policy.get_replication_allowed(),
      'preferred-nodes':
        self._replication_policy.get_preferred(),
      'blocked-nodes':
        self._replication_policy.get_blocked(),
      'number-of-replicas':
        self._replication_policy.get_number_of_replicas(),
    }
    d['access'] = {
      'allow': self._access_control.get_list(),
    }
    f.print_operation(d)

    #return
    # Debug: Print types.
    #pprint.pprint(self._variables)
    #return
    #sections = self._get_session_section_ordering()
    #for section in sections:
    #  cli_util.print_info(u'{0}:'.format(section))
    #  for k in sorted(self._variables[section].keys()):
    #    cli_util.print_info(u'  {0: <30s}{1}'.format(k, self._variables[section][k][0]))
    #cli_util.print_info(str(self._access_control))
    #cli_util.print_info(str(self._replication_policy))
    #cli_util.print_info(u'\n')

  def load(self, pickle_file_path=None, suppress_error=False):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(cli_util.os.path.expanduser(pickle_file_path), 'rb') as f:
        self.__dict__.update(pickle.load(f))
      #self._verify_session_variables()
    except (NameError, IOError, ImportError) as e:
      if not suppress_error:
        cli_util.print_error(
          'Unable to load session from file: {}\n{}'.
          format(pickle_file_path, str(e))
        )

  def save(self, pickle_file_path=None, suppress_error=False):
    if pickle_file_path is None:
      pickle_file_path = self.get_default_pickle_file_path()
    try:
      with open(cli_util.os.path.expanduser(pickle_file_path), 'wb') as f:
        pickle.dump(self.__dict__, f, 2)
    except (NameError, IOError) as e:
      if not suppress_error:
        cli_util.print_error(
          'Unable to save session to file: {}\n{}'.
          format(pickle_file_path, str(e))
        )

  def is_verbose(self):
    verbose = self.get(VERBOSE_NAME)
    return (verbose is not None) and verbose

  def get_default_pickle_file_path(self):
    # This method of finding the user's home directory is safe on all platforms.
    return os.path.join(os.path.expanduser('~'), '.dataone_cli.conf')

  #
  # Private.
  #

  def _create_default_variables(self):
    return copy.deepcopy(variable_defaults_map)

  def _assert_valid_variable(self, variable):
    if variable not in self._variables:
      raise cli_exceptions.InvalidArguments(
        'Invalid session variable: {}'.format(variable)
      )

  def _validate_variable_type(self, value, type_converter):
    # Make sure booleans are "sane"
    if isinstance(type_converter, bool):
      if value in ('true', 'True', 't', 'T', 1, '1', 'yes', 'Yes'):
        return True
      elif value in ('false', 'False', 'f', 'F', 0, '0', 'no', 'No'):
        return False
      else:
        raise ValueError('Invalid boolean value: {}'.format(value))
    else:
      return value

  def _assert_valid_variable_value(self, variable, value):
    if variable == CHECKSUM_NAME:
      try:
        d1_common.checksum.get_checksum_calculator_by_dataone_designator(value)
      except LookupError:
        raise cli_exceptions.InvalidArguments(
          'Invalid checksum algorithm: {}'.format(value)
        )
    elif variable == CN_URL_NAME:
      # TODO: Add warning if URL is not a known CN / environment
      pass
    elif variable == MN_URL_NAME:
      cn_base_url = self.get(CN_URL_NAME)
      if value not in [
          n[2] for n in self._nodes.get(cn_base_url) if n[0] == 'mn'
      ]:
        if not cli_util.confirm(
            '"{}" is not a known DataONE Member Node. Use anyway?'.
            format(value)
        ):
          raise cli_exceptions.InvalidArguments('Member Node update cancelled')
    elif variable == FORMAT_NAME:
      cn_base_url = self.get(CN_URL_NAME)
      if value not in self._format_ids.get(cn_base_url):
        raise cli_exceptions.InvalidArguments(
          'Invalid Object Format ID: {}'.format(value)
        )
