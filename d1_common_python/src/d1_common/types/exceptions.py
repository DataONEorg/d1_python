# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2010, 2011
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
"""Native objects for holding DataONE Exceptions

- Wrap the PyXB bindings with Exception based classes
- PyXB based XML serialization and deserialization
- Add deserialize to string and HTTP headers

Example of serialized DataONE Exception:

<error detailCode="1020" errorCode="404" name="NotFound" identifier="testpid">
<description>Attempted to perform operation on non-existing object</description>
<traceInformation>view_handler.py(128)
views.py(102)
auth.py(392)
auth.py(315)
</traceInformation>
</error>
"""

# Stdlib
import re
import string
import StringIO
import traceback
import xml.sax

# 3rd party
import pyxb
import pyxb.binding.datatypes as XS
import pyxb.utils.domutils

# D1
from d1_common.types import dataoneErrors
import d1_common.util


def deserialize(dataone_exception_xml):
  """Deserialize a DataONE Exception.
  """
  try:
    # Deserialize XML to a native Python object.
    dataone_exception_pyxb = dataoneErrors.CreateFromDocument(
      dataone_exception_xml
    )
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    msg = StringIO.StringIO()
    msg.write('Deserialization failed with exception:\n')
    msg.write(traceback.format_exc() + '\n')
    msg.write('On input:\n')
    msg.write(
      '<empty response>' if dataone_exception_xml == '' else dataone_exception_xml
    )
    # TODO: Instead raise a DataONE ServerFailure exception and put the
    # original exception in TraceInformation.
    raise DataONEExceptionException(msg.getvalue())

  trace = getattr(dataone_exception_pyxb, 'traceInformation', None)

  return create_exception_by_name(
    dataone_exception_pyxb.name,
    dataone_exception_pyxb.detailCode,
    dataone_exception_pyxb.description,
    trace,
    dataone_exception_pyxb.identifier,
    dataone_exception_pyxb.nodeId,
  )


def deserialize_from_headers(headers):
  """Deserialize a DataONE Exception that is stored in a map of HTTP headers
  (used in responses to HTTP HEAD requests).
  """
  return create_exception_by_name(
    _get_header(headers, 'DataONE-Exception-Name'),
    _get_header(headers, 'DataONE-Exception-DetailCode'),
    _get_header(headers, 'DataONE-Exception-Description'),
    _get_header(headers, 'DataONE-Exception-TraceInformation'),
    _get_header(headers, 'DataONE-Exception-Identifier'),
    _get_header(headers, 'DataONE-Exception-NodeId')
  )


def _get_header(headers, header):
  lower_case_headers = dict(
    zip(map(string.lower, headers.keys()), headers.values())
  )
  try:
    header = lower_case_headers[header.lower()]
  except LookupError:
    return None
  # As a header must be on a single line, the Python stack uses a
  # convention of replacing newlines with " / ".
  return header.replace(' / ', '\n')


def create_exception_by_name(
    name, detailCode="0", description='', traceInformation=None,
    identifier=None, nodeId=None
):
  name_exception_map = {
    u'AuthenticationTimeout': AuthenticationTimeout,
    u'IdentifierNotUnique': IdentifierNotUnique,
    u'InsufficientResources': InsufficientResources,
    u'InvalidCredentials': InvalidCredentials,
    u'InvalidRequest': InvalidRequest,
    u'InvalidSystemMetadata': InvalidSystemMetadata,
    u'InvalidToken': InvalidToken,
    u'NotAuthorized': NotAuthorized,
    u'NotFound': NotFound,
    u'NotImplemented': NotImplemented,
    u'ServiceFailure': ServiceFailure,
    u'UnsupportedMetadataType': UnsupportedMetadataType,
    u'UnsupportedType': UnsupportedType,
    u'SynchronizationFailed': SynchronizationFailed,
    u'VersionMismatch': VersionMismatch,
  }
  try:
    dataone_exception = name_exception_map[name]
  except LookupError:
    # The defined types are not enumerated in the schema so it is possible to
    # have a document that validates against the schema but is not a valid
    # DataONE exception.
    raise DataONEExceptionException(
      'Attempted to deserialize unknown DataONE Exception: {0}'.format(name)
    )
  return dataone_exception(
    detailCode, description, traceInformation, identifier, nodeId
  )


#===============================================================================


class DataONEException(Exception):
  """Base class for exceptions raised by DataONE.
  """

  @d1_common.util.utf8_to_unicode
  def __init__(
      self, errorCode, detailCode="0", description='', traceInformation=None,
      identifier=None, nodeId=None
  ):
    self.errorCode = errorCode
    self.detailCode = str(detailCode)
    self.description = description
    # trace information is stored internally as a unicode string that may or
    # may not be XML. Serialization will use the XML structure if it is valid,
    # otherwise it adds the content to the serialized structure as a
    # string.
    self._traceInformation = None
    self.traceInformation = traceInformation
    self.identifier = identifier
    self.nodeId = nodeId

  def __str__(self):
    msg = StringIO.StringIO()
    msg.write(self.format_message(u'name', self.name))
    msg.write(self.format_message(u'errorCode', self.errorCode))
    msg.write(self.format_message(u'detailCode', self.detailCode))
    msg.write(self.format_message(u'description', self.description))
    msg.write(self.format_message(u'traceInformation', self.traceInformation))
    msg.write(self.format_message(u'identifier', self.identifier))
    msg.write(self.format_message(u'nodeId', self.nodeId))
    return msg.getvalue()

  def friendly_format(self):
    """Serialize to a format more suitable for displaying to end users.
    """
    if self.description is not None:
      msg = self.description
    else:
      msg = 'errorCode: {0} / detailCode: {1}'.format(
        self.errorCode, self.detailCode
      )
    return self.format_message(self.name, msg)

  def format_message(self, tag, msg):
    """If msg is None, format to empty string.
    If msg has a single line, format to:
    tag: msg
    If msg has multiple lines, format to:
    tag:
      line 1
      line 2
    Msg is truncated to 1024 chars.
    """
    if msg is None:
      return
    msg = str(msg).strip()
    if len(msg) > 1024:
      msg = msg[:1024] + u' ...'
    if msg == '':
      return
    elif msg.count('\n') <= 1:
      return '{0}: {1}\n'.format(tag, msg.strip())
    else:
      return '{0}:\n  {1}\n'.format(tag, msg.replace('\n', '\n  ').strip())

  def serialize(self):
    dataone_exception_pyxb = dataoneErrors.error()
    dataone_exception_pyxb.name = self.__class__.__name__
    dataone_exception_pyxb.errorCode = self.errorCode
    dataone_exception_pyxb.detailCode = self.detailCode
    if self.description is not None:
      dataone_exception_pyxb.description = self.description
    if self._traceInformation is not None:
      elem = None
      try:
        elem = pyxb.utils.domutils.StringToDOM(self.traceInformation)
      except:
        elem = pyxb.utils.domutils.StringToDOM(
          "<x>" + self.traceInformation + "</x>"
        )
      dataone_exception_pyxb.traceInformation = elem.documentElement.firstChild
    if self.identifier is not None:
      dataone_exception_pyxb.identifier = self.identifier
    if self.nodeId is not None:
      dataone_exception_pyxb.nodeId = self.nodeId
    return dataone_exception_pyxb.toxml(encoding='utf-8')

  def toxml(self):
    return self.serialize()

  def serialize_to_headers(self):
    """Serialize to a list of HTTP headers (used in responses to HTTP HEAD
    requests).
    """
    headers = []
    self._append_header(
      headers, 'DataONE-Exception-Name', self.__class__.__name__
    )
    self._append_header(
      headers, 'DataONE-Exception-ErrorCode', str(self.errorCode)
    )
    self._append_header(
      headers, 'DataONE-Exception-DetailCode', str(self.detailCode)
    )
    self._append_header(
      headers, 'DataONE-Exception-Description', self.description
    )
    self._append_header(
      headers, 'DataONE-Exception-TraceInformation',
      self.traceInformation[:1024]
    )
    self._append_header(
      headers, 'DataONE-Exception-Identifier', self.identifier
    )
    self._append_header(headers, 'DataONE-Exception-NodeID', self.nodeId)
    return headers

  def _append_header(self, headers, k, v):
    if v is not None:
      headers.append((k, v.replace(u'\n', u' / ')))

  @property
  def name(self):
    return self.__class__.__name__

  @property
  def traceInformation(self):
    if self._traceInformation is None:
      return None
    return self._traceInformation

  @traceInformation.setter
  def traceInformation(self, traceInformation):
    if isinstance(traceInformation, XS.anyType):
      tmp = traceInformation.toxml(encoding='utf-8')
      # Remove the XML prolog from the start of the resulting string.
      traceInformation = re.sub(r'^<\?(.*)\?>', '', tmp)
      traceInformation = traceInformation.strip()
    self._traceInformation = traceInformation


#===============================================================================


class AuthenticationTimeout(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 408, detailCode, description, traceInformation, identifier, nodeId
    )


class IdentifierNotUnique(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 409, detailCode, description, traceInformation, identifier, nodeId
    )


class InsufficientResources(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 413, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidCredentials(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidRequest(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidSystemMetadata(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidToken(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class NotAuthorized(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class NotFound(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 404, detailCode, description, traceInformation, identifier, nodeId
    )
    #TODO: add link to resolve()


class NotImplemented(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 501, detailCode, description, traceInformation, identifier, nodeId
    )


class ServiceFailure(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 500, detailCode, description, traceInformation, identifier, nodeId
    )


class UnsupportedMetadataType(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class UnsupportedType(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class SynchronizationFailed(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 0, detailCode, description, traceInformation, identifier, nodeId
    )


class VersionMismatch(DataONEException):
  def __init__(
      self, detailCode, description=None, traceInformation=None,
      identifier=None, nodeId=None
  ):
    DataONEException.__init__(
      self, 409, detailCode, description, traceInformation, identifier, nodeId
    )


class DataONEExceptionException(Exception):
  """Hold exceptions raised when processing DataONEExceptions."""
  pass
