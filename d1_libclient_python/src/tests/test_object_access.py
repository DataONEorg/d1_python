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
'''Module d1_client.tests.test_object_access
============================================

This script exercises a node by retrieving the list of all objects and
for each attempts to retrieve the associated metadata and the object.

Use with caution since it iterates over every object on the node.

:Created:
:Author: DataONE (Vieglais)
:Dependencies:
  - python 2.6
'''
import sys
import logging
import d1_client.mnclient
import d1_client.objectlistiterator


def read_chunk(fobj, chunk_size=1024):
  while True:
    data = fobj.read(chunk_size)
    if not data:
      break
    yield data


def readAll(f):
  data = ''
  for chunk in read_chunk(f):
    data += chunk
  return data


def walkNode(target, start=0):
  '''Given a DataOne node, retrieve each object and it's associated system 
  metadata.
  '''
  client = d1_client.mnclient.MemberNodeClient.DataOneClient(target=target)
  objects = d1_client.objectlistiterator.ObjectListIterator(client, start=start)
  logging.info("%d objects on target" % len(objects))
  counter = 0
  for obj in objects:
    counter += 1
    logging.info("ID (%d/%d) = %s" % (counter + start, len(objects), obj.identifier))
    try:
      meta = readAll(client.getSystemMetadataResponse(obj.identifier))
      logging.info("Meta size = %d" % len(meta))
    except Exception, e:
      logging.exception(e)
      logging.error("Trying to load: %s" % client.getMetaUrl(id=obj.identifier))
    try:
      data = readAll(client.get(obj.identifier))
      logging.info("Object size (%d) = %d" % (obj.size, len(data)))
      if len(data) != obj.size:
        logging.error("Size mismatch for %s" % client.getObjectUrl(id=obj.identifier))
    except Exception, e:
      logging.exception(e)
      logging.error("Trying to load: %s" % client.getObjectUrl(id=obj.identifier))
  logging.info('Done.')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  #target = "http://dev-dryad-mn.dataone.org/mn"
  target = "http://129.24.0.15/mn"
  #target = "http://knb-mn.ecoinformatics.org/knb"
  #target = "http://cn-unm-1.dataone.org/knb"
  #target = "http://cn-ucsb-1.dataone.org/knb"
  walkNode(target, start=0)
