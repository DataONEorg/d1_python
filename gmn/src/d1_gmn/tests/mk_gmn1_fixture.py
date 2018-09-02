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
"""
"""

import subprocess
import sys

import responses

import d1_test.d1_test_case

N_OBJECTS = 200


def main():
  make_db_fixture = MakeDbFixtureGMNv1()
  make_db_fixture.run()


# flake8: noqa: F124
class MakeDbFixtureGMNv1(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def run(self):
    print((
      '# sciobj: {}'.format(
        self.run_sql(
          'SELECT count(*) FROM mn_scienceobject;',
          'gmn',
        )[0][0]
      )
    ))

    self.pg_dump('db_fixture_gmn1_before.gz')

    self.run_sql(
      'delete from mn_eventlog;',
      'gmn',
    )
    self.run_sql(
      'delete from mn_permission;',
      'gmn',
    )
    self.run_sql(
      'delete from mn_systemmetadatarefreshqueue;',
      'gmn',
    )
    pid_list = self.run_sql(
      'select pid, serial_version from mn_scienceobject order by pid limit %s;',
      'gmn',
      N_OBJECTS,
    )
    self.run_sql(
      'delete from mn_scienceobject where pid not in %s;', 'gmn',
      tuple([p[0] for p in pid_list])
    )

    self.run_sql('analyze')
    self.run_sql('vacuum full')

    self.pg_dump('db_fixture_gmn1.gz')

  def pg_dump(self, path):
    subprocess.check_call(['pg_dump', '--file', path, '--compress', '9', 'gmn'])


if __name__ == '__main__':
  sys.exit(main())
