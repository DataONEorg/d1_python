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
'''Module d1_client.tests.test_d1client
=======================================

Unit tests for d1client.

:Created: 2010-01-08
:Author: DataONE (vieglais)
:Dependencies:
  - python 2.6
'''

import unittest
import logging

from d1_common import xmlrunner
from d1_common.types import exceptions
from d1_common.types import systemmetadata
from d1_common import const
import d1_common.testcasewithurlcompare

from d1_client import client
import d1_common.util

MEMBER_NODES = {
  'dryad': 'http://dev-dryad-mn.dataone.org/mn',
  'daac': 'http://daacmn.dataone.utk.edu/mn',
  'metacat': 'http://knb-mn.ecoinformatics.org/knb/d1',
}

COORDINATING_NODES = {'cn-dev': 'http://cn-dev.dataone.org/cn', }

#===============================================================================


class TestDataOneClient(d1_common.testcasewithurlcompare.TestCaseWithURLCompare):
  def setUp(self):
    self.target = MEMBER_NODES['dryad']

  def testGet(self):
    return
    cli = client.DataOneClient(target=self.target)
    #try loading some random object
    start = 23
    count = 1
    startTime = None
    endTime = None
    requestFormat = 'text/xml'
    objlist = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    id = objlist.objectInfo[0].pid
    logging.info("Attempting to get ID=%s" % id)
    bytes = cli.get(id).read()
    headers = cli.headers
    headers['Accept'] = 'text/xml'
    sysmeta = cli.getSystemMetadata(id, headers=headers)
    self.assertEqual(sysmeta.identifier, id)

  def testGetFail(self):
    cli = client.DataOneClient(target=self.target)
    # see if failure works
    id = 'some bogus id'
    self.assertRaises(exceptions.NotFound, cli.get, id)

  def testGetSystemMetadata(self):
    #TODO: test getSystemMetadata()
    pass

  def _subListObjectTest(self, requestformat):
    cli = client.DataOneClient(target=self.target)
    start = 0
    count = 10
    startTime = None
    endTime = None
    requestFormat = 'text/xml'
    objlist = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    self.assertEqual(objlist.count, len(objlist.objectInfo))
    obj = objlist.objectInfo[0]
    tmp = obj.size
    tmp = obj.checksum
    tmp = obj.dateSysMetadataModified
    tmp = obj.identifier
    tmp = obj.objectFormat

    start = 4
    count = 3
    objlist2 = cli.listObjects(
      start=start,
      count=count,
      startTime=startTime,
      endTime=endTime,
      requestFormat=requestFormat
    )
    self.assertEqual(objlist2.count, len(objlist2.objectInfo))
    self.assertEqual(objlist2.count, count)
    i = 0
    for obj in objlist2.objectInfo:
      self.assertEqual(objlist.objectInfo[4 + i].identifier, obj.identifier)
      logging.info(obj.identifier)
      i += 1

  def testListObjectsJson(self):
    #requestFormat = 'application/json'
    #self._subListObjectTest(requestFormat)
    pass

  def testListObjectsXml(self):
    requestFormat = 'text/xml'
    self._subListObjectTest(requestFormat)

#===============================================================================


class TestListObjects(unittest.TestCase):
  def setUp(self):
    self.target = MEMBER_NODES['dryad']

  def testValidListObjects(self):
    return
    objectListUrl = "https://repository.dataone.org/software/cicore/trunk/schemas/dataoneTypes.xsd"
    cli = client.DataOneClient(target=self.target)
    response = cli.listObjects(start=0, count=5)
    logging.error("====")
    logging.error(response)
    # PyXB parser validates the object.

    #  def testListSlice(self):
    #    olist = objectlist.D1ObjectList(None)
    #    a = olist[1:10]


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
  #unittest.main(testRunner=xmlrunner.XmlTestRunner(sys.stdout))
