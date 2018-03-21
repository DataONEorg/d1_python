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
"""Extend d1_client.solr_client.SolrClient for OneDrive
"""

import logging

import d1_onedrive.impl.onedrive_exceptions
import requests

import d1_common.const
import d1_common.date_time
import d1_common.url

import d1_client.solr_client


class OneDriveSolrClient(d1_client.solr_client.SolrClient):
  def __init__(self, options, max_retries=3):
    self._solr_endpoint = options.base_url + options.solr_query_path
    self._session = requests.Session()
    self._session.mount(
      'http://', requests.adapters.HTTPAdapter(max_retries=max_retries)
    )
    self._session.mount(
      'https://', requests.adapters.HTTPAdapter(max_retries=max_retries)
    )
    self._timeout_sec = options.solr_query_timeout_sec
    self._max_objects_for_query = options.max_objects_for_query

  def run_solr_query(self, query, filter_queries=None, fields=None):
    response = self._query(query, filter_queries=filter_queries, fields=fields)
    for record in response['response']['docs']:
      self._close_open_date_ranges(record)
      self._parse_iso8601_date_to_native_date_time(record)
    return response['response']['docs']

  def get_solr_record(self, pid):
    query = 'id:{}'.format(self._escape_query_term_string(pid))
    response = self.run_solr_query(query)
    try:
      return response[0]
    except IndexError:
      raise d1_onedrive.impl.onedrive_exceptions.ONEDriveException(
        'Object does not exist. pid={}'.format(pid)
      )

  #
  # Private.
  #

  def _parse_http_date_to_native_date_time(self, describe_resp_dict):
    date_fields = ['date', 'date']
    for date_field in date_fields:
      if date_field in describe_resp_dict:
        describe_resp_dict[date_field
                           ] = d1_common.date_time.dt_from_http_datetime_str(
                             describe_resp_dict[date_field]
                           )

  def _close_open_date_ranges(self, record):
    """If a date range is missing the start or end date, close it by copying
    the date from the existing value."""
    date_ranges = (('beginDate', 'endDate'),)
    for begin, end in date_ranges:
      if begin in record and end in record:
        return
      elif begin in record:
        record[end] = record[begin]
      elif end in record:
        record[begin] = record[end]

  def _parse_iso8601_date_to_native_date_time(self, record):
    date_fields = [
      'beginDate', 'endDate', 'datePublished', 'dateModified', 'dateUploaded',
      'updateDate'
    ]
    for date_field in date_fields:
      if date_field in record:
        try:
          record[date_field] = d1_common.date_time.dt_from_iso8601_str(
            record[date_field]
          )
        except Exception as e:
          logging.exception(e)
