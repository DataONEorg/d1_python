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
"""Process and execute CLI operations.
"""

import html.entities
import io
import os
import re

import d1_cli.impl.cli_client as cli_client
import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.cli_util as cli_util
import d1_cli.impl.format_ids as format_ids
import d1_cli.impl.nodes as nodes
import d1_cli.impl.operation_maker as operation_maker
import d1_cli.impl.operation_queue as operation_queue
import d1_cli.impl.session as session
import requests

import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

DEFAULT_PREFIX = ''
DEFAULT_PROMPT = '> '
SOLR_FORMAT_ID_NAME = 'formatId'


class CommandProcessor():
  def __init__(self):
    self._nodes = nodes.Nodes()
    self._format_ids = format_ids.FormatIDs()
    self._session = session.Session(self._nodes, self._format_ids)
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

  #-----------------------------------------------------------------------------
  # Operations against Coordinating Nodes
  #-----------------------------------------------------------------------------

  # Read operations.

  def ping(self, hosts):
    if not len(hosts):
      self._ping_base(self._session.get(session.CN_URL_NAME))
      self._ping_base(self._session.get(session.MN_URL_NAME))
    else:
      for host in hosts:
        cn_base_url = d1_common.url.makeCNBaseURL(host)
        mn_base_url = d1_common.url.makeMNBaseURL(host)
        self._ping_base(cn_base_url)
        if mn_base_url != cn_base_url:
          self._ping_base(mn_base_url)

  def search(self, line):
    """CN search.
    """
    if self._session.get(session.QUERY_ENGINE_NAME) == 'solr':
      return self._search_solr(line)
    raise cli_exceptions.InvalidArguments(
      'Unsupported query engine: {}'.
      format(self._session.get(session.QUERY_ENGINE_NAME))
    )

  def list_format_ids(self):
    cn_base_url = self._session.get(session.CN_URL_NAME)
    self._output(self._format_ids.format(cn_base_url))

  def list_nodes(self):
    cn_base_url = self._session.get(session.CN_URL_NAME)
    self._output(self._nodes.format(cn_base_url))

  def resolve(self, pid):
    """Get Object Locations for Object.
    """
    client = cli_client.CLICNClient(
      **self._cn_client_connect_params_from_session()
    )
    object_location_list = client.resolve(pid)
    for location in object_location_list.objectLocation:
      cli_util.print_info(location.url)

  # Write operations (queued)

  def update_access_policy(self, pids):
    for pid in pids:
      self._queue_update_access_policy(pid)

  def update_replication_policy(self, pids):
    for pid in pids:
      self._queue_update_replication_policy(pid)

  #-----------------------------------------------------------------------------
  # Operations against Member Nodes
  #-----------------------------------------------------------------------------

  # Read operations

  def science_object_get(self, pid, path):
    """First try the MN set in the session. Then try to resolve via the CN set
    in the session."""
    mn_client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_session()
    )
    try:
      response = mn_client.get(pid)
    except d1_common.types.exceptions.DataONEException:
      pass
    else:
      self._output(response, path)
      return

    cn_client = cli_client.CLICNClient(
      **self._cn_client_connect_params_from_session()
    )
    object_location_list = cn_client.resolve(pid)
    for location in object_location_list.objectLocation:
      try:
        params = self._mn_client_connect_params_from_session()
        params['base_url'] = location.baseURL
        mn_client = cli_client.CLIMNClient(**params)
        response = mn_client.get(pid)
      except d1_common.types.exceptions.DataONEException:
        pass
      else:
        self._output(response, path)
        return

    raise cli_exceptions.CLIError('Could not find object: {}'.format(pid))

  def system_metadata_get(self, pid, path):
    metadata = None
    try:
      client = cli_client.CLICNClient(
        **self._cn_client_connect_params_from_session()
      )
      metadata = client.getSystemMetadata(pid)
    except d1_common.types.exceptions.DataONEException:
      pass
    if metadata is None:
      try:
        client = cli_client.CLIMNClient(
          **self._mn_client_connect_params_from_session()
        )
        metadata = client.getSystemMetadata(pid)
      except d1_common.types.exceptions.DataONEException:
        pass
    if metadata is None:
      raise cli_exceptions.CLIError(
        'Unable to get System Metadata: {}'.format(pid)
      )
    self._system_metadata_print(metadata, path)

  def log(self, path):
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_session()
    )
    object_log = client.getLogRecords(
      fromDate=self._session.get(session.FROM_DATE_NAME),
      toDate=self._session.get(session.TO_DATE_NAME),
      start=self._session.get(session.START_NAME),
      count=self._session.get(session.COUNT_NAME)
    )
    object_log_xml = object_log.toxml('utf-8')
    self._output(io.BytesIO(self._pretty(object_log_xml).encode('utf-8')), path)

  def list_objects(self, path):
    client = cli_client.CLIMNClient(
      **self._mn_client_connect_params_from_session()
    )
    object_list = client.listObjects(
      fromDate=self._session.get(session.FROM_DATE_NAME),
      toDate=self._session.get(session.TO_DATE_NAME),
      formatId=self._session.get(session.SEARCH_FORMAT_NAME),
      start=self._session.get(session.START_NAME),
      count=self._session.get(session.COUNT_NAME)
    )
    object_list_xml = object_list.toxml('utf-8')
    self._output(
      io.BytesIO(self._pretty(object_list_xml).encode('utf-8')), path
    )

  # Write operations (queued)

  def science_object_create(self, pid, path, format_id=None):
    """Create a new Science Object on a Member Node
    """
    self._queue_science_object_create(pid, path, format_id)

  def science_object_update(self, pid_old, path, pid_new, format_id=None):
    """Obsolete a Science Object on a Member Node with a different one.
    """
    self._queue_science_object_update(pid_old, path, pid_new, format_id)

  def create_package(self, pids):
    self._queue_create_package(pids)

  def science_object_archive(self, pids):
    for pid in pids:
      self._queue_science_object_archive(pid)

  #
  # Private.
  #

  def _output(self, file_like_object, path=None):
    """Display or save file like object"""
    if not path:
      self._output_to_display(file_like_object)
    else:
      self._output_to_file(file_like_object, path)

  def _output_to_display(self, file_like_object):
    for line in file_like_object:
      cli_util.print_info(line.rstrip())

  def _output_to_file(self, file_like_object, path):
    abs_path = cli_util.os.path.expanduser(path)
    if os.path.exists(abs_path):
      if not cli_util.confirm(
          'You are about to overwrite an existing file at "{}". Continue? '
          .format(abs_path), default='yes'
      ):
        cli_util.print_info('Cancelled')
    if isinstance(file_like_object, requests.Response):
      cli_util.copy_requests_stream_to_file(file_like_object, path)
    else:
      cli_util.copy_file_like_object_to_file(file_like_object, abs_path)
    cli_util.print_info('Created file: {}'.format(abs_path))

  def _pretty(self, xml_doc):
    return d1_common.xml.format_pretty_xml(xml_doc.decode('utf-8'))

  def _system_metadata_print(self, metadata, path=None):
    sci_meta_xml = metadata.toxml('utf-8')
    if path is not None:
      path = cli_util.os.path.expanduser(path)
    self._output(io.BytesIO(self._pretty(sci_meta_xml).encode('utf-8')), path)

  def _ping_base(self, base_url):
    result = cli_client.CLIBaseClient(base_url).ping()
    self._print_ping_result(result, base_url)

  def _print_ping_result(self, result, url):
    if result:
      cli_util.print_info('Responded:       {}'.format(url))
    else:
      cli_util.print_error('Did not respond: {}'.format(url))

  def _search_solr(self, line):
    """Perform a SOLR search.
    """
    try:
      query_str = self._create_solr_query(line)
      client = cli_client.CLICNClient(
        **self._cn_client_connect_params_from_session()
      )
      object_list = client.search(
        queryType=d1_common.const.DEFAULT_SEARCH_ENGINE,
        query=query_str,
        start=self._session.get(session.START_NAME),
        rows=self._session.get(session.COUNT_NAME),
      )
      cli_util.print_info(self._pretty(object_list.toxml('utf-8')))
    except d1_common.types.exceptions.ServiceFailure as e:
      e = "%".join(str(e).splitlines()) # Flatten line
      regexp = re.compile(
        r"errorCode: (?P<error_code>\d+)%.*%Status code: (?P<status_code>\d+)"
      )
      result = regexp.search(e)
      if ((result is not None) and (result.group('error_code') == '500') and
          (result.group('status_code') == '400')): # noqa: E129
        result = re.search(
          r"<b>description</b> <u>(?P<description>[^<]+)</u>", e
        )
        msg = re.sub(
          '&([^;]+);', lambda m: chr(html.entities.name2codepoint[m.group(1)]),
          result.group('description')
        )
        cli_util.print_info('Warning: %s' % msg)
      else:
        cli_util.print_error('Unexpected error:\n%s' % str(e))

  def _create_solr_query(self, line):
    """Actual search - easier to test. """
    p0 = ''
    if line:
      p0 = line.strip()
    p1 = self._query_string_to_solr_filter(line)
    p2 = self._object_format_to_solr_filter(line)
    p3 = self._time_span_to_solr_filter()
    result = p0 + p1 + p2 + p3
    return result.strip()

  def _query_string_to_solr_filter(self, line):
    query = self._session.get(session.QUERY_STRING_NAME)
    if not query or query == '' or (query == '*:*' and len(line) > 0):
      return ''
    else:
      return ' ' + query

  def _time_span_to_solr_filter(self):
    fromdate = self._session.get(session.FROM_DATE_NAME)
    todate = self._session.get(session.TO_DATE_NAME)
    return ' dateModified:[{} TO {}]'.format(
      d1_common.date_time.http_datetime_str_from_dt(fromdate)
      if fromdate else '*',
      d1_common.date_time.http_datetime_str_from_dt(todate) if todate else '*'
    )

  def _object_format_to_solr_filter(self, line):
    search_format_id = self._session.get(session.SEARCH_FORMAT_NAME)
    if not search_format_id or search_format_id == '':
      return ''
    else:
      if line.find(SOLR_FORMAT_ID_NAME) >= 0:
        cli_util.print_warn(
          'Using query format restriction instead: {}'.format(search_format_id)
        )
      else:
        return ' %s:%s' % (SOLR_FORMAT_ID_NAME, search_format_id)

  def _mn_client_connect_params_from_session(self):
    return self._mn_cn_client_connect_params_from_session(session.MN_URL_NAME)

  def _cn_client_connect_params_from_session(self):
    return self._mn_cn_client_connect_params_from_session(session.CN_URL_NAME)

  def _mn_cn_client_connect_params_from_session(self, url_name):
    anonymous = self._session.get(session.ANONYMOUS_NAME)
    return {
      'base_url':
        self._session.get(url_name),
      'cert_pem_path':
        self._session.get(session.CERT_FILENAME_NAME)
        if not anonymous else None,
      'cert_key_path':
        self._session.get(session.KEY_FILENAME_NAME) if not anonymous else None,
    }

  #
  # Queuing of write operations
  #

  def _queue_science_object_create(self, pid, path, format_id):
    create_operation = self._operation_maker.create(pid, path, format_id)
    self._operation_queue.append(create_operation)

  def _queue_science_object_update(self, pid_old, path, pid_new, format_id):
    update_operation = self._operation_maker.update(
      pid_old, path, pid_new, format_id
    )
    self._operation_queue.append(update_operation)

  def _queue_create_package(self, pids):
    archive_operation = self._operation_maker.create_package(pids)
    self._operation_queue.append(archive_operation)

  def _queue_science_object_archive(self, pid):
    archive_operation = self._operation_maker.archive(pid)
    self._operation_queue.append(archive_operation)

  def _queue_update_access_policy(self, pid):
    update_access_policy_operation = self._operation_maker.update_access_policy(
      pid
    )
    self._operation_queue.append(update_access_policy_operation)

  def _queue_update_replication_policy(self, pid):
    update_replication_policy_operation = self._operation_maker.update_replication_policy(
      pid
    )
    self._operation_queue.append(update_replication_policy_operation)


#def get_object_by_pid(session, pid, filename=None, resolve=True):
#  """ Create a mnclient and look for the object.  If the object is not found,
#      simply return a None, don't throw an exception.  If found, return the
#      filename.
#  """
#  if session is None:
#    raise cli_exceptions.InvalidArguments(u'Missing session')
#  if pid is None:
#    raise cli_exceptions.InvalidArguments(u'Missing pid')
#  # Create member node client and try to get the object.
#  mn_client = CLIMNClient(session)
#  try:
#    response = mn_client.get(pid)
#    if response is not None:
#      fname = _get_fname(filename)
#      cli_util.output(response, fname, session.is_verbose())
#      return fname
#  except d1_common.types.exceptions.DataONEException as e:
#    if e.errorCode != 404:
#      raise cli_exceptions.CLIError(
#        u'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format()))
#  if resolve:
#    cn_client = CLICNClient(session)
#    object_location_list = None
#    try:
#      object_location_list = cn_client.resolve(pid)
#      if ((object_location_list is not None)
#          and (len(object_location_list.objectLocation) > 0)):
#        baseUrl = object_location_list.objectLocation[0].baseURL
#        # If there is an object, go get it.
#        mn_client = CLIMNClient(session, mn_url=baseUrl)
#        response = mn_client.get(pid)
#        if response is not None:
#          fname = _get_fname(filename)
#          cli_util.output(response, os.path.expanduser(fname))
#          return fname
#    except d1_common.types.exceptions.DataONEException as e:
#      if e.errorCode != 404:
#        raise cli_exceptions.CLIError(
#          u'Unable to get resolve: {0}\n{1}'.format(pid, e.friendly_format()))
#  # Nope, didn't find anything
#  return None
#
#

#
#
#def get_baseUrl(session, nodeId):
#  """  Get the base url of the given node id.
#  """
#  cn_client = CLICNClient(session)
#  try:
#    nodes = cn_client.listNodes()
#    for node in list(nodes.node):
#      if node.identifier.value() == nodeId:
#        return node.baseURL
#  except (d1_common.types.exceptions.ServiceFailure) as e:
#    cli_util.print_error("Unable to get node list.")
#  return None
#
#
#def get_sys_meta_by_pid(session, pid, search_mn = False):
#  """  Get the system metadata object for this particular pid.
#  """
#  if not session:
#    raise cli_exceptions.InvalidArguments(u'Missing session')
#  if not pid:
#    raise cli_exceptions.InvalidArguments(u'Missing pid')
#
#  sys_meta = None
#  try:
#    cn_client = CLICNClient(session)
#    obsolete = True;
#    while obsolete:
#      obsolete = False;
#      sys_meta = cn_client.getSystemMetadata(pid)
#      if not sys_meta:
#        return None
#      if sys_meta.obsoletedBy:
#        msg = (u'Object "%s" has been obsoleted by "%s".  '
#            + u'Would you rather use that?') % (pid, sys_meta.obsoletedBy)
#        if not cli_util.confirm(msg):
#          break;
#        pid = sys_meta.obsoletedBy
#        obsolete = True
#    return sys_meta
#  except d1_common.types.exceptions.DataONEException as e:
#      if e.errorCode != 404:
#        raise cli_exceptions.CLIError(
#          u'Unable to get system metadata for: {0}\n{1}'.format(pid, e.friendly_format()))
#  # Search the member node?
#  if not sys_meta and (search_mn is not None) and search_mn:
#    try:
#      mn_client = CLIMNClient(session)
#      obsolete = True;
#      while obsolete:
#        obsolete = False;
#        sys_meta = mn_client.getSystemMetadata(pid)
#        if not sys_meta:
#          return None
#        if sys_meta.obsoletedBy:
#          msg = (u'Object "%s" has been obsoleted by "%s".  '
#              + u'Would you rather use that?') % (pid, sys_meta.obsoletedBy)
#          if not cli_util.confirm(msg):
#            break;
#          pid = sys_meta.obsoletedBy
#          obsolete = True
#      return sys_meta
#    except d1_common.types.exceptions.DataONEException as e:
#        if e.errorCode != 404:
#          raise cli_exceptions.CLIError(
#            u'Unable to get system metadata for: {0}\n{1}'.format(pid, e.friendly_format()))
#
#  return sys_meta
