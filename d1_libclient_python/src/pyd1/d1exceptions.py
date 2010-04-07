'''
Module pyd1.d1exceptions
========================

:Created: 20100111

:Author: vieglais

Implements the DataONE exceptions
'''

try:
  from xml.etree import cElementTree as ETree
except:
  from xml.etree import ElementTree as Etree

try:
  import cjson as json
except:
  import json


def instanceToSimpleType(instance):
  '''Force instance to a simple type- int, float, or string
  '''
  if isinstance(instance, float):
    return instance
  if isinstance(instance, int):
    return instance
  if isinstance(instance, basestring):
    return instance
  return repr(instance)

#===============================================================================


class DataONEException(Exception):
  '''Base class for exceptions raised by PyD1.
  '''

  def __init__(self, errorCode, detailCode, description, traceInformation={}):
    self.errorCode = errorCode
    self.detailCode = detailCode
    self.description = description
    self.traceInfo = traceInformation

  def __str__(self):
    '''
    (errorCode:detailCode) description
    tracekey tracevalue
    ...
    '''
    res = [
      "%s [%s:%s] %s" % (
        str(self.errorCode), self.name, str(self.detailCode), self.description
      ),
    ]
    for k in self.traceInfo.keys():
      res.append("  %s: %s" % (k, repr(self.traceInfo[k])))
    return "\n".join(res)

  @property
  def name(self):
    return self.__class__.__name__

  def serializeToHtml(self):
    '''Renders the exception in HTML form.
    
    :rtype: UTF-8 encoded HTML string
    '''
    root = ETree.Element("html")
    head = ETree.SubElement(
      root, "meta", {
        'http-equiv': 'content-type',
        'content': 'text/html;charset=utf-8'
      }
    )
    title = ETree.SubElement(head, "title")
    title.text = u"Error: %s %s (%s)" % (
      escape(unicode(self.errorCode)), self.name, escape(self.detailCode)
    )
    body = ETree.SubElement(root, "body")
    dl = ETree.SubElement(body, "dl")
    ETree.SubElement(dl, "dt").text = "Code"
    ETree.SubElement(dl, "dd", {'class': 'errorCode'}).text = str(self.errorCode)
    ETree.SubElement(dl, "dt").text = "Detail Code"
    ETree.SubElement(dl, "dd", {'class': 'detailCode'}).text = str(self.detailCode)
    ETree.SubElement(body, "p", {'class': 'description'}).text = self.description
    if len(self.traceInfo.keys()) > 0:
      dl = ETree.SubElement(body, 'dl', {'class': 'traceInformation'})
      for k in self.traceInfo.keys():
        ETree.SubElement(dl, 'dt').text = k
        ETree.SubElem1ent(dl, 'dd').text = repr(self.traceInfo[k])
    return ETree.tostring(root, "utf-8")

  def serializeToXml(self):
    '''Renders the exception to XML, encoded as UTF8.

    :rtype: UTF-8 encoded XML string
    '''
    root = ETree.Element(
      'error', {
        'name': self.name,
        'errorCode': str(self.errorCode),
        'detailCode': str(self.detailCode)
      }
    )
    ETree.SubElement(root, 'description').text = self.description
    trace = ETree.SubElement(root, 'traceInformation')
    for k in self.traceInfo:
      ETree.SubElement(trace, 'value', {'key': k}).text = repr(self.traceInfo[k])
    return ETree.tostring(root, "utf-8")

  def serializeToJson(self, jsonVar=None):
    '''Serialize the exception to JSON

    :rtype: JSON string
    '''
    res = {
      'name': self.name,
      'errorCode': self.errorCode,
      'detailCode': str(self.detailCode),
      'description': self.description,
      'traceInformation': {}
    }
    #Force conversion of traceInfo content to simple types
    for k in self.traceInfo:
      res['traceInformation'][k] = instanceToSimpleType(self.traceInfo[k])
    if jsonVar is None:
      return json.dumps(res)
    return u"%s=%s" % (jsonVar, json.dumps(res))

#===============================================================================


class DataONEIdentifierException(DataONEException):
  '''Base class for exceptions raised by PyD1 that include an identifier in
  the constructor.
  '''

  def __init__(self, errorCode, detailCode, description, identifier, traceInformation={}):
    DataONEException.__init__(self, errorCode, detailCode, description, traceInformation)
    self.traceInfo['identifier'] = identifier

#===============================================================================


class NotFound(DataONEIdentifierException):
  '''Implements NotFound exception
  '''

  def __init__(self, detailCode, description, identifier, traceInformation={}):
    DataONEIdentifierException.__init__(
      self, 404, detailCode, description, traceInformation
    )
    self.traceInfo['identifier'] = identifier
    #TODO: add link to resolve()

    #===============================================================================


class IdentifierNotUnique(DataONEIdentifierException):
  '''Implements IdentifierNotUnique exception
  '''

  def __init__(self, detailCode, description, identifier, traceInformation={}):
    DataONEIdentifierException.__init__(
      self, 409, detailCode, description, traceInformation
    )
    self.errorCode = 409

#===============================================================================


class AuthenticationTimeout(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 408, detailCode, description, traceInformation)

#===============================================================================


class InsufficientResources(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 413, detailCode, description, traceInformation)

#===============================================================================


class InvalidCredentials(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)

#===============================================================================


class InvalidRequest(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)

#===============================================================================


class InvalidSystemMetadata(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)

#===============================================================================


class InvalidToken(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)

#===============================================================================


class NotAuthorized(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 401, detailCode, description, traceInformation)

#===============================================================================


class NotImplemented(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 501, detailCode, description, traceInformation)

#===============================================================================


class ServiceFailure(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 500, detailCode, description, traceInformation)
#===============================================================================


class UnsupportedMetadataType(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)
#===============================================================================


class UnsupportedType(DataONEException):
  def __init__(self, detailCode, description, traceInformation={}):
    DataONEException.__init__(self, 400, detailCode, description, traceInformation)

#===============================================================================


def DataOneExceptionFactory(data):
  '''Try and create an exception from the provided data, otherwise return None.
  
  :param data: The exception rendered as a JSON object
  :type data: string
  :rtype: DataONEException
  '''
  exc = None
  exjson = json.loads(data)
  ename = exjson['name']
  traceinfo = exjson['traceInformation']
  if ename == 'NotFound':
    identifier = traceinfo['identifier']
    del traceinfo['identifier']
    exc = NotFound(exjson['detailCode'], exjson['description'], identifier, traceinfo)
  elif ename == 'IdentifierNotUnique':
    identifier = traceinfo['identifier']
    del traceinfo['identifier']
    exc = IdentifierNotUnique(
      exjson['detailCode'], exjson['description'], identifier, traceinfo
    )
  else:
    exceptions = {
      'AuthenticationTimeout': AuthenticationTimeout,
      'InsufficientResources': InsufficientResources,
      'InvalidCredentials': InvalidCredentials,
      'InvalidRequest': InvalidRequest,
      'InvalidSystemMetadata': InvalidSystemMetadata,
      'InvalidToken': InvalidToken,
      'NotAuthorized': NotAuthorized,
      'NotImplemented': NotImplemented,
      'ServiceFailure': ServiceFailure,
      'UnsupportedMetadataType': UnsupportedMetadataType,
      'UnsupportedType': UnsupportedType,
    }
    if ename in exceptions:
      exc = exceptions[ename](exjson['detailCode'], exjson['description'], traceinfo)
  return exc
