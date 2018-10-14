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

Copy from a running MN: Science objects, Permissions, Subjects,  Event logs

This function can be used for setting up a new instance of GMN to take over for
an existing MN. The import has been tested with other versions of GMN but should
also work with other node stacks.

See the GMN setup documentation for more information on how to use this command.
"""

import argparse
import logging
import multiprocessing
import os
import time

import d1_gmn.app.auth
import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log
# noinspection PyProtectedMember
import d1_gmn.app.management.commands._util as util
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.node
import d1_gmn.app.revision
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta
import d1_gmn.app.util
import d1_gmn.app.views.assert_db
import d1_gmn.app.views.create
import d1_gmn.app.views.util

import d1_common.const
import d1_common.revision
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_client.cnclient_2_0
import d1_client.d1client
import d1_client.iter.logrecord_multi
import d1_client.iter.objectlist_multi
import d1_client.iter.sysmeta_multi
import d1_client.mnclient

import django.conf
import django.core.management.base
import django.db

# 0 = Timeout disabled

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_WORKER_COUNT = 16
DEFAULT_LIST_COUNT = 1
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
  def _init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def add_arguments(self, parser):
    parser.description = __doc__
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument(
      '--debug', action='store_true', help='Debug level logging'
    )
    parser.add_argument(
      '--force', action='store_true',
      help='Import even if there are local objects or event logs in DB'
    )
    parser.add_argument(
      '--clear', action='store_true',
      help='Delete local objects or event logs from DB'
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
      help='Timeout for DataONE API calls to the source MN'
    )
    parser.add_argument(
      '--workers', type=int, action='store', default=DEFAULT_WORKER_COUNT,
      help='Max number of concurrent API calls to the source MN'
    )
    parser.add_argument(
      '--lists', type=int, action='store', default=DEFAULT_LIST_COUNT,
      help='Max number of concurrent list method API calls to source MN'
    )
    parser.add_argument(
      '--page-size', type=int, action='store', default=DEFAULT_PAGE_SIZE,
      help='Number of objects to retrieve in each list method API call to source MN'
    )
    parser.add_argument(
      '--major', type=int, action='store',
      help='Use API major version instead of finding by connecting to CN'
    )
    parser.add_argument(
      '--only-log', action='store_true', help='Only import event logs'
    )
    parser.add_argument(
      '--max-obj', type=int, action='store',
      help='Limit number of objects to import'
    )
    parser.add_argument('baseurl', help='Source MN BaseURL')

  # noinspection PyUnresolvedReferences
  def handle(self, *args, **options):
    util.log_setup(options['debug'])
    # logging.basicConfig(level=logging.DEBUG)
    # if options['debug']:
    #   logger = multiprocessing.log_to_stderr()
    #   logger.setLevel(multiprocessing.SUBDEBUG)

    logging.info('Running management command: {}'.format(__name__))
    util.exit_if_other_instance_is_running(__name__)
    run_start_sec = time.time()
    event_counter = d1_common.util.EventCounter()

    try:
      # profiler = profile.Profile()
      # profiler.runcall(handle)
      # profiler.print_stats()
      self._handle(options, event_counter)
    except Exception as e:
      logging.error(str(e))
      event_counter.dump_to_log()
      raise django.core.management.base.CommandError(str(e))

    event_counter.dump_to_log()
    total_run_sec = time.time() - run_start_sec
    logging.info(
      'Completed. total_run_sec={:.02f} total_run_dhm="{}"'.
      format(total_run_sec, d1_common.util.format_sec_to_dhm(total_run_sec))
    )

  def _handle(self, options, event_counter):
    if not util.is_db_empty() and not options['force']:
      raise django.core.management.base.CommandError(
        'There are already local objects or event logs in the DB. '
        'Use --force to import anyway. '
        'Use --clear to delete local objects and event logs from DB. '
        'Use --only-log with --clear to delete only event logs. '
      )
    if options['clear']:
      if options['only_log']:
        d1_gmn.app.models.EventLog.objects.all().delete()
        event_counter.log_and_count('Cleared event logs from DB')
      else:
        d1_gmn.app.delete.delete_all_from_db()
        event_counter.log_and_count('Cleared objects and event logs from DB')

    api_major = (
      options['major'] if options['major'] is not None else
      d1_gmn.app.management.commands._util.find_api_major(
        options['baseurl'], get_source_client_arg_dict(options)
      )
    )

    # Functions and PyXB attributes are transferred by name since they can't be
    # serialized and passed across process boundaries.

    if not options['only_log']:
      multiprocessed_import(
        options, event_counter, api_major, 'listObjects',
        get_list_objects_arg_dict(options), 'objectInfo', 'import_object',
        'Importing objects'
      )

    multiprocessed_import(
      options, event_counter, api_major, 'getLogRecords',
      get_log_records_arg_dict(options), 'logEntry', 'import_event',
      'Importing logs'
    )


def multiprocessed_import(
    options, event_counter, api_major, list_method_name, list_arg_dict,
    list_attr, import_method_name, display_str
):
  logging.info('Creating pool of {} workers'.format(options['workers']))
  pool = multiprocessing.Pool(processes=options['workers'])

  manager = multiprocessing.Manager()
  namespace = manager.Namespace()
  namespace.event_counter = event_counter
  namespace.completed_count = 0

  list_method_semaphore = manager.BoundedSemaphore(options['lists'])
  completed_count_lock = manager.Lock()

  client = create_source_client(options, api_major)

  total_count = call_client_method(
    client, list_method_name, count=0, **list_arg_dict
  ).total

  n_pages = (total_count - 1) // options['page_size'] + 1
  start_sec = time.time()

  for page_idx in range(n_pages):
    try:
      logging.debug(
        'apply_async(): page_idx={} n_pages={}'.format(page_idx, n_pages)
      )
      # DEBUG: pool.apply_async() will fail silently on errors
      # in import_page. To debug, run import in the same process by replacing
      # replace pool.apply_async() with a direct call to import_page.
      # import_page(
      #   namespace, options, api_major, list_method_name, list_arg_dict,
      #   list_attr, import_method_name, display_str, total_count, page_idx,
      #   start_sec, list_method_semaphore
      # )
      pool.apply_async(
        import_page,
        args=(
          namespace, options, api_major, list_method_name, list_arg_dict,
          list_attr, import_method_name, display_str, total_count, page_idx,
          start_sec, list_method_semaphore, completed_count_lock
        ),
      )
    except Exception as e:
      logging.error('apply_async() failed. error="{}"'.format(str(e)))
    # The pool does not support a clean way to limit the number of queued tasks
    # so we have to access the internals to check the queue size and wait if
    # necessary.
    # noinspection PyProtectedMember
    while pool._taskqueue.qsize() > 2 * options['workers']:
      logging.debug('Waiting to queue task')
      time.sleep(1)

  pool.close()
  pool.join()


def import_page(
    namespace, options, api_major, list_method_name, list_arg_dict, list_attr,
    import_method_name, display_str, total_count, page_idx, start_sec,
    list_method_semaphore, completed_count_lock
):
  client = create_source_client(options, api_major)
  page_start_idx = page_idx * options['page_size']

  # Cannot use inherited DB connections in this process. Force the process to
  # create new DB connections by closing the current ones.
  django.db.connections.close_all()

  logging.debug('Waiting for list API semaphore')

  # Prevent concurrent listObjects() and getLogRecords() calls to improve
  # performance.
  with list_method_semaphore:
    logging.debug('Acquired list API semaphore')
    call_start_sec = time.time()
    try:
      type_pyxb = call_client_method(
        client, list_method_name, start=page_start_idx,
        count=options['page_size'], **list_arg_dict
      )
    except Exception as e:
      namespace.event_counter.log_and_count(
        'Page skipped: {}() failed',
        'page_idx={} page_start_idx={} page_size={} error="{}"'.format(
          list_method_name, page_idx, page_start_idx, options['page_size'],
          str(e)
        )
      )
      return
    logging.debug(
      '{}() run_sec={:.02f}'.
      format(list_method_name, time.time() - call_start_sec)
    )

  list_pyxb = getattr(type_pyxb, list_attr)
  namespace.event_counter.log_and_count(
    'Retrieved page', 'page_idx={} n_items={} page_size={}'.format(
      page_idx, len(list_pyxb), options['page_size']
    )
  )

  page_iter_start_sec = time.time()

  for item_pyxb in list_pyxb:
    logging.info(
      util.format_progress(
        namespace.event_counter, display_str, namespace.completed_count,
        total_count, d1_common.xml.get_req_val(item_pyxb.identifier), start_sec
      )
    )

    with completed_count_lock:
      namespace.completed_count += 1

    call_import_method(import_method_name, namespace, client, item_pyxb)

  logging.debug(
    'Completed page. page_idx={} n_items={} iter_run_sec={:.02f}'.
    format(page_idx, len(list_pyxb), time.time() - page_iter_start_sec)
  )


def call_import_method(import_method_name, namespace, client, item_pyxb):
  globals()[import_method_name](namespace, client, item_pyxb)


# SciObj


def import_object(namespace, client, object_info_pyxb):
  pid = d1_common.xml.get_req_val(object_info_pyxb.identifier)

  if d1_gmn.app.did.is_existing_object(pid):
    namespace.event_counter.log_and_count(
      'Skipped object create: Local object already exists',
      'pid="{}"'.format(pid)
    )
    return

  sciobj_url = get_object_proxy_location(client, pid)

  if sciobj_url:
    namespace.event_counter.log_and_count(
      'Skipped object download: Proxy object',
      'pid="{}" sciobj_url="{}"'.format(pid, sciobj_url)
    )
  else:
    try:
      download_source_sciobj_bytes_to_store(namespace, client, pid)
    except d1_common.types.exceptions.DataONEException as e:
      namespace.event_counter.log_and_count(
        'Skipped object create: Download failed', 'error="{}"'.format(str(e))
      )
      return
    sciobj_url = d1_gmn.app.sciobj_store.get_rel_sciobj_file_url_by_pid(pid)

  try:
    sysmeta_pyxb = client.getSystemMetadata(pid)
  except d1_common.types.exceptions.DataONEException as e:
    namespace.event_counter.log_and_count(
      'Skipped object create: getSystemMetadata() failed',
      'pid="{}" error="{}"'.format(pid, str(e)),
    )
    return

  d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)


def get_object_proxy_location(client, pid):
  """If object is proxied, return the proxy location URL. If object is local,
  return None.
  """
  return client.describe(pid).get('DataONE-Proxy')


def download_source_sciobj_bytes_to_store(namespace, client, pid):
  abs_sciobj_path = d1_gmn.app.sciobj_store.get_abs_sciobj_file_path_by_pid(pid)
  if os.path.isfile(abs_sciobj_path):
    namespace.event_counter.log_and_count(
      'Skipped object download: Bytes already in local object store',
      'pid="{}" path="{}"'.format(pid, abs_sciobj_path)
    )
    return

  d1_common.util.create_missing_directories_for_file(abs_sciobj_path)
  client.get_and_save(pid, abs_sciobj_path)


def get_list_objects_arg_dict(options):
  return {
    # Restrict query for faster debugging
    # 'fromDate': datetime.datetime(2017, 1, 1),
    # 'toDate': datetime.datetime(2017, 1, 3),
  }


# Event Logs


def import_event(namespace, client, log_entry_pyxb):
  pid = d1_common.xml.get_req_val(log_entry_pyxb.identifier)

  if not d1_gmn.app.did.is_existing_object(pid):
    namespace.event_counter.log_and_count(
      'Skipped event log: Local object does not exist', 'pid="{}"'.format(pid)
    )
    return

  event_log_model = d1_gmn.app.event_log.create_log_entry(
    d1_gmn.app.model_util.get_sci_model(pid), log_entry_pyxb.event,
    log_entry_pyxb.ipAddress, log_entry_pyxb.userAgent,
    log_entry_pyxb.subject.value()
  )
  event_log_model.timestamp = d1_common.date_time.normalize_datetime_to_utc(
    log_entry_pyxb.dateLogged
  )
  event_log_model.save()


def get_log_records_arg_dict(options):
  return {}


# Client


def create_source_client(options, api_major):
  return d1_client.d1client.get_client_class_by_version_tag(api_major)(
    options['baseurl'], **get_source_client_arg_dict(options)
  )


def get_source_client_arg_dict(options):
  client_dict = {
    'timeout_sec': options['timeout'],
    'verify_tls': False,
    'suppress_verify_warnings': True,
  }
  if not options['public']:
    client_dict.update({
      'cert_pem_path':
        options['cert_pem_path'] or django.conf.settings.CLIENT_CERT_PATH,
      'cert_key_path':
        options['cert_key_path'] or
        django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
    })
  return client_dict


def call_client_method(
    client, method_name, *method_arg_list, **method_arg_dict
):
  return getattr(client, method_name)(*method_arg_list, **method_arg_dict)
