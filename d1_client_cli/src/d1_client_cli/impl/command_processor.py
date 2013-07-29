#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2013 DataONE
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
'''
:mod:`command_processor`
==================

:Synopsis: Process and execute CLI operations.
:Created: 2013-07-16
:Author: DataONE (Dahl)
'''

# Stdlib.
import cmd
import htmlentitydefs
import logging
import optparse
import os
import re
import shlex
import StringIO
from string import join
import sys
import xml.dom.minidom

# D1
import d1_common.util
import d1_common.url
import d1_common.const
import d1_common.types.exceptions

# App.
import cli_client
import cli_exceptions
import cli_util
from const import * #@UnusedWildImport
import initialize #@UnusedImport
import session
import check_dependencies
import operation_queue
import operation_maker
import nodes
import format_ids

DEFAULT_PREFIX = u''
DEFAULT_PROMPT = u'> '
SOLR_FORMAT_ID_NAME = u'formatId'


class CommandProcessor():
  def __init__(self):
    self._nodes = nodes.Nodes()
    self._format_ids = format_ids.FormatIDs()
    self._session = session.session(self._nodes, self._format_ids)
    self._session.load(suppress_error=True)
    self._object_format_id_cache = None
    self._operation_queue = operation_queue.OperationQueue(self._session)
    self._operation_maker = operation_maker.OperationMaker(self._session)

  def get_session(self):
    return self._session

  def get_operation_queue(self):
    return self._operation_queue

  def get_nodes(self):
    return self._nodes

  def get_format_ids(self):
    return self._format_ids

  def set_session_parameter(self, session_parameter, value):
    self._session.set_with_conversion_implicit_section(session_parameter, value)

  #-----------------------------------------------------------------------------
  # Operations against Coordinating Nodes
  #-----------------------------------------------------------------------------

  def ping(self, hosts):
    if not len(hosts):
      self._ping_base(self._session.get(session.CN_URL_SECT, session.CN_URL_NAME))
      self._ping_base(self._session.get(session.MN_URL_SECT, session.MN_URL_NAME))
    else:
      for host in hosts:
        cn_base_url = d1_common.url.makeCNBaseURL(host)
        mn_base_url = d1_common.url.makeMNBaseURL(host)
        self._ping_base(cn_base_url)
        if mn_base_url != cn_base_url:
          self._ping_base(mn_base_url)

  def search(self, line):
    '''CN search.
    '''
    if self._session.get(session.QUERY_ENGINE_SECT, session.QUERY_ENGINE_NAME) == u'solr':
      return self._search_solr(line)
    raise cli_exceptions.InvalidArguments(
      'Unsupported query engine: {0}'.format(
        QUERY_ENGINE_NAME
      )
    )

  def list_format_ids(self):
    cn_base_url = self._session.get(session.CN_URL_SECT, session.CN_URL_NAME)
    self._output(self._format_ids.format(cn_base_url))

  def list_nodes(self):
    cn_base_url = self._session.get(session.CN_URL_SECT, session.CN_URL_NAME)
    self._output(self._nodes.format(cn_base_url))

  def resolve(self, pid):
    '''Get Object Locations for Object.
    '''
    client = cli_client.CLICNClient(**self._cn_client_connect_params_from_session())
    object_location_list = client.resolve(pid)
    for location in object_location_list.objectLocation:
      cli_util.print_info(location.url)

  #-----------------------------------------------------------------------------
  # Operations against Member Nodes
  #-----------------------------------------------------------------------------

  # Read operations

  def science_object_get(self, pid, path, resolve=True):
    try:
      mn_client = cli_client.CLIMNClient(**self._mn_client_connect_params_from_session())
      response = mn_client.get(pid)
      self._output(response, path)
      return True
    except d1_common.types.exceptions.DataONEException as e:
      errmsg = u'Unable to get Science Object from Member Node\n{0}'\
          .format(e.friendly_format())
    # Go and find it?
    if resolve:
      cn_client = cli_client.CLICNClient(**self._mn_client_connect_params_from_session())
      try:
        object_location_list = cn_client.resolve(pid)
        if object_location_list:
          for location in object_location_list.objectLocation:
            try:
              params = self._mn_client_connect_params_from_session()
              params['base_url'] = location.baseURL
              mn_client = cli_client.CLIMNClient(**params)
              response = mn_client.get(pid)
              self._output(response, path)
              return True
            except Exception as e:
              pass
      except d1_common.types.exceptions.DataONEException as e:
        errmsg = u'Unable to get Science Object from Member Node\n{0}'\
            .format(e.friendly_format())
    # Didn't find it - was it because of an exception?
    if not errmsg:
      cli_util.print_warn(u'Could not find identifier: {0}'.format(pid))
      return False
    else:
      raise cli_exceptions.CLIError(errmsg)

  def system_metadata_get(self, pid, path):
    metadata = None
    foundOnCN = False
    try:
      client = cli_client.CLICNClient(**self._cn_client_connect_params_from_session())
      metadata = client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException as e:
      pass
    if metadata is not None:
      foundOnCN = True
    else:
      try:
        client = cli_client.CLIMNClient(**self._mn_client_connect_params_from_session())
        metadata = client.getSystemMetadata(pid)
      except d1_common.types.exceptions.DataONEException as e:
        pass
    if metadata is None:
      raise
    self._system_metadata_print(metadata, path, foundOnCN)

  def log(self, path):
    client = cli_client.CLIMNClient(**self._mn_client_connect_params_from_session())
    object_log = client.getLogRecords(
      fromDate=self._session.get(session.FROM_DATE_SECT, session.FROM_DATE_NAME),
      toDate=self._session.get(session.TO_DATE_SECT, session.TO_DATE_NAME),
      start=self._session.get(session.START_SECT, session.START_NAME),
      count=self._session.get(session.COUNT_SECT, session.COUNT_NAME)
    )
    object_log_xml = object_log.toxml()
    self._output(StringIO.StringIO(self._pretty(object_log_xml)), path)

  def list_objects(self, path):
    client = cli_client.CLIMNClient(**self._mn_client_connect_params_from_session())
    object_list = client.listObjects(
      fromDate=self._session.get(session.FROM_DATE_SECT, session.FROM_DATE_NAME),
      toDate=self._session.get(session.TO_DATE_SECT, session.TO_DATE_NAME),
      objectFormat=self._session.get(
        session.SEARCH_FORMAT_SECT, session.SEARCH_FORMAT_NAME
      ),
      start=self._session.get(session.START_SECT, session.START_NAME),
      count=self._session.get(session.COUNT_SECT, session.COUNT_NAME)
    )
    object_list_xml = object_list.toxml()
    self._output(StringIO.StringIO(self._pretty(object_list_xml)), path)

  # Write operations (queued)

  def science_object_create(self, pid, path, format_id=None):
    '''Create a new Science Object on a Member Node
    '''
    self._queue_science_object_create(pid, path, format_id)

  def science_object_update(self, pid_old, path, pid_new, format_id=None):
    '''Obsolete a Science Object on a Member Node with a different one.
    '''
    self._queue_science_object_update(pid_old, path, pid_new, format_id)

  def create_package(self, pids):
    self._queue_create_package(pids)

  def science_object_archive(self, pids):
    for pid in pids:
      self._queue_science_object_archive(pid)

  def update_access_policy(self, pids):
    for pid in pids:
      self._queue_update_access_policy(pid)

  def update_replication_policy(self, pids):
    for pid in pids:
      self._queue_update_replication_policy(pid)

  #
  # Private.
  #

  def _output(self, file_like_object, path=None):
    '''Display or save file like object'''
    if not path:
      self._output_to_dislay(file_like_object)
    else:
      self._output_to_file(file_like_object, path)

  def _output_to_dislay(self, file_like_object):
    for line in file_like_object:
      cli_util.print_info(line.rstrip())

  def _output_to_file(self, file_like_object, path):
    abs_path = cli_util.os.path.expanduser(path)
    if os.path.exists(abs_path):
      if not cli_util.confirm(
        'You are about to overwrite an existing file. Continue?',
        default='yes'
      ):
        cli_util.print_info('Cancelled')
    cli_util.copy_file_like_object_to_file(file_like_object, abs_path)
    cli_util.print_info('Created file: {0}'.format(abs_path))

  def _pretty(self, xml_doc):
    # As far as I can tell from the docs, it should not be necessary to encode
    # to UTF-8 before using the xml doc to construct the dom. But if I don't
    # do this, toxml() and toprettyxml() fail with ascii encoding errors.
    dom = xml.dom.minidom.parseString(xml_doc.encode('UTF-8'))
    return dom.toprettyxml(indent='  ')

  def _system_metadata_print(self, metadata, path=None, foundOnCN=False):
    sci_meta_xml = metadata.toxml()
    if path is not None:
      path = cli_util.os.path.expanduser(path)
    self._output(StringIO.StringIO(self._pretty(sci_meta_xml)), path)

  def _ping_base(self, base_url):
    result = cli_client.CLIBaseClient(base_url).ping()
    self._print_ping_result(result, base_url)

  def _print_ping_result(self, result, url):
    if result:
      cli_util.print_info('Responded:       {0}'.format(url))
    else:
      cli_util.print_error('Did not respond: {0}'.format(url))

  def _search_solr(self, line):
    '''Perform a SOLR search.
    '''
    try:
      query = self._create_solr_query(line)
      client = cli_client.CLICNClient(**self._cn_client_connect_params_from_session())
      object_list = client.search(
        queryType=d1_common.const.DEFAULT_SEARCH_ENGINE,
        q=query,
        start=self._session.get(session.START_SECT, session.START_NAME),
        rows=self._session.get(session.COUNT_SECT, session.COUNT_NAME)
      )
      cli_util.print_info(self._pretty(object_list.toxml()))
    #
    # SOLR returns HTML instead of XML when there's a problem.  See:
    #   https://issues.apache.org/jira/browse/SOLR-141
    except d1_common.types.exceptions.ServiceFailure as e:
      e = "%".join(str(e).splitlines()) # Flatten line
      regexp = re.compile(
        r"errorCode: (?P<error_code>\d+)%.*%Status code: (?P<status_code>\d+)"
      )
      result = regexp.search(e)
      if ((result is not None) and
          (result.group(u'error_code') == '500') and
          (result.group(u'status_code') == '400')):
        result = re.search(r"<b>description</b> <u>(?P<description>[^<]+)</u>", e)
        msg = re.sub(
          u'&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]),
          result.group(u'description')
        )
        cli_util.print_info(u'Warning: %s' % msg)
      else:
        cli_util.print_error(u'Unexpected error:\n%s' % str(e))

  def _create_solr_query(self, line):
    '''  Actual search - easier to test. '''
    p0 = u''
    if line:
      p0 = line.strip()
    p1 = self._query_string_to_solr_filter(line)
    p2 = self._object_format_to_solr_filter(line)
    p3 = self._time_span_to_solr_filter()
    result = p0 + p1 + p2 + p3
    return result.strip()

  def _query_string_to_solr_filter(self, line):
    query = self._session.get(session.QUERY_STRING_SECT, session.QUERY_STRING_NAME)
    if not query or query == u'' or (query == '*:*' and len(line) > 0):
      return u''
    else:
      return u' ' + query

  def _time_span_to_solr_filter(self):
    fromdate = self._session.get(session.FROM_DATE_SECT, session.FROM_DATE_NAME)
    todate = self._session.get(session.TO_DATE_SECT, session.TO_DATE_NAME)
    return u' dateModified:[{0} TO {1}]'.format(
      d1_common.date_time.to_http_datetime(fromdate) if fromdate else u'*',
      d1_common.date_time.to_http_datetime(todate) if todate else u'*'
    )

  def _object_format_to_solr_filter(self, line):
    search_format_id = self._session.get(
      session.SEARCH_FORMAT_SECT, session.SEARCH_FORMAT_NAME
    )
    if not search_format_id or search_format_id == u'':
      return u''
    else:
      if line.find(SOLR_FORMAT_ID_NAME) >= 0:
        cli_util.print_warn(
          u'Using query format restriction instead: {0}'.format(search_format_id)
        )
      else:
        return u' %s:%s' % (SOLR_FORMAT_ID_NAME, search_format_id)

  def _mn_client_connect_params_from_session(self):
    return self._mn_cn_client_connect_params_from_session(
      session.MN_URL_SECT, session.MN_URL_NAME
    )

  def _cn_client_connect_params_from_session(self):
    return self._mn_cn_client_connect_params_from_session(
      session.CN_URL_SECT, session.CN_URL_NAME
    )

  def _mn_cn_client_connect_params_from_session(self, url_sect, url_name):
    anonymous = self._session.get(session.ANONYMOUS_SECT, session.ANONYMOUS_NAME)
    return {
      'base_url': self._session.get(url_sect, url_name),
      'cert_path': self._session.get(session.CERT_FILENAME_SECT, session.CERT_FILENAME_NAME)
        if not anonymous  else None,
      'key_path': self._session.get(session.KEY_FILENAME_SECT, session.KEY_FILENAME_NAME)
        if not anonymous  else None,
    }

  #
  # Queuing of write operations
  #

  def _queue_science_object_create(self, pid, path, format_id):
    create_operation = self._operation_maker.create(pid, path, format_id)
    self._operation_queue.append(create_operation)

  def _queue_science_object_update(self, pid_old, path, pid_new, format_id):
    update_operation = self._operation_maker.update(pid_old, path, pid_new, format_id)
    self._operation_queue.append(update_operation)

  def _queue_create_package(self, pids):
    archive_operation = self._operation_maker.create_package(pids)
    self._operation_queue.append(archive_operation)

  def _queue_science_object_archive(self, pid):
    archive_operation = self._operation_maker.archive(pid)
    self._operation_queue.append(archive_operation)

  def _queue_update_access_policy(self, pid):
    update_access_policy_operation = self._operation_maker.update_access_policy(pid)
    self._operation_queue.append(update_access_policy_operation)

  def _queue_update_replication_policy(self, pid):
    update_replication_policy_operation = self._operation_maker.update_replication_policy(
      pid
    )
    self._operation_queue.append(update_replication_policy_operation)
