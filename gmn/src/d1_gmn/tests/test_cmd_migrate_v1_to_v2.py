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
"""Test the "migrate_v1_to_v2" management command
"""
from __future__ import absolute_import

import datetime
import gzip
import logging
import os
import random
import shutil
import subprocess
import tempfile
import zlib

import freezegun
import psycopg2
import psycopg2.extras

import d1_gmn.tests.gmn_test_case

import d1_common
import d1_common.url
import d1_common.util
import d1_common.xml

import d1_test.d1_test_case
import d1_test.instance_generator.identifier
import d1_test.instance_generator.random_data
import d1_test.instance_generator.sciobj
import d1_test.instance_generator.system_metadata
import d1_test.instance_generator.user_agent

import django
import django.core.management
import django.utils.six

shared_dict = {}


@d1_test.d1_test_case.reproducible_random_decorator('TestCmdMigrateV1toV2')
class TestCmdMigrateV1toV2(d1_gmn.tests.gmn_test_case.GMNTestCase):
  def _create_objects(self, pid_list, freeze_time):
    client = self.client_v2
    head_pid_set = set()

    for i, (pid, serial_version) in enumerate(pid_list):
      logging.info('-' * 100)
      logging.info('Creating sciobj: {} / {}'.format(i + 1, len(pid_list)))

      freeze_time.tick(delta=datetime.timedelta(days=1))

      do_chain = random.random() < 0.5

      pid, sid, sciobj_str, sysmeta_pyxb = \
        d1_test.instance_generator.sciobj.generate_reproducible(
          client, pid
        )

      # sciobj_str = StringIO.StringIO(sciobj_str)
      # self.dump_pyxb(sysmeta_pyxb)
      # recv_sysmeta_pyxb = client.getSystemMetadata(pid)
      # self.dump_pyxb(recv_sysmeta_pyxb)

      if not do_chain:
        self._save(pid, serial_version, sysmeta_pyxb, sciobj_str)
      else:
        if len(head_pid_set) < 3:
          head_pid_set.add(pid)
          self._save(pid, serial_version, sysmeta_pyxb, sciobj_str)
        else:
          sysmeta_pyxb.seriesId = None
          old_pid = random.choice(list(head_pid_set))
          head_pid_set.remove(old_pid)
          old_sysmeta_pyxb = self._load(old_pid)
          old_sysmeta_pyxb.obsoletedBy = sysmeta_pyxb.identifier.value()
          self._save(old_pid, serial_version, old_sysmeta_pyxb)
          sysmeta_pyxb.obsoletes = old_sysmeta_pyxb.identifier.value()
          self._save(pid, serial_version, sysmeta_pyxb)

  def _save(self, pid, serial_version, sysmeta_pyxb, sciobj_str=None):
    sysmeta_path = '{}.{}'.format(
      self._gmn_1_sysmeta_root_path(pid), serial_version
    )
    logging.debug('save: {}'.format(sysmeta_path))
    shared_dict['pid_to_path'][pid] = sysmeta_path
    d1_common.util.ensure_dir_exists(os.path.split(sysmeta_path)[0])
    with open(sysmeta_path, 'wb') as f:
      f.write(d1_common.xml.pretty_pyxb(sysmeta_pyxb))
    if sciobj_str is not None:
      obj_path = os.path.join(
        shared_dict['obj_root_path'], d1_common.url.encodePathElement(pid)
      )
      with open(obj_path, 'wb') as f:
        f.write(sciobj_str)

  def _load(self, pid):
    sysmeta_path = shared_dict['pid_to_path'][pid]
    logging.debug('load: {}'.format(sysmeta_path))
    with open(sysmeta_path, 'rb') as f:
      return d1_common.xml.deserialize(f.read())

  def _gmn_1_sysmeta_root_path(self, pid):
    z = zlib.adler32(pid.encode('utf-8'))
    a = z & 0xff ^ (z >> 8 & 0xff)
    b = z >> 16 & 0xff ^ (z >> 24 & 0xff)
    return os.path.join(
      shared_dict['sysmeta_root_path'],
      u'{0:03d}'.format(a),
      u'{0:03d}'.format(b),
      d1_common.url.encodePathElement(pid),
    )

  def test_1000(self):
    """migrate_v1_to_v2
    """
    test_db_name = 'gmn_v1_mig'
    connect_str = "host='' dbname='{}'".format(test_db_name)

    db = Db()
    db.connect("host='' dbname='postgres'")
    db.run("drop database if exists {};".format(test_db_name))
    db.run("create database {} encoding 'utf-8';".format(test_db_name))

    fixture_path = self.sample.get_path('db_fixture_gmn1.gz')
    self.pg_load('postgres', test_db_name, fixture_path)

    try:
      root_path = tempfile.mkdtemp()
      sysmeta_root_path = tempfile.mkdtemp(dir=root_path)
      obj_root_path = tempfile.mkdtemp(dir=root_path)

      shared_dict['obj_root_path'] = obj_root_path
      shared_dict['sysmeta_root_path'] = sysmeta_root_path
      shared_dict['pid_to_path'] = {}

      with freezegun.freeze_time('2011-11-11') as freeze_time:
        pid_list = self.run_sql(
          'select pid, serial_version from mn_scienceobject order by pid;',
          test_db_name,
        )
        self._create_objects(pid_list, freeze_time)

      with self.mock.disable_management_command_logging():
        with d1_test.d1_test_case.capture_log(logging.INFO) as log_stream:
          django.core.management.call_command(
            'migrate_v1_to_v2', '--force', '--d1root', root_path, '--v1sysmeta',
            sysmeta_root_path, '--v1obj', obj_root_path, '--dsn', connect_str
          )
        log_list = log_stream.getvalue().splitlines()
        self.sample.assert_equals(
          '\n'.join(log_list[log_list.index('Counted events:'):]),
          'migrate_v1_to_v2',
        )

    finally:
      if root_path:
        shutil.rmtree(root_path)

  def pg_load(self, user_name, db_name, fixture_path):
    with tempfile.NamedTemporaryFile() as tmp_file:
      with gzip.open(fixture_path, 'rb') as f:
        tmp_file.write(f.read())
      tmp_file.seek(0)
      subprocess.check_call(['psql', '--file', tmp_file.name,
                             db_name] # '-U', user_name,
                            )


class Db(object):
  def connect(self, dsn):
    """Connect to DB
    dbname: the database name
    user: user name used to authenticate
    password: password used to authenticate
    host: database host address (defaults to UNIX socket if not provided)
    port: connection port number (defaults to 5432 if not provided)
    """
    self.con = psycopg2.connect(dsn)
    self.cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # autocommit: Disable automatic transactions
    self.con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

  def close(self):
    self.cur.close()

  def run(self, sql_str, *args, **kwargs):
    try:
      self.cur.execute(sql_str, args, **kwargs)
    except psycopg2.DatabaseError as e:
      logging.debug('SQL query result="{}"'.format(str(e)))
      raise
    try:
      return self.cur.fetchall()
    except psycopg2.DatabaseError:
      return None
