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
"""Make an exact copy of all Science Objects, Permissions, Subjects and Event logs
available on another Member Node.

This function can be used for setting up a new instance of GMN to take over for an
existing MN. The import has been tested with other versions of GMN but should also work
with other node stacks.

See :doc:`/d1_gmn/setup/migrate` for more about how to migrate to GMN 3.x.

The importer depends on the source MN ``listObjects()`` API being accessible to one or
more of the authenticated subjects, or to the public subject if no certificate was
provided. Also, for MNs that filter results from ``listObjects()``, only objects that
are both returned by ``listObjects()`` and are readable by one or more of the
authenticated subjects(s) can be imported.

If the source MN is a GMN instance, ``PUBLIC_OBJECT_LIST`` in its settings.py controls
access to ``listObjects()``. For regular authenticated subjects, results returned by
``listObjects()`` are filtered to include only objects for which one or more of the
subjects have read or access or better. Subjects that are whitelisted for create, update
and delete access in GMN, and subjects authenticated as Coordinating Nodes, have
unfiltered access to ``listObjects()``. See settings.py for more information.

Member Nodes keep an event log, where operations on objects, such as reads, are stored
together with associated details. After completed object import, the importer will
attempt to import the events for all successfully imported objects. For event logs,
``MNRead.getLogRecords()`` provides functionality equivalent to what ``listObjects``
provides for objects, with the same access control related restrictions.

If the source MN is a GMN instance, ``PUBLIC_LOG_RECORDS`` in settings.py controls
access to ``getLogRecords()`` and is equivalent to ``PUBLIC_OBJECT_LIST``.

If a certificate is specified with the ``--cert-pub`` and (optionally) ``--cert-key``
command line switches, GMN will connect to the source MN using that certificate. Else,
GMN will connect using its client side certificate, if one has been set up via
CLIENT_CERT_PATH and CLIENT_CERT_PRIVATE_KEY_PATH in settings.py. Else, GMN connects to
the source MN without using a certificate.

After the certificate provided by GMN is accepted by the source MN, GMN is authenticated
on the source MN for the subject(s) contained in the certificate. If no certificate was
provided, only objects and APIs that are available to the public user are accessible.
"""
import asyncio
import logging

import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.utils.filesystem
import d1_common.utils.progress_tracker
import d1_common.utils.ulog
import d1_common.xml

import django.conf
import django.core.management.base
import django.db.transaction

import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.mgmt_base
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.resource_map
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.list_arg_dict = None
        self.log_records_arg_dict = None
        self.sciobj_tracker = None
        self.event_tracker = None

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_force_for_production(parser)
        self.using_pid_file(parser)
        self.using_async_d1_client(parser, default_timeout_sec=0)
        self.using_async_object_list_iter(
            parser, default_timeout_sec=0
        )  # , **self.get_list_objects_arg_dict())
        self.using_async_event_log_iter(
            parser, default_timeout_sec=0
        )  # , **self.get_log_records_arg_dict())

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete local objects or Event Logs from DB",
        )
        parser.add_argument(
            "--node-type",
            type=str,
            action="store",
            default="mn",
            choices=["mn", "cn"],
            help='Assume source node is a CN ("cn") or MN ("mn") instead of finding '
            "by reading the source Node doc",
        )
        parser.add_argument(
            "--only-log", action="store_true", help="Only import Event Logs"
        )
        parser.add_argument(
            "--max-obj",
            type=int,
            action="store",
            help="Limit number of objects to import",
        )
        parser.add_argument(
            "--deep",
            action="store_true",
            help="Recursively import all nested objects in Resource Maps",
        )

    async def handle_async(self):
        # Suppress debug output from async_client
        logging.getLogger("d1_client.aio.async_client").setLevel(logging.ERROR)

        if not self.is_db_empty() and not self.opt_dict["force"]:
            raise django.core.management.base.CommandError(
                "There are already local objects or Event Logs in the DB. "
                "Use --force to import anyway. "
                "Use --clear to delete local objects and Event Logs from DB. "
                "Use --only-log with --clear to delete only Event Logs. "
            )
        if self.opt_dict["clear"]:
            if self.opt_dict["only_log"]:
                d1_gmn.app.models.EventLog.objects.all().delete()
                self.log.info("Cleared Event Logs from DB")
            else:
                d1_gmn.app.delete.delete_all_from_db()
                self.log.info("Cleared objects and Event Logs from DB")

        if not self.opt_dict["only_log"]:
            if self.opt_dict["pid_path"]:
                await self.sciobj_import_by_pid_list()
            else:
                await self.sciobj_import_all()
            await self.await_all()
            self.sciobj_tracker.completed()

        await self.event_import_all()
        await self.await_all()
        self.event_tracker.completed()

    # SciObj

    async def sciobj_import_all(self):
        """Import all SciObj on remote MN."""
        self.log.info("Starting SciObj import")
        total_count = await self.async_object_list_iter.total
        self.log.info("Number of SciObj to import: {}".format(total_count))
        self.sciobj_tracker = self.tracker.tracker("Importing SciObj", total_count)
        async for object_info_pyxb in self.async_object_list_iter:
            pid = object_info_pyxb.identifier.value()
            await self.add_task(self.sciobj_import_pid(pid))

    async def sciobj_import_by_pid_list(self):
        """Import SciObj specified by PID list file."""
        self.log.info("Starting SciObj import from PID file")
        pid_list = self.load_set_from_file(self.opt_dict["pid_path"])
        total_count = len(pid_list)
        self.log.info("Number of SciObj to import: {}".format(total_count))
        if not total_count:
            self.log.error("Aborted: Loaded empty list from file")
            return
        self.sciobj_tracker = self.tracker.tracker(
            "Importing SciObj by PID list file", total_count
        )
        for pid in pid_list:
            await self.add_task(self.sciobj_import_pid(pid))

    async def sciobj_import_pid(self, pid):
        """Import SciObj SysMeta and bytes"""
        self.log.debug("Starting import of SciObj: {}".format(pid))
        self.sciobj_tracker.step()
        if d1_gmn.app.did.is_existing_object(pid):
            self.sciobj_tracker.event(
                "Skipped object import: Local object already exists",
                'pid="{}"'.format(pid),
            )
            return

        with django.db.transaction.atomic():
            await self.sciobj_download_and_create(pid)

        if self.opt_dict["deep"]:
            if d1_gmn.app.did.is_resource_map_db(pid):
                for (
                    member_pid
                ) in d1_gmn.app.resource_map.get_resource_map_members_by_map(pid):
                    await self.sciobj_import_pid(member_pid)
                    self.sciobj_tracker.event(
                        "Imported aggregated SciObj", 'pid="{}"'.format(pid)
                    )

    async def sciobj_download_and_create(self, pid):
        try:
            sysmeta_pyxb = await self.async_d1_client.get_system_metadata(pid)
        except d1_common.types.exceptions.DataONEException as e:
            self.sciobj_tracker.event(
                "Import failed: MNRead.getSystemMetadata() returned error",
                'pid="{}" error="{}"'.format(pid, e.friendly_format()),
                is_error=True,
            )
            return

        sciobj_url = await self.sciobj_get_proxy_location(pid)
        if sciobj_url:
            self.sciobj_tracker.event(
                "Skipped object download: Proxy object",
                'pid="{}" sciobj_url="{}"'.format(pid, sciobj_url),
            )
        else:
            try:
                await self.sciobj_download_bytes_to_store(pid)
            except d1_common.types.exceptions.DataONEException as e:
                self.sciobj_tracker.event(
                    "SciObj import failed: MNRead.get() returned error",
                    'pid="{}" error="{}"'.format(pid, e.friendly_format()),
                    is_error=True,
                )
                return
            sciobj_url = d1_gmn.app.sciobj_store.get_rel_sciobj_file_url_by_pid(pid)

        d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)

        if d1_gmn.app.resource_map.is_resource_map_sysmeta_pyxb(sysmeta_pyxb):
            d1_gmn.app.resource_map.create_or_update_db(sysmeta_pyxb)
            self.sciobj_tracker.event("Processed Resource Map", 'pid="{}"'.format(pid))

        self.sciobj_tracker.event("Imported SciObj", 'pid="{}"'.format(pid))

    async def sciobj_get_proxy_location(self, pid):
        """If object is a proxy, return the proxy location URL.

        If object is local, return None.

        """
        try:
            return (await self.async_d1_client.describe(pid)).get("DataONE-Proxy")
        except d1_common.types.exceptions.DataONEException:
            # Workaround for older GMNs that return 500 instead of 404 for describe()
            pass

    async def sciobj_download_bytes_to_store(self, pid):
        if d1_gmn.app.sciobj_store.is_existing_sciobj_file(pid):
            self.sciobj_tracker.event(
                "Skipped object bytes download: File already in local SciObj store",
                'pid="{}"'.format(pid),
            )
            return

        with d1_gmn.app.sciobj_store.open_sciobj_file_by_pid_ctx(
            pid, write=True
        ) as sciobj_file:
            await self.async_d1_client.get(sciobj_file, pid)

    def get_list_objects_arg_dict(self):
        """Create a dict of arguments that will be passed to listObjects().

        If {node_type} is a CN, add filtering to include only objects from this GMN
        instance in the ObjectList returned by CNCore.listObjects().
        """
        arg_dict = {
            # Restrict query for faster debugging
            # "fromDate": datetime.datetime(2017, 1, 1),
            # "toDate": datetime.datetime(2017, 1, 10),
        }
        if self.opt_dict["node_type"] == "cn":
            arg_dict["nodeId"] = django.conf.settings.NODE_IDENTIFIER
        self.log.debug("listObjects args: {}".format(arg_dict))
        return arg_dict

    # Event Logs

    async def event_import_all(self):
        """Import all events on remote MN."""
        self.log.info("Starting Event Log import")
        total_count = await self.async_event_log_iter.total
        self.log.info("Number of events to import: {}".format(total_count))
        self.event_tracker = self.tracker.tracker("Importing Event Logs", total_count)
        async for log_entry_pyxb in self.async_event_log_iter:
            await self.add_task(self.event_import_entry(log_entry_pyxb))

    async def event_import_entry(self, log_entry_pyxb):
        self.event_tracker.step()
        pid = d1_common.xml.get_req_val(log_entry_pyxb.identifier)
        if not d1_gmn.app.did.is_existing_object(pid):
            self.event_tracker.event(
                "Skipped Event Log: Local object does not exist", 'pid="{}"'.format(pid)
            )
            return

        with django.db.transaction.atomic():

            event_log_model = d1_gmn.app.event_log.create_log_entry(
                d1_gmn.app.model_util.get_sci_model(pid),
                log_entry_pyxb.event,
                log_entry_pyxb.ipAddress,
                log_entry_pyxb.userAgent,
                log_entry_pyxb.subject.value(),
            )
            event_log_model.timestamp = d1_common.date_time.normalize_datetime_to_utc(
                log_entry_pyxb.dateLogged
            )
            event_log_model.save()

        self.event_tracker.event("Imported Event", 'pid="{}"'.format(pid))

    def get_log_records_arg_dict(self):
        """Create a dict of arguments that will be passed to getLogRecords().

        If {node_type} is a CN, add filtering to include only objects from this GMN
        instance in the ObjectList returned by CNCore.listObjects().

        """
        arg_dict = {
            # Restrict query for faster debugging
            # "fromDate": datetime.datetime(2017, 1, 1),
            # "toDate": datetime.datetime(2017, 1, 3),
        }
        if self.opt_dict["node_type"] == "cn":
            arg_dict["nodeId"] = django.conf.settings.NODE_IDENTIFIER
        self.log.debug("getLogRecords args: {}".format(arg_dict))
        return arg_dict
