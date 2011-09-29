#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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

'''Module d1_client.cnclient
============================

This module implements CoordinatingNodeClient, which extends DataONEBaseClient
with functionality specific to Coordinating Nodes.

:Created: 2011-01-22
:Author: DataONE (Vieglais, Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import logging
import urllib
import urlparse

# 3rd party.

# D1.
from d1_common import const
from d1_common import util
import d1_common.types.generated.dataoneTypes as dataoneTypes

# App.
from d1baseclient import DataONEBaseClient

#SOLRclient is used to support search against the SOLR instance running on the
#coordinating node. 
import solrclient


class CoordinatingNodeClient(DataONEBaseClient):
  
  def __init__(self, baseurl=const.URL_DATAONE_ROOT, 
                     defaultHeaders={},
                     timeout=const.RESPONSE_TIMEOUT, 
                     keyfile=None, 
                     certfile=None,
                     strictHttps=True):
    '''Connect to a Coordinating Node.
    
    :param baseurl: Coordinating Node REST service endpoint URL.
    :type baseurl: str
    :param defaultHeaders: list of headers that will be sent with all requests.
    :type defaultHeaders: dictionary
    :param timeout: Time in seconds that requests will wait for a response.
    :type timeout: int
    :param keyfile: name of a PEM formatted file that contains a private key. 
    :type keyfile: str
    :param certfile: PEM formatted certificate chain file.
    :type certfile: str
    :param strictHttps: Raise BadStatusLine if the status line can’t be parsed
    as a valid HTTP/1.0 or 1.1 status line.
    :type strictHttps: bool
    :returns: None
    :return type: NoneType
    '''
    DataONEBaseClient.__init__(self, baseurl, defaultHeaders=defaultHeaders,
                               timeout=timeout, keyfile=keyfile, 
                               certfile=certfile, strictHttps=strictHttps)
    self.logger = logging.getLogger('CoordinatingNodeClient')
    self.methodmap.update({
      'resolve': u'resolve/%(pid)s',
      'search': u'object',
      'listobjects': u'object?qt=path',
    })

  @util.str_to_unicode
  def resolveResponse(self, pid):
    '''Wrap the CNRead.resolve() DataONE REST call.
    
    Returns the nodes (MNs or CNs) known to hold copies of the object identified
    by pid.

    :param pid: Identifier
    :type pid: string containing ASCII or UTF-8 | unicode string
    :returns: List of object locations.
    :return type: Serialized ObjectLocationList in HTTPResponse
    '''
    url = self.RESTResourceURL('resolve', pid=pid)
    return self.GET(url)

  
  @util.str_to_unicode
  def resolve(self, pid):
    '''See resolveResponse().
    
    :returns: List of object locations. 
    :return type: PyXB ObjectLocationList.
    '''
    response = self.resolveResponse(pid)
    return dataoneTypes.CreateFromDocument(response.read())


  @util.str_to_unicode
  def reserveIdentifier(self, pid=None, scope=None, format=None):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def assertRelation(self, pidOfSubject, relationship, pidOfObject):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def searchResponse(self, query):
    '''
    Wraps the CNRead.search() DataONE REST call.

    Search the metadata catalog and return identifiers of metadata records that
    match the criteria.
    
    :param query: Query string.
    :type query: str
    :returns: List of objects
    :return type: Serialized ObjectList in HttpResponse.
    '''
    url = self.RESTResourceURL('search')
    url_params = {
      'query': query,
    }
    return self.GET(url, url_params=url_params)


  @util.str_to_unicode
  def search(self, query, fields="pid,origin_mn,datemodified,size,objectformat,title",
             start=0, count=100):
    '''This is a place holder for search against the SOLR search engine.
     
    '''
    hostinfo = self._parseURL(self.baseurl)
    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
                                     persistent=True)
    params = {'q':query,
              'fl': fields,
              'start':str(start),
              'rows':str(count)}
    sres = solr.search(params)
    return sres['response']    
    #response = self.searchResponse(query)
    #return dataoneTypes.CreateFromDocument(response.read())


  def getSearchFields(self):
    #getFields
    hostinfo = self._parseURL(self.baseurl)
    solr = solrclient.SolrConnection(host=hostinfo['host'], solrBase="/solr",
                                     persistent=True)
    sres = solr.getFields()
    return sres['fields']


  @util.str_to_unicode
  def getAuthToken(self, cert):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def setOwner(self, pid, userId):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def newAccount(self, username, password, authSystem=None): 
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def verifyToken(self, token):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def mapIdentity(self, token1, token2):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def createGroup(self, token, groupName):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def addGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def removeGroupMembers(self, token, groupName, members):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def setReplicationStatus(self, token, pid, status): 
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def addNodeCapabilities(self, token, pid):
    raise Exception('Not Implemented')


  @util.str_to_unicode
  def register(self, token):
    raise Exception('Not Implemented')

