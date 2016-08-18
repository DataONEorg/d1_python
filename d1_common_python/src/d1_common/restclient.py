# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Module d1_common.restclient

HTTP client that supports core REST operations using MIME multipart mixed
encoding.

Created: 2010-03-09
Author: DataONE (Vieglais, Dahl)
Refactored: 2016-04-04 by Vieglais
"""

# Stdlib.
from __future__ import absolute_import
import datetime
import logging
import types
import requests #pip install requests, or apt-get install python-requests
import cachecontrol #pip install cachecontrol

# D1
import d1_common.const
import d1_common.url
import d1_common.date_time

try:
  import requests_toolbelt.utils.dump
  _HAS_DUMP_CAPABILITY = True
except ImportError:
  logging.info("Install requests_toolbelt to enable dump of HTTP requests.")
  _HAS_DUMP_CAPABILITY = False

DEFAULT_NUMBER_OF_TRIES = 3


def responseRead(self, nbytes=None):
  """For backwards compatibility with old RESTClient

  Added to the response instance returned from various requests to provide
  method compatibility with the old httplib version of RESTClient
  """
  if not self.raw is None:
    return self.raw.read(nbytes)
  chunk = self.text[self.__fp:nbytes]
  self.__fp += len(chunk)
  return chunk

#===============================================================================


class RESTClient(object):
  """REST HTTP client that encodes POST and PUT using MIME multipart encoding.
  
  RESTClient may be reused across multiple targets, supports keep-alive 
  connections, and if enabled, will use a cache if cache control information is
  provided by servers.
  
  Example:
  
    cli = RESTClient()
    q = {'count':0}
    res = cli.GET("https://cn.dataone.org/cn/v2/object", query=q)
    print res
    <Response [200]>
    
    print res.content #returns bytes, typically utf-8 encoded xml
          res.text    #returns unicode
          res.read()  #res as a file like object, read() returns bytes
          
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="/cn/xslt/dataone.types.v2.xsl"?>
    <d1:objectList xmlns:d1="http://ns.dataone.org/service/types/v1" 
      count="0" start="0" total="1011042"/>
  """
  def __init__(self,
               host=None,
               scheme="https",
               port=None,
               timeout=d1_common.const.RESPONSE_TIMEOUT, # TODO: Ignored now. How are timeouts managed?
               n_tries=DEFAULT_NUMBER_OF_TRIES,
               defaultHeaders=None,
               cert_path=None,
               key_path=None,
               strict=None, # TODO: Ignored now. Keep for backwards compatibility?
               use_cache=True,
               user_agent=d1_common.const.USER_AGENT):
    """Initialize the RESTClient

    Args:
      host (string): If specified, then identifies the host portion of the URL. 
        This parameter is provided for backwards compatibility with prior 
        versions of RESTClient. It is strongly recommended to use the new style,
        which passes the full scheme + host + path in the URL parameter to 
        the different types of request.
        
      scheme (string): Provided for backward compatibility. See host for 
        details.
    
      timeout (int): Time in seconds that requests will wait for a response.
   
      n_tries (int): Number of times to try a request before failing.

      defaultHeaders (dict): headers that will be sent with all requests.

      cert_path (string): Path to a PEM formatted certificate file.

      key_path (string): Path to a PEM formatted file that contains the private 
        key for the certificate file. Only required if the certificate file 
        does not itself contain a private key.

      strict (bool): Raise BadStatusLine if the status line can’t be parsed
        as a valid HTTP/1.0 or 1.1 status line.

      use_cache (bool): Use cachecontrol library to support request caching. 
        This is strongly recommended.
    """
    self.logger = logging.getLogger(__file__)

    if host is not None:
      #self.logger.warn("Use of 'host' parameter is deprecated.")
      pass
    else:
      if scheme is None:
        error_str = "'scheme' must be provided when 'host' is used"
        self.logger.error(error_str)
        raise Exception(error_str) # TODO: Convert to D1 exception

      scheme = scheme.lower()

      if scheme not in ('http', 'https'):
        error_str = "'scheme' must be 'http' or 'https'"
        self.logger.error(error_str)
        raise Exception(error_str) # TODO: Convert to D1 exception

    if port is None and scheme is not None:
      port = 443 if scheme == 'https' else 80

    if defaultHeaders is None:
      defaultHeaders = {}

    defaultHeaders.setdefault(u'User-Agent', user_agent)

    self._host = host
    self._scheme = scheme
    self._port = port
    self._defaultHeaders = defaultHeaders
    # TODO: Add default keep-alive parameters for headers
    # TODO: Add default cache-control parameters for headers
    self._cert_path = cert_path
    self._key_path = key_path
    self._use_cache = use_cache
    self._n_tries = n_tries

    self._connection = self._connect(n_tries=n_tries)

  def GET(self, url, query=None, headers=None, n_tries=None, dump_path=None):
    """Perform an HTTP request and return the response. 
    
    Important: Any Unicode values must be UTF-8 encoded.

    Params:
      url (string): The Selector URL to the target

      query (dict): Parameters that will be encoded in the query portion of
        the final URL. If duplicate keys are to be sent, then encode like:
          {'data': ['hello', 'world'] }

      headers (dict): Additional headers in addition to default to send
  
    Returns:
      requests.Response: The server response to the HTTP request
    """
    return self._send_request(
      'GET',
      url,
      query=query,
      headers=headers,
      n_tries=n_tries,
      dump_path=dump_path
    )

  def HEAD(self, url, query=None, headers=None, n_tries=None, dump_path=None):
    """Perform a HTTP HEAD request.
    """
    return self._send_request(
      'HEAD',
      url,
      query=query,
      headers=headers,
      n_tries=n_tries,
      dump_path=dump_path
    )

  def DELETE(self, url, query=None, headers=None, n_tries=None, dump_path=None):
    """Perform a HTTP DELETE request
    """
    return self._send_request(
      'DELETE',
      url,
      query=query,
      headers=headers,
      n_tries=n_tries,
      dump_path=dump_path
    )

  def POST(
    self,
    url,
    query=None,
    headers=None,
    fields=None,
    files=None,
    n_tries=None,
    dump_path=None
  ):
    """Perform a POST request using multipart encoding.
    
    POST and PUT accepts the same parameters as GET, HEAD and DELETE.
    In addition, they accept paramters that are encoded into a MIME
    multipart-mixed document and submitted in the request.

    Params:

      fields (list of (name, value)): List of fields that will be 
        included in the MIME document. Each field in the list is a name / value 
        pair.

      files (list of (name, filename, value)): List of files that will be 
        included in the MIME document. The "name" is the name of the parameter 
        in the MMP, "filename" is the value of the "filename" parameter in the 
        MMP, and "value" is a file-like object open for reading that will be 
        transmitted.

      dump_path (string): For debugging, the generated HTTP request can be 
        written to the specified file.
    """
    return self._send_request(
      'POST',
      url,
      query=query,
      headers=headers,
      files=files,
      fields=fields,
      n_tries=n_tries,
      dump_path=dump_path
    )

  def PUT(
    self,
    url,
    query=None,
    headers=None,
    fields=None,
    files=None,
    n_tries=None,
    dump_path=None
  ):
    """Perform a HTTP PUT request.
    """
    return self._send_request(
      'PUT',
      url,
      query=query,
      headers=headers,
      fields=fields,
      files=files,
      n_tries=n_tries,
      dump_path=dump_path
    )

  ##########################################
  # Private Methods: For internal use and subject to change.
  #
  def _connect(self, n_tries=DEFAULT_NUMBER_OF_TRIES):
    """Create cached session object for managing connections.
    
    Returned in a CachedSession instance which provides automated thread safe 
    caching support for the requests library. 

    Requests : http://docs.python-requests.org/en/master/
    
    CacheControl : http://cachecontrol.readthedocs.org/en/latest/
    
    Params:
      n_tries (int): Retry connections this many times before bailing.
    """
    session = requests.Session()
    session.stream = True
    if n_tries is not None:
      self._n_tries = n_tries
      session.mount(
        'http://', requests.adapters.HTTPAdapter(
          max_retries=n_tries
        )
      )
      session.mount(
        'https://',
        requests.adapters.HTTPAdapter(
          max_retries=n_tries
        )
      )

    if self._use_cache:
      session.mount('http://', cachecontrol.CacheControlAdapter())
      session.mount('https://', cachecontrol.CacheControlAdapter())
    return session

  def _prepare_url(self, url):
    if self._host is not None:
      #Support old style implementation that take host and scheme in 
      #constructor
      if not url.lower().startswith('http'):
        url = "{0}://{1}:{2}{3}".format(
          self._scheme, self._host, self._port, url
        )
    return url

  def _send_request(
    self,
    method,
    url,
    query=None,
    headers=None,
    body=None, # TODO: Ignored now. How to handle?
    files=None,
    fields=None,
    n_tries=None,
    dump_path=None
  ):
    """Send request and retrieve response.

    Params:
      method (string): HTTP verb. GET, HEAD, PUT, POST or DELETE.

      url (string): The full URL not including query parameters.

      body (string or file-like object): Request body

      query (dict): URL query parameters.

      headers (dict): HTTP headers.
    """
    url = self._prepare_url(url)
    if n_tries is not None:
      if n_tries != self._n_tries:
        self._connection = self._connect(n_tries=n_tries)
    headers = self._merge_default_headers(headers)
    cert = None
    if self._cert_path is not None:
      if self._key_path is not None:
        cert = (self._cert_path, self._key_path)
      else:
        cert = self._cert_path

    # # In DataONE, all POST data is sent by mime-multipart encoding. Merge the
    # # fields and files to a form expected by the requests library.
    # file_list = []
    # if not files is None:
    #   for f in files:
    #     # This is a requests expected structure of:
    #     # ( (param_name, (file_name, file or body, [optional mime type])) )
    #     if len(f) == 2 and not isinstance(f[1], basestring):
    #       file_list.append(f)
    #     else:
    #       # Old style RESTClient expects a structure of:
    #       # ( (param_name, file_name, file or body) )
    #       file_list.append((f[0], (f[1], f[2])))
    # # Append anything from fields:
    # if not fields is None:
    #   # Is it a dictionary structure?
    #   if isinstance(fields, dict):
    #     for k, v in fields.items():
    #       file_list.append((k, (k, v)))
    #   else:
    #     # or maybe a list of tuples?
    #     for f in fields:
    #       file_list.append(f)
    # if len(file_list) < 1:
    #   file_list = None

    file_list = None
    if not files is None:
      file_list = []
      for f in files:
        # This is a requests expected structure of:
        # ( (param_name, (file_name, file or body, [optional mime type])) )
        if len(f) == 2 and not isinstance(f[1], basestring):
          file_list.append(f)
        else:
          # Old style RESTClient expects a structure of:
          # ( (param_name, file_name, file or body) )
          file_list.append((f[0], (f[1], f[2])))

    field_list = None
    if not fields is None:
      field_list = []
      if isinstance(fields, dict):
        for k, v in fields.items():
          field_list.append((k, (k, v)))
      else:
        for f in fields:
          field_list.append(f)

    # Encode any datetime query parameters to ISO8601.
    if query is not None:
      if isinstance(query, dict):
        for k, v in query.items():
          if isinstance(v, datetime.datetime):
            query[k] = v.isoformat()

    response = self._connection.request(
      method,
      url,
      params=query,
      headers=headers,
      cert=cert,
      files=file_list,
      data=field_list,
      stream=True,
      allow_redirects=False
    )
    if dump_path is not None:
      if _HAS_DUMP_CAPABILITY:
        with open(dump_path, 'wb') as rdump:
          rdump.write(requests_toolbelt.utils.dump.dump_all(response))
      else:
        self.logger.error(
          "Request / response dump requests but requests_toolbelt not installed!"
        )
    response.read = types.MethodType(responseRead, response)
    response.__fp = 0
    response.status = response.status_code
    return response

  def _merge_default_headers(self, headers=None):
    if headers is None:
      headers = {}
    if self._defaultHeaders is not None:
      headers.update(self._defaultHeaders)
    return headers

  def _get_curl_request(self, method, url, query=None, headers=None):
    """Get request as cURL command line for debugging.
    """
    if not query is None:
      full_url = u'{0}?{1}'.format(url, d1_common.url.urlencode(query))
    curl = []
    curl.append(u'curl -X {0}'.format(method))
    for k, v in headers.items():
      curl.append(u'-H "{0}: {1}"'.format(k, v))
    curl.append(u'{0}'.format(full_url))
    return ' '.join(curl)
