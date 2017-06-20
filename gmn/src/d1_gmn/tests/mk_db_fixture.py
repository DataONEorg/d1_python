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

from __future__ import absolute_import

import bz2
import datetime
import logging
import random
import StringIO

import freezegun
import responses

import d1_gmn.settings_test
import d1_gmn.tests.gmn_mock
import d1_gmn.tests.gmn_test_case

import d1_test.d1_test_case
import d1_test.instance_generator.system_metadata
import d1_test.instance_generator.user_agent

import django as django
import django.conf
import django.core.management

N_OBJECTS = 1000
N_READ_EVENTS = 2 * N_OBJECTS


def main():
  django.conf.settings.configure(
    default_settings=d1_gmn.settings_test, DEBUG=True
  )
  django.setup()

  # os.environ['DJANGO_SETTINGS_MODULE'] = 'd1_gmn.settings_test'
  #   django.conf.settings.configure()
  make_db_fixture = MakeDbFixture()
  make_db_fixture.run()


@d1_test.d1_test_case.reproducible_random_decorator('TestMakeDbFixture')
class MakeDbFixture(d1_gmn.tests.gmn_test_case.GMNTestCase):
  """Create database entries for a set of test objects

  Objects are randomly distributed between categories:
    - Standalone, no SID
    - Standalone, SID
    - Chain, no SID
    - Chain, SID
  Notes:
    - Though object bytes are also created, they are not captured in the db
    fixture. So if a test needs get(), getChecksum() and replica() to work, it
    must first create the correct file in GMN's object store. The bytes are
    predetermined for a given test PID. See
    d1_test.d1_test_case.generate_reproducible_sciobj_str() and
    d1_gmn.app.util.sciobj_file_path().
  """

  @responses.activate
  def run(self):
    with freezegun.freeze_time('1977-06-27') as freeze_time:
      with d1_gmn.tests.gmn_mock.disable_sysmeta_sanity_checks():
        self.clear_db()
        self.create_objects(freeze_time)
        self.create_read_events(freeze_time)
        self.save_compressed_db_fixture()
        self.save_pid_list_sample()

  def clear_db(self):
    test_db_key = 'default'
    django.core.management.call_command('flush', database=test_db_key)

  def create_objects(self, freeze_time):
    client = self.client_v2
    head_pid_set = set()
    with d1_gmn.tests.gmn_mock.disable_auth():
      for i in range(N_OBJECTS):
        logging.info('-' * 100)
        logging.info('Creating sciobj: {} / {}'.format(i + 1, N_OBJECTS))

        freeze_time.tick(delta=datetime.timedelta(days=1))

        use_sid = random.random() < 0.5
        do_chain = random.random() < 0.5

        pid, sid, sciobj_str, sysmeta_pyxb = self.create_random_sciobj(
          client, sid=use_sid
        )
        sciobj_file = StringIO.StringIO(sciobj_str)
        self.dump_pyxb(sysmeta_pyxb)

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

      read_subj = d1_test.instance_generator.system_metadata.random_data.random_subj()
      with d1_gmn.tests.gmn_mock.set_auth_context(
          active_subj_list=[read_subj], trusted_subj_list=[read_subj],
          do_disable_auth=False
      ):
        client.get(
          random.choice(pid_list), vendorSpecific={
            'User-Agent': d1_test.instance_generator.user_agent.generate()
          }
        )

  def save_compressed_db_fixture(self):
    fixture_file_path = self.get_sample_path('db_fixture.json.bz2')
    logging.info('Writing fixture. path="{}"'.format(fixture_file_path))
    with bz2.BZ2File(
        fixture_file_path, 'w', buffering=1024, compresslevel=9
    ) as bz2_file:
      django.core.management.call_command('dumpdata', stdout=bz2_file)

  def save_pid_list_sample(self, chunk_size=500, **list_objects_kwargs):
    """Get list of all PIDs in the DB fixture"""
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
          print sid
          if sid is not None:
            sid_list.append(sid.value())

        start_idx += object_list_pyxb.count

    self.save_sample('db_fixture_pid.json', self.obj_to_pretty_str(pid_list))
    self.save_sample('db_fixture_sid.json', self.obj_to_pretty_str(sid_list))


if __name__ == '__main__':
  main()
