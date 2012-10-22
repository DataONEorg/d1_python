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
import logging
import os

# D1.
import d1_client.solr_client
import d1_common.const

# App.
import facet_path_parser
import query_engine_description
import settings

# Set up logger for this module.
log = logging.getLogger(__name__)

#===============================================================================
'''
If path is for facet name container, list unused facet names then result of query based on applied facets.

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
    base_url=d1_common.const.URL_DATAONE_ROOT,
    solr_path=None,
    filter_query=None
  ):
    '''
    :param base_url: The Base URL to the DataONE CN to connect to
    :type base_url: str
    :param filter_query: Optional filter query that will be applied to the view
    of DataONE. Only content matching the filter will appear in the file system
    view.
    :type filter_query: str
    '''
    self.base_url = base_url
    self.solr_path = solr_path
    self.solr_connection = d1_client.solr_client.SolrConnection(
      host=base_url, solrBase=solr_path, debug=True
    )
    #self._filter_query = filter_query
    # The columns to get from the Solr index.
    self.fields = ['id', 'identifier', 'title', 'formatId', 'update_date', 'size']

  def create_solr_connection(self, forceNew=True):
    '''Get a SolrConnection for interacting with Solr.
    :param forceNew: Create a new connection even if one exists.
    :type forceNew: bool
    :return: A connection to a Solr host.
    :rtype: SolrConnection.
    '''
    if forceNew or self.solr_connection is None:
      print '0' * 100
      print self.get_solr_host()
      print self.solr_path
      print '0' * 100
      self.solr_connection = solr_client.SolrConnection(
        self.get_solr_host(
        ),
        solrBase=self.solr_path,
        persistent=settings.SOLR_PERSIST_CONNECTION
      )
    return self.solr_connection

  def get_facet_values_for_facet_name(self, facet_name):
    facet_values = self.solr_connection.fieldValues(facet_name)
    print facet_values

  #  entries = self.getRecords(facetkey, facetval)

  # example for getting facet values:
  # Facet level of file system, subdirs are facet values
  #      st_nlink = len(facet_values)
  #    else:
  #      st_nlink = len(self.facets.keys())

  #def query(self, path):
  #  q = self.create_solr_query_string(path)
  #  print q

  #def connect(query_base_url, query_endpoint):
  #  self.solr_connection = d1_client.solr_client.SolrConnection(
  #    host=query_base_url, solrBase=options.query_endpoint)
  #
  #
  #def query(q='*:*', fq=None, fields='*', pagesize=100):
  #  return solr_client.SOLRSearchResponseIterator(self.solr_connection, q,
  #    fq=fq, fields=fields, pagesize=pagesize)

  def create_solr_query_string(self, path):
    facet_settings = 'rows=100&facet=true&facet.limit=10&facet.count=sort'
    return '?q=*:*&' + facet_settings + '&' + self.create_facet_query_string(path)

  def create_facet_query_string(self, path):
    unused_facets = self._get_unused_facet_names(path)
    facet_query = []
    for unused_facet in unused_facets:
      facet_query.append('facet.field={0}'.format(unused_facet))
    return '&'.join(facet_query)

  def _get_unused_facet_names(self, path):
    assert (self.facet_path_parser.dir_contains_facet_names(path))
    searchable_facet_names = set(
      self.query_engine_description.get_searchable_facet_names(
      )
    )
    used_facets = self.facet_path_parser.undecorate_facets(path)
    used_facets_names = set(
      [
        self.facet_path_parser.undecorate_facet_name(
          f[0]
        ) for f in used_facets
      ]
    )
    #return [self.facet_path_parser.decorate_facet_name(n) for n in
    #        searchable_facet_names - used_facets_names]
    return searchable_facet_names - used_facets_names

  def encode_path_element(path_element):
    return urllib.quote(path_element.encode('utf-8'), safe=PATHELEMENT_SAFE_CHARS)

  def get_solr_host(self):
    '''Get the Solr host from the CN Base URL.
    :return: Solr host URL.
    :rtype: str
    '''
    url_parts = urlparse.urlsplit(self.base_url)
    return url_parts.netloc

  def get_facet_values(self, facet, refresh=False):
    '''Get facet values.
    This method supports faceted search. From the user perspective, faceted
    search breaks up search results into multiple categories, typically showing
    counts for each, and allows the user to "drill down" or further restrict
    their search results based on those facets.
    :param facet: Facet for which to get values.
    :type facet: str
    :param refresh: Read facet from server even if cached
    :type refresh: bool
    :return: Facet values
    :rtype:
    '''
    self.logger.debug('get_facet_values: {0}'.format(facet))
    now = time.time()
    dt = now - self.facets[facet]['tstamp']
    self.logger.debug('dt = {0}'.format(str(dt)))
    if refresh or (len(self.facets[facet]['v']) < 1) or (dt > FACET_REFRESH):
      self.logger.debug('get_facet_values: cache miss')
      sc = self.create_solr_connection()
      self.facets[facet]['tstamp'] = time.time()
      self.facets[facet]['v'] = []
      self.facets[facet]['n'] = []
      fname = self.facets[facet]['f']
      fvals = sc.fieldValues(fname, fq=self._filter_query)
      for i in xrange(0, len(fvals[fname]), 2):
        fv = encode_path_element(fvals[fname][i])
        #fv = fvals[fname][i]
        if len(fv) > 0:
          self.logger.debug('get_facet_values: {0}'.format(fv))
          fc = fvals[fname][i + 1]
          self.facets[facet]['v'].append(fv)
          self.facets[facet]['n'].append(fc)
          # Can we also append the latest of beginDate and endDate for each of
          # the value groups?
    return self.facets[facet]['v']

  def get_records(self, facet, term):
    self.logger.debug('get_records: {0}'.format(facet))
    fname = self.facets[facet]['f']
    sc = self.create_solr_connection()
    q = "%s:%s" % (fname, sc.prepareQueryTerm(fname, term))
    self.logger.info("q= %s" % q)
    self.logger.info("fq = %s" % self._filter_query)
    records = solr_client.SOLRArrayResponseIterator(
      sc, q, fq=self._filter_query,
      cols=self.fields,
      pagesize=ITERATOR_PER_FETCH
    )
    return records

  def get_abstract(self, pid):
    ''':type pid: DataONE Persistent ID
    '''
    self.logger.debug('get_abstract: {0}'.format(pid))
    sc = self.create_solr_connection()
    q = sc.prepareQueryTerm('identifier', pid)
    records = solr_client.SOLRArrayResponseIterator(
      sc, q,
      fq=self._filter_query,
      cols=[
        'abstract',
      ], pagesize=ITERATOR_PER_FETCH
    )
    self.abstract_cache[pid] = ''
    for rec in records:
      if rec[0] is not None:
        self.abstract_cache[pid] = rec[0]
      break
    return self.abstract_cache[pid]
