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
:mod:`process_system_metadata_dirty_queue`
==========================================

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
import django.utils.log
import django.db.models

# D1.
import d1_common.const
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_client.d1client

# App.
import settings
import mn.models


class Command(NoArgsCommand):
  help = 'Process the System Metadata dirty queue.'

  def handle_noargs(self, **options):
    self.log_setup()

    self.abort_if_other_instance_is_running()

    logging.info('Running management command: ' 'process_system_metadata_dirty_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    self.process_queue()

  def process_queue(self):
    for queue_item in mn.models.SystemMetadataDirtyQueue.objects.filter(
      ~django.db.models.Q(status__status='completed')
    ):
      logging.info('Refreshing System Metadata: {0}'.format(queue_item.object.pid))
      self.process_queue_item(queue_item)

    self.delete_completed_queue_items_from_db()

  def process_queue_item(self, queue_item):
    self.update_queue_item_status(queue_item, 'processing')
    try:
      self.get_sysmeta_from_cn_and_post_to_gmn(queue_item)
    except d1_common.types.exceptions.DataONEException as e:
      logging.error(str(e))
      self.update_queue_item_status(queue_item, 'failed')
    except Exception, e:
      logging.error(str(e))
      self.update_queue_item_status(queue_item, 'failed')
      raise
    else:
      self.update_queue_item_status(queue_item, 'completed')

  def get_sysmeta_from_cn_and_post_to_gmn(self, queue_item):
    pid = queue_item.object.pid
    sysmeta = self.get_sysmeta_from_cn(pid)
    self.generate_mime_multipart_document_and_post_to_gmn(pid, sysmeta)

  def generate_mime_multipart_document_and_post_to_gmn(self, pid, sysmeta):
    sysmeta_xml = sysmeta.toxml()
    files = [('sysmeta', 'sysmeta', sysmeta_xml.encode('utf-8')), ]
    client = d1_client.mnclient.MemberNodeClient(settings.LOCAL_BASE_URL)
    response = client.POST(self.get_internal_update_sysmeta_url(pid), files=files)
    if response.status != 200:
      raise Exception('Bad response: {0}'.format(response.status))
    return response


def update_sysmeta(request, pid):
  '''Updates the System Metadata for an existing Science Object. Does not
  update the replica status on the object.
  '''
  mn.view_asserts.object_exists(pid)

  # Check that a valid MIME multipart document has been provided and that it
  # contains the required System Metadata section.
  mn.view_asserts.post_has_mime_parts(request, (('file', 'sysmeta'), ))
  mn.view_asserts.xml_document_not_too_large(request.FILES['sysmeta'])

  # Deserialize metadata (implicit validation).
  sysmeta_xml = request.FILES['sysmeta'].read().decode('utf-8')
  sysmeta = dataoneTypes.CreateFromDocument(sysmeta_xml)

  # No sanity checking is done on the provided System Metadata. It comes
  # from a CN and is implicitly trusted.
  sciobj = mn.models.ScienceObject.objects.get(pid=pid)
  sciobj.set_format(sysmeta.formatId)
  sciobj.checksum = sysmeta.checksum.value()
  sciobj.set_checksum_algorithm(sysmeta.checksum.algorithm)
  sciobj.mtime = d1_common.date_time.is_utc(sysmeta.dateSysMetadataModified)
  sciobj.size = sysmeta.size
  sciobj.serial_version = sysmeta.serialVersion
  sciobj.archived = False
  sciobj.save()

  # If an access policy was provided in the System Metadata, set it.
  if sysmeta.accessPolicy:
    mn.auth.set_access_policy(pid, sysmeta.accessPolicy)
  else:
    mn.auth.set_access_policy(pid)

  sysmeta.write_sysmeta_to_store(sysmeta)

  # Log this System Metadata update.
  mn.event_log.update(pid, request)

  return mn.view_shared.http_response_with_boolean_true_type()

  def get_sysmeta_from_cn(self, pid):
    client = d1_client.d1client.DataONEClient(settings.DATAONE_ROOT)
    sysmeta = client.getSystemMetadata(pid)
    return sysmeta

  def update_queue_item_status(self, queue_item, status):
    queue_item.set_status(status)
    queue_item.save()

  def delete_completed_queue_items_from_db(self):
    mn.models.SystemMetadataDirtyQueue.objects.filter(status__status='completed').delete()

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
