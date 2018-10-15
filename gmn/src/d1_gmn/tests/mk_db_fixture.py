#!/usr/bin/env python
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
"""Create database fixture JSON file

This creates the db entries for a set of test objects by calling the GMN D1
APIs, then uses Django to dump the database to JSON.

Objects are randomly distributed between categories:
  - Standalone, no SID
  - Standalone, SID
  - Chain, no SID
  - Chain, SID

Though object bytes are also created, they are not captured in the db fixture.
See the README.md for more info on the fixtures.

The Django init needs to occur before the django and gmn_test_case imports, so
we're stuck with a bit of a messy import section that isort and flake8 don't
like.

isort:skip_file
"""
# flake8:noqa:E402

import bz2
import datetime
import logging
import os
import random
import io
import sys

import freezegun
import responses

import django
import django.core.management
import django.db

os.environ['DJANGO_SETTINGS_MODULE'] = 'd1_gmn.settings_test'
django.setup()

import d1_gmn.settings_test
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.sciobj
import d1_test.instance_generator.system_metadata
import d1_test.instance_generator.user_agent

# Dict lookup key matching the default key in settings_test.DATABASE
TEST_DB_KEY = 'default'

N_OBJECTS = 1000
N_READ_EVENTS = 2 * N_OBJECTS


def main():
  make_db_fixture = MakeDbFixture()
  make_db_fixture.run()


class MakeDbFixture(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def __init__(self):
    super().setup_method(None)

  @responses.activate
  def run(self):
    # We control the timestamps of newly created objects directly and use
    # freeze_time to control the timestamps that GMN sets on updated objects
    # and events.
    with freezegun.freeze_time('2001-02-03') as freeze_time:
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        self.clear_db()
        self.create_objects(freeze_time)
        self.create_read_events(freeze_time)
        self.commit()
        self.save_compressed_db_fixture()
        self.save_pid_list_sample()

  def clear_db(self):
    django.core.management.call_command(
      'flush', interactive=False, database=TEST_DB_KEY
    )

  def commit(self):
    django.db.connections[TEST_DB_KEY].commit()

  def create_objects(self, freeze_time):
    client = self.client_v2
    head_pid_set = set()
    with d1_gmn.tests.gmn_mock.disable_auth():
      for i in range(N_OBJECTS):
        logging.info('-' * 100)
        logging.info('Creating sciobj: {} / {}'.format(i + 1, N_OBJECTS))

        freeze_time.tick(delta=datetime.timedelta(days=1))

        do_chain = random.random() < 0.5

        pid = d1_test.instance_generator.identifier.generate_pid('PID_GMNFXT_')
        pid, sid, sciobj_bytes, sysmeta_pyxb = (
          d1_test.instance_generator.sciobj.generate_reproducible_sciobj_with_sysmeta(
            client, pid
          )
        )
        sciobj_file = io.BytesIO(sciobj_bytes)
        # self.dump(sysmeta_pyxb)
        # recv_sysmeta_pyxb = client.getSystemMetadata(pid)
        # self.dump(recv_sysmeta_pyxb)

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

  def create_read_events(self, freeze_time):
    client = self.client_v2
    with d1_gmn.tests.gmn_mock.disable_auth():
      pid_list = [
        o.identifier.value()
        for o in client.listObjects(count=N_OBJECTS).objectInfo
      ]
    for i in range(N_READ_EVENTS):
      logging.info('-' * 100)
      logging.info('Creating read event: {} / {}'.format(i + 1, N_READ_EVENTS))

      freeze_time.tick(delta=datetime.timedelta(days=1))

      read_subj = d1_test.instance_generator.random_data.random_subj()
      with d1_gmn.tests.gmn_mock.set_auth_context(
          active_subj_list=[read_subj], trusted_subj_list=[read_subj],
          whitelisted_subj_list=None, do_disable_auth=False
      ):
        client.get(
          random.choice(pid_list), vendorSpecific={
            'User-Agent': d1_test.instance_generator.user_agent.generate()
          }
        )

  def save_compressed_db_fixture(self):
    fixture_file_path = self.sample.get_path('db_fixture.json.bz2')
    logging.info('Writing fixture. path="{}"'.format(fixture_file_path))
    with bz2.BZ2File(
        fixture_file_path, 'w', buffering=1024, compresslevel=9
    ) as bz2_file:
      django.core.management.call_command(
        'dumpdata',
        exclude=['auth.permission', 'contenttypes'],
        database=TEST_DB_KEY,
        stdout=io.TextIOWrapper(bz2_file),
      )

  def save_pid_list_sample(self, chunk_size=500, **list_objects_kwargs):
    """Get list of all PIDs in the DB fixture

    These are for use in any tests that need to know which PIDs and SIDs are
    available in the DB.
    """
    client = self.client_v2
    with d1_gmn.tests.gmn_mock.disable_auth():
      start_idx = 0
      n_total = self.get_total_objects(client)
      pid_list = []
      sid_list = []
      while start_idx < n_total:
        object_list_pyxb = self.call_d1_client(
          client.listObjects, start=start_idx, count=chunk_size,
          **list_objects_kwargs
        )
        if not object_list_pyxb.objectInfo:
          break

        for o in object_list_pyxb.objectInfo:
          pid = o.identifier.value()
          pid_list.append(pid)

          sysmeta_pyxb = self.call_d1_client(client.getSystemMetadata, pid)
          sid = getattr(sysmeta_pyxb, 'seriesId', None)
          if sid is not None:
            sid_list.append(sid.value())

        start_idx += object_list_pyxb.count

    self.sample.save(
      self.sample.obj_to_pretty_str(pid_list), 'db_fixture_pid.json'
    )
    self.sample.save(
      self.sample.obj_to_pretty_str(sid_list), 'db_fixture_sid.json'
    )


if __name__ == '__main__':
  sys.exit(main())
