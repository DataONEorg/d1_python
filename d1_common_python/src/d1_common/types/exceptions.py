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
'''
Module d1_common.types.exceptions
=================================
:Synopsis:
  - Native objects for holding DataONE Exceptions
  - XML Serialization and deserialization of DataONE Exceptions
:Created: 2010-04-12
:Author: DataONE (Vieglais, Dahl)
'''

# Stdlib.
import inspect
import string
import sys
import traceback
import xml.sax
import StringIO

# 3rd party.
import pyxb
import pyxb.utils.domutils

# D1.
import d1_common.types.generated.dataoneErrors as dataoneErrors
import d1_common.util
'''
Example of serialized DataONE Exception:

<error detailCode="1020" errorCode="404" name="NotFound" identifier="testpid">
<description>Attempted to perform operation on non-existing object</description>
<traceInformation>view_handler.py(128)
views.py(102)
lock_pid.py(110)
auth.py(392)
auth.py(315)
</traceInformation>
</error>
'''


class DataONEExceptionException(Exception):
  '''Pass exceptions related to processing DataONEExceptions.'''

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

# ==============================================================================


def deserialize(dataone_exception_xml):
  '''Deserialize a DataONE Exception.
  :param dataone_exception_xml: XML Serialized DataONE Exception in UTF-8.
  :type dataone_exception_xml: str
  :returns: Native DataONE Exception Object.
  :return type: DataONEException subclass
  '''
  try:
    dataone_exception_pyxb = dataoneErrors.CreateFromDocument(dataone_exception_xml)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    msg = StringIO.StringIO()
    msg.write('Deserialization failed with exception:\n')
    msg.write(traceback.format_exc() + '\n')
    msg.write('On input:\n')
    msg.write(
      '<empty response>' if dataone_exception_xml == '' else dataone_exception_xml
    )
    raise DataONEExceptionException(msg.getvalue())

  try:
    trace = dataone_exception_pyxb.traceInformation.toxml(),
  except AttributeError:
    trace = ''

  return _create_exception_by_name(
    dataone_exception_pyxb.name, dataone_exception_pyxb.detailCode,
    dataone_exception_pyxb.description, trace, dataone_exception_pyxb.identifier,
    dataone_exception_pyxb.nodeId
  )


def deserialize_from_headers(headers):
  '''Deserialize a DataONE Exception that is stored in a map of HTTP headers
  (used in responses to HTTP HEAD requests).
  '''
  return _create_exception_by_name(
    _get_header(headers, 'DataONE-Exception-Name'),
    _get_header(headers, 'DataONE-Exception-DetailCode'),
    _get_header(headers, 'DataONE-Exception-Description'),
    _get_header(headers, 'DataONE-Exception-TraceInformation'),
    _get_header(headers, 'DataONE-Exception-Identifier'),
    _get_header(headers, 'DataONE-Exception-NodeId')
  )


def _get_header(headers, header):
  lower_case_headers = dict(zip(map(string.lower, headers.keys()), headers.values()))
  try:
    header = lower_case_headers[header.lower()]
  except LookupError:
    return None
  # As a header must be on a single line, the Python stack uses a
  # convention of replacing newlines with " / ".
  return header.replace(' / ', '\n')


def _create_exception_by_name(
  name, detailCode, description, traceInformation, identifier, nodeId
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
      'Attempted to deserialize unknown DataONE Exception: {0}'\
      .format(name))
  return dataone_exception(detailCode, description, traceInformation, identifier, nodeId)


class DataONEException(Exception):
  '''Base class for exceptions raised by DataONE.
  '''

  @d1_common.util.utf8_to_unicode
  def __init__(
    self, errorCode, detailCode, description, traceInformation, identifier, nodeId
  ):
    self.errorCode = errorCode
    self.detailCode = str(detailCode)
    self.description = description
    self.traceInformation = traceInformation
    self.identifier = identifier
    self.nodeId = nodeId

  def __str__(self):
    msg = StringIO.StringIO()
    msg.write(u'name: {0}\n'.format(self.name))
    msg.write(u'errorCode: {0}\n'.format(self.errorCode))
    msg.write(u'detailCode: {0}\n'.format(str(self.detailCode)))
    if self.description is not None:
      msg.write(u'description: {0}\n'.format(self.description))
    if self.traceInformation is not None:
      msg.write(u'traceInformation: {0}\n'.format(self.traceInformation))
    if self.identifier is not None:
      msg.write(u'PID: {0}\n'.format(self.identifier))
    if self.nodeId is not None:
      msg.write(u'NodeID: {0}\n'.format(self.nodeId))
    # The unit test framework that comes with Python 2.6 has a bug that has been
    # fixed in later versions. http://bugs.python.org/issue8313. The bug causes
    # stack traces containing Unicode to be shown as "unprintable". So, for now,
    # string representations of exceptions are forced to ascii, where non-ascii
    # characters are replaced with a box.
    return unicode(msg.getvalue()).encode("utf-8")

  def friendly_format(self):
    '''Serialize to a format more suitable for displaying to end users.
    '''
    if self.description is not None:
      return '{0}: {1}'.format(self.name, self.description)
    else:
      return '{0}: errorCode: {1} / detailCode: {2}'.format(
        self.name, self.errorCode, self.detailCode
      )

  def serialize(self):
    dataone_exception_pyxb = dataoneErrors.error()
    dataone_exception_pyxb.name = self.__class__.__name__
    dataone_exception_pyxb.errorCode = self.errorCode
    dataone_exception_pyxb.detailCode = self.detailCode
    if self.description is not None:
      dataone_exception_pyxb.description = self.description
    if self.traceInformation is not None:
      s = pyxb.utils.domutils.StringToDOM(
        '<value>' + self.traceInformation + '</value>'
      ).documentElement
      dataone_exception_pyxb.traceInformation = s
    if self.identifier is not None:
      dataone_exception_pyxb.identifier = self.identifier
    if self.nodeId is not None:
      dataone_exception_pyxb.nodeId = self.nodeId
    return dataone_exception_pyxb.toxml()

  def serialize_to_headers(self):
    '''Serialize to a list of HTTP headers (used in responses to HTTP HEAD
    requests).
    '''
    headers = []
    self._append_header(headers, 'DataONE-Exception-Name', self.__class__.__name__)
    self._append_header(headers, 'DataONE-Exception-ErrorCode', str(self.errorCode))
    self._append_header(headers, 'DataONE-Exception-DetailCode', str(self.detailCode))
    self._append_header(headers, 'DataONE-Exception-Description', self.description)
    self._append_header(
      headers, 'DataONE-Exception-TraceInformation', self.traceInformation
    )
    self._append_header(headers, 'DataONE-Exception-Identifier', self.identifier)
    self._append_header(headers, 'DataONE-Exception-NodeID', self.nodeId)
    return headers

  def _append_header(self, headers, k, v):
    if v is not None:
      headers.append((k, v.replace(u'\n', u' / ')))

  @property
  def name(self):
    return self.__class__.__name__


class AuthenticationTimeout(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 408, detailCode, description, traceInformation, identifier, nodeId
    )


class IdentifierNotUnique(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 409, detailCode, description, traceInformation, identifier, nodeId
    )


class InsufficientResources(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 413, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidCredentials(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidRequest(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidSystemMetadata(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class InvalidToken(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class NotAuthorized(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 401, detailCode, description, traceInformation, identifier, nodeId
    )


class NotFound(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 404, detailCode, description, traceInformation, identifier, nodeId
    )
    #TODO: add link to resolve()


class NotImplemented(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 501, detailCode, description, traceInformation, identifier, nodeId
    )


class ServiceFailure(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 500, detailCode, description, traceInformation, identifier, nodeId
    )


class UnsupportedMetadataType(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class UnsupportedType(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 400, detailCode, description, traceInformation, identifier, nodeId
    )


class SynchronizationFailed(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 0, detailCode, description, traceInformation, identifier, nodeId
    )


class VersionMismatch(DataONEException):
  def __init__(
    self,
    detailCode,
    description=None,
    traceInformation=None,
    identifier=None,
    nodeId=None
  ):
    DataONEException.__init__(
      self, 409, detailCode, description, traceInformation, identifier, nodeId
    )
