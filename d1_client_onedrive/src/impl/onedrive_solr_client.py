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
import httplib
import HTMLParser
import logging
import os
import pprint
import query_engine_description
import settings
import socket
import urllib
import urlparse

# D1.
import d1_client.solr_client
import d1_common.const
import d1_common.url

# Set up logger for this module.
log = logging.getLogger(__name__)

#===============================================================================
'''
If path is for facet name container, list unapplied facet names then result of query based on applied facets.

if path is for facet value container, list facet names / counts, then result of query based on applied facets.

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=0&facet=true&indent=on&wt=python&facet.field=genus_s&facet.limit=10&facet.zeros=false&facet.sort=false

Yes, Simply add &facet=true&facet.field={fieldname} to your request Url.

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=10&facet=true&facet.field=rightsHolder

https://cn-dev-unm-1.test.dataone.org/cn/v1/query/solr/?q=*:*&rows=0&facet=true&facet.limit=10&facet.count=sort&facet.field=origin&facet.field=noBoundingBox&facet.field=endDate&facet.field=family&facet.field=text&facet.field=abstract&facet.field=rightsHolder&facet.field=LTERSite&facet.field=site&facet.field=datePublished&facet.field=topic&facet.field=edition&facet.field=geoform&facet.field=phylum&facet.field=gcmdKeyword&facet.field=keywords&facet.field=genus&facet.field=titlestr&facet.field=id&facet.field=decade&facet.field=sku&facet.field=isSpatial&facet.field=documents&facet.field=changePermission&facet.field=authorLastName&facet.field=author&facet.field=termText&facet.field=species&facet.field=source&facet.field=formatId&facet.field=contactOrganizationText&facet.field=obsoletes&facet.field=projectText&facet.field=updateDate&facet.field=parameter&facet.field=dateModified&facet.field=datasource&facet.field=kingdom&facet.field=topicText&facet.field=southBoundCoord&facet.field=westBoundCoord&facet.field=northBoundCoord&facet.field=isPublic&facet.field=namedLocation&facet.field=contactOrganization&facet.field=investigatorText&facet.field=resourceMap&facet.field=readPermission&facet.field=originator&facet.field=keyConcept&facet.field=writePermission&facet.field=siteText&facet.field=class&facet.field=parameterText&facet.field=originatorText&facet.field=term&facet.field=identifier&facet.field=pubDate&facet.field=eastBoundCoord&facet.field=keywordsText&facet.field=dateUploaded&facet.field=sensor&facet.field=beginDate&facet.field=title&facet.field=order&facet.field=sourceText&facet.field=presentationCat&facet.field=scientificName&facet.field=sensorText&facet.field=placeKey&facet.field=originText&facet.field=submitter&facet.field=isDocumentedBy&facet.field=relatedOrganizations&facet.field=project&facet.field=investigator&facet.field=fileID&facet.field=purpose
'''


class SolrClient(object):
  def __init__(
    self,
    base_url=settings.DATAONE_ROOT,
    relative_solr_path=settings.SOLR_QUERY_PATH,
    filter_query=settings.SOLR_FILTER_QUERY,
    solr_debug=settings.SOLR_DEBUG
  ):
    self.custom_filter_query = filter_query
    self.solr_debug = solr_debug
    self.solr_path = self.get_solr_path(base_url, relative_solr_path)
    self.connection = self.create_connection(base_url)
#    self.solr_connection = self.create_connection(base_url,
#                                                       relative_solr_path)

  def create_connection(self, base_url):
    solr_host = self.get_hostname(base_url)
    return httplib.HTTPSConnection(solr_host)

  # Want to return a result that:
  # - starts with all available objects
  # - returns the objects that match the applied facets.
  # - includes a list of all the unapplied facets and their counts, for counts > 0
  def faceted_search(self, all_facets, applied_facets):
    unapplied_facets = self.get_unapplied_facets(all_facets, applied_facets)
    unapplied_facet_fields = self.facet_fields_from_facet_names(unapplied_facets)
    query_params = [
      ('q', '*:*'),
      ('rows', '3'),
      ('indent', 'on'),
      ('facet', 'true'),
      ('facet.limit', '5'),
      ('facet.mincount', '1'),
      ('facet.sort', 'count'),
      #('facet.count', 'sort'),
      #('group.facet', 'true'),
      ('wt', 'python'),
    ]
    query_params.extend(unapplied_facet_fields)
    response = self.send_request(query_params)
    unapplied_facet_counts, entries = self.parse_result_dict(response)
    return unapplied_facet_counts, entries

#  def create_filter_query(self, all_facets, applied_facets, unapplied_facets):
#    facet_settings = ['rows=100', 'facet=true', 'facet.limit=10',
#                      'facet.count=sort']
#    unapplied_facets_string = self.create_facet_query_segment_for_unapplied_facets(
#      unapplied_facets)
#    return '*:*&{0}&{1}'.format('&'.join(facet_settings),
#                                unapplied_facets_string)

  def facet_fields_from_facet_names(self, facet_names):
    return [('facet.field', f) for f in facet_names]

#  def get_facet_fields_for_unapplied_facets(self, all_facets, applied_facets):
#    unapplied_facets = self.get_unapplied_facets(all_facets, applied_facets)
#    return ['facet.field={0}'.format(f) for f in unapplied_facets]

  def get_unapplied_facets(self, all_facets, applied_facets):
    return list(set(all_facets) - set(applied_facets))

#  def get_facet_values_for_facet_name(self, applied_facets, facet_name):
#    q = 'title:moorx' # moor
#    q = 'text:#1;dnatsrednu'
#    return self.solr_connection.fieldValues(facet_name, q=q)

  def get_hostname(self, base_url):
    return urlparse.urlsplit(base_url).netloc

  def get_solr_path(self, base_url, relative_solr_path):
    base = urlparse.urlsplit(base_url).path
    return '/' + d1_common.url.joinPathElements(base, relative_solr_path) + '/'

  def get_solr_base(self, base_url, relative_solr_path):
    return d1_common.url.joinPathElements(base_url, relative_solr_path) + '/'

#  def create_facet_query_segment_for_unapplied_facets(self, unapplied_facets):
#    facet_query = []
#    for unapplied_facet in unapplied_facets:
#      facet_query.append('facet.field={0}'.format(unapplied_facet))
#    return '&'.join(facet_query)

  def send_request(self, params):
    query_url = urllib.urlencode(params, doseq=True)
    response = self.get(query_url)
    return eval(response.read())

  def get(self, query_url, headers=None):
    if headers is None:
      headers = {}
    abs_query_url = self.solr_path + '?' + query_url
    log.debug('GET {0}'.format(abs_query_url))
    try:
      self.connection.request('GET', abs_query_url, headers=headers)
      response = self.connection.getresponse()
    except (socket.error, httplib.HTTPException) as e:
      log.error('Solr query failed: {0}: {0}'.format(abs_query_url, str(e)))
      raise e
    self.assert_response_is_ok(response)
    return response

  def parse_result_dict(self, d):
    unapplied_facet_counts = self.get_unapplied_facet_counts(d)
    entries = self.get_directory_entries(d)
    return unapplied_facet_counts, entries

  def get_unapplied_facet_counts(self, d):
    facet_counts = d['facet_counts']['facet_fields']
    facets = {}
    for facet_name, facet_value_counts in facet_counts.items():
      facet_count_tuples = self.pairs_from_list(facet_value_counts)
      count = 0
      for facet in facet_count_tuples:
        count += int(facet[1])
      if count:
        facets[facet_name] = {'count': count, 'values': facet_count_tuples, }
    return facets

  def pairs_from_list(self, list_with_pairs):
    pairs = []
    for i in range(0, len(list_with_pairs), 2):
      pairs.append((urllib.quote(list_with_pairs[i], safe=''), list_with_pairs[i + 1]))
    return pairs

  def get_directory_entries(self, d):
    docs = d['response']['docs']
    entry = []
    for doc in docs:
      #    # The columns to get from the Solr index.
      #    self.fields = [
      #      'id',
      #      'identifier',
      #      'title',
      #      'formatId',
      #      'update_date',
      #      'size'
      #    ]
      entry.append(
        {
          'format_id': doc['formatId'],
          'pid': urllib.quote(doc['id'], safe=''),
          'size': doc['size'],
        }
      )
    return entry

  def assert_response_is_ok(self, response):
    if response.status not in (200, ):
      try:
        html_body = response.read()
      except:
        html_body = ''
      s = SimpleHTMLToText()
      txt_body = s.get_text(html_body)
      msg = '{0}\n{1}\n{2}'.format(response.status, response.reason, txt_body)
      raise Exception(msg)

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

  def prepare_query_term(self, field, term):
    '''
    Prepare a query term for inclusion in a query.  This escapes the term and
    if necessary, wraps the term in quotes.
    '''
    if term == "*":
      return term
    addstar = False
    if term[len(term) - 1] == '*':
      addstar = True
      term = term[0:len(term) - 1]
    term = self.escape_query_term(term)
    if addstar:
      term = '%s*' % term
    if self.getSolrType(field) in ['string', 'text', 'text_ws']:
      return '"%s"' % term
    return term

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
#  return solr_client.SOLRSearchResponseIterator(self.solr_connection, q,
#    fq=fq, fields=fields, pagesize=pagesize)

#  def encode_path_element(path_element):
#    return urllib.quote(path_element.encode('utf-8'), safe=PATHELEMENT_SAFE_CHARS)

#  def get_facet_values(self, facet, refresh=False):
#    '''Get facet values.
#    This method supports faceted search. From the user perspective, faceted
#    search breaks up search results into multiple categories, typically showing
#    counts for each, and allows the user to "drill down" or further restrict
#    their search results based on those facets.
#    :param facet: Facet for which to get values.
#    :type facet: str
#    :param refresh: Read facet from server even if cached
#    :type refresh: bool
#    :return: Facet values
#    :rtype:
#    '''
#    self.logger.debug('get_facet_values: {0}'.format(facet))
#    now = time.time()
#    dt = now - self.facets[facet]['tstamp']
#    self.logger.debug('dt = {0}'.format(str(dt)))
#    if refresh or (len(self.facets[facet]['v']) < 1) or (dt > FACET_REFRESH):
#      self.logger.debug('get_facet_values: cache miss')
#      sc = self.create_connection()
#      self.facets[facet]['tstamp'] = time.time()
#      self.facets[facet]['v'] = []
#      self.facets[facet]['n'] = []
#      fname = self.facets[facet]['f']
#      fvals = sc.fieldValues(fname, fq=self.filter_query)
#      for i in xrange(0,len(fvals[fname]),2):
#        fv = encode_path_element(fvals[fname][i])
#        #fv = fvals[fname][i]
#        if len(fv) > 0:
#          self.logger.debug('get_facet_values: {0}'.format(fv))
#          fc = fvals[fname][i+1]
#          self.facets[facet]['v'].append(fv)
#          self.facets[facet]['n'].append(fc)
#          # Can we also append the latest of beginDate and endDate for each of
#          # the value groups?
#    return self.facets[facet]['v']
#
#
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
