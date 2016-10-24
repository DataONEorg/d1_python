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
"""

# Stdlib.
import logging

# Django.
import django.core.management.base
from django.db import transaction
from django.conf import settings

# D1.
import d1_client.cnclient
import d1_client.d1client
import d1_client.mnclient
import d1_common.const
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url

# App.
import mn.auth
import mn.models
import mn.sysmeta_file
import mn.views.view_asserts
import util


class Command(django.core.management.base.BaseCommand):
  help = 'Process the System Metadata refresh queue.'

  def add_arguments(self, parser):
    parser.add_argument(
      '--debug',
      action='store_true',
      default=False,
      help='debug level logging',
    )

  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    logging.info(
      u'Running management command: {}'.format(util.get_command_name())
    )
    util.abort_if_other_instance_is_running()
    util.abort_if_stand_alone_instance()
    p = SysMetaRefresher()
    p.process_refresh_queue()


#===============================================================================


class SysMetaRefresher(object):
  def __init__(self):
    self.cn_client = self._create_cn_client()

  def process_refresh_queue(self):
    queue_queryset = mn.models.SystemMetadataRefreshQueue.objects.exclude(
      status__status='completed'
    )
    if not len(queue_queryset):
      logging.debug('No System Metadata update requests to process')
      return
    for queue_model in queue_queryset:
      self._process_refresh_request(queue_model)
    self._remove_completed_requests_from_queue()

  def _process_refresh_request(self, queue_model):
    logging.info('-' * 79)
    logging.info(u'Processing PID: {}'.format(queue_model.sciobj.pid))
    try:
      self._refresh(queue_model)
    except Exception as e:
      logging.exception(
        u'System Metadata update failed with exception:'
      )
      self._gmn_refresh_queue_model_update(queue_model, str(e))
    return True

  def _refresh(self, queue_model):
    sys_meta = self._get_system_metadata(queue_model)
    with transaction.atomic():
      self._update_sys_meta(sys_meta)
      self._gmn_refresh_queue_model_update(queue_model, 'completed')

  def _gmn_refresh_queue_model_update(self, queue_model, status=None):
    if status is None or status == '':
      status = 'Unknown error. See process_system_metadata_refresh_queue log.'
    queue_model.status = mn.models.sysmeta_refresh_status(status)
    queue_model.save()

  def _remove_completed_requests_from_queue(self):
    q = mn.models.SystemMetadataRefreshQueue.objects.filter(
      status__status='completed'
    )
    q.delete()

  def _create_cn_client(self):
    return d1_client.cnclient.CoordinatingNodeClient(
      base_url=settings.DATAONE_ROOT, cert_path=settings.CLIENT_CERT_PATH,
      key_path=settings.CLIENT_CERT_PRIVATE_KEY_PATH
    )

  def _get_system_metadata(self, queue_model):
    logging.debug(
      u'Calling CNRead.getSystemMetadata(pid={})'.format(queue_model.sciobj.pid)
    )
    return self.cn_client.getSystemMetadata(queue_model.sciobj.pid)

  def _update_sys_meta(self, sys_meta):
    """Updates the System Metadata for an existing Science Object. Does not
    update the replica status on the object.
    """
    pid = sys_meta.identifier.value()

    mn.views.view_asserts.object_exists(pid)

    # No sanity checking is done on the provided System Metadata. It comes
    # from a CN and is implicitly trusted.
    sciobj = mn.models.ScienceObject.objects.get(pid__did=pid)
    sciobj.set_format(sys_meta.formatId)
    sciobj.checksum = sys_meta.checksum.value()
    sciobj.checksum_algorithm = mn.models.checksum_algorithm(
      sys_meta.checksum.algorithm
    )
    sciobj.modified_timestamp = sys_meta.dateSysMetadataModified
    sciobj.size = sys_meta.size
    sciobj.serial_version = sys_meta.serialVersion
    sciobj.is_archived = False
    sciobj.save()

    # If an access policy was provided in the System Metadata, set it.
    if sys_meta.accessPolicy:
      mn.auth.set_access_policy(pid, sys_meta.accessPolicy)
    else:
      mn.auth.set_access_policy(pid)

    mn.sysmeta_file.write_sysmeta_to_file(sys_meta)

    # Log this System Metadata update.
    request = self._make_request_object()
    mn.event_log.update(pid, request)

  def is_existing_pid(self, pid):
    return

  def update_queue_item_status(self, queue_item, status):
    queue_item.status = mn.models.sysmeta_refresh_status(status)
    queue_item.save()

  def delete_completed_queue_items_from_db(self):
    mn.models.SystemMetadataRefreshQueue.objects.filter(
      status__status='completed'
    ).delete()

  def _make_request_object(self):
    class Object(object):
      pass

    o = Object()
    o.META = {
      'REMOTE_ADDR': 'systemMetadataChanged()',
      'HTTP_USER_AGENT': 'N/A',
    }
    return o

# ==============================================================================


class RefreshError(Exception):
  pass
