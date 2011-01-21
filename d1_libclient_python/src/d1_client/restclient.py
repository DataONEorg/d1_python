'''
Created on Jan 20, 2011

@author: vieglais
'''

import sys
import logging
import httplib
import urlparse
import urllib
from d1_common import const
from d1_common import exceptions
from d1_common.mime_multipart import multipart


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

  def _getConnection(self, scheme, host, port):
    if scheme == 'http':
      conn = httplib.HTTPConnection(host, port, self.timeout)
    else:
      conn = httplib.HTTPSConnection(
        host, port, self.keyfile, self.certfile, self.strictHttps, self.timeout
      )
    #conn.set_debuglevel(logging.DEBUG)
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
    if not data is None:
      #URL encode data and append to URL
      if self.logger.getEffectiveLevel() == logging.DEBUG:
        self.logger.debug("DATA=%s" % str(data))
      if parts['query'] == '':
        parts['query'] = self.urlencode(data)
      else:
        parts['query'] = '%s&%s' % (parts['query'], \
                                    self.urlencode(data))
      targeturl = urlparse.urljoin(targeturl, "?%s" % parts['query'])
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      self.logger.debug('targetURL=%s' % targeturl)
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    conn.request(method, targeturl, None, self._mergeHeaders(headers))
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
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    conn.request(method, targeturl, mm, headers)
    return self._getResponse(conn)

  def encodePathElement(self, element):
    return urllib.quote(element.encode('utf-8'), safe=':')

  def encodeQueryElement(self, element):
    return urllib.quote(element.encode('utf-8'), safe=':')

  def urlencode(self, query, doseq=0):
    '''Modified version of the standard urllib.urlencode that is conformant
    with RFC3986. The urllib version encodes spaces as '+' which can lead
    to inconsistency. This version will always encode spaces as '%20'.
    
    TODO: verify the unicode encoding process - looks a bit suspect.

    Encode a sequence of two-element tuples or dictionary into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.
    '''
    if hasattr(query, "items"):
      # mapping objects
      query = query.items()
    else:
      # it's a bother at times that strings and string-like objects are
      # sequences...
      try:
        # non-sequence items should not work with len()
        # non-empty strings will fail this
        if len(query) and not isinstance(query[0], tuple):
          raise TypeError
        # zero-length sequences of all types will get here and succeed,
        # but that's a minor nit - since the original implementation
        # allowed empty dicts that type of behavior probably should be
        # preserved for consistency
      except TypeError:
        ty, va, tb = sys.exc_info()
        raise TypeError, "not a valid non-string sequence or mapping object", tb

    l = []
    if not doseq:
      # preserve old behavior
      for k, v in query:
        k = self.encodeQueryElement(str(k))
        v = self.encodeQueryElement(str(v))
        l.append(k + '=' + v)
    else:
      for k, v in query:
        k = self.encodeQueryElement(str(k))
        if isinstance(v, str):
          v = self.encodeQueryElement(v)
          l.append(k + '=' + v)
        elif isinstance(v, unicode):
          # is there a reasonable way to convert to ASCII?
          # encode generates a string, but "replace" or "ignore"
          # lose information and "strict" can raise UnicodeError
          v = self.encodeQueryElement(v.encode("ASCII", "replace"))
          l.append(k + '=' + v)
        else:
          try:
            # is this a sufficient test for sequence-ness?
            x = len(v)
          except TypeError:
            # not a sequence
            v = self.encodeQueryElement(str(v))
            l.append(k + '=' + v)
          else:
            # loop over the sequence
            for elt in v:
              l.append(k + '=' + self.encodeQueryElement(str(elt)))
    return '&'.join(l)

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


class DataONEClient(RESTClient):
  '''Same as RESTClient except that if the HTTPStatus code is not
  within the OK response range, then an attempt to raise a DataONE
  exception is made. If unsuccessful, the response is returned but
  read() will not return anything. The response bytes are held in 
  the *body* attribute.
  '''

  def __init__(self, defaultHeaders={}, timeout=10, keyfile=None,
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

  def isHttpStatusOK(self, status):
    status = int(status)
    if status >= 100 and status < 400:
      return True
    return False

  def _getResponse(self, conn):
    res = conn.getresponse()
    if self.isHttpStatusOK(res.status):
      return res
    body = res.read()
    exc = exceptions.DataOneExceptionFactory.createException(body)
    if not exc is None:
      raise exc
    res.body = body
    return res
