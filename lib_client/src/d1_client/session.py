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

import copy
import datetime
import logging
import os
import urllib.parse

import requests
import requests.adapters
import requests_toolbelt
import requests_toolbelt.utils.dump

import d1_common.const
import d1_common.date_time
import d1_common.url
import d1_common.util

import d1_client.util

DEFAULT_NUMBER_OF_RETRIES = 1
DEFAULT_USE_STREAM = False
DEFAULT_VERIFY_TLS = True
DEFAULT_SUPPRESS_VERIFY_WARNINGS = False

UBUNTU_CA_BUNDLE_PATH = '/etc/ssl/certs/ca-certificates.crt'


class Session(object):
  def __init__(
      self, base_url, cert_pem_path=None, cert_key_path=None, **kwargs_dict
  ):
    """The Session improves performance by keeping connection related state and
    allowing it to be reused in multiple API calls to a DataONE Coordinating
    Node or Member Node. This includes:

    - A connection pool
    - HTTP persistent connections (HTTP/1.1 and keep-alive)

    Based on Python Requests:
    - http://docs.python-requests.org/en/master/
    - http://docs.python-requests.org/en/master/user/advanced/#session-objects

    :param base_url: DataONE Node REST service BaseURL.
    :type host: string

    :param cert_pem_path: Path to a PEM formatted certificate file.
    :type cert_pem_path: string

    :param cert_key_path: Path to a PEM formatted file that contains the private
      key for the certificate file. Only required if the certificate file does
      not itself contain the private key.
    :type cert_key_path: string

    :param timeout_sec: Time in seconds that requests will wait for a response.
      None, 0, 0.0 disables timeouts. Default is DEFAULT_HTTP_TIMEOUT, currently 60
      seconds.
    :type timeout_sec: float, int, None

    :param retries: Set number of times to try a request before failing. If not
      set, retries are still performed, using the default number of retries. To
      disable retries, set to 1.
    :type retries: int

    :param headers: headers that will be included with all connections.
    :type headers: dictionary

    :param query: URL query parameters that will be included with all
      connections.
    :type query: dictionary

    :param use_stream: Use streaming response. When enabled, responses must be
      completely read to free up the connection for reuse. (default:False)
    :type use_stream: bool

    :param verify_tls: Verify the server side TLS/SSL certificate.
      (default: True). Can also hold a path that points to a trusted CA bundle
    :type verify_tls: bool or path

    :param suppress_verify_warnings: Suppress the warnings issued when
      {verify_tls} is set to False.
    :type suppress_verify_warnings: bool

    :param user_agent: Override the default User-Agent string used by d1client.
    :type user_agent: str

    :param charset: Override the default Charset used by d1client.
      (default: utf-8)
    :type charset: str

    :returns: None
    """
    self._base_url = base_url
    self._scheme, self._host, self._port, self._path = urllib.parse.urlparse(
      base_url
    )[:4]
    self._api_major = 1
    self._api_minor = 0
    # Adapter
    self._max_retries = kwargs_dict.pop('retries', DEFAULT_NUMBER_OF_RETRIES)
    # Option to suppress SSL/TLS verification warnings
    suppress_verify_warnings = kwargs_dict.pop(
      'suppress_verify_warnings', DEFAULT_SUPPRESS_VERIFY_WARNINGS
    )
    if suppress_verify_warnings:
      requests.packages.urllib3.disable_warnings()
    # Default parameters for requests
    self._default_request_arg_dict = {
      'params':
        self._datetime_to_iso8601(kwargs_dict.pop('query', {})),
      'timeout':
        kwargs_dict.pop('timeout_sec', d1_common.const.DEFAULT_HTTP_TIMEOUT),
      'stream':
        kwargs_dict.pop('use_stream', DEFAULT_USE_STREAM),
      'verify':
        kwargs_dict.pop('verify_tls', DEFAULT_VERIFY_TLS),
      'headers': {
        'User-Agent':
          kwargs_dict.pop('user_agent', d1_common.const.USER_AGENT),
        'Charset':
          kwargs_dict.pop('charset', d1_common.const.DEFAULT_CHARSET),
      },
    }
    # Use the OS trust store on Ubuntu and derivatives
    if self._default_request_arg_dict['verify'] is True:
      if os.path.isfile(UBUNTU_CA_BUNDLE_PATH):
        self._default_request_arg_dict['verify'] = UBUNTU_CA_BUNDLE_PATH
    # Default headers
    self._default_request_arg_dict['headers'].update(
      kwargs_dict.pop('headers', {})
    )
    self._default_request_arg_dict.update(kwargs_dict)
    # Requests wants cert path as string if single file and tuple if cert/key
    # pair.
    if cert_pem_path is not None:
      self._default_request_arg_dict['cert'] = (
        cert_pem_path,
        cert_key_path if cert_key_path is not None else cert_pem_path
      )
    self._session = self._create_requests_session()

  @property
  def base_url(self):
    return self._base_url

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
    pass a string, iterator or generator as the {data} argument. To post a
    multipart stream, pass a dictionary of multipart elements as the
    {fields} argument. E.g.:

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

  def OPTIONS(self, rest_path_list, **kwargs):
    """Send a OPTIONS request.
    See requests.sessions.request for optional parameters.
    :returns: Response object
    """
    return self._request('OPTIONS', rest_path_list, **kwargs)

  def get_curl_command_line(self, method, url, **kwargs):
    """Get request as cURL command line for debugging.
    """
    if kwargs.get('query'):
      url = '{}?{}'.format(url, d1_common.url.urlencode(kwargs['query']))
    curl_list = ['curl']
    if method.lower() == 'head':
      curl_list.append('--head')
    else:
      curl_list.append('-X {}'.format(method))
    for k, v in sorted(list(kwargs['headers'].items())):
      curl_list.append('-H "{}: {}"'.format(k, v))
    curl_list.append('{}'.format(url))
    return ' '.join(curl_list)

  def dump_request_and_response(self, response):
    """Return a string containing a nicely formatted representation of the
    request and response objects for logging and debugging
    - Note: Does not work if the request or response body is a MultipartEncoder
    object.
    """
    if response.reason is None:
      response.reason = '<unknown>'
    return d1_client.util.normalize_request_response_dump(
      requests_toolbelt.utils.dump.dump_response(response)
    )

  #
  # Private
  #

  def _create_requests_session(self):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=self._max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

  def _send_mmp_stream(self, method, rest_path_list, fields, **kwargs):
    url = self._prep_url(rest_path_list)
    kwargs = self._prep_request_kwargs(kwargs)
    mmp_stream = requests_toolbelt.MultipartEncoder(fields=fields)
    kwargs['data'] = mmp_stream
    kwargs['headers'].update({
      'Content-Type': mmp_stream.content_type,
      'Content-Length': str(mmp_stream.len),
    })
    return self._session.request(method, url, **kwargs)

  def _request(self, method, rest_path_list, **kwargs):
    url = self._prep_url(rest_path_list)
    kwargs = self._prep_request_kwargs(kwargs)
    logging.debug(
      'Request equivalent: {}'.format(
        self.get_curl_command_line(method, url, **kwargs)
      )
    )
    return self._session.request(method, url, **kwargs)

  def _prep_url(self, rest_path_list):
    if isinstance(rest_path_list, str):
      rest_path_list = [rest_path_list]
    return d1_common.url.joinPathElements(
      self._base_url, self._get_api_version_path_element(),
      *self._encode_path_elements(rest_path_list)
    )

  def _prep_request_kwargs(self, kwargs_in_dict):
    # TODO: Check if per-call args get the same processing as client create args
    kwargs_dict = {
      'timeout':
        self._timeout_to_float(kwargs_in_dict.pop('timeout_sec', 0.0)),
      'stream':
        kwargs_in_dict.pop('use_stream', None),
      'verify':
        kwargs_in_dict.pop('verify_tls', None),
      'params':
        self._format_query_values(kwargs_in_dict.pop('query', {})),
    }
    kwargs_dict.update(kwargs_in_dict)
    kwargs_dict = self._remove_none_value_items(kwargs_dict)
    result_dict = copy.deepcopy(self._default_request_arg_dict)
    if result_dict['timeout'] in (0, 0.0):
      result_dict['timeout'] = None
    d1_common.util.nested_update(result_dict, kwargs_dict)
    logging.debug(
      'Request kwargs:\n{}'.format(
        d1_common.util.serialize_to_normalized_compact_json(result_dict)
      )
    )
    return result_dict

  def _timeout_to_float(self, timeout):
    """Convert timeout to float. Return None if timeout is None, 0 or 0.0.
    timeout=None disables timeouts in Requests.
    """
    if timeout is not None:
      try:
        timeout_float = float(timeout)
      except ValueError:
        raise ValueError(
          'timeout_sec must be a valid number or None. timeout="{}"'.
          format(timeout)
        )
      if timeout_float:
        return timeout_float

  def _format_query_values(self, query_dict):
    return self._bool_to_string(
      self._datetime_to_iso8601(self._remove_none_value_items(query_dict))
    )

  def _remove_none_value_items(self, query_dict):
    return {k: v for k, v in list(query_dict.items()) if v is not None}

  def _datetime_to_iso8601(self, query_dict):
    """Encode any datetime query parameters to ISO8601."""
    return {
      k: v if not isinstance(v, datetime.datetime) else v.isoformat()
      for k, v in list(query_dict.items())
    }

  def _bool_to_string(self, query_dict):
    return {
      k: 'true' if v is True else 'false' if v is False else v
      for k, v in list(query_dict.items())
    }

  def _encode_path_elements(self, path_element_list):
    return [
      d1_common.url.encodePathElement(v)
      if isinstance(v,
                    (int, str)) else d1_common.url.encodePathElement(v.value())
      for v in path_element_list
    ]

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
