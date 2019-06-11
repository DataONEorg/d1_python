#!/usr/bin/env python

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
"""Create database fixture JSON file.

This creates the db entries for a set of test objects by calling the GMN D1
APIs, then uses Django to dump the database to JSON.

Objects are randomly distributed between categories:
  - Standalone, no SID
  - Standalone, SID
  - Chain, no SID
  - Chain, SID

Though object bytes are also created, they are not captured in the db fixture.
See the README.md for more info on the fixtures.
"""
# The Django init needs to occur before the django and gmn_test_case imports, so we're
# stuck with a bit of a messy import section that isort and flake8 don't like.
# isort:skip_file

import datetime
import io
import logging
import random
import sys

import freezegun
import responses

import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_gmn.app.sysmeta_extract

import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.sciobj
import d1_test.instance_generator.user_agent
import d1_test.mock_api.django_client
import d1_test.test_files

import d1_client.mnclient_2_0

N_OBJECTS = 1000
N_READ_EVENTS = 2 * N_OBJECTS


@responses.activate
def main():
    d1_test.mock_api.django_client.add_callback(
        d1_gmn.tests.gmn_test_case.MOCK_GMN_BASE_URL
    )

    db_name = d1_gmn.tests.gmn_test_case.django_get_db_name_by_key()
    d1_gmn.tests.gmn_test_case.postgres_drop_if_exists(db_name)
    d1_gmn.tests.gmn_test_case.postgres_create_blank(db_name)
    d1_gmn.tests.gmn_test_case.django_migrate()
    d1_gmn.tests.gmn_test_case.django_commit_and_close()

    client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
        d1_gmn.tests.gmn_test_case.MOCK_GMN_BASE_URL
    )

    # We control the timestamps of newly created objects directly and use
    # freeze_time to control the timestamps that GMN sets on updated objects
    # and events.
    with freezegun.freeze_time("2001-02-03") as freeze_time:
        with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
            create_objects(client, freeze_time)
            create_read_events(client, freeze_time)

    d1_gmn.tests.gmn_test_case.django_save_db_fixture()
    save_pid_list_sample()


def create_objects(client, freeze_time):
    head_pid_set = set()
    with d1_gmn.tests.gmn_mock.disable_auth():
        for i in range(N_OBJECTS):
            logging.info("-" * 100)
            logging.info("Creating sciobj: {} / {}".format(i + 1, N_OBJECTS))

            freeze_time.tick(delta=datetime.timedelta(days=1))

            do_chain = random.random() < 0.5

            pid = d1_test.instance_generator.identifier.generate_pid("PID_GMNFXT_")
            pid, sid, sciobj_bytes, sysmeta_pyxb = d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
                client, pid
            )
            sciobj_file = io.BytesIO(sciobj_bytes)

            if not do_chain:
                client.create(pid, sciobj_file, sysmeta_pyxb)
            else:
                if len(head_pid_set) < 20:
                    client.create(pid, sciobj_file, sysmeta_pyxb)
                    head_pid_set.add(pid)
                else:
                    sysmeta_pyxb.seriesId = None
                    old_pid = random.choice(list(head_pid_set))
                    head_pid_set.remove(old_pid)
                    client.update(old_pid, sciobj_file, pid, sysmeta_pyxb)


def create_read_events(client, freeze_time):
    with d1_gmn.tests.gmn_mock.disable_auth():
        pid_list = [
            o.identifier.value() for o in client.listObjects(count=N_OBJECTS).objectInfo
        ]
    for i in range(N_READ_EVENTS):
        logging.info("-" * 100)
        logging.info("Creating read event: {} / {}".format(i + 1, N_READ_EVENTS))

        freeze_time.tick(delta=datetime.timedelta(days=1))

        read_subj = (
            d1_test.instance_generator.random_data.random_regular_or_symbolic_subj()
        )
        with d1_gmn.tests.gmn_mock.set_auth_context(
            active_subj_list=[read_subj],
            trusted_subj_list=[read_subj],
            whitelisted_subj_list=None,
            do_disable_auth=False,
        ):
            client.get(
                random.choice(pid_list),
                vendorSpecific={
                    "User-Agent": d1_test.instance_generator.user_agent.generate()
                },
            )


def save_pid_list_sample():
    """Get list of all PIDs in the DB fixture.

    These are for use in any tests that need to know which PIDs and SIDs are available
    in the DB.

    """
    for did in ["pid", "sid"]:
        with open(
            d1_test.test_files.get_abs_test_file_path(
                "json/db_fixture_{}.json".format(did)
            ),
            "w",
            encoding="utf-8",
        ) as f:
            d1_gmn.app.sysmeta_extract.extract_values(field_list=[did], out_stream=f)


if __name__ == "__main__":
    sys.exit(main())
