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

:Created:
  2010-04-12
:Author:
  DataONE (Vieglais, Dahl)
:Synopsis:
  - Native objects for holding DataONE Exceptions
  - XML Serialization and deserialization of DataONE Exceptions
:Dependencies:
  - python 2.6
  - PyXB
'''

# Stdlib.
import inspect
import sys
import traceback
import xml.sax

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


def deserialize(dataone_exception_xml):
  '''Deserialize a DataONE Exception.
  :param dataone_exception_xml: XML Serialized DataONE Exception.
  :type dataone_exception_xml: str
  :returns: Native DataONE Exception Object.
  :return type: DataONEException subclass 
  '''
  try:
    dataone_exception_pyxb = dataoneErrors.CreateFromDocument(dataone_exception_xml)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    # A PyXB exception at this point means that the dataone_exception_xml did
    # not correspond to the PyXB binding class, which again means that it did
    # not comply to the schema. Handle this by returning a ServiceFailure
    # exception object that contains the information from the exception and the
    # dataone_exception_xml.
    description_list = []
    description_list.append('Deserialization failed with exception')
    description_list.append(traceback.format_exc())
    description_list.append('On input:')
    description_list.append(dataone_exception_xml)
    return ServiceFailure(0, '\n'.join(description_list))

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
  }

  try:
    dataone_exception = name_exception_map[dataone_exception_pyxb.name]
  except LookupError:
    # The dataone_exception_xml complied to the schema but the name did not
    # match any known DataONE exception types. This can happen because the
    # defined types are not enumerated in the schema. Map this to a
    # ServiceFailure exception.
    description_list = []
    description_list.append('Attempted to deserialize unknown DataONE Exception:')
    description_list.append(dataone_exception_pyxb.name)
    return ServiceFailure(0, '\n'.join(description_list))

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
    res = []
    res.append(u'name: {0}'.format(self.name))
    res.append(u'errorCode: {0}'.format(self.errorCode))
    res.append(u'detailCode: {0}'.format(str(self.detailCode)))
    res.append(u'description: {0}'.format(self.description))
    try:
      res.append(u'PID: {0}'.format(self.pid))
    except AttributeError:
      pass
    if self.traceInformation is not None:
      res.append(u'traceInformation: {0}'.format(self.traceInformation))
    return u'\n'.join(res)

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


class NotFound(DataONEIdentifierException):
  '''Implements NotFound exception
  '''

  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 404, detailCode, description, pid, traceInformation
    )
    #TODO: add link to resolve()


class IdentifierNotUnique(DataONEIdentifierException):
  '''Implements IdentifierNotUnique exception
  '''

  def __init__(self, detailCode, description, pid, traceInformation=None):
    DataONEIdentifierException.__init__(
      self, 409, detailCode, description, pid, traceInformation
    )


class AuthenticationTimeout(DataONEException):
  def __init__(self, detailCode, description, traceInformation=None):
    DataONEException.__init__(self, 408, detailCode, description, traceInformation)


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
