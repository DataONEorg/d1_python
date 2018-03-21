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
"""Call the GMN D1 APIs directly through the Django test client

These methods provide a way to issue non-compliant requests to GMN that
(hopefully) cannot be created via d1_client. Examples of broken requests include
requests with incorrectly formatted URLs, multipart documents, and DataONE XML
types.

By issuing intentionally broken requests, unit tests can ensure that the error
paths in GMN work correctly.

These methods also allow testing handling of timezones in datetimes. Some such
tests cannot be issued via d1_client because PyXB, being based on the XML DOM,
automatically adjusts all non-naive datetimes to UTC.
"""

import io
import logging
import xml.etree.ElementTree

import d1_gmn.app.views.util
import d1_gmn.tests.gmn_mock

import d1_common.type_conversions
import d1_common.url
import d1_common.util
import d1_common.wrap.simple_xml
import d1_common.xml

import django.test


def create(version_tag, sciobj_bytes, sysmeta_xml):
  """Call MNStorage.create()"""
  with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
    with d1_common.wrap.simple_xml.wrap(sysmeta_xml) as xml:
      return _get_resp_dict(
        django.test.Client().post(
          d1_common.url.joinPathElements('/', version_tag, 'object'), {
            'pid': xml.get_element_text('identifier'),
            'object': ('content.bin', io.BytesIO(sciobj_bytes)),
            'sysmeta': ('sysmeta.xml', io.BytesIO(sysmeta_xml)),
          }
        )
      )


def create_stream(version_tag, sciobj_byteseam, sysmeta_xml):
  """Call MNStorage.create()"""
  with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
    with d1_common.wrap.simple_xml.wrap(sysmeta_xml) as xml:
      return _get_resp_dict(
        django.test.Client().post(
          d1_common.url.joinPathElements('/', version_tag, 'object'), {
            'pid': xml.get_element_text('identifier'),
            'object': ('content.bin', sciobj_byteseam),
            'sysmeta': ('sysmeta.xml', io.StringIO(sysmeta_xml)),
          }
        )
      )


def get(version_tag, pid):
  """Call MNRead.get()"""
  return _get_resp_dict(
    django.test.Client().get(
      d1_common.url.
      joinPathElements('/', version_tag, 'object', pid.encode('utf-8'))
    )
  )


def get_system_metadata(version_tag, pid):
  """Call MNRead.getSystemMetadata()"""
  return _get_resp_dict(
    django.test.Client()
    .get(d1_common.url.joinPathElements('/', version_tag, 'meta', pid))
  )


def list_objects(version_tag, pid=None, start=None, count=None):
  """Call MNRead.listObjects()"""
  url_path = d1_common.url.joinPathElements('/', version_tag, 'object')

  query_dict = {}
  if pid is not None:
    query_dict['identifier'] = pid
  if start is not None:
    query_dict['start'] = start
  if count is not None:
    query_dict['count'] = count

  url_str = _add_query(query_dict, url_path)

  return _get_resp_dict(django.test.Client().get(url_str))


def get_log_records(version_tag, pid=None, start=None, count=None):
  """Call MNCore.getLogRecords()"""
  url_path = d1_common.url.joinPathElements('/', version_tag, 'log')

  query_dict = {}
  if pid is not None:
    query_dict['identifier'] = pid
  if start is not None:
    query_dict['start'] = start
  if count is not None:
    query_dict['count'] = count

  url_str = _add_query(query_dict, url_path)

  return _get_resp_dict(django.test.Client().get(url_str))


def _add_query(query_dict, url_path):
  if query_dict:
    url_str = '{}?{}'.format(url_path, d1_common.url.urlencode(query_dict))
  else:
    url_str = url_path
  return url_str


def get_object_count(version_tag):
  """Get total number of objects for which one or more subj in
  {active_subj_list} have read access or better. """
  url_path = d1_common.url.joinPathElements('/', version_tag, 'object')
  # url_path += "?identifier={}".format(d1_common.url.encodeQueryElement(pid))
  resp_dict = _get_resp_dict(django.test.Client().get(url_path))
  if resp_dict['is_ok']:
    return int(
      xml.etree.ElementTree.fromstring(resp_dict['body_str']).attrib['count']
    )
  resp_dict.pop('response', None)
  raise Exception(
    'Unable to get object count. resp_dict={}'.
    format(d1_common.util.serialize_to_normalized_compact_json(resp_dict))
  )


def _get_resp_dict(response):
  """Log return status of a django.http.response.HttpResponse and arrange the
  response into a dict of items generally more convenient to work with from
  tests.
  """
  body_str = (
    ''.join(response.streaming_content)
    if response.streaming else response.content
  )
  is_ok = response.status_code in (200,)
  if not is_ok:
    logging.warning(
      'Request returned unexpected status code. status_code={} body="{}"'.
      format(response.status_code, body_str)
    )
  else:
    logging.info(
      'Request successful. status_code={}'.format(response.status_code)
    )
  return {
    'is_ok': is_ok,
    'status_code_int': response.status_code,
    'header_dict': dict(list(response.items())),
    'body_str': body_str,
    'response': response,
  }
