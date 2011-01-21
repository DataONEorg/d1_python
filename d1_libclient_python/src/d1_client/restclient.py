'''
Created on Jan 20, 2011

@author: vieglais
'''

import httplib
import urlparse
import urllib
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

  def _getConnection(self, scheme, host, port):
    if scheme == 'http':
      conn = httplib.HTTPConnection(host, port, self.timeout)
    else:
      conn = httplib.HTTPSConnection(
        host, port, self.keyfile, self.certfile, self.strictHttps, self.timeout
      )
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

  def _doRequestNoBody(self, method, url, data=None, headers=None):
    parts = self._parseURL(url)
    targeturl = parts['path']
    if not data is None:
      #URL encode data and append to URL
      if parts['query'] == '':
        parts['query'] = urllib.urlencode(data)
      else:
        parts['query'] = '%s&%s' % (parts['query'], urllib.urlencode(data))
      targeturl = urlparse.urljoin(targeturl, "?%s" % parts['query'])
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    conn.request(method, targeturl, None, self._mergeHeaders(headers))
    return conn.getresponse()

  def _doRequestMMBody(self, method, url, data=None, files=None, headers=None):
    parts = self._parseURL(url)
    targeturl = parts['path']
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    conn.request(method, targeturl, None, self._mergeHeaders(headers))
    mm = multipart(headers, data, files)
    headers['Content-Type'] = mm._get_content_type()
    headers['Content-Length'] = mm.getContentLength()
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    conn.request(method, targeturl, mm, self._mergeHeaders(headers))
    return conn.getresponse()

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
    return self._doRequestNoBody('GET', url, data, headers)

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
