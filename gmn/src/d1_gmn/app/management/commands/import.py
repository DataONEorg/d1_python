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
"""Bulk Import

Copy from a running MN:

- Science objects
- Permissions
- Subjects
- Event logs

This function can be used for setting up a new instance of GMN to take over
for an existing MN. The import has been tested with other versions of GMN but
should also work with other node stacks.

This command can be run before the new GMN instance has been set up to run as
a web service, so the procedure does not require two web servers to run at the
same time.

The new GMN instance can be installed on the same server as the source MN or on a
different server.

When replacing an older GMN instance by installing a new instance on the same
server, the general procedure is:

- Install the new GMN instance using the regular install procedure, with the
following exceptions:

    - Install the new GMN instance to a different virtualenv by using a
    different virtualenv directory name for the new instance.

    - Skip all Apache related steps.

    - Skip all certificate related steps.

    - Use a separate database for the new instance by modifying the database
    name in settings.py and using the new name when initializing the database.

- Manually copy individual settings from settings.py / settings_site.py of the
old instance to settings.py of the new instance. The new instance will be using
the same settings as the old one, including client side certificate paths and
science object storage root.

- To make sure that all the settings were correctly copied from the old
instance, Generate a Node document in the new instance and compare it with the
version registered in the DataONE environment for the old instance.

    $ manage.py node view

- If a certificate is specified with the `--cert-pub` and (optionally)
`--cert-key` command line switches, GMN will connect to the source MN using that
certificate. Else, GMN will connect using its client side certificate, if one
has been set up via CLIENT_CERT_PATH and CLIENT_CERT_PRIVATE_KEY_PATH in
settings.py. Else, GMN connects to the source MN without using a certificate.

The `--public` switch causes GMN to ignore any available certificates and
connect as the public user. This is useful if the source MN has only public
objects and a certificate that would be accepted by the source MN is not
available.

After the certificate provided by GMN is accepted by the source MN, GMN is
authenticated on the source MN for the subject(s) contained in the certificate.
If no certificate was provided, only objects and APIs that are available to the
public user are accessible

The importer depends on the source MN `listObjects()` API being accessible to
one or more of the authenticated subjects, or to the public subject if no
certificate was provided. Also, for MNs that filter results from
`listObjects()`, only objects that are both returned by `listObjects()` and are
readable by one or more of the authenticated subjects(s) can be imported.

If the source MN is a GMN instance, `PUBLIC_OBJECT_LIST` in its settings.py
controls access to `listObjects()`. For regular authenticated subjects, results
returned by `listObjects()` are filtered to include only objects for which one
or more of the subjects have read or access or better. Subjects that are
whitelisted for create, update and delete access in GMN, and subjects
authenticated as Coordinating Nodes, have unfiltered access to `listObjects()`.
See settings.py for more information.

Member Nodes keep an event log, where operations on objects, such as reads, are
stored together with associated details. After completed object import, the
importer will attempt to import the events for all successfully imported
objects. For event logs, `getLogRecords()` provides functionality equivalent to
what `listObjects` provides for objects, with the same access control related
restrictions.

If the source MN is a GMN instance, `PUBLIC_LOG_RECORDS` in settings.py controls
access to `getLogRecords()` and is equivalent to `PUBLIC_OBJECT_LIST`.

- Start the import. Since the new instance has been set up to use the same
object storage location as the old instance, use the `--no-bytes` switch, which
tells GMN not to copy the object bytes and instead assume that they are already
available in the object storage location.

    $ manage.py import --no-bytes

- Temporarily start the new MN with connect to it and check that all data is
showing as expected.

    $ manage.py runserver

- Stop the source MN by stopping Apache.

- Modify the VirtualHost file for the source MN, e.g.,
`/etc/apache2/sites-available/gmn2-ssl.conf`, to point to the new instance,
e.g., by changing `gmn_venv` to the new virtualenv location.

- Start the new instance by starting Apache.

- From the point of view of the CNs and other nodes in the environment, the node
will not have changed, as it will be serving the same objects as before, so no
further processing or synchronization is required.

If the new instance is set up on a different server, extra steps likely to be
required include:

- Modify the BaseURL in settings.py

- Update the Node registration

    $ manage.py node update


Notes:

- Any replica requests that have been accepted but not yet processed by the
source MN will not be completed. However, requests expire and are automatically
reissued by the CN after a certain amount of time, so this should be handled
gracefully by the system.

- Any changes on the source MN that occur during the import may or may not be
included in the import. To avoid issues such as lost objects, events and system
metadata updates, it may be necessary to restrict access to the source MN during
the transition.
"""

from __future__ import absolute_import

import argparse
import logging
import os

import d1_gmn.app.auth
import d1_gmn.app.delete
import d1_gmn.app.event_log
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.asserts
import d1_gmn.app.views.create
import d1_gmn.app.views.diagnostics
import d1_gmn.app.views.util

import d1_common.revision
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.iter.logrecord
import d1_client.iter.objectlist_multi
import d1_client.iter.sysmeta_multi
import d1_client.mnclient
import d1_client.util

import django.conf
import django.core.management.base

ROOT_PATH = '/var/local/dataone'
REVISION_LIST_PATH = os.path.join(ROOT_PATH, 'import_revision_list.json')
TOPO_LIST_PATH = os.path.join(ROOT_PATH, 'import_topo_list.json')
IMPORTED_LIST_PATH = os.path.join(ROOT_PATH, 'import_imported_list.json')
UNCONNECTED_DICT_PATH = os.path.join(ROOT_PATH, 'import_unconnected.json')

DEFAULT_TIMEOUT_SEC = 3 * 60
DEFAULT_N_WORKERS = 10


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
  def __init__(self, *args, **kwargs):
    super(Command, self).__init__(*args, **kwargs)
    self._db = util.Db()
    self._events = d1_common.util.EventCounter()

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument(
      '--force', action='store_true',
      help='Import even if local database is not empty'
    )
    parser.add_argument(
      '--clear', action='store_true', help='Clear local database'
    )
    parser.add_argument(
      '--cert-pub', dest='cert_pem_path', action='store',
      help='Path to PEM formatted public key of certificate'
    )
    parser.add_argument(
      '--cert-key', dest='cert_key_path', action='store',
      help='Path to PEM formatted private key of certificate'
    )
    parser.add_argument(
      '--public', action='store_true',
      help='Do not use certificate even if available'
    )
    parser.add_argument(
      '--timeout', type=float, action='store', default=DEFAULT_TIMEOUT_SEC,
      help='Timeout for D1 API call to the source MN'
    )
    parser.add_argument(
      '--workers', type=int, action='store', default=DEFAULT_N_WORKERS,
      help='Max number of concurrent connections made to the source MN'
    )
    parser.add_argument('baseurl', help='Source MN BaseURL')

  def handle(self, *args, **opt):
    util.log_setup(opt['debug'])
    logging.info(
      u'Running management command: {}'.format(__name__) # util.get_command_name())
    )
    util.exit_if_other_instance_is_running(__name__)
    self._opt = opt
    self._api_major = d1_client.util.get_api_major_by_base_url(opt['baseurl'])
    try:
      self._handle()
    except d1_common.types.exceptions.DataONEException as e:
      logging.error(str(e))
      raise django.core.management.base.CommandError(str(e))
    self._events.dump_to_log()

  def _handle(self):
    if not self._opt['force'] and not util.is_db_empty():
      raise django.core.management.base.CommandError(
        'There are already objects in the local database. '
        'Use --force to import anyway.'
      )
    if self._opt['clear']:
      d1_gmn.app.delete.delete_all()
      self._events.log_and_count('Cleared database')

    revision_list = self._find_revision_chains()
    # revision_list = d1_common.util.load_json(REVISION_LIST_PATH)
    d1_common.util.save_json(revision_list, REVISION_LIST_PATH)
    self._events.log_and_count(
      'revision_list', 'path="{}"'.format(REVISION_LIST_PATH),
      inc_int=len(revision_list)
    )

    obsoletes_dict = d1_common.revision.revision_list_to_obsoletes_dict(
      revision_list
    )
    topo_list, unconnected_dict = d1_common.revision.topological_sort(
      obsoletes_dict
    )
    d1_common.util.save_json(topo_list, TOPO_LIST_PATH)
    self._events.log_and_count(
      'topo_list', 'path="{}"'.format(TOPO_LIST_PATH), inc_int=len(topo_list)
    )
    d1_common.util.save_json(unconnected_dict, UNCONNECTED_DICT_PATH)
    self._events.log_and_count(
      'unconnected_dict', 'path="{}"'.format(UNCONNECTED_DICT_PATH),
      inc_int=len(unconnected_dict)
    )

    imported_pid_list = self._import_objects(topo_list)
    d1_common.util.save_json(imported_pid_list, IMPORTED_LIST_PATH)
    self._events.log_and_count(
      'imported_pid_list', 'path="{}"'.format(IMPORTED_LIST_PATH),
      inc_int=len(imported_pid_list)
    )
    self._import_logs(imported_pid_list)

  def _find_revision_chains(self):
    sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
      self._opt['baseurl'],
      api_major=self._api_major,
      client_dict=self._get_client_args_dict(),
      list_objects_dict=self._get_list_objects_args_dict(),
      max_workers=self._opt['workers'],
    )
    revision_list = []
    for i, sysmeta_pyxb in enumerate(sysmeta_iter):
      util.log_progress(
        self._events, 'Finding revision chains', i, sysmeta_iter.total,
        d1_common.xml.get_req_val(sysmeta_pyxb.identifier)
      )
      if not d1_common.system_metadata.is_sysmeta_pyxb(sysmeta_pyxb):
        logging.error(d1_common.xml.pretty_pyxb(sysmeta_pyxb))
        continue
      revision_list.append(d1_common.revision.get_identifiers(sysmeta_pyxb))
    return revision_list

  def _import_objects(self, topo_list):
    imported_pid_list = []
    for i, pid in enumerate(topo_list):
      util.log_progress(
        self._events, 'Importing objects', i, len(topo_list), pid
      )
      try:
        self._import_object(pid)
      except d1_common.types.exceptions.DataONEException as e:
        logging.error(d1_common.xml.pretty_pyxb(e))
        continue
      imported_pid_list.append(pid)
    return imported_pid_list

  def _import_object(self, pid):
    if d1_gmn.app.sysmeta.is_did(pid):
      self._events.log_and_count(
        'Skipped object that already exists', 'pid="{}"'.format(pid)
      )
      return
    sysmeta_pyxb = self._get_source_sysmeta(pid)
    self._download_source_sciobj_bytes_to_store(pid)
    d1_gmn.app.views.create.create_native_sciobj(sysmeta_pyxb)

  def _import_logs(self, imported_pid_list):
    client = self._create_source_client()
    log_record_iterator = d1_client.iter.logrecord.LogRecordIterator(
      client,
    )
    imported_pid_set = set(imported_pid_list)
    for i, log_record in enumerate(log_record_iterator):
      pid = d1_common.xml.get_req_val(log_record.identifier)
      util.log_progress(
        self._events, 'Importing event logs', i, log_record_iterator.total, pid
      )
      if pid not in imported_pid_set:
        self._events.log_and_count(
          'Skipped object that was not imported', 'pid="{}"'.format(pid)
        )
        continue
      self._create_log_entry(log_record)

  def _create_log_entry(self, log_record):
    event_log_model = d1_gmn.app.event_log.create_log_entry(
      d1_gmn.app.util.
      get_sci_model(d1_common.xml.get_req_val(log_record.identifier)),
      log_record.event,
      log_record.ipAddress,
      log_record.userAgent,
      log_record.subject.value(),
    )
    event_log_model.timestamp = log_record.dateLogged
    event_log_model.save()

  def _get_source_sysmeta(self, pid):
    client = self._create_source_client()
    return client.getSystemMetadata(pid)

  def _get_source_log(self, pid):
    client = self._create_source_client()
    return client.getgetSystemMetadata(pid)

  def _download_source_sciobj_bytes_to_store(self, pid):
    sciobj_path = d1_gmn.app.util.get_sciobj_file_path(pid)
    d1_common.util.create_missing_directories_for_file(sciobj_path)
    client = self._create_source_client()
    client.get_and_save(pid, sciobj_path)

  def _get_client_args_dict(self):
    client_args_dict = {
      'timeout_sec': self._opt['timeout'],
    }
    if not self._opt['public']:
      client_args_dict.update({
        'cert_pem_path':
          self._opt['cert_pem_path'] or django.conf.settings.CLIENT_CERT_PATH,
        'cert_key_path':
          self._opt['cert_key_path'] or
          django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
      })
    return client_args_dict

  def _get_list_objects_args_dict(self):
    return {
      # Restrict query for faster debugging
      # 'fromDate': datetime.datetime(2017, 1, 1),
      # 'toDate': datetime.datetime(2017, 1, 3),
      # 'start': 83880,
    }

  def _create_source_client(self):
    return d1_client.util.get_client_class_by_version_tag(self._api_major)(
      self._opt['baseurl'], **self._get_client_args_dict()
    )
