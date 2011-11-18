# Stdlib.
import ast
import logging
import os
import pprint
import ConfigParser

# D1.
import d1_common.const

# App.
import cli_exceptions
import system_metadata
import access_control


class session(object):
  def __init__(self):
    self.session = self.get_default_session()
    self.access_control = access_control.access_control()

  def reset(self):
    self.__init__()

  def get_default_session(self):
    return {
      'cli': {
        'pretty': (True, bool),
        'verbose': (False, bool),
      },
      'node': {
        'dataone_url': (d1_common.const.URL_DATAONE_ROOT, str),
        'mn_url': ('https://localhost/mn/', str),
      },
      'slice': {
        'start': (0, int),
        'count': (d1_common.const.MAX_LISTOBJECTS, int),
      },
      'auth': {
        'anonymous': (False, bool),
        'cert_path': (None, str),
        'key_path': (None, str),
      },
      'sysmeta': {
        'pid': (None, str),
        'object_format': (None, str),
        'submitter': (None, str),
        'rightsholder': (None, str),
        'origin_member_node': (None, str),
        'authoritative_member_node': (None, str),
        'algorithm': (d1_common.const.DEFAULT_CHECKSUM_ALGORITHM, str),
      },
      'search': {
        'start_time': (None, str),
        'end_time': (None, str),
        'search_object_format': (None, str),
        'query': ('*:*', str),
        'fields': (None, str),
      },
    }

  def get_session_section_ordering(self):
    return 'cli', 'node', 'slice', 'auth', 'sysmeta', 'search'

  def get_default_ini_file_path(self):
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

  #=============================================================================
  # Public.
  #=============================================================================

  def get(self, section, name):
    self._assert_valid_session_parameter(section, name)
    return self.session[section][name][0]

  def get_with_implicit_section(self, name):
    section = self._find_section_containing_session_parameter(name)
    return self.get(section, name)

  def set(self, section, name, value):
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
    except ValueError:
      v = value_string
    if v is None:
      self.set(section, name, None)
    else:
      try:
        type_converter = self.session[section][name][1]
        self.set(section, name, type_converter(v))
      except ValueError as e:
        raise cli_exceptions.InvalidArguments(
          'Invalid value for {0} / {1}: {2}'.format(section, name, value_string)
        )

  def set_with_conversion_implicit_section(self, name, value_string):
    section = self._find_section_containing_session_parameter(name)
    self.set_with_conversion(section, name, value_string)

  def access_control_add_allowed_subject(self, subject, permission):
    self.access_control.add_allowed_subject(subject, permission)

  def access_control_remove_allowed_subject(self, subject):
    self.access_control.remove_allowed_subject(subject)

  def access_control_allow_public(self, allow):
    self.access_control.allow_public(allow)

  def access_control_remove_all_allowed_subjects(self, line):
    self.access_control.remove_all_allowed_subjects(line)

  def print_single_parameter(self, name):
    section = self._find_section_containing_session_parameter(name)
    print '{0: <30s}{1}'.format(name, self.get(section, name))

  def print_all_parameters(self):
    # Debug: Print types.
    pprint.pprint(self.session)
    #return
    sections = self.get_session_section_ordering()
    for section in sections:
      print '{0}:'.format(section)
      for k in sorted(self.session[section].keys()):
        print '  {0: <30s}{1}'.format(k, self.session[section][k][0])
    print str(self.access_control)

  def print_parameter(self, name):
    if name.strip() == '':
      self.print_all_parameters()
    else:
      self.print_single_parameter(name)

  def load_session_from_ini_file(self, suppress_error=False, ini_file_path=None):
    if ini_file_path is None:
      ini_file_path = self.get_default_ini_file_path()
    logging.debug("Loading session from .ini file: {0}".format(ini_file_path))
    ini = ConfigParser.RawConfigParser()
    file_count = len(ini.read([ini_file_path]))
    if file_count == 1:
      self.ini_to_session(ini)
      self.access_control.from_ini(ini)
      logging.debug('Loaded session from .ini file: {0}'.format(ini_file_path))
    else:
      if not suppress_error:
        logging.error('Unable to load session from .ini file: {0}'.format(ini_file_path))

  def session_to_ini(self):
    ini = ConfigParser.RawConfigParser()
    sections = self.get_session_section_ordering()
    for section in sections:
      ini.add_section(section)
      for k in sorted(self.session[section].keys()):
        ini.set(section, k, repr(self.session[section][k][0]))
    return ini

  def add_access_control_to_ini(self, ini):
    self.access_control.add_to_ini(ini)

  def save_session_to_ini_file(self, ini_file_path=None):
    if ini_file_path is None:
      ini_file_path = self.get_default_ini_file_path()
    logging.debug('Saving session to .ini file: {0}'.format(ini_file_path))
    ini = self.session_to_ini()
    self.add_access_control_to_ini(ini)
    with open(ini_file_path, 'wb') as f:
      ini.write(f)

  def ini_to_session(self, ini):
    for section in self.session:
      for name in self.session[section]:
        self.set_with_conversion(section, name, ini.get(section, name))

  def create_system_metadata(self, pid, checksum, size):
    access_policy = self.access_control.to_pyxb()
    sysmeta_creator = system_metadata.system_metadata()
    sysmeta = sysmeta_creator.create_pyxb_object(self, pid, size, checksum, access_policy)

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
