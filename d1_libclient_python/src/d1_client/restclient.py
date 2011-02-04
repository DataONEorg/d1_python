'''
Created on Jan 20, 2011

@author: vieglais
'''

import logging
import httplib
import urlparse
from d1_common import const
from d1_common import util
from d1_common.mime_multipart import multipart
from d1_common.types import exception_serialization
from d1_common.types import systemmetadata
from d1_common.types import objectlist_serialization
from d1_common.types import logrecords_serialization
from d1_common.types import nodelist_serialization


class RESTClient(object):
  '''Implements a REST HTTP client that encodes POST and PUT using 
  MIME multipart encoding.
  '''

  def __init__(self, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True):
    self.defaultHeaders = defaultHeaders
    self.timeout = timeout
    self.keyfile = keyfile
    self.certfile = certfile
    self.strictHttps = strictHttps
    self.logger = logging.getLogger('RESTClient')
    self._lasturl = ''
    self._curlrequest = []

  def _getConnection(self, scheme, host, port):
    if scheme == 'http':
      conn = httplib.HTTPConnection(host, port, self.timeout)
    else:
      conn = httplib.HTTPSConnection(
        host, port, self.keyfile, self.certfile, self.strictHttps, self.timeout
      )
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      conn.set_debuglevel(logging.DEBUG)
    return conn

  def _parseURL(self, url):
    parts = urlparse.urlsplit(url)
    res = {
      'scheme': parts.scheme,
      'host': parts.netloc,
      'path': parts.path,
      'query': parts.query,
      'fragment': parts.fragment
    }
    try:
      res['port'] = int(parts.port)
    except:
      if res['scheme'] == 'https':
        res['port'] = 443
      else:
        res['port'] = 80
    return res

  def _mergeHeaders(self, headers):
    res = self.defaultHeaders
    if headers is not None:
      for header in headers.keys():
        res[header] = headers[header]
    return res

  def _getResponse(self, conn):
    return conn.getresponse()

  def _doRequestNoBody(self, method, url, data=None, headers=None):
    parts = self._parseURL(url)
    targeturl = parts['path']
    headers = self._mergeHeaders(headers)
    if not data is None:
      #URL encode data and append to URL
      if self.logger.getEffectiveLevel() == logging.DEBUG:
        self.logger.debug("DATA=%s" % str(data))
      if parts['query'] == '':
        parts['query'] = util.urlencode(data)
      else:
        parts['query'] = '%s&%s' % (parts['query'], \
                                    util.urlencode(data))
      targeturl = urlparse.urljoin(targeturl, "?%s" % parts['query'])
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      self.logger.debug('targetURL=%s' % targeturl)
      self.logger.debug('HEADERS=%s' % str(headers))
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    self._lasturl = '%s://%s:%s%s' % (
      parts['scheme'], parts['host'], parts['port'], targeturl
    )
    self._curlrequest = ['curl', '-X %s' % method]
    for h in headers.keys():
      self._curlrequest.append('-H "%s: %s"' % (h, headers[h]))
    self._curlrequest.append('"%s"' % self._lasturl)
    conn.request(method, targeturl, None, headers)
    return self._getResponse(conn)

  def _doRequestMMBody(self, method, url, data=None, files=None, headers=None):
    parts = self._parseURL(url)
    targeturl = parts['path']
    headers = self._mergeHeaders(headers)
    if not data is None:
      try:
        data.__getattribute__('keys')
        fdata = []
        for k in data.keys():
          fdata.append((k, data[k]))
      except:
        pass
      data = fdata
    else:
      data = []
    if files is None:
      files = []
    mm = multipart(headers, data, files)
    headers['Content-Type'] = mm._get_content_type()
    headers['Content-Length'] = mm.getContentLength()
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      self.logger.debug('targetURL=%s' % targeturl)
      self.logger.debug('HEADERS=%s' % str(headers))
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    self._lasturl = '%s://%s:%s%s' % (
      parts['scheme'], parts['host'], parts['port'], targeturl
    )
    self._curlrequest = ['curl', '-X %s' % method]
    for h in headers.keys():
      self._curlrequest.append('-H "%s: %s"' % (h, headers[h]))
    for d in data:
      self._curlrequest.append('-F %s=%s' % (d[0], d[1]))
    for f in files:
      self._curlrequest.append('-F %s=@%s' % (f['name'], f['filename']))
    self._curlrequest.append('"%s"' % self._lasturl)
    conn.request(method, targeturl, mm, headers)
    return self._getResponse(conn)

  def getLastRequestAsCurlCommand(self):
    return " ".join(self._curlrequest)

  def getlastUrl(self):
    return self._lasturl

  def GET(self, url, data=None, headers=None):
    '''Perform a HTTP GET and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.
    
    :param url: The full URL to the target
    :type url: String
    :param data: Parameters that will be encoded in the query portion of the 
      final URL.
    :type data: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('GET', url, data=data, headers=headers)

  def HEAD(self, url, data=None, headers=None):
    '''Perform a HTTP HEAD and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. Note that HEAD 
    requests return no body.
    
    :param url: The full URL to the target
    :type url: String
    :param data: Parameters that will be encoded in the query portion of the 
      final URL.
    :type data: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('HEAD', url, data, headers)

  def DELETE(self, url, data=None, headers=None):
    '''Perform a HTTP DELETE and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.
    
    :param url: The full URL to the target
    :type url: String
    :param data: Parameters that will be encoded in the query portion of the 
      final URL.
    :type data: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('DELETE', url, data, headers)

  def POST(self, url, data=None, files=None, headers=None):
    '''Perform a HTTP POST and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The full URL to the target
    :type url: String
    :param data: Parameters that will be send in the message body.
    :type data: dictionary of key-value pairs, or list of (key, value)
    :param files: List of files that will be sent with the POST request. The
      "name" is the name of the parameter in the MM body, "filename" is the 
      value of the "filename" parameter in the MM body, and "value" is a 
      file-like object open for reading that will be transmitted. 
    :type files: list of (name, filename, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestMMBody('POST', url, data, files, headers)

  def PUT(self, url, data=None, files=None, headers=None):
    '''Perform a HTTP PUT and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The full URL to the target
    :type url: String
    :param data: Parameters that will be send in the message body.
    :type data: dictionary of key-value pairs, or list of (key, value)
    :param files: List of files that will be sent with the POST request. The
      "name" is the name of the parameter in the MM body, "filename" is the 
      value of the "filename" parameter in the MM body, and "value" is a 
      file-like object open for reading that will be transmitted. 
    :type files: list of (name, filename, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestMMBody('PUT', url, data, files, headers)

#=============================================================================


class DataONEBaseClient(RESTClient):
  '''Same as RESTClient except that if the HTTPStatus code is not
  within the OK response range, then an attempt to raise a DataONE
  exception is made. If unsuccessful, the response is returned but
  read() will not return anything. The response bytes are held in 
  the *body* attribute.
  
  Also implements DataONE API methods that are common to both Member and
  Coordinating Nodes.
  
  Unless otherwise indicated, methods with names that end in "Response" return 
  the HTTPResponse object, otherwise the de-serialized object is returned.
  '''

  def __init__(self, baseurl, defaultHeaders={}, timeout=10, keyfile=None,
               certfile=None, strictHttps=True):
    if not defaultHeaders.has_key('Accept'):
      defaultHeaders['Accept'] = const.DEFAULT_MIMETYPE
    if not defaultHeaders.has_key('User-Agent'):
      defaultHeaders['User-Agent'] = const.USER_AGENT
    if not defaultHeaders.has_key('Charset'):
      defaultHeaders['Charset'] = const.DEFAULT_CHARSET
    RESTClient.__init__(
      self,
      defaultHeaders=defaultHeaders,
      timeout=timeout,
      keyfile=keyfile,
      certfile=certfile,
      strictHttps=strictHttps
    )
    self.baseurl = baseurl
    self.logger = logging.getLogger('DataONEBaseClient')
    ## A dictionary that provides a mapping from method name (from the DataONE
    ## APIs to a string format pattern that will be appended to the baseurl
    self.methodmap = {
      'get': u'object/%(pid)s',
      'getsystemmetadata': u'meta/%(pid)s',
      'listobjects': u'object',
      'getlogrecords': u'log',
      'ping': u'health/ping'
    }
    self.methodmap['listnodes'] = u'node'
    self.lastresponse = None

  def _getResponse(self, conn):
    res = conn.getresponse()
    self.lastresponse = res
    if self.isHttpStatusOK(res.status):
      return res
    res.body = res.read()
    serializer = exception_serialization.DataONEExceptionSerialization(None)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    try:
      if format.startswith(const.MIMETYPE_XML):
        raise (serializer.deserialize_xml(res.body))
      elif format.startswith(const.MIMETYPE_JSON):
        raise (serializer.deserialize_json(res.body))
      raise Exception("No DataONE exception in response. " + \
                      "content-type = %s" % format)
    except ValueError, e:
      logging.error("Invalid error message returned. " +\
                    "Deserializing raised: %s" % str(e))
    return res

  def _getAuthHeader(self, token):
    if token is not None:
      return {const.AUTH_HEADER_NAME: str(token)}
    return None

  def _normalizeTarget(self, target):
    if not target.endswith('/'):
      target += '/'
    return target

  def _makeUrl(self, meth, **args):
    meth = meth.lower()
    for k in args.keys():
      args[k] = util.encodePathElement(args[k])
    base = self._normalizeTarget(self.baseurl)
    path = self.methodmap[meth] % args
    url = urlparse.urljoin(base, path)
    self.logger.debug("%s URL=%s" % (meth, url))
    return url

  def isHttpStatusOK(self, status):
    status = int(status)
    if status >= 100 and status < 400:
      return True
    return False

  def get(self, token, pid):
    '''Implements CRUD.get()
    
    :param token: Authentication token
    :param pid: Identifier
    :returns: HTTPResponse instance, a file like object that supports read().
    :return type: HTTPResponse
    '''
    url = self._makeUrl('get', pid=pid)
    self.logger.info("URL = %s" % url)
    return self.GET(url, headers=self._getAuthHeader(token))

  def getSystemMetadataResponse(self, token, pid):
    '''Implements the MN getSystemMetadata call, returning a HTTPResponse 
    object. See getSystemMetada() for method that returns a deserialized
    system metadata object.
    
    :return type: HTTPResponse
    '''
    url = self._makeUrl('getSystemMetadata', pid=pid)
    self.logger.info("URL = %s" % url)
    return self.GET(url, headers=self._getAuthHeader(token))

  def getSystemMetadata(self, token, pid):
    '''
    :return type: SystemMetadata
    '''
    res = self.getSystemMetadataResponse(token, pid)
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    return systemmetadata.CreateFromDocument(res.read(), )

  def listObjectsResponse(
    self,
    token,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS
  ):
    '''
    :return type: HTTPResponse
    '''
    url = self._makeUrl('listObjects')
    params = {}
    if startTime is not None:
      params['startTime'] = startTime
    if endTime is not None:
      params['endTime'] = endTime
    if objectFormat is not None:
      params['objectFormat'] = objectFormat
    if replicaStatus is not None:
      params['replicaStatus'] = replicaStatus
    if start is not None:
      params['start'] = str(int(start))
    if count is not None:
      params['count'] = str(int(count))
    return self.GET(url, data=params, headers=self._getAuthHeader(token))

  def listObjects(
    self,
    token,
    startTime=None,
    endTime=None,
    objectFormat=None,
    replicaStatus=None,
    start=0,
    count=const.DEFAULT_LISTOBJECTS
  ):
    '''
    :return type: ObjectList
    '''
    res = self.listObjectsResponse(
      token,
      startTime=startTime,
      endTime=endTime,
      objectFormat=objectFormat,
      replicaStatus=replicaStatus,
      start=start,
      count=count
    )
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    serializer = objectlist_serialization.ObjectList()
    return serializer.deserialize(res.read(), format)

  def getLogRecordsResponse(self, token, fromDate, toDate=None, event=None):
    '''
    :return type: HTTPResponse
    '''
    url = self._makeUrl('log')
    params = {'fromDate': fromDate}
    if not toDate is None:
      params['toDate'] = toDate
    if not event is None:
      params['event'] = event
    return self.GET(url, data=params, headers=self._getAuthHeader(token))

  def getLogRecords(self, token, fromDate, toDate=None, event=None):
    '''
    :return type: LogRecords
    '''
    response = self.getLogRecordsResponse(token, fromDate, toDate=toDate, event=event)

    format = response.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = logrecords_serialization.LogRecords()
    return deser.deserialize(response.read(), format)

  def ping(self):
    '''
    :return type: Boolean
    '''
    url = self._makeUrl('ping')
    try:
      response = self.GET(url)
    except Exception, e:
      logging.exception(e)
      return False
    if response.status == 200:
      return True
    return False

  def isAuthorized(self, token, pid, action):
    '''
    '''
    raise Exception('Not Implemented')

  def setAccess(self, token, pid, accessPolicy):
    '''
    '''
    raise Exception('Not Implemented')

  def listNodesResponse(self):
    url = self._makeUrl('listnodes')
    response = self.GET(url)
    return response

  def listNodes(self):
    res = self.listNodesResponse()
    format = res.getheader('content-type', const.DEFAULT_MIMETYPE)
    deser = nodelist_serialization.NodeList()
    return deser.deserialize(res.read(), format)
