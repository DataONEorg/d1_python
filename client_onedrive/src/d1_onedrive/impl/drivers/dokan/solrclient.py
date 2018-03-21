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
"""
This client code is built from:
http://svn.apache.org/viewvc/lucene/solr/tags/release-1.2.0/client/python/solr.py

though has been modified in many respects.
"""
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

# $Id: solrclient.py 251 2009-12-02 16:38:01Z DaveV $
# A simple Solr client for python.
# This is prototype level code and subject to change.
#
# quick examples on use:
#
# from solr import *
# c = SolrConnection(host='localhost:8983', persistent=True)
# c.add(id='500',name='python test doc')
# c.delete('123')
# c.commit()
# print c.search(q='id:[* TO *]', wt='python', rows='10',indent='on')
# data = c.search(q='id:500', wt='python')
# print 'first match=', eval(data)['response']['docs'][0]

import codecs
#===============================================================================
import datetime
import http.client
import logging
import random
import socket
import urllib.error
import urllib.parse
import urllib.request
import xml.dom.minidom


class SolrException(Exception):
  """ An exception thrown by solr connections """

  def __init__(self, httpcode, reason=None, body=None):
    self.httpcode = httpcode
    self.reason = reason
    self.body = body

  def __repr__(self):
    return 'HTTP code=%s, Reason=%s, body=%s' % (
      self.httpcode, self.reason, self.body
    )

  def __str__(self):
    return 'HTTP code=%s, reason=%s' % (self.httpcode, self.reason)


#===============================================================================


class SolrConnection:
  """
  Provides a connection to the SOLR index.
  """

  def __init__(
      self, host='localhost:8080', solrBase='/v1/solr', persistent=True,
      postHeaders={}
  ):
    self.logger = logging.getLogger('solrclient.SolrConnection')
    self.fieldtypes = {
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
    self.host = host
    self.solrBase = solrBase
    self.persistent = persistent
    self.reconnects = 0
    self.encoder = codecs.getencoder('utf-8')
    #responses from Solr will always be in utf-8
    self.decoder = codecs.getdecoder('utf-8')
    #a real connection to the server is not opened at this point.
    self.conn = http.client.HTTPConnection(self.host)
    ##Cache fields
    self._fields = None
    #self.conn.set_debuglevel(1000000)
    self.xmlheaders = {'Content-Type': 'text/xml; charset=utf-8'}
    self.xmlheaders.update(postHeaders)
    if not self.persistent:
      self.xmlheaders['Connection'] = 'close'
    self.formheaders = {
      'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    if not self.persistent:
      self.formheaders['Connection'] = 'close'

  def __str__(self):
    return 'SolrConnection{host=%s, solrBase=%s, persistent=%s, postHeaders=%s, reconnects=%s}' % \
        (self.host, self.solrBase, self.persistent, self.xmlheaders, self.reconnects)

  def __reconnect(self):
    self.reconnects += 1
    self.conn.close()
    self.conn.connect()

  def __errcheck(self, rsp):
    if rsp.status != 200:
      ex = SolrException(rsp.status, rsp.reason)
      try:
        ex.body = rsp.read()
      except Exception:
        pass
      raise ex
    return rsp

  def close(self):
    try:
      self.conn.close()
    except Exception:
      pass

  def doPost(self, url, body, headers):
    try:
      self.conn.request('POST', url, body, headers)
    except (socket.error, http.client.CannotSendRequest):
      #Reconnect in case the connection was broken from the server going down,
      #the server timing out our persistent connection, or another
      #network failure. Also catch httplib.CannotSendRequest because the
      #HTTPConnection object can get in a bad state.
      self.logger.info('SOLR connection socket error, trying to resend')
      self.__reconnect()
      self.conn.request('POST', url, body, headers)
    finally:
      if not self.persistent:
        self.conn.close()
    res = None
    try:
      res = self.__errcheck(self.conn.getresponse())
    except http.client.BadStatusLine:
      self.logger.exception(
        'Received bad response from SOLR connection.  Retrying.'
      )
      self.__reconnect()
      self.conn.request('POST', url, body, headers)
      res = self.__errcheck(self.conn.getresponse())
    return res

  def doUpdateXML(self, request):
    #logging.debug(request)
    rsp = self.doPost(self.solrBase + '/update', request, self.xmlheaders)
    data = rsp.read()
    #detect old-style error response (HTTP response code of
    #200 with a non-zero status.
    if data.startswith('<result status="'
                       ) and not data.startswith('<result status="0"'):
      data = self.decoder(data)[0]
      parsed = xml.dom.minidom.parseString(data)
      status = parsed.documentElement.getAttribute('status')
      if status != 0:
        #reason = parsed.documentElement.firstChild.nodeValue
        reason = data
        raise SolrException(rsp.status, reason)
    return data

  def escapeQueryTerm(self, term):
    """
    + - && || ! ( ) { } [ ] ^ " ~ * ? : \
    """
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
    term = term.replace('\\', '\\\\')
    for c in reserved:
      term = term.replace(c, "\%s" % c)
    return term

  def prepareQueryTerm(self, field, term):
    """
    Prepare a query term for inclusion in a query.  This escapes the term and
    if necessary, wraps the term in quotes.
    """
    if term == "*":
      return term
    addstar = False
    if term[len(term) - 1] == '*':
      addstar = True
      term = term[0:len(term) - 1]
    term = self.escapeQueryTerm(term)
    if addstar:
      term = '%s*' % term
    if self.getSolrType(field) in ['string', 'text', 'text_ws']:
      return '"%s"' % term
    return term

  def escapeVal(self, val):
    val = val.replace("&", "&amp;")
    val = val.replace("<", "&lt;")
    val = val.replace("]]>", "]]&gt;")
    return self.encoder(val)[0] # to utf8

  def escapeKey(self, key):
    key = key.replace("&", "&amp;")
    key = key.replace('"', "&quot;")
    return self.encoder(key)[0] # to utf8

  def delete(self, id):
    xstr = '<delete><id>' + self.escapeVal(str(id)) + '</id></delete>'
    return self.doUpdateXML(xstr)

  def deleteByQuery(self, query):
    xstr = '<delete><query>' + self.escapeVal(query) + '</query></delete>'
    return self.doUpdateXML(xstr)

  def coerceType(self, ftype, value):
    """
    Returns unicode(value) after trying to coerce it into the SOLR field type.

    @param ftype(string) The SOLR field type for the value
    @param value(any) The value that is to be represented as unicode text.
    """
    if value is None:
      return None
    if ftype == 'string':
      return str(value)
    elif ftype == 'text':
      return str(value)
    elif ftype == 'int':
      try:
        v = int(value)
        return str(v)
      except Exception:
        return None
    elif ftype == 'float':
      try:
        v = float(value)
        return str(v)
      except Exception:
        return None
    elif ftype == 'date':
      try:
        v = datetime.datetime.strptime(value, '%b %d %Y %I:%M%p')
        return v.isoformat()
      except Exception:
        return None
    return str(value)

  def getSolrType(self, field):
    """
    Returns the SOLR type of the specified field name.  Assumes the convention
    of dynamic fields using an underscore + type character code for the field
    name.
    """
    ftype = 'string'
    try:
      ftype = self.fieldtypes[field]
      return ftype
    except Exception:
      pass
    fta = field.split('_')
    if len(fta) > 1:
      ft = fta[len(fta) - 1]
      try:
        ftype = self.fieldtypes[ft]
        #cache the type so it's used next time
        self.fieldtypes[field] = ftype
      except Exception:
        pass
    return ftype

  def __add(self, lst, fields):
    lst.append('<doc>')
    for f, v in list(fields.items()):
      ftype = self.getSolrType(f)
      if isinstance(v, list):
        for vi in v:
          vi = self.coerceType(ftype, vi)
          if vi is not None:
            lst.append('<field name="')
            lst.append(self.escapeKey(str(f)))
            lst.append('">')
            lst.append(self.escapeVal(vi))
            lst.append('</field>')
      else:
        v = self.coerceType(ftype, v)
        if v is not None:
          lst.append('<field name="')
          lst.append(self.escapeKey(str(f)))
          lst.append('">')
          lst.append(self.escapeVal(v))
          lst.append('</field>')
    lst.append('</doc>')

  def add(self, **fields):
    lst = ['<add>']
    self.__add(lst, fields)
    lst.append('</add>')
    xstr = ''.join(lst)
    return self.doUpdateXML(xstr)

  def addDocs(self, docs):
    """docs is a list of fields that are a dictionary of name:value for a record
    """
    lst = [
      '<add>',
    ]
    for fields in docs:
      self.__add(lst, fields)
    lst.append('</add>')
    xstr = ''.join(lst)
    return self.doUpdateXML(xstr)

  def addMany(self, arrOfMap):
    lst = ['<add>']
    for doc in arrOfMap:
      self.__add(lst, doc)
    lst.append('</add>')
    xstr = ''.join(lst)
    return self.doUpdateXML(xstr)

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
    return self.doUpdateXML(xstr)

  def search(self, params):
    params['wt'] = 'python'
    request = urllib.parse.urlencode(params, doseq=True)
    rsp = self.doPost(self.solrBase + '', request, self.formheaders)
    data = eval(rsp.read())
    return data

  def count(self, q='*:*', fq=None):
    """
    Return the number of entries that match query
    """
    params = {'q': q, 'rows': '0'}
    if fq is not None:
      params['fq'] = fq
    res = self.search(params)
    hits = res['response']['numFound']
    return hits

  def getIds(self, query='*:*', fq=None, start=0, rows=1000):
    """Returns a dictionary of:
      matches: number of matches
      failed: if true, then an exception was thrown
      start: starting index
      ids: [id, id, ...]

    See also the SOLRSearchResponseIterator class
    """
    params = {
      'q': query,
      'start': str(start),
      'rows': str(rows),
      'wt': 'python',
    }
    if fq is not None:
      params['fq'] = fq
    request = urllib.parse.urlencode(params, doseq=True)
    data = None
    response = {
      'matches': 0,
      'start': start,
      'failed': True,
      'ids': [],
    }
    try:
      rsp = self.doPost(self.solrBase + '', request, self.formheaders)
      data = eval(rsp.read())
    except Exception:
      pass
    if data is None:
      return response
    response['failed'] = False
    response['matches'] = data['response']['numFound']
    for doc in data['response']['docs']:
      response['ids'].append(doc['id'][0])
    return response

  def get(self, id):
    """
    Retrieves the specified document.
    """
    params = {'q': 'id:%s' % str(id), 'wt': 'python'}
    request = urllib.parse.urlencode(params, doseq=True)
    data = None
    try:
      rsp = self.doPost(self.solrBase + '', request, self.formheaders)
      data = eval(rsp.read())
    except Exception:
      pass
    if data['response']['numFound'] > 0:
      return data['response']['docs'][0]
    return None

  def getFields(self, numTerms=1):
    """Retrieve a list of fields.  The response looks something like:
{
 'responseHeader':{
    'status':0,
    'QTime':44},
 'index':{
    'numDocs':2000,
    'maxDoc':2000,
    'numTerms':23791,
    'version':1227298371173,
    'optimized':True,
    'current':True,
    'hasDeletions':False,
    'directory':'org.apache.lucene.store.FSDirectory:org.apache.lucene.store.FSDirectory@/Users/vieglais/opt/localsolr_svn/home/data/index',
    'lastModified':'2009-03-12T18:27:59Z'},
 'fields':{
    'created':{
      'type':'date',
      'schema':'I-S----O----l',
      'index':'I-S----O-----',
      'docs':2000,
      'distinct':1,
      'topTerms':['2009-03-12T18:13:22Z',2000],
      'histogram':['2',0,'4',0,'8',0,'16',0,'32',0,'64',0,'128',0,'256',0,
       '512',0,'1024',0,'2048',1]},
    'species_s':{
      'type':'string',
      'schema':'I-SM---O----l',
      'dynamicBase':'*_s',
      'index':'I-S----O-----',
      'docs':1924,
      'distinct':209,
      'topTerms':['cepedianum',352],
      'histogram':['2',34,'4',34,'8',16,'16',13,'32',6,'64',3,'128',1,
       '256',2,'512',2]},
    """
    if self._fields is not None:
      return self._fields
    params = {'numTerms': str(numTerms), 'wt': 'python'}
    request = urllib.parse.urlencode(params, doseq=True)
    rsp = self.doPost(self.solrBase + '/admin/luke', request, self.formheaders)
    data = eval(rsp.read())
    self._fields = data
    return data

  def fieldValues(self, name, q="*:*", fq=None, maxvalues=-1):
    """
    Retrieve the unique values for a field, along with their usage counts.
    http://localhost:8080/solr/select/?q=*:*&rows=0&facet=true&indent=on&wt=python&facet.field=genus_s&facet.limit=10&facet.zeros=false&facet.sort=false

    @param name(string) Name of field to retrieve values for
    @param q(string) Query identifying the records from which values will be retrieved
    @param fq(string) Filter query restricting operation of query
    @param maxvalues(int) Maximum number of values to retrieve.  Default is -1,
      which causes retrieval of all values.
    @return dict of {fieldname: [[value, count], ... ], }
    """
    params = {
      'q': q,
      'rows': '0',
      'facet': 'true',
      'facet.field': name,
      'facet.limit': str(maxvalues),
      'facet.zeros': 'false',
      'wt': 'python',
      'facet.sort': 'false'
    }
    if fq is not None:
      params['fq'] = fq
    request = urllib.parse.urlencode(params, doseq=True)
    rsp = self.doPost(self.solrBase + '', request, self.formheaders)
    data = eval(rsp.read())
    return data['facet_counts']['facet_fields'] # , data['response']['numFound']

  def fieldMinMax(self, name, q='*:*', fq=None):
    """
    Returns the minimum and maximum values of the specified field.
    This requires two search calls to the service, each requesting a single
    value of a single field.

    @param name(string) Name of the field
    @param q(string) Query identifying range of records for min and max values
    @param fq(string) Filter restricting range of query

    @return list of [min, max]
    """
    minmax = [None, None]
    oldpersist = self.persistent
    self.persistent = True
    params = {
      'q': q,
      'rows': 1,
      'fl': name,
      'sort': '%s asc' % name,
      'wt': 'python',
    }
    if fq is not None:
      params['fq'] = fq
    try:
      data = self.search(params)
      minmax[0] = data['response']['docs'][0][name][0]
      params['sort'] = '%s desc' % name
      data = self.search(params)
      minmax[1] = data['response']['docs'][0][name][0]
    except Exception as e:
      self.logger.debug('Exception in MinMax: %s' % str(e))
      pass
    finally:
      self.persistent = oldpersist
      if not self.persistent:
        self.conn.close()
    return minmax

  def getftype(self, name):
    """
    Returns the python type for the specified field name.  The field list is
    cached so multiple calls do not invoke a getFields request each time.

    @param name(string) The name of the SOLR field
    @returns Python type of the field.
    """
    fields = self.getFields()
    try:
      fld = fields['fields'][name]
    except Exception:
      return str
    if fld['type'] in ['string', 'text', 'stext', 'text_ws']:
      return str
    if fld['type'] in ['sint', 'integer', 'long', 'slong']:
      return int
    if fld['type'] in ['sdouble', 'double', 'sfloat', 'float']:
      return float
    if fld['type'] in ['boolean']:
      return bool
    return fld['type']

  def fieldAlphaHistogram(
      self, name, q='*:*', fq=None, nbins=10, includequeries=True
  ):
    """
    Generates a histogram of values from a string field.
    Output is:
      [[low, high, count, query],
       ... ]
    Bin edges is determined by equal division of the fields
    """
    oldpersist = self.persistent
    self.persistent = True
    bins = []
    qbin = []
    fvals = []
    try:
      #get total number of values for the field
      #TODO: this is a slow mechanism to retrieve the number of distinct values
      #Need to replace this with something more efficient.
      ## Can probably replace with a range of alpha chars - need to check on
      ## case sensitivity
      fvals = self.fieldValues(name, q, fq, maxvalues=-1)
      nvalues = len(fvals[name]) / 2
      if nvalues < nbins:
        nbins = nvalues
      if nvalues == nbins:
        #Use equivalence instead of range queries to retrieve the values
        for i in range(0, nbins):
          bin = [fvals[name][i * 2], fvals[name][i * 2], 0]
          binq = '%s:%s' % (name, self.prepareQueryTerm(name, bin[0]))
          qbin.append(binq)
          bins.append(bin)
      else:
        delta = nvalues / nbins
        if delta == 1:
          #Use equivalence queries, except the last one which includes the
          # remainder of terms
          for i in range(0, nbins - 2):
            bin = [fvals[name][i * 2], fvals[name][i * 2], 0]
            binq = '%s:%s' % (name, self.prepareQueryTerm(name, bin[0]))
            qbin.append(binq)
            bins.append(bin)
          term = fvals[name][(nbins - 1) * 2]
          bin = [term, fvals[name][((nvalues - 1) * 2)], 0]
          binq = '%s:[%s TO *]' % (name, self.prepareQueryTerm(name, term))
          qbin.append(binq)
          bins.append(bin)
        else:
          #Use range for all terms
          #now need to page through all the values and get those at the edges
          coffset = 0.0
          delta = float(nvalues) / float(nbins)
          for i in range(0, nbins):
            idxl = int(coffset) * 2
            idxu = (int(coffset + delta) * 2) - 2
            bin = [fvals[name][idxl], fvals[name][idxu], 0]
            #logging.info(str(bin))
            binq = ''
            try:
              if i == 0:
                binq = '%s:[* TO %s]' % \
                   (name, self.prepareQueryTerm(name, bin[1]))
              elif i == nbins - 1:
                binq = '%s:[%s TO *]' % \
                   (name, self.prepareQueryTerm(name, bin[0]))
              else:
                binq = '%s:[%s TO %s]' % \
                  (name,
                   self.prepareQueryTerm(name, bin[0]),
                   self.prepareQueryTerm(name, bin[1]))
            except Exception:
              self.logger.exception('Exception 1 in fieldAlphaHistogram:')
            qbin.append(binq)
            bins.append(bin)
            coffset = coffset + delta
      #now execute the facet query request
      params = {
        'q': q,
        'rows': '0',
        'facet': 'true',
        'facet.field': name,
        'facet.limit': '1',
        'facet.mincount': 1,
        'wt': 'python'
      }
      request = urllib.parse.urlencode(params, doseq=True)
      for sq in qbin:
        try:
          request = request + '&%s' % urllib.parse.urlencode({
            'facet.query': self.encoder(sq)[0],
          })
        except Exception:
          self.logger.exception('Exception 2 in fieldAlphaHistogram')
      rsp = self.doPost(self.solrBase + '', request, self.formheaders)
      data = eval(rsp.read())
      for i in range(0, len(bins)):
        v = data['facet_counts']['facet_queries'][qbin[i]]
        bins[i][2] = v
        if includequeries:
          bins[i].append(qbin[i])
    finally:
      self.persistent = oldpersist
      if not self.persistent:
        self.conn.close()
    return bins

  def fieldHistogram(
      self, name, q="*:*", fq=None, nbins=10, minmax=None, includequeries=True
  ):
    """
    Generates a histogram of values.
    Expects the field to be integer or floating point.

    @param name(string) Name of the field to compute
    @param q(string) The query identifying the set of records for the histogram
    @param fq(string) Filter query to restrict application of query
    @param nbins(int) Number of bins in resulting histogram

    @return list of [binmin, binmax, n, binquery]
    """
    oldpersist = self.persistent
    self.persistent = True
    ftype = self.getftype(name)
    if ftype == str:
      ##handle text histograms over here
      bins = self.fieldAlphaHistogram(
        name, q=q, fq=fq, nbins=nbins, includequeries=includequeries
      )
      self.persistent = oldpersist
      if not self.persistent:
        self.conn.close()
      return bins
    bins = []
    qbin = []
    fvals = self.fieldValues(name, q, fq, maxvalues=nbins + 1)
    if len(fvals[name]) < 3:
      return bins
    nvalues = len(fvals[name]) / 2
    if nvalues < nbins:
      nbins = nvalues
    minoffset = 1
    if ftype == float:
      minoffset = 0.00001
    try:
      if minmax is None:
        minmax = self.fieldMinMax(name, q=q, fq=fq)
        #logging.info("MINMAX = %s" % str(minmax))
        minmax[0] = float(minmax[0])
        minmax[1] = float(minmax[1])
      delta = (minmax[1] - minmax[0]) / nbins
      for i in range(0, nbins):
        binmin = minmax[0] + (i * delta)
        bin = [binmin, binmin + delta, 0]
        if ftype == int:
          bin[0] = int(bin[0])
          bin[1] = int(bin[1])
          if i == 0:
            binq = '%s:[* TO %d]' % (name, bin[1])
          elif i == nbins - 1:
            binq = '%s:[%d TO *]' % (name, bin[0] + minoffset)
            bin[0] = bin[0] + minoffset
            if bin[1] < bin[0]:
              bin[1] = bin[0]
          else:
            binq = '%s:[%d TO %d]' % (name, bin[0] + minoffset, bin[1])
            bin[0] = bin[0] + minoffset
        else:
          if i == 0:
            binq = '%s:[* TO %f]' % (name, bin[1])
          elif i == nbins - 1:
            binq = '%s:[%f TO *]' % (name, bin[0] + minoffset)
          else:
            binq = '%s:[%f TO %f]' % (name, bin[0] + minoffset, bin[1])
        qbin.append(binq)
        bins.append(bin)

      #now execute the facet query request
      params = {
        'q': q,
        'rows': '0',
        'facet': 'true',
        'facet.field': name,
        'facet.limit': '1',
        'facet.mincount': 1,
        'wt': 'python'
      }
      request = urllib.parse.urlencode(params, doseq=True)
      for sq in qbin:
        request = request + '&%s' % urllib.parse.urlencode({
          'facet.query': sq,
        })
      rsp = self.doPost(self.solrBase + '', request, self.formheaders)
      data = eval(rsp.read())
      for i in range(0, len(bins)):
        v = data['facet_counts']['facet_queries'][qbin[i]]
        bins[i][2] = v
        if includequeries:
          bins[i].append(qbin[i])
    finally:
      self.persistent = oldpersist
      if not self.persistent:
        self.conn.close()
    return bins

  def fieldHistogram2d(
      self, colname, rowname, q="*:*", fq=None, ncols=10, nrows=10
  ):
    """
    Generates a 2d histogram of values.
    Expects the field to be integer or floating point.

    @param name1(string) Name of field1 columns to compute
    @param name2(string) Name of field2 rows to compute
    @param q(string) The query identifying the set of records for the histogram
    @param fq(string) Filter query to restrict application of query
    @param nbins1(int) Number of columns in resulting histogram
    @param nbins2(int) Number of rows in resulting histogram

    @return dict of {colname:  name of column index
                     rowname:  name of row index
                     cols: [] list of min values for each column bin
                     rows: [] list of min values for each row bin
                     z: [[],
                         []]
    """

    def _mkQterm(name, minv, maxv, isint, isfirst, islast):
      q = ''
      if isint:
        minv = int(minv)
        maxv = int(maxv)
        if isfirst:
          q = '%s:[* TO %d]' % (name, maxv)
        elif islast:
          q = '%s:[%d TO *]' % (name, maxv)
        else:
          q = '%s:[%d TO %d]' % (name, minv, maxv)
      else:
        if isfirst:
          q = '%s:[* TO %f]' % (name, maxv)
        elif islast:
          q = '%s:[%f TO *]' % (name, maxv)
        else:
          q = '%s:[%f TO %f]' % (name, minv, maxv)
      return q

    oldpersist = self.persistent
    self.persistent = True
    ftype_col = self.getftype(colname)
    ftype_row = self.getftype(rowname)
    result = {
      'colname': colname,
      'rowname': rowname,
      'cols': [],
      'rows': [],
      'z': []
    }
    minoffsetcol = 1
    minoffsetrow = 1
    if ftype_col == float:
      minoffsetcol = 0.00001 # noqa: F841
    if ftype_row == float:
      minoffsetrow = 0.00001 # noqa: F841
    try:
      rowminmax = self.fieldMinMax(rowname, q=q, fq=fq)
      rowminmax[0] = float(rowminmax[0])
      rowminmax[1] = float(rowminmax[1])
      colminmax = self.fieldMinMax(colname, q=q, fq=fq)
      colminmax[0] = float(colminmax[0])
      colminmax[1] = float(colminmax[1])
      rowdelta = (rowminmax[1] - rowminmax[0]) / nrows
      coldelta = (colminmax[1] - colminmax[0]) / ncols

      for rowidx in range(0, nrows):
        rmin = rowminmax[0] + (rowidx * rowdelta)
        result['rows'].append(rmin)
        rmax = rmin + rowdelta
        rowq = _mkQterm(
          rowname, rmin, rmax,
          (ftype_row == int), (rowidx == 0), (rowidx == nrows - 1)
        )
        qq = "%s AND %s" % (q, rowq)
        logging.debug("row=%d, q= %s" % (rowidx, qq))
        bins = []
        cline = []
        for colidx in range(0, ncols):
          cmin = colminmax[0] + (colidx * coldelta)
          result['cols'].append(cmin)
          cmax = cmin + coldelta
          colq = _mkQterm(
            colname, cmin, cmax,
            (ftype_col == int), (colidx == 0), (colidx == ncols - 1)
          )
          bin = [colidx, rowidx, cmin, rmin, cmax, rmax, 0, colq]
          bins.append(bin)
        #now execute the facet query request
        params = {
          'q': qq,
          'rows': '0',
          'facet': 'true',
          'facet.field': colname,
          'facet.limit': '1',
          'facet.mincount': 1,
          'wt': 'python'
        }
        if fq is not None:
          params['fq'] = fq
        request = urllib.parse.urlencode(params, doseq=True)
        for bin in bins:
          request = request + '&%s' % urllib.parse.urlencode({
            'facet.query': bin[7],
          })
        rsp = self.doPost(self.solrBase + '', request, self.formheaders)
        data = eval(rsp.read())
        for bin in bins:
          v = data['facet_counts']['facet_queries'][bin[7]]
          cline.append(v)
        result['z'].append(cline)
    finally:
      self.persistent = oldpersist
      if not self.persistent:
        self.conn.close()
    return result


#===============================================================================


class SOLRRecordTransformer(object):
  """
  A SOLR record transformer.  Used to transform a SOLR search response document
  into some other form, such as a dictionary or list of values.

  This base implementation just returns the record unchanged.
  """

  def __init__(self):
    pass

  def transform(self, record):
    return record


#===============================================================================


class SOLRArrayTransformer(SOLRRecordTransformer):
  """
  A transformer that returns a list of values for the sepcified columns.
  """

  def __init__(self, cols=[
      'lng',
      'lat',
  ]):
    self.cols = cols

  def transform(self, record):
    res = []
    for col in self.cols:
      try:
        v = record[col]
        if isinstance(v, list):
          res.append(v[0])
        else:
          res.append(v)
      except Exception:
        res.append(None)
    return res


#===============================================================================


class SOLRSearchResponseIterator(object):
  """
  Performs a search against a SOLR index and acts as an iterator to
  retrieve all the values.
  """

  def __init__(
      self, client, q, fq=None, fields='*', pagesize=100,
      transformer=SOLRRecordTransformer()
  ):
    """
    Initialize.

    @param client(SolrConnection) An instance of a solr connection to use.
    @param q(string) The SOLR query to restrict results
    @param fq(string) A facet query, restricts the set of rows that q is applied to
    @param fields(string) A comma delimited list of field names to return
    @param pagesize(int) Number of rows to retrieve in each call.
    """
    self.logger = logging.getLogger('solrclient.SOLRSearchResponseIterator')
    self.client = client
    self.q = q
    self.fq = fq
    self.fields = fields
    self.crecord = 0
    self.pagesize = pagesize
    self.res = None
    self.done = False
    self.transformer = transformer
    self._nextPage(self.crecord)
    self._numhits = 0
    self.logger.debug(
      "Iterator hits=%s" % str(self.res['response']['numFound'])
    )

  def _nextPage(self, offset):
    """
    Retrieves the next set of results from the service.
    """
    self.logger.debug("Iterator crecord=%s" % str(self.crecord))
    params = {
      'q': self.q,
      'start': str(offset),
      'rows': str(self.pagesize),
      'fl': self.fields,
      'explainOther': '',
      'hl.fl': ''
    }
    if self.fq is not None:
      params['fq'] = self.fq
    self.res = self.client.search(params)
    self._numhits = int(self.res['response']['numFound'])

  def __iter__(self):
    return self

  def processRow(self, row):
    """
    Override this method in derived classes to reformat the row response
    """
    return row

  def __next__(self):
    if self.done:
      raise StopIteration()
    idx = self.crecord - self.res['response']['start']
    try:
      row = self.res['response']['docs'][idx]
    except IndexError:
      self._nextPage(self.crecord)
      idx = self.crecord - self.res['response']['start']
      try:
        row = self.res['response']['docs'][idx]
      except IndexError:
        self.done = True
        raise StopIteration()
    self.crecord = self.crecord + 1
    return self.transformer.transform(row)


#===============================================================================


class SOLRArrayResponseIterator(SOLRSearchResponseIterator):
  """
  Returns an interator that operates on a SOLR result set.  The output for each
  document is a list of values for the columns specified in the cols parameter
  of the constructor.
  """

  def __init__(self, client, q, fq=None, pagesize=100, cols=[
      'lng',
      'lat',
  ]):
    transformer = SOLRArrayTransformer(cols)
    fields = ",".join(cols)
    SOLRSearchResponseIterator.__init__(
      self, client, q, fq, fields, pagesize, transformer=transformer
    )
    self.logger = logging.getLogger('solrclient.SOLRArrayResponseIterator')


#===============================================================================


class SOLRSubsampleResponseIterator(SOLRSearchResponseIterator):
  """Returns a pseudo-random subsample of the result set.  Works by calculating
  the number of pages required for the entire data set and taking a random sample
  of pages until nsamples can be retrieved.  So pages are random, but records
  within a page are not.
  """

  def __init__(
      self, client, q, fq=None, fields='*', pagesize=100, nsamples=10000,
      transformer=SOLRRecordTransformer()
  ):
    self._pagestarts = [
      0,
    ]
    self._cpage = 0
    SOLRSearchResponseIterator.__init__(
      self, client, q, fq, fields, pagesize, transformer
    )
    npages = self._numhits / self.pagesize
    if npages > 0:
      samplesize = nsamples / pagesize
      if samplesize > npages:
        samplesize = npages
      self._pagestarts += random.sample(list(range(0, npages)), samplesize)
      self._pagestarts.sort()

  def __next__(self):
    """
    Overrides the default iteration by sequencing through records within a page
    and when necessary selecting the next page from the randomly generated list.
    """
    if self.done:
      raise StopIteration()
    idx = self.crecord - self.res['response']['start']
    try:
      row = self.res['response']['docs'][idx]
    except IndexError:
      self._cpage += 1
      try:
        self._crecord = self._pagestarts[self._cpage]
        self._nextPage(self.crecord)
        idx = self.crecord - self.res['response']['start']
        row = self.res['response']['docs'][idx]
      except IndexError:
        self.done = True
        raise StopIteration()
    self.crecord = self.crecord + 1
    return self.processRow(row)


#===============================================================================


class SOLRValuesResponseIterator(object):
  """
  Iterates over a SOLR get values response.  This returns a list of distinct
  values for a particular field.
  """

  def __init__(self, client, field, q='*:*', fq=None, pagesize=1000):
    """
    Initialize.

    @param client(SolrConnection) An instance of a solr connection to use.
    @param field(string) name of the field from which to retrieve values
    @param q(string) The SOLR query to restrict results
    @param fq(string) A facet query, restricts the set of rows that q is applied to
    @param fields(string) A comma delimited list of field names to return
    @param pagesize(int) Number of rows to retrieve in each call.
    """
    self.logger = logging.getLogger('solrclient.SOLRValuesResponseIterator')
    self.client = client
    self.q = q
    self.fq = fq
    self.field = field
    self.crecord = 0
    self.pagesize = pagesize
    self.res = None
    self.done = False
    self._nextPage(self.crecord)

  def __iter__(self):
    return self

  def _nextPage(self, offset):
    """
    Retrieves the next set of results from the service.
    """
    self.logger.debug("Iterator crecord=%s" % str(self.crecord))

    params = {
      'q': self.q,
      'rows': '0',
      'facet': 'true',
      'facet.field': self.field,
      'facet.limit': str(self.pagesize),
      'facet.offset': str(offset),
      'facet.zeros': 'false',
      'wt': 'python'
    }
    if self.fq is not None:
      params['fq'] = self.fq
    request = urllib.parse.urlencode(params, doseq=True)
    rsp = self.client.doPost(
      self.client.solrBase + '', request, self.client.formheaders
    )
    data = eval(rsp.read())
    try:
      self.res = data['facet_counts']['facet_fields'][self.field]
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
      self._nextPage(self.crecord)
      try:
        row = [self.res[self.index], self.res[self.index + 1]]
        self.index = self.index + 2
      except IndexError:
        self.done = True
        raise StopIteration()
    self.crecord = self.crecord + 1
    return row


#===============================================================================

if __name__ == '__main__':
  #some simple tests

  def test1():

    client = SolrConnection(
      host="cn-dev-unm-1.test.dataone.org/", solrBase="/solr"
    )
    q = 'sciName_s:Ba*'
    fq = None
    fields = 'lat,lng'
    pagesize = 5
    rows = SOLRSearchResponseIterator(
      client, q, fq=fq, fields=fields, pagesize=pagesize
    )
    for row in rows:
      print(row)
    rows = SOLRArrayResponseIterator(
      client, q, fq=fq, fields=fields, pagesize=pagesize
    )
    for row in rows:
      print(row)

  #def test2():
  #  client = SolrConnection(host="cn-dev.dataone.org", solrBase="/datanet_solr")
  #  q = '*:*'
  #  fq = None
  #  field = 'size'
  #  pagesize = 5
  #  rows = SOLRValuesResponseIterator(client, field, q, fq, pagesize=pagesize)
  #  for row in rows:
  #    print row
  #
  #def listFields():
  #  client = SolrConnection(host="cn-dev.dataone.org", solrBase="/datanet_solr")
  #  flds = client.getFields()
  #  print "%d fields indexed\n" % len(flds['fields'].keys())
  #  for name in flds['fields'].keys():
  #    fld = flds['fields'][name]
  #    print "%s (%s) %d / %d" % (name, fld['type'], fld['distinct'], fld['docs'])
  #
  #def test4():
  #  solr = SolrConnection(host="cn-dev.dataone.org", solrBase="/datanet_solr")
  #  results = SOLRSearchResponseIterator(solr, 'id:[* TO *]')
  #  for rec in results:
  #    print rec

  logging.basicConfig(level=logging.DEBUG)
  test1()
