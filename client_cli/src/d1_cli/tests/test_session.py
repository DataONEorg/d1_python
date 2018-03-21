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
"""Test handling of session variables
"""

import io
import sys
import uuid

import d1_cli.impl.cli_exceptions as cli_exceptions
import d1_cli.impl.format_ids as format_ids
import d1_cli.impl.nodes as nodes
import d1_cli.impl.session as session
import pytest

import d1_common.const

import d1_test.d1_test_case

nodes = nodes.Nodes()
#  'node_a',
#  'node_b',
#  'node_c',
#]

format_ids = format_ids.FormatIDs()

#  'format_id_a',
#  'format_id_b',
#  'format_id_c',
#]

#===============================================================================


class TestSession(d1_test.d1_test_case.D1TestCase):
  def test_1000(self):
    """__init__()"""
    s = session.Session(nodes, format_ids)
    assert s is not None, 'Could not instantiate session'

  def test_1010(self):
    """After instatiation, the default session parameters are available via get()"""
    s = session.Session(nodes, format_ids)
    #self.assertEqual(s.get('pretty'), True)
    assert s.get('cn-url') == d1_common.const.URL_DATAONE_ROOT

  def test_1020(self):
    """Session parameters can be updated with set()"""
    s = session.Session(nodes, format_ids)
    s.set('verbose', False),
    s.set('rights-holder', 'test')
    assert s.get('verbose') is False
    assert s.get('rights-holder') == 'test'

  def test_1030(self):
    """Setting valid CN is successful"""
    s = session.Session(nodes, format_ids)
    valid_cn = 'https://cn-unm-1.dataone.org/cn'
    s.set('cn-url', valid_cn)
    assert s.get('cn-url') == valid_cn

  def test_1040(self):
    """Session parameters can be brought back to their defaults with reset()"""
    s = session.Session(nodes, format_ids)
    s.set('query', 'testquery'),
    assert s.get('query') == 'testquery'
    s.reset()
    assert s.get('query') == '*:*'

  def test_1050(self):
    """Getting an non-existing session parameter raises InvalidArguments"""
    s = session.Session(nodes, format_ids)
    with pytest.raises(cli_exceptions.InvalidArguments):
      s.get('bogus-value')

  def test_1060(self):
    """set_with_conversion() handles None"""
    s = session.Session(nodes, format_ids)
    assert s.get('verbose') is True
    s.set_with_conversion('verbose', 'None')
    assert s.get('verbose') is None

  def test_1070(self):
    """set_with_conversion() handles integer conversions"""
    s = session.Session(nodes, format_ids)
    assert s.get('verbose') is True
    s.set_with_conversion('verbose', '1')
    assert s.get('verbose') == 1

  def test_1080(self):
    """set_with_conversion() raises InvalidArguments on non-existing session parameter"""
    s = session.Session(nodes, format_ids)
    with pytest.raises(cli_exceptions.InvalidArguments):
      s.set_with_conversion('bogus-value', '1')

  def test_1090(self):
    """Session object exposes access control"""
    s = session.Session(nodes, format_ids)
    s.get_access_control().add_allowed_subject('newsubject', 'write')

  def test_1100(self):
    """print_all_variables() is available and appears to work"""
    # capture stdout
    old = sys.stdout
    sys.stdout = io.StringIO()
    # run print
    s = session.Session(nodes, format_ids)
    s.print_all_variables()
    # release stdout
    out = sys.stdout.getvalue()
    sys.stdout = old
    # validate
    assert len(out) > 100
    assert type(out) is str

  def test_1110(self, tmpdir):
    """Session is successfully saved and then loaded (pickled and unpickled)"""
    tmp_pickle_path = str(tmpdir.join('session.pickle'))
    s1 = session.Session(nodes, format_ids)
    u = str(uuid.uuid1())
    s1.set('rights-holder', u)
    s1.save(tmp_pickle_path)
    s2 = session.Session(nodes, format_ids)
    s2.load(tmp_pickle_path)
    assert s2.get('rights-holder') == u
    # TODO: Use sample to check more of the pickled fields
