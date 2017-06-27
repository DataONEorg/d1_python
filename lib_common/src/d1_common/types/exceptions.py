# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

- Wrap the PyXB client with Exception based classes
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

from __future__ import absolute_import

import logging
import re
import string
import StringIO
import traceback

import pyxb
import pyxb.binding.datatypes as XS
import pyxb.utils.domutils

import d1_common.util
import d1_common.xml
from d1_common.types import dataoneErrors


def deserialize(dataone_exception_xml):
  """Deserialize a DataONE Exception.
  """
  # logging.debug('dataone_exception_xml="{}"'
  # .format(d1_common.xml.pretty_xml(dataone_exception_xml)))
  try:
    dataone_exception_pyxb = d1_common.xml.deserialize_d1_exc(
      dataone_exception_xml
    )
  except ValueError as e:
    raise ServiceFailure(
      detailCode=0,
      description='Deserialization failed. error="{}" doc="{}"'.format(
        str(e),
        '<empty response>'
        if not dataone_exception_xml else dataone_exception_xml,
      ),
      traceInformation=traceback.format_exc(),
    )
  else:
    # logging.debug('dataone_exception_pyxb="{}"'
    # .format(d1_common.xml.pretty_pyxb(dataone_exception_pyxb)))
    return create_exception_by_name(
      dataone_exception_pyxb.name,
      dataone_exception_pyxb.detailCode,
      dataone_exception_pyxb.description,
      getattr(dataone_exception_pyxb, 'traceInformation', None),
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
    name, detailCode='0', description='', traceInformation=None,
    identifier=None, nodeId=None
):
  try:
    dataone_exception = globals()[name]
  except LookupError:
    # The defined types are not enumerated in the schema so it is possible to
    # have a document that validates against the schema but is not a valid
    # DataONE exception.
    dataone_exception = ServiceFailure
  return dataone_exception(
    detailCode, description, traceInformation, identifier, nodeId
  )


def create_exception_by_error_code(
    errorCode, detailCode='0', description='', traceInformation=None,
    identifier=None, nodeId=None
):
  try:
    dataone_exception = ERROR_CODE_TO_EXCEPTION_DICT[errorCode]
  except LookupError:
    # The defined types are not enumerated in the schema so it is possible to
    # have a document that validates against the schema but is not a valid
    # DataONE exception. In this case, we create a ServiceFailure.
    dataone_exception = ServiceFailure
  return dataone_exception(
    detailCode, description, traceInformation, identifier, nodeId
  )


#===============================================================================


class DataONEException(Exception):
  """Base class for exceptions raised by DataONE.
  """
  #@d1_common.util.utf8_to_unicode
  @d1_common.util.unicode_to_utf8
  def __init__(
      self, errorCode, detailCode='0', description='', traceInformation=None,
      identifier=None, nodeId=None
  ):
    self.errorCode = errorCode
    self.detailCode = detailCode
    self.description = description
    # trace information is stored internally as a unicode string that may or
    # may not be XML. Serialization will use the XML structure if it is valid,
    # otherwise it adds the content to the serialized structure as a
    # string.
    self._traceInformation = None
    self.traceInformation = traceInformation
    self.identifier = identifier
    self.nodeId = nodeId

  def __repr__(self):
    for attr_str in [
        'errorCode', 'detailCode', 'description', 'identifier', 'nodeId',
        'traceInformation'
    ]:
      logging.error(type(getattr(self, attr_str)))

    s = '{}({})'.format(
      self.__class__.__name__, ', '.join([
        '{}="{}"'.format(attr_str, getattr(self, attr_str))
        for attr_str in [
          'errorCode', 'detailCode', 'description', 'identifier', 'nodeId',
          'traceInformation'
        ]
      ])
    )

    logging.error(s)
    return s

  def __str__(self):
    """If msg is None, format to empty string.
    If msg has a single line, format to:
    tag: msg
    If msg has multiple lines, format to:
    tag:
      line 1
      line 2
    Msg is truncated to 1024 chars.
    """
    msg = StringIO.StringIO()
    msg.write(self.fmt('name', self.name))
    msg.write(self.fmt('errorCode', self.errorCode))
    msg.write(self.fmt('detailCode', self.detailCode))
    msg.write(self.fmt('description', self.description))
    msg.write(self.fmt('traceInformation', self.traceInformation))
    msg.write(self.fmt('identifier', self.identifier))
    msg.write(self.fmt('nodeId', self.nodeId))
    return msg.getvalue()

  def fmt(self, tag, msg):
    if msg is None:
      return
    # assert isinstance(tag, unicode)
    # assert isinstance(msg, unicode)
    if isinstance(msg, unicode):
      msg = msg.encode('utf-8')
    elif not isinstance(msg, basestring):
      msg = str(msg)
    msg = msg.strip()
    if not msg:
      return
    if len(msg) > 2048:
      msg = msg.decode('utf-8')[:1024].encode('utf-8') + ' ...'
    if msg.count('\n') <= 1:
      return '{}: {}\n'.format(tag, msg.strip())
    else:
      return '{}:\n  {}\n'.format(tag, msg.replace('\n', '\n  ').strip())

  def friendly_format(self):
    """Serialize to a format more suitable for displaying to end users.
    """
    if self.description is not None:
      msg = self.description
    else:
      msg = 'errorCode: {} / detailCode: {}'.format(
        self.errorCode, self.detailCode
      )
    return self.fmt(self.name, msg)

  def serialize(self):
    dataone_exception_pyxb = dataoneErrors.error()
    dataone_exception_pyxb.name = self.__class__.__name__
    dataone_exception_pyxb.errorCode = self.errorCode
    dataone_exception_pyxb.detailCode = self.detailCode
    if self.description is not None:
      dataone_exception_pyxb.description = self.description
    if self._traceInformation is not None:
      try:
        trace_info_el = pyxb.utils.domutils.StringToDOM(self.traceInformation)
      except Exception:
        trace_info_el = pyxb.utils.domutils.StringToDOM(
          u"<value>" + self.traceInformation + u"</value>"
        )
      dataone_exception_pyxb.traceInformation = (
        trace_info_el.documentElement.firstChild
      )
    if self.identifier is not None:
      dataone_exception_pyxb.identifier = self.identifier
    if self.nodeId is not None:
      dataone_exception_pyxb.nodeId = self.nodeId
    # TODO: Check if this is still needed
    #pyxb.utils.domutils.BindingDOMSupport.SetDefaultNamespace(None)
    return dataone_exception_pyxb.toxml('utf-8')

  def toxml(self):
    return self.serialize()

  def serialize_to_headers(self):
    """Serialize to a list of HTTP headers
    Used in responses to HTTP HEAD requests.
    """
    return {
      'DataONE-Exception-Name':
        self.__class__.__name__,
      'DataONE-Exception-ErrorCode':
        self._format_header(self.errorCode),
      'DataONE-Exception-DetailCode':
        self._format_header(self.detailCode),
      'DataONE-Exception-Description':
        self._format_header(self.description),
      'DataONE-Exception-TraceInformation':
        self._format_header(self.traceInformation),
      'DataONE-Exception-Identifier':
        self._format_header(self.identifier),
      'DataONE-Exception-NodeID':
        self._format_header(self.nodeId),
    }

  def _format_header(self, v):
    if v is None:
      return ''
    else:
      return str(v)[:1024].replace('\n', ' / ')

  @property
  def name(self):
    return self.__class__.__name__

  @property
  def traceInformation(self):
    if self._traceInformation is None:
      return None
    return self._traceInformation

  @traceInformation.setter
  def traceInformation(self, trace_information):
    if isinstance(trace_information, XS.anyType):
      tmp = trace_information.toxml('utf-8')
      # Remove the XML prolog from the start of the resulting string.
      trace_information = re.sub(r'^<\?(.*)\?>', '', tmp)
      trace_information = trace_information.strip()
    self._traceInformation = trace_information


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
    # TODO: add link to resolve()
    DataONEException.__init__(
      self, 404, detailCode, description, traceInformation, identifier, nodeId
    )


# noinspection PyShadowingBuiltins
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


ERROR_CODE_TO_EXCEPTION_DICT = {
  # 400: InvalidRequest,
  400: InvalidSystemMetadata,
  # 400: UnsupportedMetadataType,
  # 400: UnsupportedType,
  # 401: InvalidCredentials,
  # 401: InvalidToken,
  401: NotAuthorized,
  404: NotFound,
  408: AuthenticationTimeout,
  409: IdentifierNotUnique,
  # 409: VersionMismatch,
  413: InsufficientResources,
  500: ServiceFailure,
  501: NotImplemented,
}
