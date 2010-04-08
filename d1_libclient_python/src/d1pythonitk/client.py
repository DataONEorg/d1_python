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

import logging
import httplib
import urllib
import urllib2
import urlparse

try:
  import cjson as json
except:
  import json
from d1pythonitk import const
from d1pythonitk import exceptions
from d1pythonitk import systemmetadata

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

  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.status = None
    self.responseInfo = None
    self._BASE_DETAIL_CODE = '10000'
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
    try:
      edata = response.read()
      exc = exceptions.DataOneExceptionFactory(edata)
      if not exc is None:
        raise exc
    finally:
      message = 'A bad response was received from the target %s' % response.url
      traceInfo = {'body': edata}
      raise exceptions.ServiceFailure(self.exceptioncode(2), message, traceInfo)
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
    response = urllib2.urlopen(request)
    self.status = response.code
    self.responseInfo = response.info()
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

  def DELETE(self, url, headers=None):
    self.logger.debug("%s: %s" % (__name__, url))
    return self.sendRequest(url, data=data, headers=headers, method='DELETE')

#===============================================================================


class DataOneClient(RESTClient):
  '''Implements a simple DataONE client.
  '''

  def __init__(self, d1Root=const.URL_DATAONE_ROOT, userAgent=const.USER_AGENT):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.d1Root = d1Root
    self.userAgent = userAgent
    self._BASE_DETAIL_CODE = '11000'
    #TODO: Need to define this detailCode base value

  @property
  def headers(self):
    res = {'User-Agent': self.userAgent, 'Accept': '*/*'}
    return res

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
    try:
      response = urllib2.urlopen(request)
      self.status = response.code
      self.responseInfo = response.info()
    except urllib2.HTTPError, e:
      self.logger.warn('%s: HTTP Error encountered.' % __name__)
      self.status = e.code
      self.responseInfo = e.info()
      if not self.loadError(e):
        description = "HTTPError. Code=%s" % str(e.code)
        traceInfo = {'body': e.read()}
        raise exceptions.ServiceFailure('10000.0', description, traceInfo)
    except urllib2.URLError, e:
      self.logger.warn('%s: URL Error encountered.' % __name__)
      if not self.loadError(e):
        description = "URL Error. Reason=%s" % e.reason
        raise exceptions.ServiceFailure('10000.1', description)
    return response

  def getObjectUrl(self, target):
    '''Returns the full URL to the object collection on target
    '''
    target = self._normalizeTarget(target)
    url = urlparse.urljoin(target, d1const.URL_OBJECT_PATH)
    if not url.endswith("/"):
      url += "/"
    return url

  ## === DataONE API Methods ===
  def get(self, identifier, target):
    '''Retrieve an object from DataONE.
    
    :param identifier: Identifier of object to retrieve
    :param target: Host URL from which to retrieve object
    :rtype: open file stream
    '''
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectUrl(target), identifier)
    self.logger.debug("%s: url=%s" % (__name__, url))
    response = self.GET(url, self.headers)
    return response

  def getSystemMetadata(self, identifier, target=const.URL_DATAONE_ROOT):
    '''Retrieve system metadata for an object.
    :param identifier: Identifier of the object to retrieve
    :param target: Optional node URL
    :rtype: :class:d1sysmeta.SystemMetadata
    '''
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectUrl(target), identifier, 'meta/')
    self.logger.debug("%s: url=%s" % (__name__, url))
    raise exceptions.NotImplemented(self.exceptioncode('1.2'), __name__)
    response = self.GET(url, self.headers)
    return response.data

  def resolve(self, identifier, target=const.URL_DATAONE_ROOT):
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectUrl(target), identifier, 'resolve/')
    self.logger.debug("%s: url=%s" % (__name__, url))
    headers = self.headers
    headers['Accept'] = ''
    raise exceptions.NotImplemented(self.exceptioncode('1.3'), __name__)
    response = self.GET(url, headers)

  def listObjects(
    self,
    startTime,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=1000,
    target=const.URL_DATAONE_ROOT
  ):
    if start < 0:
      start = 0
    if count < 0:
      count = 0
    if count > const.MAX_LISTOBJECTS:
      raise exceptions.InvalidRequest(
        10002, "Count can not be higher than %d" % const.MAX_LISTOBJECTS
      )
    params = {}
    self.logger.debug("%s: %s" % (__name__, identifier))
    url = urlparse.urljoin(self.getObjectUrl(target), identifier, '')
    self.logger.debug("%s: url=%s" % (__name__, url))
    raise exceptions.NotImplemented(self.exceptioncode('1.4'), __name__)
    response = self.GET(url, headers)

  def getLogRecords(self, startTime, endTime=None, event=None):
    raise exceptions.NotImplemented(self.exceptioncode('1.5'), __name__)
