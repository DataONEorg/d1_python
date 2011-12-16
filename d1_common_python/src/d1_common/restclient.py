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
:Author: DataONE (Vieglais, Dahl)
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
               host,
               scheme="https",
               port=None,
               timeout=const.RESPONSE_TIMEOUT, 
               defaultHeaders=None, 
               cert_path=None, 
               key_path=None, 
               strict=True):
    '''Connect to an HTTP service.

    :param host: Hostname.
    :type host: string
    :param scheme: HTTP protocol. Must be "http" or "https". Defaults to
      "https".
    :type scheme: string
    :param port: TCP/IP port. Defaults to 80 for HTTP and 443 for HTTPS.
    :type port: integer
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: integer
    :param defaultHeaders: headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param cert_path: Path to a PEM formatted certificate file.
    :type cert_path: string
    :param key_path: Path to a PEM formatted file that contains the private key
      for the certificate file. Only required if the certificate file does not
      itself contain a private key. 
    :type key_path: string
    :param strict: Raise BadStatusLine if the status line can’t be parsed
      as a valid HTTP/1.0 or 1.1 status line.
    :type strict: boolean
    :returns: None
    '''
    if defaultHeaders is None:
      defaultHeaders = {
        'User-Agent': const.USER_AGENT,
      }
    self.connection = self._connect(scheme, host, port, timeout, cert_path,
                                    key_path, strict)
    self.defaultHeaders = defaultHeaders
    self.logger = logging.getLogger(__file__)


  def _connect(self, scheme, host, port, timeout, cert_path, key_path, strict):
    '''Create connection object. As of Python 2.6, this does not establish a
    connection. Instead, a separate connection is established for each request.
    http://bugs.python.org/issue9740
    '''
    if scheme == 'https':
      return httplib.HTTPSConnection(host=host, port=port, timeout=timeout,
        cert_file=cert_path, key_file=key_path, strict=strict)
    else:
      return httplib.HTTPConnection(host, port, timeout)


  def _merge_default_headers(self, headers=None):
    if headers is None:
      headers = {}
    if self.defaultHeaders is not None:
      headers.update(self.defaultHeaders)
    return headers


  def _join_url_with_query_params(self, selector, query):
    if query is None:
      return selector
    else:
      return u'{0}?{1}'.format(selector, util.urlencode(query))


  def _get_curl_request(self, method, selector, query=None, headers=None):
    '''Get request as cURL command line for debugging.
    '''
    curl = []
    curl.append('curl -X {0}'.format(method))
    for k, v in headers.items():
      curl.append('-H "{0}: {1}"'.format(k, v))    
    curl.append('{0}'.format(self._join_url_with_query_params(selector, query)))
    return ' '.join(curl)


  def _get_response(self):
    '''Override this to provide automatic processing of response.
    '''
    return self.connection.getresponse()


  def _send_request(self, method, selector, body=None, query=None,
                    headers=None):
    '''Send request and retrieve response.

    :param method: HTTP verb. GET, HEAD, PUT, POST or DELETE.
    :type method: string
    :param selector: Selector URL.
    :type selector: string
    :param body: Request body
    :type body: string or open file-like object
    :param query: URL query parameters.
    :type query: dictionary
    :param headers: HTTP headers.
    :type headers: dictionary
    '''
    headers = self._merge_default_headers(headers)
    url = self._join_url_with_query_params(selector, query)
    self.logger.debug('operation: {0} {1}'.format(method, url))
    self.logger.debug('headers: {0}'.format(str(headers)))
    self.connection.request(method, url, body, headers)
    return self._get_response()
    

  def _send_mime_multipart_request(self, method, selector, query=None,
                                   headers=None, fields=None, files=None):
    '''Generate MIME multipart document, send it and retrieve response.

    :param method: HTTP verb. GET, HEAD, PUT, POST or DELETE.
    :type method: string
    :param selector: Selector URL.
    :type selector: string
    :param query: URL query parameters.
    :type query: dictionary
    :param headers: HTTP headers.
    :type headers: dictionary
    :param fields: MIME multipart document fields
    :type fields: dictionary of strings
    :param files: MIME multipart document files
    :type files: dictionary of file-like-objects
    '''
    if headers is None:
      headers = {}
    if fields is None:
      fields = {}
    if files is None:
      files = []
    mmp_body = multipart(fields, files)
    headers['Content-Type'] = mmp_body.get_content_type_header()
    headers['Content-Length'] = mmp_body.get_content_length()
    return self._send_request(method, selector, body=mmp_body,
                              query=query, headers=headers)


  def GET(self, url, query=None, headers=None):
    '''Perform a HTTP GET and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.

    :param url: The Selector URL to the target
    :type url: string
    :param query: Parameters that will be encoded in the query portion of
    the final URL.
    :type query: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._send_request('GET', url, query=query,
                              headers=headers)

  
  def HEAD(self, url, query=None, headers=None):
    '''Perform a HTTP HEAD and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. Note that HEAD 
    requests return no body.
    
    :param url: The Selector URL to the target
    :type url: string
    :param query: Parameters that will be encoded in the query portion of
    the final URL.
    :type query: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :returns: The result of the HTTP request
    :return type: httplib.HTTPResponse 
    '''
    return self._send_request('HEAD', url, query, headers)

  
  def DELETE(self, url, query=None, headers=None):
    '''Perform a HTTP DELETE and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method.
    
    :param url: The Selector URL to the target
    :type url: string
    :param query: Parameters that will be encoded in the query portion of
    the final URL.
    :type query: dictionary of key-value pairs, or list of (key, value)
    :param headers: Additional headers in addition to default to send
    :type headers: Dictionary
    :return: The result of the HTTP request
    :type return: httplib.HTTPResponse 
    '''
    return self._send_request('DELETE', url, query, headers)

  
  def POST(self, url, query=None, headers=None, fields=None, files=None):
    '''Perform a HTTP POST and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The Selector URL to the target
    :type url: string
    :param query: Parameters that will be send in the message body.
    :type query: dictionary of key-value pairs, or list of (key, value)
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
    return self._send_mime_multipart_request('POST', url, query, headers,
                                             fields, files)

  
  def PUT(self, url, query=None, headers=None, fields=None, files=None):
    '''Perform a HTTP PUT and return the response. All values are to be UTF-8
    encoded - no Unicode encoding is done by this method. The body of the POST 
    message is encoded using MIME multipart-mixed.
    
    :param url: The Selector URL to the target
    :type url: string
    :param query: Parameters that will be send in the message body.
    :type query: dictionary of key-value pairs, or list of (key, value)
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
    return self._send_mime_multipart_request('PUT', url, query, headers,
                                             fields, files)

