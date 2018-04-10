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
"""Iterate over queue of objects registered to have their System Metadata
refreshed and refresh them by pulling the latest version from a CN.
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter

"""

import argparse
import logging

import d1_gmn.app.auth
import d1_gmn.app.event_log
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.sysmeta

import d1_common.types
import d1_common.util

import d1_client.cnclient

import django.conf
import django.core.management.base
from django.db import transaction


# noinspection PyClassHasNoInit,PyProtectedMember
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._events = d1_common.util.EventCounter()
    self.cn_client = self._create_cn_client()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )

  def handle(self, *args, **opt):
    assert not args
    util.log_setup(opt['debug'])
    logging.info(
      'Running management command: {}'.format(__name__) # util.get_command_name())
    )
    util.exit_if_other_instance_is_running(__name__)
    util.abort_if_stand_alone_instance()
    try:
      self._handle(opt)
    except d1_common.types.exceptions.DataONEException as e:
      raise django.core.management.base.CommandError(str(e))

  def _handle(self, opt):
    queue_queryset = d1_gmn.app.models.SystemMetadataRefreshQueue.objects.filter(
      status__status='queued'
    ).order_by('timestamp', 'sciobj__pid__did')
    if not len(queue_queryset):
      logging.debug('No System Metadata refresh requests to process')
      return
    for queue_model in queue_queryset:
      self._process_refresh_request(queue_model)
    self._remove_completed_requests_from_queue()

  def _process_refresh_request(self, queue_model):
    logging.info('-' * 100)
    logging.info('Processing PID: {}'.format(queue_model.sciobj.pid.did))
    try:
      self._refresh(queue_model)
    except Exception:
      logging.exception('System Metadata refresh failed with exception:')
      num_failed_attempts = self._inc_and_get_failed_attempts(queue_model)
      if num_failed_attempts < django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS:
        logging.warning(
          'SysMeta refresh failed and will be retried during next processing. '
          'failed_attempts={}, max_attempts={}'.format(
            num_failed_attempts,
            django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS
          )
        )
      else:
        logging.warning(
          'SysMeta refresh failed and has reached the maximum number of '
          'attempts. Recording the request as permanently failed and '
          'removing from queue. failed_attempts={}, max_attempts={}'.format(
            num_failed_attempts,
            django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS
          )
        )
        self._update_request_status(queue_model, 'failed')
    return True

  def _refresh(self, queue_model):
    sysmeta_pyxb = self._get_system_metadata(queue_model)
    pid = queue_model.sciobj.pid.did
    self._assert_is_pid_of_native_object(pid)
    self._assert_pid_matches_request(sysmeta_pyxb, pid)
    with transaction.atomic():
      self._update_sysmeta(sysmeta_pyxb)
      self._update_request_status(queue_model, 'completed')
      d1_gmn.app.event_log.create_log_entry(
        queue_model.sciobj, 'update', '0.0.0.0', '[refresh]', '[refresh]'
      )

  def _update_request_status(self, queue_model, status_str):
    queue_model.status = d1_gmn.app.models.sysmeta_refresh_status(status_str)
    queue_model.save()

  def _inc_and_get_failed_attempts(self, queue_model):
    # refresh_queue_model = mn.models.SystemMetadataRefreshQueue.objects.get(
    #   local_replica=queue_model.local_replica
    # )
    queue_model.failed_attempts += 1
    queue_model.save()
    return queue_model.failed_attempts

  def _remove_completed_requests_from_queue(self):
    d1_gmn.app.models.SystemMetadataRefreshQueue.objects.filter(
      status__status__in=('completed', 'failed')
    ).delete()

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=django.conf.settings.DATAONE_ROOT,
      cert_pem_path=django.conf.settings.CLIENT_CERT_PATH,
      cert_key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )

  def _get_system_metadata(self, queue_model):
    logging.debug(
      'Calling CNRead.getSystemMetadata(pid={})'.format(queue_model.sciobj.pid)
    )
    return self.cn_client.getSystemMetadata(queue_model.sciobj.pid.did)

  def _update_sysmeta(self, sysmeta_pyxb):
    """Update the System Metadata for an existing Science Object.

    No sanity checking is done on the provided System Metadata. It comes from a
    CN and is implicitly trusted.
    """
    d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb)

  def _assert_is_pid_of_native_object(self, pid):
    if not d1_gmn.app.did.is_existing_object(pid):
      raise django.core.management.base.CommandError(
        'Object referenced by PID does not exist or is not valid target for'
        'System Metadata refresh. pid="{}"'.format(pid)
      )

  def _assert_pid_matches_request(self, sysmeta_pyxb, pid):
    if d1_common.xml.get_req_val(sysmeta_pyxb.identifier) != pid:
      raise django.core.management.base.CommandError(
        'PID in retrieved System Metadata does not match the object for which '
        'refresh was requested. pid="{}"'.format(pid)
      )

  def _assert_sysmeta_is_complete(self, sysmeta_pyxb):
    pass
