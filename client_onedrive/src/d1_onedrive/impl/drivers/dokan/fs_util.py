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
"""DataONE file system utilities

TODO: This file should be merged with the equivalent used in the FUSE
implementation.  The main difference between the two is the caching
mechanism.
"""

import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from . import solrclient

import d1_common.const

import d1_client.d1client

# Config
PATHELEMENT_SAFE_CHARS = ' @$,~*&'
ITERATOR_PER_FETCH = 400
FACET_REFRESH = 20 # seconds between cache refresh for facet values
PERSIST_SOLR_CLIENT = True

## set up caching ##
# set up caching data and lock dirs
#base_dir = os.path.dirname(__file__)
base_dir = os.environ['TEMP']
data_dir = base_dir + '\\d1_drive\\cache\\data'
lock_dir = base_dir + '\\d1_drive\\cache\\lock'
# create the data dir if it doesn't exist
if not os.path.exists(data_dir):
  os.makedirs(data_dir)
# create the lock dir if it doesn't exist
if not os.path.exists(lock_dir):
  os.makedirs(lock_dir)
# set up the caching parameters
cache_opts = {
  'cache.data_dir': data_dir,
  'cache.lock_dir': lock_dir,
  'cache.regions': 'mem_cache', # 'mem_cache, file_cache',
  # 'cache.file_cache.type':'file',
  # 'cache.file_cache.enabled':'True',
  # 'cache.file_cache.expire':'60',
  'cache.mem_cache.type': 'memory',
  'cache.mem_cache.enabled': 'True',
  'cache.mem_cache.expire': '300'
}

cache = None # d1_onedrive.impl.CacheManager(**parse_cache_config_options(cache_opts))


class D1FS():
  def __init__(
      self, baseurl=d1_common.const.URL_DATAONE_ROOT, filter_query=None
  ):
    self.logger = logging.getLogger('DataOneFS')
    self.baseurl = baseurl
    self._solrclient = None
    self._filter_query = filter_query

    # The columns to get from the Solr index.
    self.fields = [
      'id', 'identifier', 'title', 'objectFormat', 'update_date', 'size'
    ]
    # Solr search facets.
    self.facets = {
      'projects': {
        'f': 'project',
        'tstamp': 0,
        'v': [],
        'n': [],
      },
      'data_providers': {
        'f': 'datasource',
        'tstamp': 0,
        'v': [],
        'n': [],
      },
      'decade': {
        'f': 'decade',
        'tstamp': 0,
        'v': [],
        'n': [],
      },
      'keywords': {
        'f': 'keywords',
        'tstamp': 0,
        'v': [],
        'n': [],
      },
      'title': {
        'f': 'title',
        'tstamp': 0,
        'v': [],
        'n': [],
      },
    }

  def getSolrHost(self):
    url_parts = urllib.parse.urlsplit(self.baseurl)
    return url_parts.netloc

  def getSolrClient(self, forceNew=True):
    if forceNew or self._solrclient is None:
      self._solrclient = solrclient.SolrConnection(
        self.getSolrHost(), solrBase='cn/v1/solr',
        persistent=PERSIST_SOLR_CLIENT
      )
    return self._solrclient

  def getObject(self, pid, refresh=False):
    @cache.region('mem_cache', 'getObject')
    def getObject(pid):
      return d1_client.d1client.DataONEObject(pid, cnBaseUrl=self.baseurl)

    if refresh:
      cache.region_invalidate(getObject, 'mem_cache', 'getObject', pid)
    return getObject(pid)

  def getSystemMetadata(self, pid, refresh=False):
    @cache.region('mem_cache', 'getSystemMetadata')
    def getSystemMetadata(pid):
      obj = self.getObject(pid)
      sysm = obj.getSystemMetadata()
      return sysm

    if refresh:
      cache.region_invalidate(
        getSystemMetadata, 'mem_cache', 'getSystemMetadata', pid
      )
    return getSystemMetadata(pid)

  def getObjectFileName(self, pid):
    sysm = self.getSystemMetadata(pid)
    ofmt = sysm.objectFormat
    extension = self.getExtensionFromObjectFormat(ofmt)
    filename = pid + extension
    return filename

  def getObjectPid(self, filename):
    return filename[:filename.rfind('.')]

  def get(self, pid, refresh=False):
    @cache.region('mem_cache', 'get')
    def get(pid):
      obj = self.getObject(pid)
      return obj.get().read()

    if refresh:
      cache.region_invalidate(get, 'mem_cache', 'get', pid)
    return get(pid)

  def getFacetValues(self, facet, refresh=False):
    @cache.region('mem_cache', 'getFacetValues')
    def getFacetValues(facet):
      now = time.time()
      dt = now - self.facets[facet]['tstamp']
      if refresh or (len(self.facets[facet]['v']) < 1) or (dt > FACET_REFRESH):
        sc = self.getSolrClient()
        self.facets[facet]['tstamp'] = time.time()
        self.facets[facet]['v'] = []
        self.facets[facet]['n'] = []
        fname = self.facets[facet]['f']
        fvals = sc.fieldValues(fname, fq=self._filter_query)
        for i in range(0, len(fvals[fname]), 2):
          fv = self.encodePathName(fvals[fname][i])
          if len(fv) > 0:
            fc = fvals[fname][i + 1]
            self.facets[facet]['v'].append(fv)
            self.facets[facet]['n'].append(fc)
            # Can we also append the latest of beginDate and endDate for each of
            # the value groups?
      return self.facets[facet]['v']

    if refresh:
      cache.region_invalidate(
        getFacetValues, 'mem_cache', 'getFacetValues', facet
      )
    return getFacetValues(facet)

  def getRecords(self, facet, term):
    fname = self.facets[facet]['f']
    sc = self.getSolrClient()
    q = sc.prepareQueryTerm(fname, term)
    records = solrclient.SOLRArrayResponseIterator(
      sc, q, fq=self._filter_query, cols=self.fields,
      pagesize=ITERATOR_PER_FETCH
    )
    return records

  #This is a helper method to extract the identifiers from the records
  # returned by get records.  It mainly exists because the records themselves
  # are not cachable ("picklable").
  def getIdentifiers(self, facet, term, refresh=False):
    @cache.region('mem_cache', 'getIdentifiers')
    def getIdentifiers(facet, term):
      records = self.getRecords(facet, term)
      ret = []
      for r in records:
        ret.append(r[1])
      return ret

    if refresh:
      cache.region_invalidate(
        getIdentifiers, 'mem_cache', 'getIdentifiers', facet, term
      )
    return getIdentifiers(facet, term)

  @cache.region('mem_cache', 'getAbstract')
  def getAbstract(self, pid):
    self.logger.debug('getAbstract: {}'.format(pid))
    sc = self.getSolrClient()
    q = sc.prepareQueryTerm('identifier', pid)
    records = solrclient.SOLRArrayResponseIterator(
      sc, q, fq=self._filter_query, cols=[
        'abstract',
      ], pagesize=ITERATOR_PER_FETCH
    )
    ret = ''
    for rec in records:
      if rec[0] is not None:
        ret = rec[0]
      break
    return ret

  def encodePathName(cls, name):
    return urllib.parse.quote(name.encode('utf-8'), safe=PATHELEMENT_SAFE_CHARS)

  def getExtensionFromObjectFormat(cls, ofmt):
    formats = {
      'eml://ecoinformatics.org/eml-2.0.0': '.xml',
      'eml://ecoinformatics.org/eml-2.0.1': '.xml',
      'eml://ecoinformatics.org/eml-2.1.0': '.xml',
      'FGDC-STD-001.1-1999': '.xml',
      'eml://ecoinformatics.org/eml-2.1.1': '.xml',
      'FGDC-STD-001-1998': '.xml',
      'INCITS 453-2009': '.xml',
      'http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2': '.xml',
      'CF-1.0': '.xml',
      'CF-1.1': '.xml',
      'CF-1.2': '.xml',
      'CF-1.3': '.xml',
      'CF-1.4': '.xml',
      'http://www.cuahsi.org/waterML/1.0/': '.xml',
      'http://www.cuahsi.org/waterML/1.1/': '.xml',
      'http://www.loc.gov/METS/': '.xml',
      'netCDF-3': '.cd3',
      'netCDF-4': '.cd4',
      'text/plain': '.txt',
      'text/csv': '.csv',
      'image/bmp': '.bmp',
      'image/gif': '.gif',
      'image/jp2': '.jp2',
      'image/jpeg': '.jpg',
      'image/png': '.png',
      'image/svg+xml': '.svg',
      'image/tiff': '.tif',
      'http://rs.tdwg.org/dwc/xsd/simpledarwincore/': '.xml',
      'http://digir.net/schema/conceptual/darwin/2003/1.0/darwin2.xsd': '.xml',
      'application/octet-stream': '.bin',
    }
    res = '.bin'
    try:
      res = formats[ofmt]
    except Exception:
      logging.error('Unknown file format requested: {}'.format(ofmt))
    return res
