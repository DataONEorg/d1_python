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

"""Get the location of the raw bytes for a Science Object.

For locally stored objects, the location will be a path into GMN's local filesystem
store hierarchy.

For proxy objects, the location will be a HTTP or HTTPS URL to a 3rd party server.
Note that the URL may be lead to nested redirects that must be followed to the final
location of the object.

"""
import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.model_util


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "identifier", help="PID or SID of a Science Object on this GMN"
        )

    def handle_serial(self):
        did = self.opt_dict["identifier"]

        if d1_gmn.app.did.is_sid(did):
            pid = d1_gmn.app.did.resolve_sid_v2(did)
            '"{}" is a SID referencing PID "{}"'.format(did, pid)
            did = pid
        if not d1_gmn.app.did.is_did(did):
            self.log.info('PID "{}" is unknown on this GMN'.format(did))
            return
        self.log.info(
            'Identifier "{}" is {}'.format(did, d1_gmn.app.did.classify_identifier(did))
        )
        if d1_gmn.app.did.is_existing_object(did):
            sciobj_model = d1_gmn.app.model_util.get_sci_model(did)
            self.log.info(
                "The bytes are stored at: {}".format(did, sciobj_model.pid.did)
            )
        else:
            self.log.info("SciObj is not yet tracked by this GMN")
