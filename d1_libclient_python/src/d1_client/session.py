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

# Stdlib
import datetime
import logging
import pprint
import urlparse

# 3rd party
import requests # pip install requests[security]
import requests.adapters
import cachecontrol # pip install cachecontrol
import requests_toolbelt # pip install requests-toolbelt
import requests_toolbelt.utils.dump

# D1
import d1_common.const
import d1_common.url
import d1_common.date_time


DEFAULT_NUMBER_OF_RETRIES = 3


class Session(object):
  def __init__(
    self, base_url, cert_pem_path=None, cert_key_path=None, **kwargs
  ):
    """The Session improves performance by keeping connection related state and
    allowing it to be reused in multiple API calls to a DataONE Coordinating
    Node or Member Node. This includes:

    - A connection pool
    - HTTP persistent connections (HTTP/1.1 and keep-alive)
    - Cached responses

    Based on Python Requests:
    - http://docs.python-requests.org/en/master/
    - http://docs.python-requests.org/en/master/user/advanced/#session-objects

    CacheControl is used for automated thread safe caching support:
    - http://cachecontrol.readthedocs.org/en/latest/

    :param base_url: DataONE Node REST service BaseURL.
    :type host: string
    
    :param cert_pem_path: Path to a PEM formatted certificate file.
    :type cert_pem_path: string
    
    :param cert_key_path: Path to a PEM formatted file that contains the private
      key for the certificate file. Only required if the certificate file does
      not itself contain the private key.
    :type cert_key_path: string

    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: float or int

    :param retries: Set number of times to try a request before failing. If not
      set, retries are still performed, using the default number of retries. To
      disable retries, set to 1.
    :type retries: int
    
    :param headers: headers that will be included with all connections.
    :type headers: dictionary
    
    :param query: URL query parameters that will be included with all
      connections.
    :type query: dictionary

    :param use_cache: Use the cachecontrol library to cache request responses.
      (default: True)
    :type use_cache: bool

    :param use_stream: Use streaming response. When enabled, responses must be
      completely read to free up the connection for reuse. (default:False)
    :type use_stream: bool

    :param verify_tls: Verify the server side TLS/SSL certificate.
      (default: True)
    :type verify_tls: bool

    :param user_agent: Override the default User-Agent string used by d1client.
    :type user_agent: str

    :param charset: Override the default Charset used by d1client.
      (default: UTF-8)
    :type charset: str

    :returns: None
    """
    self._base_url = base_url
    self._scheme, self._host, self._port, self._path = urlparse.urlparse(
      base_url
    )[:4]
    self._cert_pem_path = cert_pem_path
    self._cert_key_path = cert_key_path

    # kwargs

    self._timeout_sec = kwargs.pop('timeout', d1_common.const.RESPONSE_TIMEOUT)
    self._n_retries = kwargs.pop('retries', DEFAULT_NUMBER_OF_RETRIES)

    self._headers = kwargs.pop('headers', {})
    self._headers.setdefault(
      u'User-Agent', kwargs.pop('user_agent', d1_common.const.USER_AGENT)
    )
    self._headers.setdefault(
      u'Charset', kwargs.pop('charset', d1_common.const.DEFAULT_CHARSET)
    )

    self._query_params = kwargs.pop('query', {})
    self._use_cache = kwargs.pop('use_cache', True)
    self._use_stream = kwargs.pop('use_stream', False)
    self._verify_tls = kwargs.pop('verify_tls', False)

    self._default_kwargs = kwargs

    self._create_requests_session()

  def GET(self, rest_path_list, **kwargs):
    """Send a GET request.
    See requests.sessions.request for optional parameters.
    :returns: Response object
    """
    return self._request('GET', rest_path_list, **kwargs)

  def HEAD(self, rest_path_list, **kwargs):
    """Send a HEAD request.
    See requests.sessions.request for optional parameters.
    :returns: Response object
    """
    kwargs.setdefault('allow_redirects', False)
    return self._request('HEAD', rest_path_list, **kwargs)

  def POST(self, rest_path_list, **kwargs):
    """Send a POST request with optional streaming multipart encoding.
    See requests.sessions.request for optional parameters. To post regular data,
    pass a string, iterator og generator as the `data` argument. To post a
    multipart stream, pass a dictionary multipart elements as the
    `fields` argument. E.g.:

    fields = {
      'field0': 'value',
      'field1': 'value',
      'field2': ('filename.xml', open('file.xml', 'rb'), 'application/xml')
    }

    :returns: Response object
    """
    fields = kwargs.pop('fields', None)
    if fields is not None:
      return self._send_mmp_stream('POST', rest_path_list, fields, **kwargs)
    else:
      return self._request('POST', rest_path_list, **kwargs)

  def PUT(self, rest_path_list, **kwargs):
    """Send a PUT request with optional streaming multipart encoding.
    See requests.sessions.request for optional parameters. See post() for
    parameters.
    :returns: Response object
    """
    fields = kwargs.pop('fields', None)
    if fields is not None:
      return self._send_mmp_stream('PUT', rest_path_list, fields, **kwargs)
    else:
      return self._request('PUT', rest_path_list, **kwargs)

  def DELETE(self, rest_path_list, **kwargs):
    """Send a DELETE request.
    See requests.sessions.request for optional parameters.
    :returns: Response object
    """
    return self._request('DELETE', rest_path_list, **kwargs)

  def get_curl_command_line(self, method, url, **kwargs):
    """Get request as cURL command line for debugging.
    """
    if kwargs['params']:
      url = u'{0}?{1}'.format(url, d1_common.url.urlencode(kwargs['params']))
    curl_cmd = []
    curl_cmd.append(u'curl -X {0}'.format(method))
    for k, v in kwargs['headers'].items():
      curl_cmd.append(u'-H "{0}: {1}"'.format(k, v))
    curl_cmd.append(u'{0}'.format(url))
    return ' '.join(curl_cmd)

  def dump_request_and_response(self, response):
    return requests_toolbelt.utils.dump.dump_response(response)

  #
  # Private
  #

  def _create_requests_session(self):
    self._session = requests.Session()
    self._session.stream = self._use_stream
    self._session.params = self._query_params

    if self._use_cache:
      adapter_cls = cachecontrol.CacheControlAdapter
    else:
      adapter_cls = requests.adapters.HTTPAdapter

    adapter = adapter_cls(max_retries=self._n_retries)

    self._session.mount('http://', adapter)
    self._session.mount('https://', adapter)

  def _send_mmp_stream(self, method, rest_path_list, fields, **kwargs):
    url = self._prep_url(rest_path_list)
    kwargs = self._prep_args(kwargs)
    mmp_stream = requests_toolbelt.MultipartEncoder(fields=fields)
    kwargs['data'] = mmp_stream
    kwargs['headers'].update({
      'Content-Type': mmp_stream.content_type,
      'Content-Length': str(mmp_stream.len),
    })
    return self._session.request(method, url, **kwargs)

  def _request(self, method, rest_path_list, **kwargs):
    url = self._prep_url(rest_path_list)
    kwargs = self._prep_args(kwargs)
    logging.info(self.get_curl_command_line(method, url, **kwargs))
    return self._session.request(method, url, **kwargs)

  def _prep_url(self, rest_path_list):
    if isinstance(rest_path_list, basestring):
      rest_path_list = [rest_path_list]
    return d1_common.url.joinPathElements(
      self._base_url,
      self._get_api_version_path_element(),
      *self._encode_path_elements(rest_path_list)
    )

  def _prep_args(self, kwargs):
    # Remove None kwargs
    kwargs = {k:v for k, v in kwargs.items() if v is not None}
    # Merge default kwargs
    kwargs.update(self._default_kwargs)
    # Encode any datetime query parameters to ISO8601
    kwargs['params'] = kwargs.pop('query', {})
    self._datetime_to_iso8601(kwargs['params'])
    # Merge default headers
    if kwargs.get('headers', None) is None:
      kwargs['headers'] = {}
    kwargs['headers'].update(self._headers)
    # Requests wants cert path as string if single file and tuple if cert/key
    # pair.
    if 'cert' not in kwargs:
      if self._cert_pem_path is not None:
        if self._cert_key_path is not None:
          kwargs['cert'] = self._cert_pem_path, self._cert_key_path
        else:
          kwargs['cert'] = self._cert_pem_path
    return kwargs

  def _datetime_to_iso8601(self, query):
    """Encode any datetime query parameters to ISO8601."""
    for k, v in query.items():
      if isinstance(v, datetime.datetime):
        query[k] = v.isoformat()

  def _encode_path_elements(self, path_element_list):
    return [d1_common.url.encodePathElement(v) for v in path_element_list]

  def _get_api_version_path_element(self):
    return 'v{}'.format(self._api_major)

  def _get_api_version_xml_type(self):
    if (self._api_major, self._api_minor) == (1, 0):
      return 'v1'
    else:
      return 'v{}.{}'.format(self._api_major, self._api_minor)

  def _get_expected_schema_type_attribute(self):
    return '{}{}'.format(
      d1_common.const.DATAONE_SCHEMA_ATTRIBUTE_BASE,
      self._get_api_version_xml_type()
    )
