#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
''':mod:`solr_client`
====================

:Synopsis:
 - Generate and run queries against Solr.
:Author: DataONE (Dahl)
'''

# Stdlib.
import HTMLParser
import httplib
import logging
import os
import pprint
import socket
import urllib
import urlparse

# D1.
import d1_client.solr_client
import d1_common.const
import d1_common.date_time
import d1_common.url

# App.
import path_exception
import query_engine_description
import settings

# Set up logger for this module.
log = logging.getLogger(__name__)

#===============================================================================
'''
If path is for facet name container, list unapplied facet names then result of
query based on applied facets.

if path is for facet value container, list facet names / counts, then result of
query based on applied facets.

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=0&facet=true&
indent=on&wt=python&facet.field=genus_s&facet.limit=10&facet.zeros=false&facet.s
ort=false

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10&facet=true
&facet.field=rightsHolder
'''


# SolrConnection is a thin layer on top of HTTPSConnection that automatically
# retries queries and connection attempts.
class SolrConnection(object):
  def __init__(
    self,
    base_url=settings.DATAONE_ROOT,
    solr_selector='/v1/query/solr/',
    _n_tries=3
  ):
    self._base_url = base_url
    self._solr_host = self._get_hostname(base_url)
    self._solr_selector = self._get_solr_selector(base_url, solr_selector)
    self._connection = self._create_connection()
    self._n_tries = _n_tries

  def get(self, query_url, headers=None):
    if headers is None:
      headers = {}
    abs_query_url = self._solr_selector + '?' + query_url
    for i in range(self._n_tries):
      log.debug('get({0}{1})'.format(self._solr_host, abs_query_url))
      try:
        self._connection.request('GET', abs_query_url, headers=headers)
        response = self._connection.getresponse()
      except (
        httplib.BadStatusLine, httplib.CannotSendRequest, socket.error,
        httplib.HTTPException
      ) as e:
        log.exception('Solr query failed: {0}: Exception:'.format(query_url))
        self._connection = self._create_connection()
      else:
        self._assert_response_is_ok(response)
        return response.read()

    raise path_exception.PathException(
      'Giving up Solr query after {0} tries: {1}'.format(self._n_tries, query_url)
    )

  def _assert_response_is_ok(self, response):
    if response.status not in (200, ):
      try:
        html_doc = response.read()
      except:
        html_doc = ''
      #s = SimpleHTMLToText()
      #txt_doc = s.get_text(html_doc)
      log.error(
        'Error in Solr response: {0}\n{1}\n{2}'
        .format(response.status, response.reason, html_doc)
      )
      raise path_exception.PathException(
        'Error in Solr response: {0}'.format(response.reason)
      )
      #raise Exception(msg)

  def _create_connection(self):
    log.info('Creating new connection to Solr')
    return httplib.HTTPSConnection(self._solr_host)

  def _get_hostname(self, base_url):
    return urlparse.urlsplit(base_url).netloc

  def _get_solr_selector(self, base_url, solr_selector):
    base_selector = urlparse.urlsplit(base_url).path
    return d1_common.url.joinPathElementsNoStrip(base_selector, solr_selector)

#===============================================================================


class SolrClient(object):
  def __init__(self, base_url=settings.DATAONE_ROOT,
               relative_solr_path=settings.SOLR_QUERY_PATH,
               filter_query=None, # settings.SOLR_FILTER_QUERY,
               solr_debug=settings.SOLR_DEBUG
               ):
    self._solr_connection = SolrConnection(base_url)
    self.custom_filter_query = filter_query
    self.solr_debug = solr_debug
    #self.solr_path = self.get_solr_path(base_url, relative_solr_path)
    self.base_url = base_url

  def query(self, query, field_list, filter_query=None):
    query_params = [
      ('q', query),
      ('fl', field_list), #'id,dateModified,size,formatId'),
      ('rows', settings.MAX_OBJECTS_FOR_SEARCH),
      ('indent', 'on'),
      #('facet', 'true'),
      #('facet.limit', '5'),
      #('facet.mincount', '1'),
      #('facet.sort', 'count'),
      #('facet.count', 'sort'),
      #('group.facet', 'true'),
      ('wt', 'python'),
    ]
    if filter_query is not None:
      query_params.append(('fq', filter_query))

    #print query_params
    return self._get_query(query_params)
    #response = self.send_request(query_params)
    #unapplied_facet_counts, entries = self.parse_result_dict(response)
    #return unapplied_facet_counts, entries

    # Disk cashed _get_query() for faster debugging.
  def _get_query(self, params):
    import hashlib
    query_url = urllib.urlencode(params, doseq=True)
    sha1 = hashlib.sha1(query_url).hexdigest()
    try:
      with open(os.path.join('cache', sha1)) as f:
        log.debug('SOLR DISK CACHE({0}, {1})'.format(sha1, query_url))
        response = f.read()
    except IOError:
      log.debug("SOLR GET = %s" % query_url)
      response = self._solr_connection.get(query_url)
      with open(os.path.join('cache', sha1), 'w') as f:
        f.write(response)
    return eval(response)

  #def raw_query(self, query_string):
  #  query_params = [tuple(field_value.split('=')) for field_value in query_string.split('&')]
  #  query_params.append(('fl', 'python'))
  #  query_params.append(('wt', 'python'))
  #  ('rows', settings.MAX_OBJECTS_IN_DIRECTORY),
  #  return self.send_request(query_params)

  ## Want to return a result that:
  ## - starts with all available objects
  ## - returns the objects that match the applied facets.
  ## - includes a list of all the unapplied facets and their counts, for counts > 0
  #def faceted_search(self, all_facet_names, applied_facets, filter_queries):
  #  unapplied_facets = self.get_unapplied_facets(all_facet_names, applied_facets)
  #  unapplied_facet_fields = self.facet_fields_from_facet_names(unapplied_facets)
  #  query_params = [
  #    ('q', '*:*'),
  #    ('fq', self.format_filter_query(applied_facets)),
  #    ('fl', 'id,dateModified,size,formatId'),
  #    ('rows', settings.MAX_OBJECTS_IN_DIRECTORY),
  #    ('indent', 'on'),
  #    ('facet', 'true'),
  #    ('facet.limit', '5'),
  #    ('facet.mincount', '1'),
  #    ('facet.sort', 'count'),
  #    #('facet.count', 'sort'),
  #    #('group.facet', 'true'),
  #    ('wt', 'python'),
  #  ]
  #  query_params.extend(unapplied_facet_fields)
  #  query_params.extend(filter_queries)
  #  response = self.send_request(query_params)
  #  #log.debug(pprint.pformat(response))
  #  unapplied_facet_counts, entries = self.parse_result_dict(response)
  #  return unapplied_facet_counts, entries

  #def format_filter_query(self, applied_facets):
  #  return ' AND '.join(['{0}:{1}'.format(f[0],
  #    self.escape_query_term(f[1])) for f in applied_facets])

  #  def create_filter_query(self, all_facet_names, applied_facets, unapplied_facets):
  #    facet_settings = ['rows=100', 'facet=true', 'facet.limit=10',
  #                      'facet.count=sort']
  #    unapplied_facets_string = self.create_facet_query_segment_for_unapplied_facets(
  #      unapplied_facets)
  #    return '*:*&{0}&{1}'.format('&'.join(facet_settings),
  #                                unapplied_facets_string)

  #def facet_fields_from_facet_names(self, facet_names):
  #  return [('facet.field', f) for f in facet_names]

  #  def get_facet_fields_for_unapplied_facets(self, all_facet_names, applied_facets):
  #    unapplied_facets = self.get_unapplied_facets(all_facet_names, applied_facets)
  #    return ['facet.field={0}'.format(f) for f in unapplied_facets]

  #def get_unapplied_facets(self, all_facet_names, applied_facets):
  #  return list(set(all_facet_names) - set(f[0] for f in applied_facets))

  #  def get_facet_values_for_facet_name(self, applied_facets, facet_name):
  #    q = 'title:moorx' # moor
  #    q = 'text:#1;dnatsrednu'
  #    return self._solr_connection.fieldValues(facet_name, q=q)

  #def get_solr_path(self, base_url, relative_solr_path):
  #  base = urlparse.urlsplit(base_url).path
  #  return '/' + d1_common.url.joinPathElements(base, relative_solr_path) + '/'

  #def get_solr_base(self, base_url, relative_solr_path):
  #   return d1_common.url.joinPathElements(base_url, relative_solr_path) + '/'

  #  def create_facet_query_segment_for_unapplied_facets(self, unapplied_facets):
  #    facet_query = []
  #    for unapplied_facet in unapplied_facets:
  #      facet_query.append('facet.field={0}'.format(unapplied_facet))
  #    return '&'.join(facet_query)

  # Non-cached send_request()
  #def send_request(self, params):
  #  query_url = urllib.urlencode(params, doseq=True)
  #  log.debug("SOLR GET = %s" % query_url)
  #  response = self.get(query_url)
  #  return eval(response.read())

  #def parse_result_dict(self, d):
  #  unapplied_facet_counts = self.get_unapplied_facet_counts(d)
  #  entries = self.get_directory_entries(d)
  #  return unapplied_facet_counts, entries

  #def get_unapplied_facet_counts(self, d):
  #  facet_counts = d['facet_counts']['facet_fields']
  #  facets = {}
  #  for facet_name, facet_value_counts in facet_counts.items():
  #    facet_count_tuples = self.pair_list_elements(facet_value_counts)
  #    count = 0
  #    for facet in facet_count_tuples:
  #      count += int(facet[1])
  #    if count:
  #      facets[facet_name] = {
  #        'count': count,
  #        'values': facet_count_tuples,
  #      }
  #  return facets

  #def pair_list_elements(self, list_with_pairs):
  #  p = list_with_pairs[:]
  #  p.append(None)
  #  return zip(p[::2], p[1::2])

  #def get_directory_entries(self, d):
  #  docs = d['response']['docs']
  #  return [self.object_info_from_solr_record(r) for r in docs]

  #def object_info_from_solr_record(self, r):
  #  return {
  #    'pid': r['id'],
  #    'format_id': r['formatId'],
  #    'size': r['size'],
  #    'date': d1_common.date_time.from_iso8601(r['dateModified'])
  #  }
  #

  def escape_query_term(self, term):
    reserved = [
      '+',
      '-',
      '&',
      '|',
      '!',
      '(',
      ')',
      '{',
      '}',
      '[',
      ']',
      '^',
      '"',
      '~',
      '*',
      '?',
      ':',
    ]
    term = term.replace(u'\\', u'\\\\')
    for c in reserved:
      term = term.replace(c, u"\%s" % c)
    return term

  def escape_query_term_string(self, term):
    '''Escape a query term string and wrap it in quotes.
    '''
    return '"{0}"'.format(self.escape_query_term(term))

  #def prepare_query_term(self, field, term):
  #  '''
  #  Prepare a query term for inclusion in a query.  This escapes the term and
  #  if necessary, wraps the term in quotes.
  #  '''
  #  if term == "*":
  #    return term
  #  addstar = False
  #  if term[len(term)-1] == '*':
  #    addstar = True
  #    term = term[0:len(term)-1]
  #  term = self.escape_query_term(term)
  #  if addstar:
  #    term = '%s*' % term
  #  if self.getSolrType(field) in ['string', 'text', 'text_ws']:
  #    return '"%s"' % term
  #  return term

  #  def escapeVal(self,val):
  #    val = val.replace(u"&", u"&amp;")
  #    val = val.replace(u"<", u"&lt;")
  #    val = val.replace(u"]]>", u"]]&gt;")
  #    return self.encoder(val)[0]  #to utf8
  #
  #
  #  def escapeKey(self,key):
  #    key = key.replace(u"&", u"&amp;")
  #    key = key.replace(u'"', u"&quot;")
  #    return self.encoder(key)[0]  #to utf8

  # USED
  ################################################################################
  # UNUSED

  #  entries = self.getRecords(facetkey, facetval)

  #
  #
  #def query(q='*:*', fq=None, fields='*', pagesize=100):
  #  return solr_client.SOLRSearchResponseIterator(self._solr_connection, q,
  #    fq=fq, fields=fields, pagesize=pagesize)

  #  def encode_path_element(path_element):
  #    return urllib.quote(path_element.encode('utf-8'), safe=PATHELEMENT_SAFE_CHARS)

  #  def get_records(self, facet, term):
  #    self.logger.debug('get_records: {0}'.format(facet))
  #    fname = self.facets[facet]['f']
  #    sc = self.create_connection()
  #    q = "%s:%s" % (fname, sc.prepare_query_term(fname, term))
  #    self.logger.info("q= %s" % q)
  #    self.logger.info("fq = %s" % self.filter_query)
  #    records = solr_client.SOLRArrayResponseIterator(sc, q, fq=self.filter_query,
  #                                                   cols=self.fields,
  #                                                   pagesize=ITERATOR_PER_FETCH)
  #    return records
  #
  #
  #  def get_abstract(self, pid):
  #    ''':type pid: DataONE Persistent ID
  #    '''
  #    self.logger.debug('get_abstract: {0}'.format(pid))
  #    sc = self.create_connection()
  #    q = sc.prepare_query_term('identifier', pid)
  #    records = solr_client.SOLRArrayResponseIterator(sc, q, fq=self.filter_query,
  #                                                   cols=['abstract', ],
  #                                                   pagesize=ITERATOR_PER_FETCH)
  #    self.abstract_cache[pid] = ''
  #    for rec in records:
  #      if rec[0] is not None:
  #        self.abstract_cache[pid] = rec[0]
  #      break
  #    return self.abstract_cache[pid]

  #===============================================================================


class SimpleHTMLToText(HTMLParser.HTMLParser):
  def __init__(self):
    self.reset()
    self.fed = []

  def get_text(self, html):
    self.feed(html)
    return self.get_data()

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)
