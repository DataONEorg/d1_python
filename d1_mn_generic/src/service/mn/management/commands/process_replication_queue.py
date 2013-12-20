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
'''
:mod:`process_replication_queue`
================================

:Synopsis:
  Iterate over queue of objects registered for replication and attempt to
  replicate them.
:Created: 2011-01-01
:Author: DataONE (Dahl)
'''

# Stdlib.
import StringIO
import fcntl
import logging
import os
import shutil
import sys
import tempfile

# Django.
from django.core.management.base import NoArgsCommand

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.url
import d1_common.util

# Add some GMN paths to include path.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../'))
sys.path.append(_here('../types/generated'))

# App.
import gmn_types
import settings

# TODO: Currently copies the objects to temporary files. Everything is in place
# for streaming the objects instead.


class Command(NoArgsCommand):
  help = 'Process the replication queue.'

  def handle_noargs(self, **options):
    self.log_setup()

    self.abort_if_other_instance_is_running()

    logging.info('Running management command: ' 'process_replication_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

#    logging.getLogger('').setLevel(logging.DEBUG if settings.GMN_DEBUG
#                                   else logging.WARNING)

#    print settings.NODE_BASEURL
#    print settings.DATAONE_ROOT
#    print settings.CLIENT_CERT_PATH
#    print settings.CLIENT_CERT_PRIVATE_KEY_PATH

    p = ProcessReplicationQueue()
    p.process_replication_queue()

  def log_setup(self):
    # Set up logging. We output only to stdout. Instead of also writing to a log
    # file, redirect stdout to a log file when the script is executed from cron.
    logging.getLogger('').setLevel(logging.DEBUG)
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)

  def abort_if_other_instance_is_running(self):
    single_path = os.path.join(
      tempfile.gettempdir(), os.path.splitext(__file__)[0] + '.single'
    )
    f = open(single_path, 'w')
    try:
      fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
      self.logger.info('Aborted: Another instance is still running')
      exit(0)

#===============================================================================


class ProcessReplicationQueue(object):
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.gmn_client = GMNReplicationClient(settings.INTERNAL_BASEURL, timeout=60 * 60)
    self.cn_client = self._create_cn_client()

  def process_replication_queue(self):
    while self._process_replication_task():
      pass
    self.gmn_client.remove_completed_tasks_from_queue()

  def _process_replication_task(self):
    task = self._get_next_replication_task()
    if not task:
      return False
    self.logger.info('-' * 40)
    self.logger.info('Processing PID: {0}'.format(task.pid))
    try:
      self._replicate(task)
    except d1_common.types.exceptions.DataONEException as e:
      self.logger.exception('Replication failed with DataONE Exception:')
      self._cn_replicate_task_update(task, 'failed', e)
      self._gmn_replicate_task_update(task, str(e))
    except (ReplicateError, Exception, object) as e:
      self.logger.exception('Replication failed with internal exception:')
      self._cn_replicate_task_update(task, 'failed')
      self._gmn_replicate_task_update(task, str(e))
    return True

  def _get_next_replication_task(self):
    try:
      return self.gmn_client.internal_replicate_task_get()
    except d1_common.types.exceptions.NotFound:
      return None

  def _replicate(self, task):
    self._gmn_replicate_task_update(task, 'in progress')
    sysmeta_tmp_file = self._get_system_metadata(task)
    science_data_tmp_file = self._get_science_data(task)
    self._gmn_replicate_create(task, science_data_tmp_file, sysmeta_tmp_file)
    self._gmn_replicate_task_update(task, 'completed')
    self._cn_replicate_task_update(task, 'completed')

  def _cn_replicate_task_update(self, task, replication_status, e=None):
    try:
      self.cn_client.setReplicationStatus(
        task.pid, settings.NODE_IDENTIFIER, replication_status, e
      )
    except Exception as e:
      self.logger.exception(
        'CNReplication.setReplicationStatus() failed with '
        'the following exception:'
      )

  # Allow any exception in _gmn_replicate_task_update() to remain unhandled
  # so that the script exits. This causes a delay until the next time this
  # script is run by cron, before the task is retried. Without this, this
  # script would not exit and a continuous series of retries would happen as
  # fast as the system could manage.
  def _gmn_replicate_task_update(self, task, status=None):
    if status is None or status == '':
      status = 'Unknown error. See replication log.'
    return self.gmn_client.update_replicate_task_status(task.taskId, status[:1024])

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=settings.DATAONE_ROOT,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )

  def _get_system_metadata(self, task):
    sysmeta = self._open_sysmeta_stream_on_coordinating_node(task.pid)
    return self._copy_string_to_tmp_file(sysmeta.toxml())

  def _open_sysmeta_stream_on_coordinating_node(self, pid):
    return self.cn_client.getSystemMetadata(pid)

  def _get_science_data(self, task):
    source_node_base_url = self._resolve_source_node_id_to_base_url(task.sourceNode)
    mn_client = d1_client.mnclient.MemberNodeClient(
      base_url=source_node_base_url,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )
    sci_data_stream = self._open_sci_obj_stream_on_member_node(mn_client, task.pid)
    return self._copy_stream_to_tmp_file(sci_data_stream)

  def _copy_string_to_tmp_file(self, s):
    return self._copy_stream_to_tmp_file(StringIO.StringIO(s))

  def _copy_stream_to_tmp_file(self, stream):
    #f = tempfile.TemporaryFile() # for production
    f = tempfile.NamedTemporaryFile(delete=False) # for debugging
    self.logger.debug(f.name)
    shutil.copyfileobj(stream, f)
    f.seek(0)
    return f

  def _resolve_source_node_id_to_base_url(self, source_node):
    node_list = self._get_node_list()
    discovered_nodes = []
    for node in node_list.node:
      discovered_node_id = node.identifier.value()
      discovered_nodes.append(discovered_node_id)
      if discovered_node_id == source_node:
        return node.baseURL
    raise ReplicateError(
      'Unable to resolve Source Node ID: {0}. '
      'Discovered nodes: {1}'.format(source_node, ', '.join(discovered_nodes))
    )

  def _get_node_list(self):
    return self.cn_client.listNodes()

  def _open_sci_obj_stream_on_member_node(self, mn_client, pid):
    return mn_client.getReplica(pid)

  def _gmn_replicate_create(self, task, sci_obj, sysmeta):
    return self.gmn_client.internal_replicate_create(task.pid, sci_obj, sysmeta)

# ==============================================================================


class GMNReplicationClient(d1_client.mnclient.MemberNodeClient):
  '''Extend the d1_client.MemberNodeClient class with wrappers for the internal
  GMN REST calls that support the replication process.
  '''

  def __init__(
    self,
    base_url,
    timeout=d1_common.const.RESPONSE_TIMEOUT,
    defaultHeaders=None,
    cert_path=None,
    key_path=None,
    strict=True,
    capture_response_body=False,
    version='internal',
    types=gmn_types
  ):

    d1_client.mnclient.MemberNodeClient.__init__(
      self,
      base_url=base_url,
      timeout=timeout,
      defaultHeaders=defaultHeaders,
      cert_path=cert_path,
      key_path=key_path,
      strict=strict,
      capture_response_body=capture_response_body,
      version=version,
      types=types
    )

    self.logger = logging.getLogger(self.__class__.__name__)

  def internal_get_setting(self, setting):
    url = self._rest_url('get_setting/%(setting)s', setting=setting)
    response = self.GET(url)
    return self._read_dataone_type_response(response)

  def internal_replicate_task_get(self):
    url = self._rest_url('replicate/task_get')
    response = self.GET(url)
    return self._read_dataone_type_response(response)

  def update_replicate_task_status(self, task_id, status):
    url = self._rest_url(
      'replicate/task_update/%(task_id)s/%(status)s',
      task_id=str(task_id),
      status=status
    )
    response = self.GET(url)
    return self._read_boolean_response(response)

  #@util.utf8_to_unicode
  def internal_replicate_create(self, pid, sci_obj, sysmeta, vendorSpecific=None):
    '''Create replica of object on GMN'''
    if vendorSpecific is None:
      vendorSpecific = {}
    url = self._rest_url('replicate/create/%(pid)s', pid=pid)
    mime_multipart_fields = [('pid', pid.encode('utf-8')), ]
    mime_multipart_files = [
      ('object', 'content.bin', sci_obj),
      ('sysmeta', 'sysmeta.xml', sysmeta),
    ]
    response = self.POST(
      url,
      fields=mime_multipart_fields,
      files=mime_multipart_files,
      headers=vendorSpecific
    )
    return self._read_boolean_response(response)

  def remove_completed_tasks_from_queue(self):
    url = self._rest_url('replicate/remove_completed_tasks_from_queue')
    response = self.GET(url)
    return self._read_boolean_response(response)

# ==============================================================================


class ReplicateError(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)
