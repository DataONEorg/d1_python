#!/usr/bin/env python
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
""":mod:`workspace_solr_client`
===============================

:Synopsis:
 - Generate and run queries against Solr.
:Author:
  DataONE (Dahl)
"""

import HTMLParser

import requests


class SolrClient(object):
  def __init__(
      self, base_url, solr_selector='/v1/query/solr/', max_retries=3,
      timeout_sec=30, max_objects_for_query=50
  ):
    self._solr_endpoint = base_url + solr_selector
    self._session = requests.Session()
    self._session.mount(
      'http://', requests.adapters.HTTPAdapter(max_retries=max_retries)
    )
    self._session.mount(
      'https://', requests.adapters.HTTPAdapter(max_retries=max_retries)
    )
    self._timeout_sec = timeout_sec
    self._max_objects_for_query = max_objects_for_query

  def query(self, query, filter_queries=None, fields=None):
    if fields is None:
      fields = ['*']

    query_params = {
      'q': query,
      'fl': ','.join(fields),
      'rows': self._max_objects_for_query,
      'indent': 'on',
      'wt': 'json'
    }

    if filter_queries is not None:
      query_params.extend(self._make_query_param_tuples('fl', filter_queries))

    r = requests.get(
      self._solr_endpoint, timeout_sec=self._timeout_sec, params=query_params,
      verify=False
    )
    return r.json()

  def escape_query_term_string(self, term):
    """Escape a query term string and wrap it in quotes.
    """
    return u'"{0}"'.format(self._escape_query_term(term))

  # Private.

  def _make_query_param_tuples(self, query_type, terms):
    return [(query_type, t) for t in self.__escape_query_term_list(terms)]

  def __escape_query_term_list(self, terms):
    return [self._escape_query_term(term) for term in terms]

  def _escape_query_term(self, term):
    reserved = [
      '+', '-', '&', '|', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*',
      '?', ':'
    ]
    term = term.replace(u'\\', u'\\\\')
    for c in reserved:
      term = term.replace(c, u'\{0}'.format(c))
    return term

  #def prepare_query_term(self, field, term):
  #  """
  #  Prepare a query term for inclusion in a query.  This escapes the term and
  #  if necessary, wraps the term in quotes.
  #  """
  #  if term == "*":
  #    return term
  #  addstar = False
  #  if term[len(term)-1] == '*':
  #    addstar = True
  #    term = term[0:len(term)-1]
  #  term = self._escape_query_term(term)
  #  if addstar:
  #    term = '%s*' % term
  #  if self.getSolrType(field) in ['string', 'text', 'text_ws']:
  #    return '"%s"' % term
  #  return term

  #def escapeVal(self,val):
  #  val = val.replace(u"&", u"&amp;")
  #  val = val.replace(u"<", u"&lt;")
  #  val = val.replace(u"]]>", u"]]&gt;")
  #  return self.encoder(val)[0]  #to utf8

  #def escapeKey(self,key):
  #  key = key.replace(u"&", u"&amp;")
  #  key = key.replace(u'"', u"&quot;")
  #  return self.encoder(key)[0]  #to utf8

  #===============================================================================


class SimpleHTMLToText(HTMLParser.HTMLParser):
  def __init__(self):
    self.reset()
    self.fed = []
    super(SimpleHTMLToText, self).__init__()

  def get_text(self, html):
    self.feed(html)
    return self.get_data()

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)
