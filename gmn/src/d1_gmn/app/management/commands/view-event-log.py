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

"""View the Event Log for one or more Science Objects.

By default, events are displayed for all objects on this GMN.

The display can be be restricted to a smaller set of objects by providing a path to a
file holding a list of PIDs of objects to check or by passing one or more PIDs directly
on the command line.

The Event Log contains a log of events that have occurred on objects. The event types
are:

    create
    read
    update
    delete
    replicate
    synchronization_failed
    replication_failed

The information logged logged for each event is:

    entryId: A unique identifier for the log entry
    identifier: PID of the Science Object for which the event was logged
    ipAddress: IP address of client that made the request that triggered the event
    userAgent: User-Agent of the client that made the request
    subject: DataONE subject that made the request
    event: Type of event that was logged
    dateLogged: Timestamp indicating when the event was logged
    nodeIdentifier: NodeID of the Node that logged the event

"""
import d1_gmn.app.mgmt_base


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_components(self, parser):
        self.using_single_instance(parser)
        self.using_pid_file(parser)

    def add_arguments(self, parser):
        parser.add_argument(
            "pid",
            action="store",
            nargs="*",
            type=str,
            help="One or more PIDs for which to show Event Logs",
        )

    def handle_serial(self):
        i = 0
        # async for log_pyxb in event_log_iterator.itr():
        #     i += 1
        #     self.log.info(i)
        #     self.log.info(log_pyxb.toxml())
        #
        # await aclient.close()
