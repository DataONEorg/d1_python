# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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
"""Bulk Import.

Copy from a running MN: Science objects, Permissions, Subjects,  Event logs

This function can be used for setting up a new instance of GMN to take over for
an existing MN. The import has been tested with other versions of GMN but should
also work with other node stacks.

See the GMN setup documentation for more information on how to use this command.

"""

import argparse
import logging
import os
import time

import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log
# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.util
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta

import d1_common.const
import d1_common.date_time
import d1_common.system_metadata
import d1_common.type_conversions
import d1_common.types.exceptions
import d1_common.util
import d1_common.utils.filesystem
import d1_common.xml

import d1_client.d1client
import d1_client.iter.logrecord_multi
import d1_client.iter.sysmeta_multi

import django.conf
import django.core.management.base

DEFAULT_TIMEOUT_SEC = 3 * 60
DEFAULT_N_WORKERS = 8
# See notes in sysmeta iterator docstring before changing
MAX_RESULT_QUEUE_SIZE = 100
MAX_TASK_QUEUE_SIZE = 16


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def __init__(self, *args, **kwargs):
        """Args:

        *args:
        **kwargs:

        """
        super().__init__(*args, **kwargs)
        self._db = d1_gmn.app.management.commands.util.util.Db()
        self._events = d1_common.util.EventCounter()

    def add_arguments(self, parser):
        """Args:

        parser:

        """
        parser.description = __doc__
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument("--debug", action="store_true", help="Debug level logging")
        parser.add_argument(
            "--force",
            action="store_true",
            help="Import even if local database is not empty",
        )
        parser.add_argument("--clear", action="store_true", help="Clear local database")
        parser.add_argument(
            "--cert-pub",
            dest="cert_pem_path",
            action="store",
            help="Path to PEM formatted public key of certificate",
        )
        parser.add_argument(
            "--cert-key",
            dest="cert_key_path",
            action="store",
            help="Path to PEM formatted private key of certificate",
        )
        parser.add_argument(
            "--public",
            action="store_true",
            help="Do not use certificate even if available",
        )
        parser.add_argument(
            "--timeout",
            type=float,
            action="store",
            default=DEFAULT_TIMEOUT_SEC,
            help="Timeout for D1 API call to the source MN",
        )
        parser.add_argument(
            "--workers",
            type=int,
            action="store",
            default=DEFAULT_N_WORKERS,
            help="Max number workers making concurrent connections to the source MN",
        )
        parser.add_argument(
            "--object-page-size",
            type=int,
            action="store",
            default=d1_common.const.DEFAULT_SLICE_SIZE,
            help="Number of objects to retrieve in each listObjects() call",
        )
        parser.add_argument(
            "--log-page-size",
            type=int,
            action="store",
            default=d1_common.const.DEFAULT_SLICE_SIZE,
            help="Number of log records to retrieve in each getLogRecords() call",
        )
        parser.add_argument(
            "--major",
            type=int,
            action="store",
            help="Use API major version instead of finding by connecting to CN",
        )
        parser.add_argument(
            "--only-log", action="store_true", help="Only import event logs"
        )
        parser.add_argument(
            "--max-obj",
            type=int,
            action="store",
            help="Limit number of objects to import",
        )
        parser.add_argument("baseurl", help="Source MN BaseURL")

    def handle(self, *args, **opt):
        """Args:

        *args:
        **opt:

        """
        d1_gmn.app.management.commands.util.util.log_setup(opt["debug"])
        logging.info(
            "Running management command: {}".format(
                __name__
            )  # util.get_command_name())
        )
        d1_gmn.app.management.commands.util.util.exit_if_other_instance_is_running(
            __name__
        )
        self._opt = opt
        try:
            # profiler = profile.Profile()
            # profiler.runcall(self._handle)
            # profiler.print_stats()
            self._handle()
        except d1_common.types.exceptions.DataONEException as e:
            logging.error(str(e))
            raise django.core.management.base.CommandError(str(e))
        self._events.dump_to_log()

    def _handle(self):
        if (
            not self._opt["force"]
            and not d1_gmn.app.management.commands.util.util.is_db_empty()
        ):
            raise django.core.management.base.CommandError(
                "There are already objects in the local database. "
                "Use --force to import anyway"
            )
        if self._opt["clear"]:
            if not self._opt["only_log"]:
                self._events.log_and_count("Clearing database")
                d1_gmn.app.delete.delete_all_from_db()
            else:
                self._events.log_and_count("Clearing event log records")
                d1_gmn.app.models.EventLog.objects.all().delete()

        self._api_major = (
            self._opt["major"]
            if self._opt["major"] is not None
            else self._find_api_major()
        )

        if not self._opt["only_log"]:
            self._import_objects()

        self._import_logs()

    def _import_objects(self):
        client = self._create_source_client()

        sysmeta_iter = d1_client.iter.sysmeta_multi.SystemMetadataIteratorMulti(
            base_url=self._opt["baseurl"],
            page_size=self._opt["object_page_size"],
            max_workers=self._opt["workers"],
            max_result_queue_size=MAX_RESULT_QUEUE_SIZE,
            max_task_queue_size=MAX_TASK_QUEUE_SIZE,
            api_major=self._api_major,
            client_dict=self._get_client_dict(),
            list_objects_dict=self._get_list_objects_args_dict(),
        )
        start_sec = time.time()
        for i, sysmeta_pyxb in enumerate(sysmeta_iter):
            if self._opt["max_obj"] is not None and i >= self._opt["max_obj"]:
                self._events.log_and_count(
                    "Limiting import to {} objects (--max-obj)".format(
                        self._opt["max_obj"]
                    )
                )
                break
            if not d1_common.system_metadata.is_sysmeta_pyxb(sysmeta_pyxb):
                if isinstance(
                    sysmeta_pyxb, d1_common.types.exceptions.DataONEException
                ):
                    self._events.log_and_count(
                        "Unable to get SysMeta", 'error="{}"'.format(str(sysmeta_pyxb))
                    )
                    continue
                elif d1_common.type_conversions.is_pyxb(sysmeta_pyxb):
                    self._events.log_and_count(
                        "Unexpected PyXB type instance",
                        'pyxb="{}"'.format(
                            d1_common.xml.serialize_to_xml_str(sysmeta_pyxb)
                        ),
                    )
                    continue

            pid = d1_common.xml.get_req_val(sysmeta_pyxb.identifier)

            self.stdout.write(
                d1_gmn.app.management.commands.util.util.format_progress(
                    self._events,
                    "Importing objects",
                    i,
                    sysmeta_iter.total,
                    pid,
                    start_sec,
                )
            )

            if d1_gmn.app.did.is_existing_object(pid):
                self._events.log_and_count(
                    "Object already exists", 'pid="{}"'.format(pid)
                )
                continue

            sciobj_url = self._get_object_proxy_location(client, pid)

            if sciobj_url:
                self._events.log_and_count(
                    "Skipped download of proxied object bytes",
                    'pid="{}" sciobj_url="{}"'.format(pid, sciobj_url),
                )
            else:
                try:
                    self._download_source_sciobj_bytes_to_store(client, pid)
                except d1_common.types.exceptions.DataONEException as e:
                    self._events.log_and_count(
                        "Unable to get SciObj", 'error="{}"'.format(str(e))
                    )
                    continue
                else:
                    sciobj_url = d1_gmn.app.sciobj_store.get_rel_sciobj_file_url_by_pid(
                        pid
                    )

            d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)

    def _import_logs(self):
        log_record_iterator = d1_client.iter.logrecord_multi.LogRecordIteratorMulti(
            base_url=self._opt["baseurl"],
            page_size=self._opt["log_page_size"],
            max_workers=self._opt["workers"],
            max_result_queue_size=MAX_RESULT_QUEUE_SIZE,
            max_task_queue_size=MAX_TASK_QUEUE_SIZE,
            api_major=self._api_major,
            client_dict=self._get_client_dict(),
        )
        start_sec = time.time()
        for i, log_record_pyxb in enumerate(log_record_iterator):
            if isinstance(log_record_pyxb, d1_common.types.exceptions.DataONEException):
                self._events.log_and_count(
                    "Unable to get SysMeta", 'error="{}"'.format(str(log_record_pyxb))
                )
                continue
            elif not d1_common.type_conversions.is_pyxb(log_record_pyxb):
                self._events.log_and_count(
                    "Unexpected object",
                    'obj="{}"'.format(
                        d1_common.xml.serialize_to_xml_str(log_record_pyxb)
                    ),
                )
                continue

            pid = d1_common.xml.get_req_val(log_record_pyxb.identifier)

            self.stdout.write(
                d1_gmn.app.management.commands.util.util.format_progress(
                    self._events,
                    "Importing event logs",
                    i,
                    log_record_iterator.total,
                    pid,
                    start_sec,
                )
            )

            if not d1_gmn.app.did.is_existing_object(pid):
                self._events.log_and_count(
                    "Skipped object that does not exist", 'pid="{}"'.format(pid)
                )
                continue

            self._create_log_entry(log_record_pyxb)

    def _create_log_entry(self, log_record_pyxb):
        """Args:

        log_record_pyxb:

        """
        event_log_model = d1_gmn.app.event_log.create_log_entry(
            d1_gmn.app.model_util.get_sci_model(
                d1_common.xml.get_req_val(log_record_pyxb.identifier)
            ),
            log_record_pyxb.event,
            log_record_pyxb.ipAddress,
            log_record_pyxb.userAgent,
            log_record_pyxb.subject.value(),
        )
        event_log_model.timestamp = d1_common.date_time.normalize_datetime_to_utc(
            log_record_pyxb.dateLogged
        )
        event_log_model.save()

    def _get_object_proxy_location(self, client, pid):
        """If object is proxied, return the proxy location URL. If object is local,
        return None.

        Args:     client:     pid:

        """
        return client.describe(pid).get("DataONE-Proxy")

    def _download_source_sciobj_bytes_to_store(self, client, pid):
        """Args:

        client: pid:

        """
        abs_sciobj_path = d1_gmn.app.sciobj_store.get_abs_sciobj_file_path_by_pid(pid)
        if os.path.isfile(abs_sciobj_path):
            self._events.log_and_count(
                "Skipped download of existing sciobj bytes",
                'pid="{}" path="{}"'.format(pid, abs_sciobj_path),
            )
        else:
            d1_common.utils.filesystem.create_missing_directories_for_file(
                abs_sciobj_path
            )
            client.get_and_save(pid, abs_sciobj_path)
        return

    def _get_client_dict(self):
        client_dict = {
            "timeout_sec": self._opt["timeout"],
            "verify_tls": False,
            "suppress_verify_warnings": True,
        }
        if not self._opt["public"]:
            client_dict.update(
                {
                    "cert_pem_path": self._opt["cert_pem_path"]
                    or django.conf.settings.CLIENT_CERT_PATH,
                    "cert_key_path": self._opt["cert_key_path"]
                    or django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
                }
            )
        return client_dict

    def _get_list_objects_args_dict(self):
        return {
            # Restrict query for faster debugging
            # 'fromDate': datetime.datetime(2017, 1, 1),
            # 'toDate': datetime.datetime(2017, 1, 3),
        }

    def _create_source_client(self):
        return d1_client.d1client.get_client_class_by_version_tag(self._api_major)(
            self._opt["baseurl"], **self._get_client_dict()
        )

    def _assert_path_is_dir(self, dir_path):
        """Args:

        dir_path:

        """
        if not os.path.isdir(dir_path):
            raise django.core.management.base.CommandError(
                'Invalid dir path. path="{}"'.format(dir_path)
            )

    def _find_api_major(self):
        return d1_client.d1client.get_api_major_by_base_url(
            self._opt["baseurl"], **self._get_client_dict()
        )

    # def _migrate_filesystem(self):
    #   for dir_path, dir_list, file_list in os.walk(V1_OBJ_PATH, topdown=False):
    #     for file_name in file_list:
    #       pid = d1_common.url.decodePathElement(file_name)
    #       old_file_path = os.path.join(dir_path, file_name)
    #       new_file_path = d1_gmn.app.sciobj_store.get_sciobj_file_path(pid)
    #       d1_common.util.create_missing_directories_for_file(new_file_path)
    #       new_dir_path = os.path.dirname(new_file_path)
    #       if self._are_on_same_disk(old_file_path, new_dir_path):
    #         self._events.log_and_count('Creating SciObj hard link')
    #         os.link(old_file_path, new_file_path)
    #       else:
    #         self._events.log_and_count('Copying SciObj file')
    #         shutil.copyfile(old_file_path, new_file_path)
    #
    # def _are_on_same_disk(self, path_1, path_2):
    #   return os.stat(path_1).st_dev == os.stat(path_2).st_dev
    #
    # def _file_path(self, root, pid):
    #   z = zlib.adler32(pid.encode('utf-8'))
    #   a = z & 0xff ^ (z >> 8 & 0xff)
    #   b = z >> 16 & 0xff ^ (z >> 24 & 0xff)
    #   return os.path.join(
    #     root,
    #     u'{0:03d}'.format(a),
    #     u'{0:03d}'.format(b),
    #     d1_common.url.encodePathElement(pid),
    #   )
