# Stdlib.
import datetime
import logging

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# 3rd party.
import pyxb

# App.
import cli_exceptions


class MissingSysmetaParameters(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class system_metadata():
  def __init__(self):
    pass

  def __repr__(self):
    return self.to_xml()

  def _get_missing_sysmeta_session_parameters(self, sysmeta):
    missing_values = []
    for k in sorted(sysmeta.keys()):
      if sysmeta[k][0] is None:
        missing_values.append(k)
    return missing_values

  def _assert_no_missing_sysmeta_session_parameters(self, sysmeta):
    missing_values = self._get_missing_sysmeta_session_parameters(sysmeta)
    if len(missing_values):
      msg = 'Missing system metadata parameters: {0}'.format(', '.join(missing_values))
      raise MissingSysmetaParameters(msg)

  def _create_pyxb_object(self, session, pid, size, checksum, access_policy):
    sysmeta = dataoneTypes.systemMetadata()
    sysmeta.serialVersion = 1
    sysmeta.identifier = pid
    sysmeta.formatId = session.get('sysmeta', 'object_format')
    sysmeta.size = size
    sysmeta.submitter = session.get('sysmeta', 'submitter')
    sysmeta.rightsHolder = session.get('sysmeta', 'rightsholder')
    sysmeta.checksum = dataoneTypes.checksum(checksum)
    sysmeta.checksum.algorithm = session.get('sysmeta', 'algorithm')
    sysmeta.dateUploaded = datetime.datetime.now()
    sysmeta.dateSysMetadataModified = datetime.datetime.now()
    sysmeta.originMemberNode = session.get('sysmeta', 'origin_member_node')
    sysmeta.authoritativeMemberNode = \
      session.get('sysmeta', 'authoritative_member_node')
    sysmeta.accessPolicy = access_policy
    #pyxb.RequireValidWhenGenerating(False)
    return sysmeta

  def create_pyxb_object(self, session, pid, size, checksum, access_policy):
    self._assert_no_missing_sysmeta_session_parameters(session.session['sysmeta'])
    return self._create_pyxb_object(session, pid, size, checksum, access_policy)

  def to_xml(self):
    return self.to_pyxb().toxml()
