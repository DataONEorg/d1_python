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
import asyncio
import contextlib
import logging
import os

import d1_gmn.app.delete
import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.management.commands.async_client
import d1_gmn.app.management.commands.util.standard_args
# noinspection PyProtectedMember
import d1_gmn.app.management.commands.util.util
import d1_gmn.app.model_util
import d1_gmn.app.models
import d1_gmn.app.resource_map
import d1_gmn.app.sciobj_store
import d1_gmn.app.sysmeta

import d1_common.date_time
import d1_common.type_conversions
import d1_common.types.dataoneTypes
import d1_common.types.exceptions
import d1_common.utils.filesystem
import d1_common.utils.progress_logger
import d1_common.xml

import django.conf
import django.core.management.base

# import d1_client.cnclient_2_0
# import d1_client.d1client
# import d1_client.mnclient


# 0 = Timeout disabled

DEFAULT_TIMEOUT_SEC = 0
DEFAULT_WORKER_COUNT = 16
DEFAULT_LIST_COUNT = 1
DEFAULT_PAGE_SIZE = 1000
DEFAULT_API_MAJOR = 2
DEFAULT_MAX_CONCURRENT_TASK_COUNT = 20


# noinspection PyClassHasNoInit,PyAttributeOutsideInit
class Command(django.core.management.base.BaseCommand):
    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        d1_gmn.app.management.commands.util.standard_args.add_arguments(parser, __doc__)
        parser.add_argument(
            "--force",
            action="store_true",
            help="Import even if there are local objects or event logs in DB",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete local objects or event logs from DB",
        )
        parser.add_argument(
            "--type",
            action="store",
            help='Assume source node is a CN ("cn") or MN ("mn") instead of finding '
            "by reading the source Node doc",
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
        parser.add_argument(
            "--pid-path",
            action="store",
            help='Import only the Science Objects specified by a text file. The file must be UTF-8 encoded and contain one PIDs or SIDs per line',
        )
        parser.add_argument("pid", nargs="*", help="")

    def handle(self, *args, **options):
        self.options = options
        d1_gmn.app.management.commands.util.util.log_setup(self.options["debug"])
        self._logger = logging.getLogger(__name__.split(".")[-1])
        self.progress_logger = d1_common.utils.progress_logger.ProgressLogger(
            logger=self._logger
        )
        # Suppress error logging from d1_client
        logging.getLogger("d1_client").setLevel(logging.CRITICAL)
        # if self.options['debug']:
        #   logger = multiprocessing.log_to_stderr()
        #   logger.setLevel(multiprocessing.SUBDEBUG)
        logging.info("Running management command: {}".format(__name__))
        d1_gmn.app.management.commands.util.util.exit_if_other_instance_is_running(
            __name__
        )

        # import logging_tree
        # logging_tree.printout()
        # sys.exit()

        # Python 3.7
        # asyncio.run(self._handle(options))
        # Python 3.6
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._handle())
        except Exception as e:
            self._logger.exception("Import failed with exception")
            raise django.core.management.base.CommandError(str(e))
        finally:
            loop.close()
            self.progress_logger.completed()

    async def _handle(self):
        if (
            not d1_gmn.app.management.commands.util.util.is_db_empty()
            and not self.options["force"]
        ):
            raise django.core.management.base.CommandError(
                "There are already local objects or event logs in the DB. "
                "Use --force to import anyway. "
                "Use --clear to delete local objects and event logs from DB. "
                "Use --only-log with --clear to delete only event logs. "
            )
        if self.options["clear"]:
            if self.options["only_log"]:
                d1_gmn.app.models.EventLog.objects.all().delete()
                self.progress_logger.event("Cleared event logs from DB")
            else:
                d1_gmn.app.delete.delete_all_from_db()
                self.progress_logger.event("Cleared objects and event logs from DB")

        async with self.create_async_client() as async_client:
            node_type, api_major = await self.probe_node_type_major(async_client)

            if not self.options['pid_path']:
                await self.bulk_import(async_client, node_type)
            else:
                await self.restricted_import(async_client, node_type)

    async def bulk_import(self, async_client, node_type):
        if not self.options["only_log"]:
            await self.import_all(
                async_client,
                async_client.list_objects,
                self.get_list_objects_arg_dict(node_type),
                "objectInfo",
                self.import_object,
                "Importing objects",
            )
        await self.import_all(
            async_client,
            async_client.get_log_records,
            self.get_log_records_arg_dict(node_type),
            "logEntry",
            self.import_event,
            "Importing logs",
        )

    async def import_all(
        self,
        client,
        list_func,
        list_arg_dict,
        iterable_attr,
        import_func,
        import_task_name,
    ):
        total_count = (await list_func(count=0, **list_arg_dict)).total

        if not total_count:
            self.progress_logger.event(
                "{}: Aborted: Received empty list from Node".format(import_task_name)
            )
            self._logger.info(
                "{}: Aborted: Received empty list from Node. list_arg_dict={}".format(
                    import_task_name, list_arg_dict
                )
            )
            return

        n_pages = (total_count - 1) // self.options["page_size"] + 1

        slice_task_name = "{}: Retrieved slice".format(import_task_name)
        item_task_name = "{}: Retrieved item".format(import_task_name)

        self.progress_logger.start_task_type(slice_task_name, n_pages)
        self.progress_logger.start_task_type(item_task_name, total_count)

        task_set = set()

        for page_idx in range(n_pages):
            self.progress_logger.start_task(slice_task_name)

            if len(task_set) >= self.options["max_concurrent"]:
                result_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )

            # noinspection PyTypeChecker
            task_set.add(
                self.import_page(
                    client,
                    list_func,
                    list_arg_dict,
                    iterable_attr,
                    import_func,
                    import_task_name,
                    page_idx,
                )
            )

            # Debug
            # if page_idx >= 10:
            #     break

        await asyncio.wait(task_set)

        # except Exception as e:
        #     self._logger.error(
        #         '{}: Retrieved slice failed: page_idx={} n_pages={} error="{}"'.format(
        #             import_task_name, page_idx, n_pages, str(e)
        #         )
        #     )

        self.progress_logger.end_task_type(slice_task_name)
        self.progress_logger.end_task_type(item_task_name)

    async def restricted_import(self, async_client, node_type):
        """Import only the Science Objects specified by a text file.

        The file must be UTF-8 encoded and contain one PIDs or SIDs per line.

        """
        item_task_name = "Importing objects"
        pid_path = self.options['pid_path']

        if not os.path.exists(pid_path):
            raise ConnectionError('File does not exist: {}'.format(pid_path))

        with open(pid_path, encoding='UTF-8') as pid_file:
            self.progress_logger.start_task_type(
                item_task_name, len(pid_file.readlines())
            )
            pid_file.seek(0)

            for pid in pid_file.readlines():
                pid = pid.strip()
                self.progress_logger.start_task(item_task_name)

                # Ignore any blank lines in the file
                if not pid:
                    continue

                await self.import_aggregated(async_client, pid)

        self.progress_logger.end_task_type(item_task_name)

    async def import_aggregated(self, async_client, pid):
        """Import the SciObj at {pid}.

        If the SciObj is a Resource Map, also recursively import the aggregated objects.

        """
        self._logger.info('Importing: {}'.format(pid))

        task_set = set()

        object_info_pyxb = d1_common.types.dataoneTypes.ObjectInfo()
        object_info_pyxb.identifier = pid
        task_set.add(self.import_object(async_client, object_info_pyxb))

        result_set, task_set = await asyncio.wait(task_set)

        assert len(result_set) == 1
        assert not task_set

        sysmeta_pyxb = result_set.pop().result()

        if not sysmeta_pyxb:
            # Import was skipped
            return

        assert d1_common.xml.get_req_val(sysmeta_pyxb.identifier) == pid

        if d1_gmn.app.did.is_resource_map_db(pid):
            for member_pid in d1_gmn.app.resource_map.get_resource_map_members_by_map(
                pid
            ):
                self.progress_logger.event("Importing aggregated SciObj")
                self._logger.info('Importing aggregated SciObj. pid="{}"'.format(pid))
                await self.import_aggregated(async_client, member_pid)

    async def import_page(
        self,
        client,
        list_func,
        list_arg_dict,
        iterable_attr,
        import_func,
        import_task_name,
        page_idx,
    ):
        page_start_idx = page_idx * self.options["page_size"]

        type_pyxb = None
        try:
            type_pyxb = await list_func(
                start=page_start_idx, count=self.options["page_size"], **list_arg_dict
            )
        except Exception as e:
            self.progress_logger.event("{}: Skipped slice".format(import_task_name))
            self._logger.error(
                '{}: Skipped slice. page_idx={} page_start_idx={} page_size={} error="{}"'.format(
                    import_task_name,
                    page_idx,
                    page_start_idx,
                    self.options["page_size"],
                    str(e),
                )
            )

        list_pyxb = getattr(type_pyxb, iterable_attr)
        self.progress_logger.event("{}: Retrieved slice".format(import_task_name))
        self._logger.debug(
            "{}: Retrieved slice: page_idx={} n_items={} page_size={}".format(
                import_task_name, page_idx, len(list_pyxb), self.options["page_size"]
            )
        )

        task_set = set()

        for i, item_pyxb in enumerate(list_pyxb):
            self.progress_logger.start_task(
                "{}: Retrieved item".format(import_task_name)
            )

            if len(task_set) >= self.options["max_concurrent"]:
                result_set, task_set = await asyncio.wait(
                    task_set, return_when=asyncio.FIRST_COMPLETED
                )

            task_set.add(import_func(client, item_pyxb))

            # Debug
            # if i >= 10:
            #     break

        await asyncio.wait(task_set)

        self._logger.debug(
            "{}: Completed page: page_idx={} n_items={}".format(
                import_task_name, page_idx, len(list_pyxb)
            )
        )

    # SciObj

    async def import_object(self, client, object_info_pyxb):
        pid = d1_common.xml.get_req_val(object_info_pyxb.identifier)

        if d1_gmn.app.did.is_existing_object(pid):
            self.progress_logger.event(
                "Skipped object import: Local object already exists"
            )
            self._logger.info(
                'Skipped object import: Local object already exists. pid="{}"'.format(
                    pid
                )
            )
            return

        sciobj_url = await self.get_object_proxy_location(client, pid)

        if sciobj_url:
            self.progress_logger.event("Skipped object download: Proxy object")
            self._logger.info(
                'Skipped object download: Proxy object. pid="{}" sciobj_url="{}"'.format(
                    pid, sciobj_url
                )
            )
        else:
            try:
                await self.download_source_sciobj_bytes_to_store(client, pid)
            except d1_common.types.exceptions.DataONEException as e:
                self.progress_logger.event("Skipped object import: Download failed")
                self._logger.error(
                    'Skipped object import: Download failed. pid="{}" error="{}"'.format(
                        pid, e.friendly_format()
                    )
                )
                return
            sciobj_url = d1_gmn.app.sciobj_store.get_rel_sciobj_file_url_by_pid(pid)

        try:
            sysmeta_pyxb = await client.get_system_metadata(pid)
        except d1_common.types.exceptions.DataONEException as e:
            self.progress_logger.event(
                "Skipped object import: getSystemMetadata() failed"
            )
            self._logger.error(
                'Skipped object import: getSystemMetadata() failed. pid="{}" error="{}"'.format(
                    pid, e.friendly_format()
                )
            ),
            return

        d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, sciobj_url)
        d1_gmn.app.resource_map.create_or_update_db(sysmeta_pyxb)
        self.progress_logger.event("Imported object")
        self._logger.info('Imported object: pid="{}"'.format(pid)),

        return sysmeta_pyxb

    async def get_object_proxy_location(self, client, pid):
        """If object is proxied, return the proxy location URL.

        If object is local, return None.

        """
        try:
            return (await client.describe(pid)).get("DataONE-Proxy")
        except d1_common.types.exceptions.DataONEException:
            # Workaround for older GMNs that return 500 instead of 404 for describe()
            pass

    async def download_source_sciobj_bytes_to_store(self, client, pid):
        # if d1_gmn.app.sciobj_store.is_existing_sciobj_file(pid):
        #     self.progress_logger.event(
        #         "Skipped object bytes download: File already in local object store"
        #     )
        #     self._logger.info(
        #         'Skipped object bytes download: File already in local object store. pid="{}"'.format(
        #             pid
        #         )
        #     )
        #     return

        with d1_gmn.app.sciobj_store.open_sciobj_file_by_pid(pid, write=True) as (
            sciobj_file,
            file_url,
        ):
            await client.get(sciobj_file, pid)

    def get_list_objects_arg_dict(self, node_type):
        """Create a dict of arguments that will be passed to listObjects().

        If {node_type} is a CN, add filtering to include only objects from this GMN
        instance in the ObjectList returned by CNCore.listObjects().

        """
        arg_dict = {
            # Restrict query for faster debugging
            # "fromDate": datetime.datetime(2017, 1, 1),
            # "toDate": datetime.datetime(2017, 1, 10),
        }
        if node_type == "cn":
            arg_dict["nodeId"] = django.conf.settings.NODE_IDENTIFIER
        return arg_dict

    # Event Logs

    async def import_event(self, client_, log_entry_pyxb):
        pid = d1_common.xml.get_req_val(log_entry_pyxb.identifier)

        if not d1_gmn.app.did.is_existing_object(pid):
            self.progress_logger.event("Skipped event log: Local object does not exist")
            self._logger.info(
                'Skipped event log: Local object does not exist. pid="{}"'.format(pid)
            )
            return

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

    def get_log_records_arg_dict(self, node_type):
        """Create a dict of arguments that will be passed to getLogRecords().

        If {node_type} is a CN, add filtering to include only objects from this GMN
        instance in the ObjectList returned by CNCore.listObjects().

        """
        arg_dict = {
            # Restrict query for faster debugging
            # "fromDate": datetime.datetime(2017, 1, 1),
            # "toDate": datetime.datetime(2017, 1, 3),
        }
        if node_type == "cn":
            arg_dict["nodeId"] = django.conf.settings.NODE_IDENTIFIER
        return arg_dict

    # Client

    # def create_source_client(self, api_major, node_type):
    #     if node_type == "cn":
    #         return self.create_async_client()
    #     elif node_type == "mn":
    #         return self.create_async_client()
    #     raise AssertionError(
    #         'node_type must be "mn" or "cn", not "{}"'.format(node_type)
    #     )

    @contextlib.asynccontextmanager
    async def create_async_client(self):
        async with d1_gmn.app.management.commands.async_client.AsyncDataONEClient(
            self.options["baseurl"]
        ) as async_client:
            yield async_client

    def get_client_arg_dict(self):
        client_dict = {"timeout_sec": self.options["timeout"]}
        if self.options["disable_server_cert_validation"]:
            client_dict.update({"verify_tls": False, "suppress_verify_warnings": True})
        if not self.options["public"]:
            client_dict.update(
                {
                    "cert_pem_path": self.options["cert_pem_path"]
                    or django.conf.settings.CLIENT_CERT_PATH,
                    "cert_key_path": self.options["cert_key_path"]
                    or django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
                }
            )
        return client_dict

    async def is_cn(self, client):
        """Return True if node at {base_url} is a CN, False if it is an MN.

        Raise a DataONEException if it's not a functional CN or MN.

        """
        node_pyxb = await client.get_capabilities()
        return d1_common.type_conversions.pyxb_get_type_name(node_pyxb) == "NodeList"

    async def get_node_doc(self, client):
        """If options["baseurl"] is a CN, return the NodeList.

        If it's a MN, return the Node doc.

        """
        return await client.get_capabilities()

    async def probe_node_type_major(self, client):
        """Determine if import source node is a CN or MN and which major version API to
        use."""
        try:
            node_pyxb = await self.get_node_doc(client)
        except d1_common.types.exceptions.DataONEException as e:
            raise django.core.management.base.CommandError(
                "Could not find a functional CN or MN at the provided BaseURL. "
                'base_url="{}" error="{}"'.format(
                    self.options["baseurl"], e.friendly_format()
                )
            )

        is_cn = d1_common.type_conversions.pyxb_get_type_name(node_pyxb) == "NodeList"

        if is_cn:
            self.assert_is_known_node_id(
                node_pyxb, django.conf.settings.NODE_IDENTIFIER
            )
            self._logger.info(
                "Importing from CN: {}. filtered on MN: {}".format(
                    d1_common.xml.get_req_val(
                        self.find_node(node_pyxb, self.options["baseurl"]).identifier
                    ),
                    django.conf.settings.NODE_IDENTIFIER,
                )
            )
            return "cn", "v2"
        else:
            self._logger.info(
                "Importing from MN: {}".format(
                    d1_common.xml.get_req_val(node_pyxb.identifier)
                )
            )
            return "mn", self.find_node_api_version(node_pyxb)

    def find_node(self, node_list_pyxb, base_url):
        """Search NodeList for Node that has {base_url}.

        Return matching Node or None

        """
        for node_pyxb in node_list_pyxb.node:
            if node_pyxb.baseURL == base_url:
                return node_pyxb

    def assert_is_known_node_id(self, node_list_pyxb, node_id):
        """When importing from a CN, ensure that the NodeID which the ObjectList will be
        filtered by is known to the CN."""
        node_pyxb = self.find_node_by_id(node_list_pyxb, node_id)
        assert node_pyxb is not None, (
            "The NodeID of this GMN instance is unknown to the CN at the provided BaseURL. "
            'node_id="{}" base_url="{}"'.format(node_id, self.options["baseurl"])
        )

    def find_node_api_version(self, node_pyxb):
        """Find the highest API major version supported by node."""
        max_major = 0
        for s in node_pyxb.services.service:
            max_major = max(max_major, int(s.version[1:]))
        return max_major

    def find_node_by_id(self, node_list_pyxb, node_id):
        """Search NodeList for Node with {node_id}.

        Return matching Node or None

        """
        for node_pyxb in node_list_pyxb.node:
            # if node_pyxb.baseURL == base_url:
            if d1_common.xml.get_req_val(node_pyxb.identifier) == node_id:
                return node_pyxb
