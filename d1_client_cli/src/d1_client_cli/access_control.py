# Stdlib.
import logging
import shlex

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
import cli_exceptions


class access_control():
  def __init__(self):
    self.allow = {}
    self.public = False

  def __repr__(self):
    return self.to_comma_string()

  def __str__(self):
    return self._pretty_format()

  def _get_valid_permissions(self):
    return ('read', 'write', 'changePermission', 'execute', 'replicate')

  def _clear(self):
    self.allow.clear()
    self.public = False

  def _list_to_pyxb(self):
    access_policy = dataoneTypes.accessPolicy()
    for subject in sorted(self.allow.keys()):
      access_rule = dataoneTypes.AccessRule()
      access_rule.subject.append(subject)
      permission = dataoneTypes.Permission(self.allow[subject])
      access_rule.permission.append(permission)
      access_policy.append(access_rule)
    return access_policy

  def _add_public_subject(self, access_policy):
    access_rule = dataoneTypes.AccessRule()
    access_rule.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission = dataoneTypes.Permission('read')
    access_rule.permission.append(permission)
    access_policy.append(access_rule)
    return access_policy

  def _add_allowed_subject(self, subject, permission):
    self.allow[subject] = permission

  def _pretty_format(self):
    lines = []
    format = '  {0: <30s}{1}'
    if not len(lines):
      lines.append(format.format('submitter', 'full access'))
    if self.public:
      lines.append(format.format('public', 'read'))
    for subject in sorted(self.allow.keys()):
      lines.append(format.format(subject, self.allow[subject]))
    return 'access:\n' + '\n'.join(lines) + '\n'

  # ============================================================================

  def to_pyxb(self):
    access_policy = self._list_to_pyxb()
    if self.public:
      access_policy = self._add_public_subject(access_policy)
    return access_policy

  def to_xml(self):
    return self.to_pyxb().toxml()

  def from_xml(self, xml):
    access_policy = dataoneTypes.CreateFromDocument(xml)
    #print dir(access_policy)
    for access_rule in access_policy.allow:
      subject = access_rule.subject[0].value()
      permission = access_rule.permission[0]
      self._add_allowed_subject(subject, permission)

  def to_comma_string(self):
    lines = []
    for subject in sorted(self.allow.keys()):
      lines.append('{0}={1}'.format(subject, self.allow[subject]))
    return ','.join(lines)

  def from_comma_string(self, comma_string):
    self.allow.clear()
    lines = comma_string.split(',')
    for line in lines:
      line = line.strip()
      if line == '':
        continue
      subject, permission = line.split('=')
      self._add_allowed_subject(subject, permission)

  def add_to_ini(self, ini):
    ini.add_section('access')
    ini.set('access', 'allow', self.to_comma_string())
    ini.set('access', 'public', self.public)

  def from_ini(self, ini):
    self.from_comma_string(ini.get('access', 'allow'))
    self.public = ini.getboolean('access', 'public')

  def clear(self):
    self._clear()

  def add_allowed_subject(self, subject, permission):
    if permission is None:
      permission = 'read'
    if permission not in self._get_valid_permissions():
      msg = 'Invalid permission: {0}. Must be one of: {1}'\
        .format(permission, ', '.join(self._get_valid_permissions()))
      raise cli_exceptions.InvalidArguments(msg)
    self._add_allowed_subject(subject, permission)

  def remove_allowed_subject(self, subject):
    try:
      del self.allow[subject]
    except KeyError:
      raise cli_exceptions.InvalidArguments('Subject not in access control list: {0}'\
        .format(subject))

  def allow_public(self, allow):
    self.public = allow

  def remove_all_allowed_subjects(self, line):
    self.clear()
    self.allow_public(False)
