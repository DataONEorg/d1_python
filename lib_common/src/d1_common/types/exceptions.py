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

traceInformation:

traceInformation is an xs:anyType, meaning that is essentially the root of a new
XML document of arbitrary complexity. Since the contents of the elements are
unknown at the time when the PyXB bindings are created, PyXB cannot
automatically serialize and deserialize the traceInformation field together with
the rest of the DataONEException XML type.

To make it easier to use the traceInformation element, we support a special case
where it can be read and written as a single string of bytes, where the contents
are application specific. Any other content must be generated and parsed as XML
by the user.

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

import io
import logging
import traceback

import d1_common.type_conversions
import d1_common.util
import d1_common.xml
from d1_common.types import dataoneErrors


def xml_is_dataone_exception(xml_str):
  try:
    return pyxb_is_dataone_exception(deserialize(xml_str))
  except ServiceFailure:
    return False


def pyxb_is_dataone_exception(obj_pyxb):
  return isinstance(obj_pyxb, DataONEException)


def deserialize(dataone_exception_xml):
  """Deserialize a DataONE Exception XML doc.
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
    x = create_exception_by_name(
      dataone_exception_pyxb.name,
      dataone_exception_pyxb.detailCode,
      dataone_exception_pyxb.description,
      _get_trace_information_content(dataone_exception_pyxb),
      dataone_exception_pyxb.identifier,
      dataone_exception_pyxb.nodeId,
    )
    return x


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
    list(
      zip(list(map(str.lower, list(headers.keys()))), list(headers.values()))
    )
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


# def _prep_trace(trace_information):
#   return xml.sax.saxutils.escape(trace_information)


def _get_trace_information_content(err_pyxb):
  assert d1_common.xml.is_pyxb(err_pyxb)
  if err_pyxb.traceInformation is None:
    return None
  try:
    return '\n'.join(err_pyxb.traceInformation.content())
  except TypeError:
    return d1_common.xml.serialize_to_xml_str(
      err_pyxb.traceInformation, pretty=True, strip_prolog=True
    )


# def _deserialize_trace_information(self, trace_information):
#   """To PyXB TraceInformation
#   <pyxb.binding.datatypes.anyType object at 0x7fe77a9c19b0>"""
#   if trace_information is None:
#     return None
#   if isinstance(trace_information, str):
#     import xml.dom.minidom
#     return xml.dom.minidom.parseString(
#       "<traceInformation><value>" + xml.sax.saxutils.escape(
#         trace_information) + "</value></traceInformation>")
#   return 111

#===============================================================================


class DataONEException(Exception):
  """Base class for exceptions raised by DataONE.
  """

  def __init__(
      self, errorCode, detailCode='0', description='', traceInformation=None,
      identifier=None, nodeId=None
  ):
    # self._traceInformation = None
    self.errorCode = errorCode
    self.detailCode = detailCode
    self.description = description
    self.traceInformation = traceInformation
    self.identifier = identifier
    self.nodeId = nodeId

  def __repr__(self):
    for attr_str in [
        'errorCode',
        'detailCode',
        'description',
        'traceInformation',
        'identifier',
        'nodeId',
    ]:
      logging.error(type(getattr(self, attr_str)))

    s = '{}({})'.format(
      self.__class__.__name__, ', '.join([
        '{}="{}"'.format(attr_str, getattr(self, attr_str))
        for attr_str in [
          'errorCode',
          'detailCode',
          'description',
          'traceInformation',
          'identifier',
          'nodeId',
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
    msg = io.StringIO()
    msg.write(self.fmt('name', self.name))
    msg.write(self.fmt('errorCode', self.errorCode))
    msg.write(self.fmt('detailCode', self.detailCode))
    msg.write(self.fmt('description', self.description))
    msg.write(self.fmt('traceInformation', self.traceInformation))
    msg.write(self.fmt('identifier', self.identifier))
    msg.write(self.fmt('nodeId', self.nodeId))
    return msg.getvalue()

  def fmt(self, tag, msg):
    msg = msg or '<unset>'
    msg = str(msg)
    msg = msg.strip()
    if not msg:
      return
    if len(msg) > 2048:
      msg = msg[:1024] + '...'
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

  def serialize_to_transport(self, encoding='utf-8', xslt_url=None):
    """Serialize to UTF-8 encoded XML bytes with prolog
    - {xslt_url} is an optional link to an XSLT stylesheet. If provided, a
    processing instruction for the stylesheet is included in the XML prolog.
    """
    assert encoding in ('utf-8', 'UTF-8')
    dataone_exception_pyxb = self.get_pyxb()
    return d1_common.xml.serialize_to_transport(
      dataone_exception_pyxb, xslt_url=xslt_url
    )

  def serialize_to_display(self, xslt_url=None):
    """Serialize to a pretty printed Unicode str, suitable for display
    - {xslt_url} is an optional link to an XSLT stylesheet. If provided, a
    processing instruction for the stylesheet is included in the XML prolog.
    """
    return d1_common.xml.serialize_to_xml_str(
      self.get_pyxb(), pretty=True, xslt_url=xslt_url
    )

  def encode(self, encoding='utf-8'):
    return self.serialize_to_transport(encoding)

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

  def get_pyxb(self):
    """Generate PyXB object"""
    dataone_exception_pyxb = dataoneErrors.error()
    dataone_exception_pyxb.name = self.__class__.__name__
    dataone_exception_pyxb.errorCode = self.errorCode
    dataone_exception_pyxb.detailCode = self.detailCode
    if self.description is not None:
      dataone_exception_pyxb.description = self.description
    dataone_exception_pyxb.traceInformation = self.traceInformation
    if self.identifier is not None:
      dataone_exception_pyxb.identifier = self.identifier
    if self.nodeId is not None:
      dataone_exception_pyxb.nodeId = self.nodeId
    return dataone_exception_pyxb

  def _format_header(self, v):
    if v is None:
      return ''
    else:
      return str(v)[:1024].replace('\n', ' / ')

  @property
  def name(self):
    return self.__class__.__name__


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
