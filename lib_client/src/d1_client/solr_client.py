#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Basic Solr client

Based on: http://svn.apache.org/viewvc/lucene/solr/tags/release-1.2.0/
client/python/solr.py
"""

import datetime
import logging
import pprint
import random
from xml.sax.saxutils import quoteattr

import requests.structures

import d1_client.baseclient_1_2

FIELD_TYPE_CONVERSION_MAP = {
  't': 'text',
  's': 'string',
  'dt': 'date',
  'd': 'double',
  'f': 'float',
  'i': 'int',
  'l': 'long',
  'tw': 'text_ws',
  'text': 'text',
  'guid': 'string',
  'itype': 'string',
  'origin': 'string',
  'oid': 'string',
  'gid': 'string',
  'modified': 'date',
  'created': 'date',
}

RESERVED_CHAR_LIST = [
  '+', '-', '&', '|', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*',
  '?', ':'
]


class SolrClient(d1_client.baseclient_1_2.DataONEBaseClient_1_2):
  """Extend DataONEBaseClient_1_2 with functions for querying Solr indexes
  hosted on CNs and MNs.

  Example:

  solr_client = SolrClient('https://cn.dataone.org/cn')

  For the supported keyword args, see:

  d1_client.session.Session()

  - Most methods take a **query_dict as a parameter. It allows passing any number
  of query parameters that will be sent to Solr.

  Pass the query parameters as regular keyword arguments. E.g.:

  solr_client.search(q='id:abc*', fq='id:def*')

  To pass multiple query parameters of the same type, pass a list. E.g., to
  pass multiple filter query (fq) parameters:

  solr_client.search(q='id:abc*', fq=['id:def*', 'id:ghi'])

  - Do not encode the query parameters before passing them to the methods.

  For more information about DataONE's Solr index, see:

  https://releases.dataone.org/online/api-documentation-v2.0/design/SearchMetadata.html
  """

  def __init__(self, *args, **kwargs):
    self.logger = logging.getLogger(__name__)
    header_dict = requests.structures.CaseInsensitiveDict(
      kwargs.pop('headers', {})
    )
    header_dict.setdefault(
      'Content-Type', 'application/x-www-form-urlencoded; charset=utf-8'
    )
    self._query_engine = kwargs.pop('query_engine', 'solr')
    d1_client.baseclient_1_2.DataONEBaseClient_1_2.__init__(
      self, headers=header_dict, *args, **kwargs
    )

  def __str__(self):
    return 'SolrClient(base_url="{}")'.format(self._base_url)

  # GET queries

  def search(self, **query_dict):
    """Search the Solr index

    Example:

    result_dict = search(q=['id:abc*'], fq=['id:def*', 'id:ghi'])
    """
    return self._get_query(**query_dict)

  # noinspection PyMethodOverriding
  def get(self, doc_id):
    """Retrieve the specified document."""
    resp_dict = self._get_query(q='id:{}'.format(doc_id))
    if resp_dict['response']['numFound'] > 0:
      return resp_dict['response']['docs'][0]

  # noinspection PyTypeChecker
  def get_ids(self, start=0, rows=1000, **query_dict):
    """Retrieve a list of identifiers for documents matching the query"""
    resp_dict = self._get_query(start=start, rows=rows, **query_dict)
    return {
      'matches': resp_dict['response']['numFound'],
      'start': start,
      'ids': [d['id'] for d in resp_dict['response']['docs']],
    }

  def count(self, **query_dict):
    """Return the number of entries that match query."""
    param_dict = query_dict.copy()
    param_dict['count'] = 0
    resp_dict = self._get_query(**param_dict)
    return resp_dict['response']['numFound']

  def get_field_values(self, name, maxvalues=-1, sort=True, **query_dict):
    """Retrieve the unique values for a field, along with their usage counts.

    :param name: Name of field for which to retrieve values
    :type name: string

    :param sort: Sort the result

    :param maxvalues: Maximum number of values to retrieve. Default is -1,
      which causes retrieval of all values.
    :type maxvalues: int

    :returns: dict of {fieldname: [[value, count], ... ], }
    """
    param_dict = query_dict.copy()
    param_dict.update({
      'rows': '0',
      'facet': 'true',
      'facet.field': name,
      'facet.limit': str(maxvalues),
      'facet.zeros': 'false',
      'facet.sort': str(sort).lower(),
    })
    resp_dict = self._post_query(**param_dict)
    result_dict = resp_dict['facet_counts']['facet_fields']
    result_dict['numFound'] = resp_dict['response']['numFound']
    return result_dict

  def get_field_min_max(self, name, **query_dict):
    """Returns the minimum and maximum values of the specified field. This
    requires two search calls to the service, each requesting a single value of
    a single field.

    @param name(string) Name of the field
    @param q(string) Query identifying range of records for min and max values
    @param fq(string) Filter restricting range of query

    @return list of [min, max]
    """
    param_dict = query_dict.copy()
    param_dict.update({
      'rows': 1,
      'fl': name,
      'sort': '%s asc' % name,
    })
    try:
      min_resp_dict = self._post_query(**param_dict)
      param_dict['sort'] = '%s desc' % name
      max_resp_dict = self._post_query(**param_dict)
      return (
        min_resp_dict['response']['docs'][0][name],
        max_resp_dict['response']['docs'][0][name],
      )
    except Exception:
      self.logger.exception('Exception')
      raise

  def field_alpha_histogram(
      self, name, n_bins=10, include_queries=True, **query_dict
  ):
    """Generates a histogram of values from a string field.

    Output is: [[low, high, count, query], ... ]. Bin edges is determined by
    equal division of the fields.
    """
    bin_list = []
    q_bin = []
    try:
      # get total number of values for the field
      # TODO: this is a slow mechanism to retrieve the number of distinct values
      # Need to replace this with something more efficient.
      # Can probably replace with a range of alpha chars - need to check on
      # case sensitivity
      param_dict = query_dict.copy()
      f_vals = self.get_field_values(name, maxvalues=-1, **param_dict)
      n_values = len(f_vals[name]) // 2
      if n_values < n_bins:
        n_bins = n_values
      if n_values == n_bins:
        # Use equivalence instead of range queries to retrieve the
        # values
        for i in range(n_bins):
          a_bin = [f_vals[name][i * 2], f_vals[name][i * 2], 0]
          bin_q = '{}:{}'.format(name, self._prepare_query_term(name, a_bin[0]))
          q_bin.append(bin_q)
          bin_list.append(a_bin)
      else:
        delta = n_values / n_bins
        if delta == 1:
          # Use equivalence queries, except the last one which includes the
          # remainder of terms
          for i in range(n_bins - 1):
            a_bin = [f_vals[name][i * 2], f_vals[name][i * 2], 0]
            bin_q = '{}:{}'.format(
              name, self._prepare_query_term(name, a_bin[0])
            )
            q_bin.append(bin_q)
            bin_list.append(a_bin)
          term = f_vals[name][(n_bins - 1) * 2]
          a_bin = [term, f_vals[name][((n_values - 1) * 2)], 0]
          bin_q = '{}:[{} TO *]'.format(
            name, self._prepare_query_term(name, term)
          )
          q_bin.append(bin_q)
          bin_list.append(a_bin)
        else:
          # Use range for all terms
          # now need to page through all the values and get those at
          # the edges
          c_offset = 0.0
          delta = float(n_values) / float(n_bins)
          for i in range(n_bins):
            idx_l = int(c_offset) * 2
            idx_u = (int(c_offset + delta) * 2) - 2
            a_bin = [f_vals[name][idx_l], f_vals[name][idx_u], 0]
            # logging.info(str(a_bin))
            try:
              if i == 0:
                bin_q = '{}:[* TO {}]'.format(
                  name, self._prepare_query_term(name, a_bin[1])
                )
              elif i == n_bins - 1:
                bin_q = '{}:[{} TO *]'.format(
                  name, self._prepare_query_term(name, a_bin[0])
                )
              else:
                bin_q = '{}:[{} TO {}]'.format(
                  name,
                  self._prepare_query_term(name, a_bin[0]),
                  self._prepare_query_term(name, a_bin[1])
                )
            except Exception:
              self.logger.exception('Exception:')
              raise
            q_bin.append(bin_q)
            bin_list.append(a_bin)
            c_offset = c_offset + delta
      # now execute the facet query request
      param_dict = query_dict.copy()
      param_dict.update({
        'rows': '0',
        'facet': 'true',
        'facet.field': name,
        'facet.limit': '1',
        'facet.mincount': 1,
        'facet.query': [sq.encode('utf-8') for sq in q_bin],
      })
      resp_dict = self._post_query(**param_dict)
      for i in range(len(bin_list)):
        v = resp_dict['facet_counts']['facet_queries'][q_bin[i]]
        bin_list[i][2] = v
        if include_queries:
          bin_list[i].append(q_bin[i])
    except Exception:
      logging.exception('Exception')
      raise
    return bin_list

  # POST queries

  def delete(self, doc_id):
    return self.query(
      'solr',
      '<delete><id>' + self._escape_xml_entity(str(doc_id)) + '</id></delete>',
      do_post=True,
    )

  def delete_by_query(self, query):
    return self.query(
      'solr',
      '<delete><query>' + self._escape_xml_entity(query) + '</query></delete>',
      do_post=True,
    )

  def add(self, **fields):
    return self.query(
      'solr',
      '<add>{}</add>'.format(self._format_add(fields)),
      do_post=True,
    )

  def add_docs(self, docs):
    """docs is a list of fields that are a dictionary of name:value for a
    record."""
    return self.query(
      'solr',
      '<add>{}</add>'.
      format(''.join([self._format_add(fields) for fields in docs])),
      do_post=True,
    )

  def commit(self, waitFlush=True, waitSearcher=True, optimize=False):
    xstr = '<commit'
    if optimize:
      xstr = '<optimize'
    if not waitSearcher: # just handle deviations from the default
      if not waitFlush:
        xstr += ' waitFlush="false" waitSearcher="false"'
      else:
        xstr += ' waitSearcher="false"'
    xstr += '/>'
    return self.query('solr', xstr, do_post=True)

  # Private

  def _escape_xml_entity(self, s):
    return quoteattr(s).encode('utf-8')

  def _coerce_type(self, field_type, value):
    """Returns unicode(value) after trying to coerce it into the Solr field
    type.

    @param field_type(string) The Solr field type for the value
    @param value(any) The value that is to be represented as unicode text.
    """
    if value is None:
      return None
    if field_type == 'string':
      return str(value)
    elif field_type == 'text':
      return str(value)
    elif field_type == 'int':
      try:
        v = int(value)
        return str(v)
      except:
        return None
    elif field_type == 'float':
      try:
        v = float(value)
        return str(v)
      except:
        return None
    elif field_type == 'date':
      try:
        v = datetime.datetime(
          value['year'], value['month'], value['day'], value['hour'],
          value['minute'], value['second']
        )
        v = v.strftime('%Y-%m-%dT%H:%M:%S.0Z')
        return v
      except:
        return None
    return str(value)

  def _get_solr_type(self, field):
    """Returns the Solr type of the specified field name.

    Assumes the convention of dynamic fields using an underscore + type
    character code for the field name.
    """
    field_type = 'string'
    try:
      field_type = FIELD_TYPE_CONVERSION_MAP[field]
      return field_type
    except:
      pass
    fta = field.split('_')
    if len(fta) > 1:
      ft = fta[len(fta) - 1]
      try:
        field_type = FIELD_TYPE_CONVERSION_MAP[ft]
        # cache the type so it's used next time
        FIELD_TYPE_CONVERSION_MAP[field] = field_type
      except:
        pass
    return field_type

  def _format_add(self, fields):
    el_list = ['<doc>']
    for f, v in list(fields.items()):
      field_type = self._get_solr_type(f)
      if isinstance(v, list):
        for vi in v:
          vi = self._coerce_type(field_type, vi)
          if vi is not None:
            el_list.append('<field name="')
            el_list.append(self._escape_xml_entity(str(f)))
            el_list.append('">')
            el_list.append(self._escape_xml_entity(vi))
            el_list.append('</field>')
      else:
        v = self._coerce_type(field_type, v)
        if v is not None:
          el_list.append('<field name="')
          el_list.append(self._escape_xml_entity(str(f)))
          el_list.append('">')
          el_list.append(self._escape_xml_entity(v))
          el_list.append('</field>')
    el_list.append('</doc>')
    return ''.join(el_list)

  def _get_query(self, **query_dict):
    """Perform a GET query against Solr and return the response as a Python
    dict"""
    param_dict = query_dict.copy()
    return self._send_query(do_post=False, **param_dict)

  def _post_query(self, **query_dict):
    """Perform a POST query against Solr and return the response as a Python
    dict"""
    param_dict = query_dict.copy()
    return self._send_query(do_post=True, **param_dict)

  def _send_query(self, do_post=False, **query_dict):
    """Perform a query against Solr and return the response as a Python
    dict"""
    # self._prepare_query_term()
    param_dict = query_dict.copy()
    param_dict.setdefault('wt', 'json')
    param_dict.setdefault('q', '*.*')
    param_dict.setdefault('fl', '*')
    return self.query('solr', '', do_post=do_post, query=param_dict)

  # Building queries

  def _prepare_query_term(self, field, term):
    """Prepare a query term for inclusion in a query.
    This escapes the term and if necessary, wraps the term in quotes.
    """
    if term == "*":
      return term
    add_star = False
    if term[len(term) - 1] == '*':
      add_star = True
      term = term[0:len(term) - 1]
    term = self._escape_query_term(term)
    if add_star:
      term = '{}*'.format(term)
    if self._get_solr_type(field) in ['string', 'text', 'text_ws']:
      return '"{}"'.format(term)
    return term

  def _escape_query_term(self, term):
    """Escape a query term for inclusion in a query
    - Also see: prepare_query_term().
    """
    term = term.replace('\\', '\\\\')
    for c in RESERVED_CHAR_LIST:
      term = term.replace(c, '\{}'.format(c))
    return term


# =========================================================================


class SolrRecordTransformerBase(object):
  """Base for Solr record transformers.

  Used to transform a Solr search response document into some other
  form, such as a dictionary or list of values.
  """

  def __init__(self):
    pass

  def transform(self, record):
    return record


# =========================================================================


class SolrArrayTransformer(SolrRecordTransformerBase):
  """A transformer that returns a list of values for the specified columns."""

  def __init__(self, cols=None):
    super().__init__()
    self.cols = cols or [
      'lng',
      'lat',
    ]

  def transform(self, record):
    res = []
    for col in self.cols:
      try:
        v = record[col]
        if isinstance(v, list):
          res.append(v[0])
        else:
          res.append(v)
      except:
        res.append(None)
    return res


# =========================================================================


class SolrSearchResponseIterator(object):
  """Performs a search against a Solr index and acts as an iterator to retrieve
  all the values."""

  def __init__(
      self, client, page_size=100, max_records=1000,
      transformer=SolrRecordTransformerBase(), **query_dict
  ):
    self.logger = logging.getLogger(__name__)

    self.client = client
    self.query_dict = query_dict.copy()
    self.page_size = page_size
    self.max_records = max_records or 99999999

    self.c_record = 0
    self.res = None
    self.done = False
    self.transformer = transformer
    self._next_page(self.c_record)
    self._num_hits = 0

    self.logger.debug(
      "Iterator hits={}".format(self.res['response']['numFound'])
    )

  def _next_page(self, offset):
    """Retrieves the next set of results from the service."""
    self.logger.debug("Iterator c_record={}".format(self.c_record))
    page_size = self.page_size
    if (offset + page_size) > self.max_records:
      page_size = self.max_records - offset
    param_dict = self.query_dict.copy()
    param_dict.update({
      'start': str(offset),
      'rows': str(page_size),
      'explainOther': '',
      'hl.fl': '',
    })
    self.res = self.client.search(**param_dict)
    self._num_hits = int(self.res['response']['numFound'])

  def __iter__(self):
    return self

  def process_row(self, row):
    """Override this method in derived classes to reformat the row response."""
    return row

  def __next__(self):
    if self.done:
      raise StopIteration()
    if self.c_record > self.max_records:
      self.done = True
      raise StopIteration()
    idx = self.c_record - self.res['response']['start']
    try:
      row = self.res['response']['docs'][idx]
    except IndexError:
      self._next_page(self.c_record)
      idx = self.c_record - self.res['response']['start']
      try:
        row = self.res['response']['docs'][idx]
      except IndexError:
        self.done = True
        raise StopIteration()
    self.c_record = self.c_record + 1
    return self.transformer.transform(row)


# =========================================================================


class SolrArrayResponseIterator(SolrSearchResponseIterator):
  """Returns an iterator that operates on a Solr result set.

  The output for each document is a list of values for the columns
  specified in the cols parameter of the constructor.
  """

  def __init__(self, client, page_size=100, cols=None, **query_dict):
    self.logger = logging.getLogger(__name__)

    cols = cols or [
      'lng',
      'lat',
    ]
    transformer = SolrArrayTransformer(cols)

    param_dict = query_dict.copy()
    param_dict.update({
      'fields': ",".join(cols),
    })

    SolrSearchResponseIterator.__init__(
      self, client, page_size, transformer=transformer, **param_dict
    )


# =========================================================================


class SolrSubsampleResponseIterator(SolrSearchResponseIterator):
  """Returns a pseudo-random subsample of the result set.

  Works by calculating the number of pages required for the entire data
  set and taking a random sample of pages until n_samples can be
  retrieved.  So pages are random, but records within a page are not.
  """

  def __init__(
      self, client, q, fq=None, fields='*', page_size=100, n_samples=10000,
      transformer=SolrRecordTransformerBase()
  ):
    self._c_record = None
    self._page_starts = [
      0,
    ]
    self._c_page = 0
    SolrSearchResponseIterator.__init__(
      self, client, q, fq, fields, page_size, transformer
    )
    n_pages = self._num_hits / self.page_size
    if n_pages > 0:
      sample_size = n_samples / page_size
      if sample_size > n_pages:
        sample_size = n_pages
      self._page_starts += random.sample(list(range(0, n_pages)), sample_size)
      self._page_starts.sort()

  def __next__(self):
    """Overrides the default iteration by sequencing through records within a
    page and when necessary selecting the next page from the randomly generated
    list."""
    if self.done:
      raise StopIteration()
    idx = self.c_record - self.res['response']['start']
    try:
      row = self.res['response']['docs'][idx]
    except IndexError:
      self._c_page += 1
      try:
        self._c_record = self._page_starts[self._c_page]
        self._next_page(self.c_record)
        idx = self.c_record - self.res['response']['start']
        row = self.res['response']['docs'][idx]
      except IndexError:
        self.done = True
        raise StopIteration()
    self.c_record = self.c_record + 1
    return self.process_row(row)


# =========================================================================


class SolrValuesResponseIterator(object):
  """Iterates over a Solr get values response.

  This returns a list of distinct values for a particular field.
  """

  def __init__(self, client, field, page_size=1000, **query_dict):
    """Initialize.

    @param client(SolrConnection) An instance of a solr connection to use.
    @param field(string) name of the field from which to retrieve values
    @param q(string) The Solr query to restrict results
    @param fq(string) A facet query, restricts the set of rows that q is applied to
    @param fields(string) A comma delimited list of field names to return
    @param page_size(int) Number of rows to retrieve in each call.
    """

    self.logger = logging.getLogger(__name__)

    self.client = client
    self.field = field
    self.page_size = page_size
    self.query_dict = query_dict

    self.c_record = 0
    self.res = None
    self.done = False
    self.index = None

    self._next_page(self.c_record)

  def __iter__(self):
    return self

  def _next_page(self, offset):
    """Retrieves the next set of results from the service."""
    self.logger.debug("Iterator c_record={}".format(self.c_record))
    param_dict = self.query_dict.copy()
    param_dict.update({
      'rows': '0',
      'facet': 'true',
      'facet.limit': str(self.page_size),
      'facet.offset': str(offset),
      'facet.zeros': 'false',
    })
    print(param_dict)
    # resp_dict = self.client._get_query(**param_dict)
    resp_dict = self.client._post_query(**param_dict)
    # resp_dict = self.client.search(**param_dict)
    pprint.pprint(resp_dict)
    try:
      self.res = resp_dict['facet_counts']['facet_fields'][self.field]
      self.logger.debug(self.res)
    except Exception:
      self.res = []
    self.index = 0

  def __next__(self):
    if self.done:
      raise StopIteration()
    if len(self.res) == 0:
      self.done = True
      raise StopIteration()
    try:
      row = [self.res[self.index], self.res[self.index + 1]]
      self.index = self.index + 2
    except IndexError:
      self._next_page(self.c_record)
      try:
        row = [self.res[self.index], self.res[self.index + 1]]
        self.index = self.index + 2
      except IndexError:
        self.done = True
        raise StopIteration()
    self.c_record = self.c_record + 1
    return row
