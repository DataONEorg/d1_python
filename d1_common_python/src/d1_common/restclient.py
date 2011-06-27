# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2011
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
Module d1_common.restclient
===========================

HTTP client that supports core REST operations using MIME multipart mixed
encoding.

:Created: 2010-03-09
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import httplib
import urlparse
import util
from d1_common import const
from d1_common.mime_multipart import multipart


class RESTClient(object):
  '''REST HTTP client that encodes POST and PUT using MIME multipart encoding.
  '''

  def __init__(self,
               defaultHeaders={'User-Agent': const.USER_AGENT},
               timeout=const.RESPONSE_TIMEOUT,
               keyfile=None,
               certfile=None,
               strictHttps=True):
    '''Constructor for RESTClient.
    
    :param defaultHeaders: list of headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param keyfile: name of a PEM formatted file that contains a private key. 
    :type keyfile: string
    :param certfile: PEM formatted certificate chain file.
    :type certfile: string
    :param strictHttps: 
    :type strictHttps: boolean
    '''
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
        host=host,
        port=port,
        key_file=self.keyfile,
        cert_file=self.certfile,
        strict=self.strictHttps,
        timeout=self.timeout
      )
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      conn.set_debuglevel(logging.DEBUG)
    return conn

  def _parseURL(self, url):
    parts = urlparse.urlsplit(url)
    res = {
      'scheme': parts.scheme,
      'host': parts.netloc.split(':')[0],
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

  def _doRequestNoBody(self, method, url, url_params=None, headers=None):
    parts = self._parseURL(url)
    targeturl = parts['path']
    headers = self._mergeHeaders(headers)
    if not url_params is None:
      #URL encode url_params and append to URL
      if self.logger.getEffectiveLevel() == logging.DEBUG:
        self.logger.debug("DATA=%s" % str(url_params))
      if parts['query'] == '':
        parts['query'] = util.urlencode(url_params)
      else:
        parts['query'] = '%s&%s' % (parts['query'], \
                                    util.urlencode(url_params))
      targeturl = urlparse.urljoin(targeturl, "?%s" % parts['query'])
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      self.logger.debug('targetURL=%s' % targeturl)
      self.logger.debug('HEADERS=%s' % str(headers))
    # Create the HTTP or HTTPS connection.
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    # Store URL and equivalent CURL request for debugging.
    self._lasturl = '%s://%s:%s%s' % (
      parts['scheme'], parts['host'], parts['port'], targeturl
    )
    self._curlrequest = ['curl', '-X %s' % method]
    for h in headers.keys():
      self._curlrequest.append('-H "%s: %s"' % (h, headers[h]))
    self._curlrequest.append('"%s"' % self._lasturl)
    # Perform request using specified HTTP verb.
    conn.request(method, targeturl, None, headers)
    return self._getResponse(conn)

  def _doRequestMMBody(
    self, method,
    url, url_params=None,
    headers=None,
    fields=None, files=None
  ):
    parts = self._parseURL(url)
    targeturl = parts['path']
    headers = self._mergeHeaders(headers)
    if not url_params is None:
      try:
        url_params.__getattribute__('keys')
        fdata = []
        for k in url_params.keys():
          fdata.append((k, url_params[k]))
      except:
        pass
      url_params = fdata
    if headers is None:
      headers = {}
    if fields is None:
      fields = {}
    if files is None:
      files = []
    mm = multipart(fields, files)
    headers['Content-Type'] = mm.get_content_type_header()
    headers['Content-Length'] = mm.get_content_length()
    if self.logger.getEffectiveLevel() == logging.DEBUG:
      self.logger.debug('targetURL=%s' % targeturl)
      self.logger.debug('HEADERS=%s' % str(headers))
    # Create the HTTP or HTTPS connection.
    conn = self._getConnection(parts['scheme'], parts['host'], parts['port'])
    # Store URL and equivalent CURL request for debugging.
    self._lasturl = '%s://%s:%s%s' % (
      parts['scheme'], parts['host'], parts['port'], targeturl
    )
    self._curlrequest = ['curl', '-X %s' % method]
    for h in headers.keys():
      self._curlrequest.append('-H "%s: %s"' % (h, headers[h]))
    for d in fields:
      self._curlrequest.append('-F %s=%s' % (d[0], d[1]))
    for f in files:
      #self._curlrequest.append('-F %s=@%s' % (f['name'], f['filename']))
      self._curlrequest.append('-F %s=@%s' % (f[0], f[1]))
    self._curlrequest.append('"%s"' % self._lasturl)
    # Perform request using specified HTTP verb.
    conn.request(method, targeturl, mm, headers)
    return self._getResponse(conn)

  def getLastRequestAsCurlCommand(self):
    '''Returns a curl command line equivalent of the last request issued by
    this client instance.
    
    :return type: unicode
    '''
    return u" ".join(self._curlrequest)

  def getlastUrl(self):
    '''Returns the last URL that was opened using this client instance.
    
    :return type: string
    '''
    return self._lasturl

  def GET(self, url, url_params=None, headers=None):
    '''Perform a HTTP GET and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.
    
    :param url: The full URL to the target
    :type url: String
    :param url_params: Parameters that will be encoded in the query portion of the 
      final URL.
    :type url_params: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('GET', url, url_params=url_params, headers=headers)

  def HEAD(self, url, url_params=None, headers=None):
    '''Perform a HTTP HEAD and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. Note that HEAD 
    requests return no body.
    
    :param url: The full URL to the target
    :type url: String
    :param url_params: Parameters that will be encoded in the query portion of the 
      final URL.
    :type url_params: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('HEAD', url, url_params, headers)

  def DELETE(self, url, url_params=None, headers=None):
    '''Perform a HTTP DELETE and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.
    
    :param url: The full URL to the target
    :type url: String
    :param url_params: Parameters that will be encoded in the query portion of the 
      final URL.
    :type url_params: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :return: The result of the HTTP request
    :type return: httplib.HTTPResponse 
    '''
    return self._doRequestNoBody('DELETE', url, url_params, headers)

  def POST(self, url, url_params=None, headers=None, fields=None, files=None):
    '''Perform a HTTP POST and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The full URL to the target
    :type url: String
    :param url_params: Parameters that will be send in the message body.
    :type url_params: dictionary of key-value pairs, or list of (key, value)
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
    return self._doRequestMMBody('POST', url, url_params, headers, fields, files)

  def PUT(self, url, url_params=None, headers=None, fields=None, files=None):
    '''Perform a HTTP PUT and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The full URL to the target
    :type url: String
    :param url_params: Parameters that will be send in the message body.
    :type url_params: dictionary of key-value pairs, or list of (key, value)
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
    return self._doRequestMMBody('PUT', url, url_params, headers, fields, files)
