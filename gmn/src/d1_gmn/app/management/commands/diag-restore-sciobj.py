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

"""Attempt to restore missing local Science Objects from replicas.

A DataONE Science Object is a block of bytes with an associated System Metadata XML
doc.
GMN stores the bytes in a directory hierarchy on the local filesystem and the System
Metadata in a Postgres database.

This will attempt to restore objects that have been lost or damaged due to data
corruption or loss in the filesystem or database.

This procedure should be able to always restore system metadata. However, restore of
object bytes depends on a valid replica being available on the CN or another MN.

The procedure is as follows:

- For the purposes of this command, "damaged" and "lost" data are equivalents. Both are
  handled with the same software procedure, where an attempt is made to completely
  replace the data with a recovered version. So this documentation uses "lost" to
  describe both lost and damaged data.

- The CN is queried for a list of PIDs of objects for which this GMN is registered as
  either the authoritative source, or holder of a replica.

- For each PID, both the System Metadata and the object bytes are checked to be
  available and undamaged on this GMN.

  - System Metadata is checked by fully generating the System Metadata document from
    the database, then validating it against the XMLSchema for the DataONE types. The
    System metadata is considered to be lost if any step of the procedure cannot be
    completed.

  - Object bytes are checked by recalculating the checksum from the currently stored
    bytes (if any) and comparing it with the correct checksum, stored in the System
    Metadata. The object is considered to be lost if unable to generate a checksum or
    if the checksum does not match the checksum stored for the object.

- Proxy objects are checked in the same way, except that the checksum is recalculated
  on the object bytes as streamed from its location on the 3rd party server.

- Lost System Metadata is always restored from the CN, which holds a copy of system
  metadata for all objects that are known to the CN, which will include the objects for
  which the CN returned the PIDs in the initial query that this procedure performed.

- For lost object bytes, the restore process depends on the type of storage used for
  the object bytes, which is either local filesystem or proxy from 3rd party server.

- The bytes for objects stored in the filesystem, which is the most common situation,
  are restored by querying the CN for a list of known locations for the object. If this
  GMN, where the object bytes are known to be lost, is the only available location
  listed, the object bytes cannot be restored by this command. If the object bytes are
  not available elsewhere, the object will have to be considered as lost by DataONE. It
  should be set as archived in the CN system metadata, so that it is not listed in any
  further search results. To help prevent this from happening, make sure that all
  objects on this GMN have a replication policy allowing replicas to be distributed to
  other MNs in the DataONE federation.

- Proxy objects are objects where the bytes are stored on a 3rd party server instead of
  on the local filesystem, and GMN stores only a URL reference to the location. Support
  for proxy objects is a vendor specific GMN feature, so the URL is not part of the
  official system metadata. As the URL is stored together with the system metadata in
  the database, lost system metadata will mean lost object reference URL as well. Since
  the URL is not in the system metadata, restoring the system metadata from the CN will
  not restore the URL and so will not recover the actual location.

- Since object bytes for proxy objects are not stored locally, lost object bytes will
  either have been caused by lost URL reference, which is handled as described above,
  or by the 3rd party server no longer returning the object bytes at the URL reference
  location. In both cases,the only remaining option for a fully automated restore of
  the object depends on a valid replica being available on the CN or another MN, in
  which case GMN can restore the object as a regular local object from the replica.
  However, this converts the object from a proxy object to a local object. Depending on
  the available hardware vs. the added storage space that will be required, this may
  not be desirable, so the option to convert proxy objects to local if required for
  automated restore is disabled by default. See --help for how to set this option.

- See the documentation for ``audit-proxy-sciobj`` for information on how to repair
  proxy objects that could not be restored automatically by this command.

"""

import d1_gmn.app.did
import d1_gmn.app.mgmt_base
import d1_gmn.app.sysmeta


class Command(d1_gmn.app.mgmt_base.GMNCommandBase):
    def __init__(self, *args, **kwargs):
        super().__init__(__doc__, __name__, *args, **kwargs)

    def add_components(self, parser):
        self.using_single_instance(parser)

    def handle_serial(self):
        pass

    # async def fix(self, async_client, url):
    #     self.log.info("Processing: {}".format(url))
    #     proxy_tracker = self.tracker("Create missing proxy objects")
    #
    #     sysmeta_pyxb = await async_client.get_system_metadata(url)
    #
    #     sysmeta_checksum_pyxb = sysmeta_pyxb.checksum
    #     # print(d1_common.checksum.format_checksum(calculated_checksum_pyxb))
    #     calculated_checksum_pyxb = await self.calculate_checksum(
    #         async_client, url, sysmeta_checksum_pyxb.algorithm
    #     )
    #     # print(d1_common.checksum.format_checksum(sysmeta_checksum_pyxb))
    #     if not d1_common.checksum.are_checksums_equal(
    #         sysmeta_checksum_pyxb, calculated_checksum_pyxb
    #     ):
    #         proxy_tracker.event(
    #             "Skipped: Checksum mismatch", f'url="{url}"', is_error=True
    #         )
    #
    #     d1_gmn.app.sysmeta.create_or_update(sysmeta_pyxb, url)
    #
    #     proxy_tracker.event("Fixed", f'url="{url}"')
    #
    # async def is_online(self, async_client, url):
    #     try:
    #         async with await async_client.session.head(url) as response:
    #             # Handle redirect responses as well, as redirects are not followed for
    #             # HEAD requests.
    #             return response.status in (200, 300, 301, 302, 303, 307, 308)
    #     except aiohttp.ClientError:
    #         return False
    #
    # async def calculate_checksum(self, async_client: t.D1Client, url: str, checksum_algo: str) -> t.Checksum:
    #     """Calculate the checksum on proxy object stored on a 3rd party server.
    #
    #     The objected is calculated on the stream, without bytes being buffered in memory
    #     or stored locally.
    #
    #     Returns:
    #         A DataONE Checksum PyXB type.
    #
    #     """
    #     checksum_calculator = d1_common.checksum.get_checksum_calculator_by_dataone_designator(
    #         checksum_algo
    #     )
    #     async with await async_client.session.get(url) as response:
    #         async for chunk_str, _ in response.content.iter_chunks():
    #             checksum_calculator.update(chunk_str)
    #
    #     checksum_pyxb = d1_common.types.dataoneTypes.checksum(
    #         checksum_calculator.hexdigest()
    #     )
    #     checksum_pyxb.algorithm = checksum_algo
    #     return checksum_pyxb
