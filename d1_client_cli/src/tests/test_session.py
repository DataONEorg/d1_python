#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_client_cli.tests.test_session
=======================================

:Synopsis:
  Unit tests for session parameters.
:Created: 2011-11-10
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Stdlib.
import unittest
import logging
import os
import sys
import uuid
import StringIO

# D1.
import d1_common.const
import d1_common.testcasewithurlcompare
import d1_common.types.exceptions
import d1_common.xmlrunner

# App.
sys.path.append('../d1_client_cli/')
import session
import cli_exceptions

#===============================================================================


class TESTCLISession(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    pass

  def test_010(self):
    '''The session object can be instantiated'''
    s = session.session()

  def test_020(self):
    '''After instatiation, the default session parameters are available via get()'''
    s = session.session()
    self.assertEqual(s.get('cli', 'pretty'), True)
    self.assertEqual(s.get('node', 'dataoneurl'), d1_common.const.URL_DATAONE_ROOT)

  def test_030(self):
    '''Session parameters can be updated with set()'''
    s = session.session()
    s.set('cli', 'pretty', False),
    s.set('node', 'dataoneurl', 'test')
    self.assertEqual(s.get('cli', 'pretty'), False)
    self.assertEqual(s.get('node', 'dataoneurl'), 'test')

  def test_040(self):
    '''Session parameters can be brought back to their defaults with reset()'''
    s = session.session()
    s.set('search', 'query', 'testquery'),
    self.assertEqual(s.get('search', 'query'), 'testquery')
    s.reset()
    self.assertEqual(s.get('search', 'query'), '*:*')

  def test_050(self):
    '''Getting an non-existing session parameter raises InvalidArguments'''
    s = session.session()
    self.assertRaises(cli_exceptions.InvalidArguments, s.get, 'search', 'query-bogus')
    self.assertRaises(cli_exceptions.InvalidArguments, s.get, 'search-bogus', 'query')

  def test_100(self):
    '''set_with_conversion() handles None'''
    s = session.session()
    self.assertEqual(s.get('cli', 'pretty'), True)
    s.set_with_conversion('cli', 'pretty', 'None')
    self.assertEqual(s.get('cli', 'pretty'), None)

  def test_110(self):
    '''set_with_conversion() handles integer conversions'''
    s = session.session()
    self.assertEqual(s.get('cli', 'pretty'), True)
    s.set_with_conversion('cli', 'pretty', '1')
    self.assertEqual(s.get('cli', 'pretty'), 1)

  def test_120(self):
    '''set_with_conversion() raises InvalidArguments on non-existing session parameter'''
    s = session.session()
    self.assertRaises(
      cli_exceptions.InvalidArguments, s.set_with_conversion, 'search-bogus', 'query', '1'
    )

  def test_130(self):
    '''Session object exposes access control'''
    s = session.session()
    s.access_control_add_allowed_subject('newsubject', 'write')

  def test_140(self):
    '''print_session() is available and appears to work'''
    # capture stdout
    old = sys.stdout
    sys.stdout = StringIO.StringIO()
    # run print
    s = session.session()
    s.print_parameter('')
    # release stdout
    out = sys.stdout.getvalue()
    sys.stdout = old
    # validate
    self.assertTrue(len(out) > 100)
    self.assertTrue('sysmeta' in out)
    self.assertTrue('None' in out)

  def test_200(self):
    '''Session is successfully saved and then loaded (pickled and unpickled)'''
    tmp_pickle = './pickle.tmp'
    try:
      os.unlink(tmp_pickle)
    except OSError:
      pass
    s1 = session.session()
    u = str(uuid.uuid1())
    s1.set('sysmeta', 'rightsholder', u)
    s1.save(tmp_pickle)
    s2 = session.session()
    s2.load(False, tmp_pickle)
    self.assertEqual(s2.get('sysmeta', 'rightsholder'), u)

  def test_300(self):
    '''assert_required_parameters_present() returns successfully on no missing parameters'''
    s = session.session()
    s.assert_required_parameters_present(('dataoneurl', 'count', 'algorithm'))

  def test_310(self):
    '''assert_required_parameters_present() raises exception on missing parameters'''
    s = session.session()
    s.set('node', 'dataoneurl', None)
    self.assertRaises(
      cli_exceptions.InvalidArguments, s.assert_required_parameters_present,
      ('dataoneurl', 'count', 'algorithm')
    )


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
