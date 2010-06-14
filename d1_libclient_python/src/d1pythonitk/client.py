'''
Module d1pythonitk.d1client
===========================

This module implements DataOneClient which provides a client supporting basic 
interaction with the DataONE infrastructure.

:Created: 20100111
:Author: vieglais

:Dependencies:

  - python 2.6

----

.. autoclass:: RESTClient
   :members:

----

.. autoclass:: DataOneClient
   :members:
'''

# Stdlib.
import logging
import httplib
import urllib
import urllib2
import urlparse
import sys
import os
import xml.dom.minidom

try:
  import cjson as json
except:
  import json

# DataONE.
from d1common import exceptions
from d1pythonitk import const
from d1pythonitk import systemmetadata
import lib.upload

#===============================================================================


class HttpRequest(urllib2.Request):
  '''Overrides the default Request class to enable setting the HTTP method.
  '''

  def __init__(self, *args, **kwargs):
    self._method = 'GET'
    if kwargs.has_key('method'):
      self._method = kwargs['method']
      del kwargs['method']
    urllib2.Request.__init__(self, *args, **kwargs)

  def get_method(self):
    return self._method

#===============================================================================


class RESTClient(object):
  '''Implements a simple REST client that utilizes the base DataONE exceptions
  for error handling if possible.
  '''

  def __init__(self, target=const.URL_DATAONE_ROOT):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.status = None
    self.responseInfo = None
    self._BASE_DETAIL_CODE = '10000'
    self.target = self._normalizeTarget(target)
    #TODO: Need to define these detailCode values

  def exceptionCode(self, extra):
    return "%s.%s" % (self._BASE_DETAIL_CODE, str(extra))

  def _normalizeTarget(self, target):
    '''Internal method to ensure target url is in suitable form before 
    adding paths.
    '''
    if not target.endswith("/"):
      target += "/"
    return target

  @property
  def headers(self):
    '''Returns a dictionary of headers
    '''
    return {'User-Agent': 'Test client', 'Accept': '*/*'}

  def loadError(self, response):
    '''Try and create a DataONE exception form the response.  If successful, 
    then the DataONE error will be raised, otherwise the error is encapsulated
    with a DataONE ServiceFailure exception and re-raised.
    
    :param response: Response from urllib2.urlopen
    :returns: Should not return - always raises an exception.
    '''
    edata = response.read()
    exc = exceptions.DataOneExceptionFactory.createException(edata)
    if not exc is None:
      raise exc
    return False

  def sendRequest(self, url, method='GET', data=None, headers=None):
    '''Sends a HTTP request and returns the response as a file like object.
    
    Has the side effect of setting the status and responseInfo properties. 
    
    :param url: The target URL
    :type url: string
    :param method: The HTTP method to use.
    :type method: string
    :param data: Optional dictionary of data to pass on to urllib2.urlopen
    :type data: dictionary
    :param headers: Optional header information
    :type headers: dictionary
    '''
    if headers is None:
      headers = self.headers
    request = HttpRequest(url, data=data, headers=headers, method=method)
    self.logger.debug('{0}: sendRequest({1})'.format(__name__, url))
    try:
      response = urllib2.urlopen(request, timeout=const.RESPONSE_TIMEOUT)
      self.status = response.code
      self.responseInfo = response.info()
    except urllib2.HTTPError, e:
      self.logger.warn('{0}: HTTP Error: {1}'.format(__name__, e))
      self.status = e.code
      self.responseInfo = e.info()
      if hasattr(e, 'read'):
        if self.loadError(e):
          return None
      raise (e)
#      if not self.loadError(e):
#        description = "HTTPError. Code=%s" % str(e.code)
#        traceInfo = {'body': e.read()}
#        raise exceptions.ServiceFailure('10000.0',description,traceInfo)
    except urllib2.URLError, e:
      self.logger.warn('{0}: URL Error: {1}'.format(__name__, e))
      if hasattr(e, 'read'):
        if self.loadError(e):
          return None
      raise (e)
      #description = "URL Error. Reason=%s" % e.reason
      #raise exceptions.ServiceFailure('10000.1',description)
    return response

  def HEAD(self, url, headers=None):
    '''Issues a HTTP HEAD request.
    '''
    self.logger.debug("%s: %s" % (__name__, url))
    return self.sendRequest(url, headers=headers, method='HEAD')

  def GET(self, url, headers=None):
    self.logger.debug("%s: %s" % (__name__, url))
    return self.sendRequest(url, headers=headers, method='GET')

  def PUT(self, url, data, headers=None):
    self.logger.debug("%s: %s" % (__name__, url))
    if isinstance(data, dict):
      data = urllib.urlencode(data)
    return self.sendRequest(url, data=data, headers=headers, method='PUT')

  def POST(self, url, data, headers=None):
    self.logger.debug("%s: %s" % (__name__, url))
    if isinstance(data, dict):
      data = urllib.urlencode(data)
    return self.sendRequest(url, data=data, headers=headers, method='POST')

  def DELETE(self, url, data=None, headers=None):
    self.logger.debug("%s: %s" % (__name__, url))
    return self.sendRequest(url, data=data, headers=headers, method='DELETE')

#===============================================================================


class DataOneClient(object):
  '''Implements a simple DataONE client.
  '''

  def __init__(
    self,
    target=const.URL_DATAONE_ROOT,
    userAgent=const.USER_AGENT,
    clientClass=RESTClient,
  ):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.userAgent = userAgent
    self._BASE_DETAIL_CODE = '11000'
    #TODO: Need to define this detailCode base value
    self.client = clientClass(target)

  def exceptionCode(self, extra):
    return "%s.%s" % (self._BASE_DETAIL_CODE, str(extra))

  @property
  def headers(self):
    res = {'User-Agent': self.userAgent, 'Accept': '*/*'}
    return res

  def getObjectUrl(self):
    '''Returns the base URL to an object on target.
    '''
    return urlparse.urljoin(self.client.target, const.URL_OBJECT_PATH)

  def getObjectListUrl(self):
    '''Returns the full URL to the object collection on target.
    '''
    return urlparse.urljoin(self.client.target, const.URL_OBJECT_LIST_PATH)

  def getAccessLogUrl(self):
    '''Returns the full URL to the access log collection on target.
    '''
    return urlparse.urljoin(self.client.target, const.URL_ACCESS_LOG_PATH)

  def getSystemMetadataSchema(self, schemaUrl=const.SYSTEM_METADATA_SCHEMA_URL):
    '''Convenience function to retrieve a copy of the system metadata schema.
    
    :param schemaUrl: The URL from which to load the schema from
    :type schemaUrl: string
    :rtype: unicode copy of the system metadata schema
    '''
    response = self.client.GET(schemaUrl)
    return response

    ## === DataONE API Methods ===
  def get(self, identifier):
    '''Retrieve an object from DataONE.
    
    :param identifier: Identifier of object to retrieve
    :rtype: open file stream
    '''
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectListUrl(), identifier)
    self.logger.debug("%s: url=%s" % (__name__, url))
    response = self.client.GET(url, self.headers)
    return response

  def getSystemMetadata(self, identifier):
    '''Retrieve system metadata for an object.
    :param identifier: Identifier of the object to retrieve
    :rtype: :class:d1sysmeta.SystemMetadata
    '''
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectListUrl(), identifier, 'meta/')
    self.logger.debug("%s: url=%s" % (__name__, url))
    raise exceptions.NotImplemented(self.exceptioncode('1.2'), __name__)
    response = self.client.GET(url, self.headers)
    return response.data

  def resolve(self, identifier):
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectListUrl(), identifier, 'resolve/')
    self.logger.debug("%s: url=%s" % (__name__, url))
    headers = self.headers
    headers['Accept'] = ''
    raise exceptions.NotImplemented(self.exceptioncode('1.3'), __name__)
    response = self.client.GET(url, headers)

  def listObjects(
    self,
    startTime=None,
    endTime=None,
    objectFormat=None,
    start=0,
    count=const.MAX_LISTOBJECTS
  ):

    params = {}

    try:
      if start < 0:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(10002, "start must be a positive integer")
    else:
      params['start'] = start

    try:
      if count < 1:
        raise ValueError
      if count > const.MAX_LISTOBJECTS:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(
        10002, "count must be an integer between 1 and {0}".format(const.MAX_LISTOBJECTS)
      )
    else:
      params['count'] = count

    try:
      if startTime is not None and endTime is None:
        raise ValueError
      elif endTime is not None and startTime is None:
        raise ValueError
      elif endTime is not None and startTime is not None and startTime >= endTime:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(
        10002,
        "startTime and endTime must be specified together, must be valid dates and endTime must be after startTime"
      )
    else:
      params['startTime'] = startTime
      params['endTime'] = endTime

    url = self.getObjectListUrl() + '?pretty&' + urllib.urlencode(params)
    self.logger.debug("%s: url=%s" % (__name__, url))

    headers = self.headers
    headers['Accept'] = 'text/xml'

    # Fetch.
    response = self.client.GET(url, headers)

    # Deserialize.
    xml = response.read()
    return DeserializeObjectList(self.logger, xml).get()

  def getLogRecords(
    self,
    startTime=None,
    endTime=None,
    objectFormat=None,
    start=0,
    count=const.MAX_LISTOBJECTS
  ):

    params = {}

    try:
      if start < 0:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(10002, "start must be a positive integer")
    else:
      params['start'] = start

    try:
      if count < 1:
        raise ValueError
      if count > const.MAX_LISTOBJECTS:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(
        10002, "count must be an integer between 1 and {0}".format(const.MAX_LISTOBJECTS)
      )
    else:
      params['count'] = count

    try:
      if startTime is not None and endTime is None:
        raise ValueError
      elif endTime is not None and startTime is None:
        raise ValueError
      elif endTime is not None and startTime is not None and startTime >= endTime:
        raise ValueError
    except ValueError:
      raise exceptions.InvalidRequest(
        10002,
        "startTime and endTime must be specified together, must be valid dates and endTime must be after startTime"
      )
    else:
      params['startTime'] = startTime
      params['endTime'] = endTime

    url = self.getAccessLogUrl() + '?pretty&' + urllib.urlencode(params)
    self.logger.debug("%s: url=%s" % (__name__, url))

    headers = self.headers
    headers['Accept'] = 'text/xml'

    # Fetch.
    response = self.client.GET(url, headers)

    # Deserialize.
    xml = response.read()
    return DeserializeLogRecords(self.logger, xml).get()

  def create(self, identifier, object_bytes, sysmeta_bytes):
    # Parameter validation.
    if len(identifier) == 0 or len(object_bytes) == 0 or len(sysmeta_bytes) == 0:
      self.logger.error("")

      # Create MIME-multipart Mixed Media Type body.
    files = []
    files.append(('object', 'object', object_bytes))
    files.append(('systemmetadata', 'systemmetadata', sysmeta_bytes))
    content_type, mime_doc = lib.upload.encode_multipart_formdata([], files)

    # Send REST POST call to register object.
    self.logger.debug("%s: %s" % (__name__, identifier))

    headers = {'Content-Type': content_type, 'Content-Length': str(len(mime_doc)), }

    crud_create_url = urlparse.urljoin(self.getObjectUrl(), urllib.quote(identifier, ''))

    self.logger.debug('~' * 79)
    self.logger.debug('REST call: {0}'.format(crud_create_url))
    self.logger.debug('~' * 10)
    self.logger.debug(headers)
    self.logger.debug('~' * 10)
    self.logger.debug(mime_doc)
    self.logger.debug('~' * 79)

    try:
      res = self.client.POST(crud_create_url, data=mime_doc, headers=headers)
      res = '\n'.join(res)
      if res != r'OK':
        raise Exception(res)
    except Exception as e:
      logging.error('REST call failed: {0}'.format(str(e)))
      raise

#<?xml version='1.0' encoding='UTF-8'?>
#<d1:response xmlns:d1="http://ns.dataone.org/core/objects">
#  <start>0</start>
#  <count>243</count>
#  <total>243</total>
#  <objectInfo>
#    <checksum>5f173b60a36d4ce42e90b1698dcb10631de6dee0</checksum>
#    <dateSysMetadataModified>2010-04-26T07:23:42.380413</dateSysMetadataModified>
#    <format>eml://ecoinformatics.org/eml-2.0.0</format>
#    <identifier>hdl:10255/dryad.1099/mets.xml</identifier>
#    <size>3636</size>
#  </objectInfo>
#</d1:response>


class DeserializeObjectList():
  def __init__(self, logger, d):
    self.r = {'objectInfo': []}
    self.logger = logger
    self.d = d

  def get(self):
    try:
      dom = xml.dom.minidom.parseString(self.d)
      self.handleObjectList(dom)
      return self.r
    except (TypeError, AttributeError, ValueError):
      self.logger.error("Could not deserialize XML result")
      raise

  def getText(self, nodelist):
    rc = []
    for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
        rc.append(node.data)
    return ''.join(rc)

  def handleObjectList(self, dom):
    # start, count and total
    self.handleObjectStart(dom.getElementsByTagName("start")[0])
    self.handleObjectCount(dom.getElementsByTagName("count")[0])
    self.handleObjectTotal(dom.getElementsByTagName("total")[0])
    objects = dom.getElementsByTagName("objectInfo")
    self.handleObjects(objects)

  def handleObjects(self, objects):
    for object in objects:
      self.handleObject(object)

  def handleObject(self, object):
    objectInfo = {}
    self.handleObjectChecksum(objectInfo, object.getElementsByTagName("checksum")[0])
    self.handleObjectDateSysMetadataModified(
      objectInfo, object.getElementsByTagName(
        "dateSysMetadataModified"
      )[0]
    )
    self.handleObjectFormat(objectInfo, object.getElementsByTagName("format")[0])
    self.handleObjectIdentifier(objectInfo, object.getElementsByTagName("identifier")[0])
    self.handleObjectSize(objectInfo, object.getElementsByTagName("size")[0])
    self.r['objectInfo'].append(objectInfo)

    # Header.

  def handleObjectStart(self, title):
    self.r['start'] = int(self.getText(title.childNodes))

  def handleObjectCount(self, title):
    self.r['count'] = int(self.getText(title.childNodes))

  def handleObjectTotal(self, title):
    self.r['total'] = int(self.getText(title.childNodes))

  # Objects.

  def handleObjectChecksum(self, objectInfo, checksum):
    objectInfo['checksum'] = self.getText(checksum.childNodes)

  def handleObjectDateSysMetadataModified(self, objectInfo, dateSysMetadataModified):
    objectInfo['dateSysMetadataModified'] = self.getText(
      dateSysMetadataModified.childNodes
    )

  def handleObjectFormat(self, objectInfo, format):
    objectInfo['format'] = self.getText(format.childNodes)

  def handleObjectIdentifier(self, objectInfo, identifier):
    objectInfo['identifier'] = self.getText(identifier.childNodes)

  def handleObjectSize(self, objectInfo, size):
    objectInfo['size'] = int(self.getText(size.childNodes))


class DeserializeLogRecords():
  def __init__(self, logger, d):
    self.r = {'logRecord': []}
    self.logger = logger
    self.d = d

  def get(self):
    try:
      dom = xml.dom.minidom.parseString(self.d)
      self.handleLogRecords(dom)
      return self.r
    except (TypeError, AttributeError, ValueError):
      self.logger.error("Could not deserialize XML result")
      raise

  def getText(self, nodelist):
    rc = []
    for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
        rc.append(node.data)
    return ''.join(rc)

  def handleLogRecords(self, dom):
    # start, count and total
    self.handleObjectStart(dom.getElementsByTagName("start")[0])
    self.handleObjectCount(dom.getElementsByTagName("count")[0])
    self.handleObjectTotal(dom.getElementsByTagName("total")[0])
    objects = dom.getElementsByTagName("logRecord")
    self.handleObjects(objects)

  def handleObjects(self, objects):
    for object in objects:
      self.handleObject(object)

  def handleObject(self, object):
    logRecord = {}
    self.handleObjectIdentifier(logRecord, object.getElementsByTagName("identifier")[0])
    self.handleObjectOperationType(
      logRecord, object.getElementsByTagName("operationType")[0]
    )
    self.handleObjectRequestorIdentity(
      logRecord, object.getElementsByTagName(
        "requestorIdentity"
      )[0]
    )
    self.handleObjectAccessTime(logRecord, object.getElementsByTagName("accessTime")[0])
    self.r['logRecord'].append(logRecord)

    # Header.

  def handleObjectStart(self, title):
    self.r['start'] = int(self.getText(title.childNodes))

  def handleObjectCount(self, title):
    self.r['count'] = int(self.getText(title.childNodes))

  def handleObjectTotal(self, title):
    self.r['total'] = int(self.getText(title.childNodes))

  # Log Records.

  def handleObjectIdentifier(self, logRecord, identifier):
    logRecord['identifier'] = self.getText(identifier.childNodes)

  def handleObjectOperationType(self, logRecord, operationType):
    logRecord['operationType'] = self.getText(operationType.childNodes)

  def handleObjectRequestorIdentity(self, logRecord, requestorIdentity):
    logRecord['requestorIdentity'] = self.getText(requestorIdentity.childNodes)

  def handleObjectAccessTime(self, logRecord, accessTime):
    logRecord['accessTime'] = self.getText(accessTime.childNodes)
