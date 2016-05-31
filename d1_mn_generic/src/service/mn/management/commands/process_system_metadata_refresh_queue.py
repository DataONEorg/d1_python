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
"""
:mod:`process_system_metadata_refresh_queue`
============================================

:Synopsis:
  Iterate over queue of objects registered to have their System Metadata
  refreshed and refresh them by pulling the latest version from a CN.
:Created: 2011-11-8
:Author: DataONE (Dahl)
"""

# Stdlib.
import fcntl
import logging
import os
import sys
import tempfile
import urlparse

# Django.
from django.core.management.base import NoArgsCommand
from django.db import transaction

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url

# Add some GMN paths to include path.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../'))
sys.path.append(_here('../types/generated'))
sys.path.append(
  os.path.dirname(
    os.path.dirname(
      os.path.dirname(
        os.path.dirname(
          os.path.abspath(
            __file__
          )
        )
      )
    )
  )
)
sys.path.append('/home/mark/d1/d1_python/d1_certificate_python/src')
# App.
import settings
import mn.models
import mn.view_asserts
import mn.auth
import mn.sysmeta_store


class Command(NoArgsCommand):
  help = 'Process the System Metadata refresh queue.'

  def __init__(self):
    super(Command, self).__init__()
    self.filename = os.path.join(
      tempfile.gettempdir(), os.path.splitext(__file__)[0] + '.single'
    )
    # This will create it if it does not exist already
    self.file_handle = open(self.filename, 'w')
    self.locked = False

  def _acquire(self):
    fcntl.flock(self.file_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)

  def _release(self):
    fcntl.flock(self.file_handle, fcntl.LOCK_UN)
    self.file_handle.close()
    # self.__del__()

  def _get_lock(self):
    try:
      if self.locked:
        return
      self._acquire()
      self.locked = True
    except IOError, e:
      print e
      sys.exit(0)

  def _remove_lock(self):
    try:
      self._release()
      self.locked = False
    except IOError, e:
      print e
      sys.exit(0)

  def _abort_if_stand_alone_instance(self):
    if settings.STAND_ALONE:
      logging.info(
        'Aborted: Stand-alone instance cannot be a replication target. See settings_site.STAND_ALONE.'
      )
      sys.exit(0)

  def handle_noargs(self, **options):

    verbosity = int(options.get('verbosity', 1))
    self._log_setup(verbosity)
    logging.debug('Running management command: process_system_metadata_refresh_queue')
    self._abort_if_stand_alone_instance()
    try:
      self._get_lock()
      p = SysMetaRefresher()
      p.process_refresh_queue()
    finally:
      self._remove_lock()

  def _log_setup(self, verbosity):
    # Set up logging. We output only to stdout. Instead of also writing to a log
    # file, redirect stdout to a log file when the script is executed from cron.
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
    if verbosity >= 1:
      logging.getLogger('').setLevel(logging.DEBUG)
    else:
      logging.getLogger('').setLevel(logging.INFO)

#===============================================================================


class SysMetaRefresher(object):
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.cn_client = self._create_cn_client()

  def process_refresh_queue(self):
    q = mn.models.SystemMetadataRefreshQueue.objects.exclude(status__status='completed')
    if not len(q):
      self.logger.debug('No System Metadata update requests to process')
      return
    for task in q:
      self._process_refresh_task(task)
    self._remove_completed_tasks_from_queue()

  def _process_refresh_task(self, task):
    self.logger.info('-' * 79)
    self.logger.info('Processing PID: {0}'.format(task.object.pid))
    try:
      self._refresh(task)
    except d1_common.types.exceptions.DataONEException as e:
      self.logger.exception('System Metadata update failed with DataONE Exception:')
      self._gmn_refresh_task_update(task, str(e))
    except (RefreshError, Exception, object) as e:
      self.logger.exception('System Metadata update failed with internal exception:')
      self._gmn_refresh_task_update(task, str(e))
    return True

  def _refresh(self, task):
    sys_meta = self._get_system_metadata(task)
    with transaction.atomic():
      self._update_sys_meta(sys_meta)
      self._gmn_refresh_task_update(task, 'completed')

  def _gmn_refresh_task_update(self, task, status=None):
    if status is None or status == '':
      status = 'Unknown error. See process_system_metadata_refresh_queue log.'
    task.set_status(status)
    task.save()

  def _remove_completed_tasks_from_queue(self):
    q = mn.models.SystemMetadataRefreshQueue.objects.filter(status__status='completed')
    q.delete()

  def _create_cn_client(self):
    #return d1_client.mnclient.MemberNodeClient(base_url='http://127.0.0.1:8000')
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=settings.DATAONE_ROOT,
      cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )

  def _get_system_metadata(self, task):
    self.logger.debug('Calling CNRead.getSystemMetadata(pid={0})'.format(task.object.pid))
    return self.cn_client.getSystemMetadata(task.object.pid)

  def _update_sys_meta(self, sys_meta):
    '''Updates the System Metadata for an existing Science Object. Does not
    update the replica status on the object.
    '''
    pid = sys_meta.identifier.value()

    mn.view_asserts.object_exists(pid)

    # No sanity checking is done on the provided System Metadata. It comes
    # from a CN and is implicitly trusted.
    sciobj = mn.models.ScienceObject.objects.get(pid=pid)
    sciobj.set_format(sys_meta.formatId)
    sciobj.checksum = sys_meta.checksum.value()
    sciobj.set_checksum_algorithm(sys_meta.checksum.algorithm)
    sciobj.mtime = sys_meta.dateSysMetadataModified
    sciobj.size = sys_meta.size
    sciobj.serial_version = sys_meta.serialVersion
    sciobj.archived = False
    sciobj.save()

    # If an access policy was provided in the System Metadata, set it.
    if sys_meta.accessPolicy:
      mn.auth.set_access_policy(pid, sys_meta.accessPolicy)
    else:
      mn.auth.set_access_policy(pid)

    mn.sysmeta_store.write_sysmeta_to_store(sys_meta)

    # Log this System Metadata update.
    request = self._make_request_object()
    mn.event_log.update(pid, request)

  def update_queue_item_status(self, queue_item, status):
    queue_item.set_status(status)
    queue_item.save()

  def delete_completed_queue_items_from_db(self):
    mn.models.SystemMetadataRefreshQueue.objects.filter(
      status__status='completed').delete()

  def _make_request_object(self):
    class Object(object):
      pass

    o = Object()
    o.META = {'REMOTE_ADDR': 'systemMetadataChanged()', 'HTTP_USER_AGENT': 'N/A', }
    return o

# ==============================================================================


class RefreshError(Exception):
  def __init__(self, error_msg, pid=None):
    self.error_msg = error_msg
    self.pid = pid

  def __str__(self):
    msg = str(self.error_msg)
    if self.pid is not None:
      msg += '\nIdentifier: {0}'.format(self.pid)
    return msg
