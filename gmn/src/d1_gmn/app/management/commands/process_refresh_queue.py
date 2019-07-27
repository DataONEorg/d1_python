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
"""Process queue of System Metadata refresh requests received from Coordinating Nodes.

This command should run periodically, typically via cron. It can also be run manually as
required.

CNs call MNStorage.systemMetadataChanged() to nofify MNs that System Metadata has
changed. GMN stores the requests in a queue. This iterates over the queue, downloads
the updated versions from the CN and replaces the current current local System Metadata.

"""

import d1_common.types
import d1_common.types.exceptions
import d1_common.util
import d1_common.utils.ulog
import d1_common.xml

import d1_client.cnclient_2_0

import django.conf
import django.core.management.base
from django.db import transaction

import d1_gmn.app.did
import d1_gmn.app.event_log
import d1_gmn.app.mgmt_base
import d1_gmn.app.models
import d1_gmn.app.sysmeta


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)
        self.cn_client = None

    def add_components(self, parser):
        self.using_single_instance(parser)

    def handle_serial(self):
        self.cn_client = self.create_cn_client()
        queue_queryset = d1_gmn.app.models.SystemMetadataRefreshQueue.objects.filter(
            status__status="queued"
        ).order_by("timestamp", "sciobj__pid__did")
        if not len(queue_queryset):
            self.log.debug("No System Metadata refresh requests to process")
            return
        for queue_model in queue_queryset:
            self.process_refresh_request(queue_model)
        self.remove_completed_requests_from_queue()

    def process_refresh_request(self, queue_model):
        self.log.info("-" * 100)
        self.log.info("Processing PID: {}".format(queue_model.sciobj.pid.did))
        try:
            self.refresh(queue_model)
        except Exception:
            self.log.exception("System Metadata refresh failed with exception:")
            num_failed_attempts = self.inc_and_get_failed_attempts(queue_model)
            if num_failed_attempts < django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS:
                self.log.warning(
                    "SysMeta refresh failed and will be retried during next processing. "
                    "failed_attempts={}, max_attempts={}".format(
                        num_failed_attempts,
                        django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS,
                    )
                )
            else:
                self.log.warning(
                    "SysMeta refresh failed and has reached the maximum number of "
                    "attempts. Recording the request as permanently failed and "
                    "removing from queue. failed_attempts={}, max_attempts={}".format(
                        num_failed_attempts,
                        django.conf.settings.SYSMETA_REFRESH_MAX_ATTEMPTS,
                    )
                )
                self.update_request_status(queue_model, "failed")
        return True

    def refresh(self, queue_model):
        sysmeta_pyxb = self.get_system_metadata(queue_model)
        pid = queue_model.sciobj.pid.did
        self.assert_is_pid_of_native_object(pid)
        self.assert_pid_matches_request(sysmeta_pyxb, pid)
        with transaction.atomic():
            self.update_sysmeta(sysmeta_pyxb)
            self.update_request_status(queue_model, "completed")
            d1_gmn.app.event_log.create_log_entry(
                queue_model.sciobj, "update", "0.0.0.0", "[refresh]", "[refresh]"
            )

    def update_request_status(self, queue_model, status_str):
        queue_model.status = d1_gmn.app.models.sysmeta_refresh_status(status_str)
        queue_model.save()

    def inc_and_get_failed_attempts(self, queue_model):
        # refresh_queue_model = mn.models.SystemMetadataRefreshQueue.objects.get(
        #   local_replica=queue_model.local_replica
        # )
        queue_model.failed_attempts += 1
        queue_model.save()
        return queue_model.failed_attempts

    def remove_completed_requests_from_queue(self):
        d1_gmn.app.models.SystemMetadataRefreshQueue.objects.filter(
            status__status__in=("completed", "failed")
        ).delete()

    def create_cn_client(self):
        return d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
            base_url=django.conf.settings.DATAONE_ROOT,
            cert_pem_path=django.conf.settings.CLIENT_CERT_PATH,
            cert_key_path=django.conf.settings.CLIENT_CERT_PRIVATE_KEY_PATH,
        )

    def get_system_metadata(self, queue_model):
        self.log.debug(
            "Calling CNRead.getSystemMetadata(pid={})".format(queue_model.sciobj.pid)
        )
        return self.cn_client.getSystemMetadata(queue_model.sciobj.pid.did)

    def update_sysmeta(self, sysmeta_pyxb):
        """Update the System Metadata for an existing Science Object.

        No sanity checking is done on the provided System Metadata. It comes from a CN
        and is implicitly trusted.

        """
        d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb)

    def assert_is_pid_of_native_object(self, pid):
        if not d1_gmn.app.did.is_existing_object(pid):
            raise self.CommandError(
                "Object referenced by PID does not exist or is not valid target for"
                'System Metadata refresh. pid="{}"'.format(pid)
            )

    def assert_pid_matches_request(self, sysmeta_pyxb, pid):
        if d1_common.xml.get_req_val(sysmeta_pyxb.identifier) != pid:
            raise self.CommandError(
                "PID in retrieved System Metadata does not match the object for which "
                'refresh was requested. pid="{}"'.format(pid)
            )

    def assert_sysmeta_is_complete(self, sysmeta_pyxb):
        pass
