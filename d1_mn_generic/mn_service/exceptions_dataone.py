#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Module d1pythonitk.d1exceptions
===============================

:Modified: 20100408, Dahl
:Created: 20100111

:Author: vieglais

:Synopsis:
  Implements:
  - A class for holding DataONE exceptions.
  - Serialization and deserialization of DataONE exceptions.

  Creating a DataONEException object:
  
  DataONEException(AuthenticationTimeout = ('123.12', 'Message'))
  
  Serializing a DataONEException object:
  
  DataONEException.serialize(contentType)
  
  where contentType is one of:
  
  application/json
  text/csv
  text/xml
  application/rdf+xml
  text/html
  text/log
'''

# Stdlib.

import logging
try:
  from xml.etree import cElementTree as ETree
except:
  from xml.etree import ElementTree as Etree

try:
  import cjson as json
except:
  import json

import csv
import StringIO
import types

try:
  from functools import update_wrapper
except ImportError:
  from django.utils.functional import update_wrapper

# # 3rd party.

# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys_log.error('Import error: %s' % str(e))
  sys_log.error('Try: sudo apt-get install python-lxml')
  sys.exit(1)

# DataONEException(InvalidToken = ('things did not go well', 'gurf', '123')).serialize(content_type)


class DataONEException():
  # DataONE exceptions.
  exceptionMap = {
    # Exception name: (HTTP error code, generic description)
    'AuthenticationTimeout': (408, 'The authentication request timed out.'),
    'IdentifierNotUnique': (409, 'The provided identifier conflicts with an existing identifier in the DataONE system. When serializing, the identifier in conflict should be rendered in traceInformation as the value of an identifier key.'),
    'InsufficientResources': (413, 'There are insufficient resources at the node to support the requested operation.'),
    'InvalidCredentials': (401, 'Indicates that the credentials supplied (to CN_crud.login() for example) are invalid for some reason.'),
    'InvalidRequest': (400, 'The parameters provided in the call were invalid. The names and values of parameters should included in traceInformation.'),
    'InvalidSystemMetadata': (400, 'The supplied system metadata is invalid. This could be because some required field is not set, the metadata document is malformed, or the value of some field is not valid. The content of traceInformation should contain additional information about the error encountered (e.g. name of the field with bad value, if the document is malformed).'),
    'InvalidToken': (401, 'The supplied authentication token could not be verified as being valid.'),
    'NotAuthorized': (401, 'The supplied identity information is not authorized for the requested operation.'),
    'NotFound': (404, 'Used to indicate that an object is not present on the node where the exception was raised. The error message should include a reference to the CN_crud.resolve() method URL for the object.'),
    'NotImplemented': (501, 'A method is not implemented, or alternatively, features of a particular method are not implemented.'),
    'ServiceFailure': (500, 'Some sort of system failure occurred that is preventing the requested operation from completing successfully. This error can be raised by any method in the DataONE API.'),
    'UnsupportedMetadataType': (400, 'The science metadata document submitted is not of a type that is recognized by the DataONE system.'),
    'UnsupportedType': (400, 'The information presented appears to be unsupported. This error might be encountered when attempting to register unrecognized science metadata for example.'),
  }

  def __init__(self, **kw):
    # Make sure we got one and only one keyword argument.
    if len(kw) != 1:
      # TODO: Log error here.
      raise KeyError() # TODO: Raise something proper here.

    exceptionName = kw.keys()[0]
    exceptionArgs = kw.values()[0]

    # Make sure exception name is valid
    try:
      exceptionInfo = exceptionMap[exceptionName]
    except KeyError:
      # TODO: Log error here.
      raise

    # Make sure argument is tuple with exactly 2 args
    if len(exceptionArgs) != 2:
      # TODO: Log error here.
      raise KeyError() # TODO: Raise something proper here.

    self.exceptionName = exceptionName
    self.errorCode = exceptionInfo[0]
    self.detailCode = exceptionArgs[0]
    self.description = exceptionArgs[1]
    self.traceInfo = exceptionArgs[2]

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

  def serialize(self, contentType):
    try:
      serializeFunc = contentTypeToSerializeMap[contentType]
    except KeyError:
      # TODO: Log error here.
      raise

  # TODO: Insert special case for jsonVar when serializing to JSON.

    if serializeFunc is None:
      # TODO: Log error here.
      return

    serializeFunc(self)

  def serializeToJSON(self, jsonVar=None, pretty=False):
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

  def SerializeToCSV(self, pretty=False):
    """
    Serialize object to CSV.
    """

    io = StringIO.StringIO()

    csv_writer = csv.writer(
      io, dialect=csv.excel,
      quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    first = True
    for d in obj:
      if first == True:
        # Don't know if it's possible for the order of the keys to change during
        # iteration of the data objects, so grab the keys once here and use those
        # for iteration.
        keys = d.keys()
        # Header containing names of fields.
        io.write(','.join(keys) + '\n')
        first = False

      row = []

      for key in keys:
        val = d[key]
        if type(val) is types.IntType:
          row.append(val)
        else:
          row.append(val.encode('utf-8'))

      csv_writer.writerow(row)

    return io.getvalue()

  def serializeToXML(self, pretty=False):
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

  def serializeToRDFXML(self, pretty=False):
    # TODO: Not implemented.
    pass

  def serializeToHTML(self, pretty=False):
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

  def serializeToLog(obj, pretty=False):
    """
    Serialize object to log.
    
    Example:
    # [detail:1020.1][identifier:123XYZ, method:mn.get]The specified object does not exist on this node.
    """

    io = StringIO.StringIO()

    io.write(obj['errorCode'])
    io.write(obj['detailCode'])
    io.write(obj['description'])

    return io.getvalue()

  contentTypeToSerializeMap = {
    'application/json': serializeToJSON,
    'text/csv': serializeToCSV,
    'text/xml': serializeToXML,
    'application/rdf+xml': serializeToRDFXML,
    'text/html': serializeToHTML,
    'text/log': serializeToLog,
  }


class DataOneExceptionFactory(object):
  '''Implements a simple factory that generates a DataONE exception from the
  serialized form.
  '''

  @staticmethod
  def returnException(data):
    exc = None
    exceptions = {'NotFound': NotFound, 'IdentifierNotUnique': IdentifierNotUnique}
    if data['name'] in exceptions.keys():
      identifier = data['traceInformation']['identifier']
      del data['traceInformation']['identifier']
      exc = exceptions[data['name']](
        data['detailCode'], data['description'], identifier, data['traceInformation']
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
      if data['name'] in exceptions.keys():
        exc = exceptions[data['name']](
          data['detailCode'], data['description'], data['traceInformation']
        )
    return exc

  @staticmethod
  def createExceptionFromJSON(data):
    '''Try and create an exception from the provided data, otherwise return None.
    
    :param data: The exception rendered as a JSON string
    :type data: string
    :rtype: DataONEException
    '''
    exjson = json.loads(data)
    return DataOneExceptionFactory.returnException(exjson)

  @staticmethod
  def createExceptionFromXML(data):
    '''Try and create an exception from the provided data, otherwise return None.
    
    :param data: The exception rendered as an XML string
    :type data: string
    :rtype: DataONEException
    '''
    etree = ETree.fromstring(data)
    edata = {
      'name': etree.attrib['name'],
      'errorCode': int(etree.attrib['errorCode']),
      'detailCode': etree.attrib['detailCode'],
      'description': '',
      'traceInformation': {}
    }
    try:
      edata['description'] = etree.findall('description')[0].text
    except:
      pass
    tinfo = etree.findall("traceInformation/value")
    for element in tinfo:
      try:
        k = element.attrib['key']
        v = element.text
        edata['traceInformation'][k] = v
      except Exception, e:
        logging.exception(e)
    return DataOneExceptionFactory.returnException(edata)

  @staticmethod
  def createException(data):
    '''Try and create an exception from the provided data, otherwise return None.
    
    :param data: The exception rendered as an XML string
    :type data: string
    :rtype: DataONEException
    '''
    data = data.strip()
    if data[0] == "<":
      return DataOneExceptionFactory.createExceptionFromXML(data)
    return DataOneExceptionFactory.createExceptionFromJSON(data)
