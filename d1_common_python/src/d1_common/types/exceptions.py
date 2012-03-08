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
import sys
import traceback
import xml.sax
import StringIO

# 3rd party.
import pyxb

# D1.
import d1_common.types.generated.dataoneErrors as dataoneErrors
'''
Example of serialized DataONE Exception:

<error detailCode="1020" errorCode="404" name="NotFound" pid="testpid">
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
    dataone_exception = name_exception_map[dataone_exception_pyxb.name]
  except LookupError:
    # The dataone_exception_xml complied to the schema but the name did not
    # match any known DataONE exception types. This can happen because the
    # defined types are not enumerated in the schema.
    raise DataONEExceptionException(
      'Attempted to deserialize unknown DataONE Exception: {0}'\
      .format(dataone_exception_pyxb.name))

  if dataone_exception_pyxb.pid is None:
    return dataone_exception(
      dataone_exception_pyxb.detailCode, dataone_exception_pyxb.description,
      dataone_exception_pyxb.traceInformation
    )
  else:
    return dataone_exception(
      dataone_exception_pyxb.detailCode, dataone_exception_pyxb.description,
      dataone_exception_pyxb.pid, dataone_exception_pyxb.traceInformation
    )


class DataONEException(Exception):
  '''Base class for exceptions raised by DataONE.
  '''

  def __init__(self, errorCode, detailCode, description, traceInformation=None):
    self.errorCode = errorCode
    self.detailCode = detailCode
    self.description = description
    self.traceInformation = traceInformation

  def __str__(self):
    msg = StringIO.StringIO()
    msg.write(u'name: {0}\n'.format(self.name))
    msg.write(u'errorCode: {0}\n'.format(self.errorCode))
    msg.write(u'detailCode: {0}\n'.format(str(self.detailCode)))
    msg.write(u'description: {0}\n'.format(self.description))
    try:
      msg.write(u'PID: {0}\n'.format(self.pid))
    except AttributeError:
      pass
    if self.traceInformation is not None:
      msg.write(u'traceInformation: {0}\n'.format(self.traceInformation))
    return msg.getvalue()

  def friendly_format(self):
    '''Serialize to a format more suitable for displaying to end users.
    '''
    return '{0}: {1}'.format(self.name, self.description)

  def serialize(self):
    dataone_exception_pyxb = dataoneErrors.error()
    dataone_exception_pyxb.name = self.__class__.__name__
    dataone_exception_pyxb.errorCode = self.errorCode
    dataone_exception_pyxb.detailCode = self.detailCode
    dataone_exception_pyxb.description = self.description
    try:
      dataone_exception_pyxb.pid = self.pid
    except AttributeError:
      pass
    dataone_exception_pyxb.traceInformation = self.traceInformation
    return dataone_exception_pyxb.toxml()

  @property
  def name(self):
    return self.__class__.__name__


class DataONEIdentifierException(DataONEException):
  '''Base class for exceptions that include a PID in the constructor.
  '''

  def __init__(self, errorCode, detailCode, description, pid, traceInformation=None):
    DataONEException.__init__(self, errorCode, detailCode, description, traceInformation)
    self.pid = pid


class AuthenticationTimeout(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 408, detailCode, description, traceInformation)


class IdentifierNotUnique(DataONEIdentifierException):
  '''Implements IdentifierNotUnique exception
  '''

  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 409, detailCode, description, pid, traceInformation
    )


class InsufficientResources(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 413, detailCode, description, traceInformation)


class InvalidCredentials(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)


class InvalidRequest(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)


class InvalidSystemMetadata(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)


class InvalidToken(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)


class NotAuthorized(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)


class NotFound(DataONEIdentifierException):
  '''Implements NotFound exception
  '''

  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 404, detailCode, description, pid, traceInformation
    )
    #TODO: add link to resolve()


class NotImplemented(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 501, detailCode, description, traceInformation)


class ServiceFailure(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 500, detailCode, description, traceInformation)


class UnsupportedMetadataType(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)


class UnsupportedType(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)


class SynchronizationFailed(DataONEIdentifierException):
  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 0, detailCode, description, pid, traceInformation
    )


class VersionMismatch(DataONEIdentifierException):
  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 409, detailCode, description, pid, traceInformation
    )
