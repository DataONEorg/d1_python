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

import logging

# import d1_common
import d1_common.type_conversions

import d1_client.baseclient

#=============================================================================


class DataONEBaseClient_1_1(
    d1_client.baseclient.DataONEBaseClient,
):
  """Extend DataONEBaseClient with functionality common between Member and
  Coordinating nodes that was added in v1.1 of the DataONE infrastructure.

  For details on how to use these methods, see:

  https://releases.dataone.org/online/api-documentation-v2.0/apis/MN_APIs.html
  https://releases.dataone.org/online/api-documentation-v2.0/apis/CN_APIs.html
  """

  def __init__(self, *args, **kwargs):
    """See d1_client.baseclient.DataONEBaseClient for args."""
    super(DataONEBaseClient_1_1, self).__init__(*args, **kwargs)

    self.logger = logging.getLogger(__file__)

    self._api_major = 1
    self._api_minor = 1
    self._bindings = d1_common.type_conversions.get_bindings_by_api_version(
      self._api_major, self._api_minor
    )

  #=============================================================================
  # v1.1 APIs shared between CNs and MNs.
  #=============================================================================

  # CNRead.query(session, queryEngine, query) → OctetStream
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.query
  # MNQuery.query(session, queryEngine, query) → OctetStream
  # http://jenkins-1.dataone.org/jenkins/job/API%20Documentation%20-%20trunk/ws/api-documentation/build/html/apis/MN_APIs.html#MNQuery.query

  def queryResponse(
      self, queryEngine, query_str, vendorSpecific=None, do_post=False, **kwargs
  ):
    logging.debug(
      'Solr query: {}'.format(
        ', '.join(['{}={}'.format(k, v) for (k, v) in list(locals().items())])
      )
    )
    return (self.POST
            if do_post else self.GET)(['query', queryEngine, query_str],
                                      headers=vendorSpecific, **kwargs)

  def query(
      self, queryEngine, query_str, vendorSpecific=None, do_post=False, **kwargs
  ):
    response = self.queryResponse(
      queryEngine, query_str, vendorSpecific, do_post, **kwargs
    )
    if self._content_type_is_json(response):
      return self._read_json_response(response)
    else:
      return self._read_stream_response(response)

  # CNRead.getQueryEngineDescription(session, queryEngine) → QueryEngineDescription
  # https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html#CNRead.getQueryEngineDescription
  # MNQuery.getQueryEngineDescription(session, queryEngine) → QueryEngineDescription
  # http://jenkins-1.dataone.org/jenkins/job/API%20Documentation%20-%20trunk/ws/api-documentation/build/html/apis/MN_APIs.html#MNQuery.getQueryEngineDescription

  def getQueryEngineDescriptionResponse(self, queryEngine, **kwargs):
    return self.GET(['query', queryEngine], query=kwargs)

  def getQueryEngineDescription(self, queryEngine, **kwargs):
    response = self.getQueryEngineDescriptionResponse(queryEngine, **kwargs)
    return self._read_dataone_type_response(response, 'QueryEngineDescription')

  # TODO: Implement these:
  # CNRead.listQueryEngines(session) → QueryEngineList
  # http://jenkins-1.dataone.org/jenkins/job/API%20Documentation%20-%20trunk/ws/api-documentation/build/html/apis/CN_APIs.html#CNRead.listQueryEngines
  # MNQuery.listQueryEngines(session) → QueryEngineList
  # http://jenkins-1.dataone.org/jenkins/job/API%20Documentation%20-%20trunk/ws/api-documentation/build/html/apis/MN_APIs.html#MNQuery.listQueryEngines
