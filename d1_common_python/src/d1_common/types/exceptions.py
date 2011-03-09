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
===========================

:Created: 20100111

:Authors: vieglais, dahl

Implements the DataONE exceptions, shared between client and member node.
'''


class DataONEException(Exception):
  '''Base class for exceptions raised by DataONE.
  '''

  def __init__(self, errorCode, detailCode, description, traceInformation=None):
    self.errorCode = errorCode
    self.detailCode = detailCode
    self.description = description
    if isinstance(traceInformation, list) or \
       isinstance(traceInformation, tuple):
      self.traceInformation = u"\n".join(traceInformation)
    else:
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

# Keeping this around in case we need this particular layout.
#    '''
#    (errorCode:detailCode) description
#    ...
#    '''
#    res = [u'{0} [{0}:{0}] {0}'.format(str(self.errorCode),
#                                        self.name, 
#                                        str(self.detailCode), 
#                                        self.description), ]
#    for v in self.traceInformation:
#      res.append(u'{0}'.format(unicode(v)))
#    
#    return u'\n'.join(res)

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
