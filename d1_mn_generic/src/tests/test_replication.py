#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
:mod:`test_replication`
=======================

:Synopsis:
  Test replication between two GMN instances.

  This test will only work until security is added to the DataONE
  infrastructure as the test works in part by simulating a CN. 
:Author: DataONE (Dahl)
"""

import logging
import sys
import optparse
import urlparse
import urllib
import StringIO
import time
import sys
import os
import glob
import re
import subprocess

import d1_common.types.generated.dataoneTypes as dataoneTypes
from django.test.utils import override_settings
sys.path.append('/home/mark/d1/d1_python/d1_mn_generic/src/service')
# D1
try:
  #import d1_common.mime_multipart
  import d1_common.types.exceptions
  # import d1_common.types.checksum_serialization
  # import d1_common.types.objectlist_serialization
  import d1_common.util
  import d1_common.date_time
  import d1_common.url
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.d1client
  import d1_client.mnclient
  import d1_client.systemmetadata
  import mn.sysmeta_store
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise

# App.
import gmn_test_client


class options():
  def __init__(self, host=None):
    if not host:
      self.gmn_url = 'http://127.0.0.1:8000'
    else:
      self.gmn_url = host
    self.obj_path = '/home/mark/d1/d1_client_bash/test_objects'
    self.wrapped = False
    self.obj_url = 'http://127.0.0.1:8000'


def log_setup():
  # Set up logging.
  # We output everything to both file and stdout.
  logging.getLogger('').setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def baseurl_by_noderef(opts, node_ref):
  # Resolve dst_ref to URL.
  # Call to /cn/test_baseurl_by_noderef/<dst_node_ref>
  cn_client = d1_client.cnclient.CoordinatingNodeClient(base_url=opts.d1_root)
  cn_nodes = cn_client.listNodes()
  for node in cn_nodes.node:
    if node.identifier.value() == node_ref:
      return node.baseURL
  # baseurl_by_noderef_url = urlparse.urljoin(opts.d1_root,
  #   'test_baseurl_by_noderef/{0}'.format(
  #     d1_common.url.encodePathElement(node_ref)))
  #
  # client_root = d1_client.d1client.DataONEClient(opts.d1_root)
  # response = client_root.GET(baseurl_by_noderef_url)
  # return response.read()


def replicate(opts, args):
  '''Replication. Requires fake CN.
  '''
  # The object we will replicate.
  #pid = 'hdl:10255/dryad.105/mets.xml'
  # Source and destination node references.
  dst_ref = args[0]
  src_ref = args[1]
  pid = args[2]

  logging.debug('src_ref({0}) dst_ref({1}) pid({2})'.format(src_ref, dst_ref, pid))

  # # Create connections to src and dst.
  # dst_base = baseurl_by_noderef(opts, dst_ref)
  # client_dst = d1_client.client.DataOneClient(dst_base)
  src_base = baseurl_by_noderef(opts, src_ref)

  opts = options()
  dst_base = opts.gmn_url
  # client_src = d1_client.client.DataOneClient(src_base)
  client_dst = d1_client.mnclient.MemberNodeClient(dst_base)
  client_src = d1_client.mnclient.MemberNodeClient(src_base)

  # For easy testing, delete the object on the destination node if it exists
  # there, so that we can test on the same object each time.
  # try:
  #   pid_deleted = client_dst.delete(pid)
  #   assert(pid == pid_deleted.value())
  # except d1_common.types.exceptions.NotFound:
  #   pass

  # Check that the object does not already exist on dst.
  #   We check for SyntaxError raised by the XML deserializer when it attempts
  #   to deserialize a DataONEException. The exception is caused by the body
  #   being empty since describe() uses a HEAD request.
  # try:
  #   client_dst.describe(pid)
  # except SyntaxError:
  #   pass
  # else:
  #   logging.error('pid({0}): Object already exists on destination'.format(pid))
  #   exit()

  # Download the SysMeta doc from the source.
  # sysmeta_obj = client_src.getSystemMetadata(pid)

  # sysmeta_doc = sysmeta_obj.toxml()
  opts = options(host=src_ref)
  # client = gmn_test_client.GMNTestClient(src_ref)
  # client.delete_all_objects()
  # opts.gmn_url = src_ref
  client = gmn_test_client.GMNTestClient(client_dst.base_url)
  client.clear_replication_queue()
  # gmn_test_client.populate_mn(client,'/home/mark/d1/d1_client_bash/test_objects')
  for obj in glob.glob(os.path.join(opts.obj_path, 'test1005*.sysmeta')):
    # Get name of corresponding object and open it.
    pid = obj.split('/')[-1].split('.')[0]
    try:
      client.test_delete_single_object(pid)
    except:
      pass

    sysmeta_path = os.path.join(
      '/home/mark/d1/d1_client_bash/test_objects', pid + ".sysmeta"
    )
    object_path = re.match(r'(.*)\.sysmeta', sysmeta_path).group(1)
    object_file = open(object_path, 'r')

    # The pid is stored in the sysmeta.
    sysmeta_file = open(sysmeta_path, 'r')
    sysmeta_xml = sysmeta_file.read()
    sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)
    # sysmeta_obj.rightsHolder = 'test_user_1'
    #
    # # headers = self.include_subjects('test_user_1')
    # # headers.update({'VENDOR_TEST_OBJECT': 1})
    # #
    # # if self.options.wrapped:
    # #   vendor_specific = {
    # #     'VENDOR_GMN_REMOTE_URL': self.options.obj_url + '/' + \
    # #     d1_common.url.encodePathElement(
    # #       d1_common.url.encodePathElement(sysmeta_obj.identifier.value()))
    # #   }
    # #   headers.update(vendor_specific)
    #
    # sysmeta_path = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_objects/15Jmatrix2.txt.sysmeta'
    # with open(sysmeta_path, 'rb') as f:
    #     sysmeta_xml = f.read()
    #   # SysMeta is stored in UTF-8 and CreateFromDocument() does not handle
    #   # native Unicode objects, so the SysMeta is passed to CreateFromDocument()
    #   # as UTF-8.
    # sysmeta_obj = dataoneTypes.CreateFromDocument(sysmeta_xml)
    client.create_replication_queue(pid, sysmeta_obj, src_ref)
  # os.chdir('../service')
  # subprocess.call(['python manage.py process_replication_queue'], shell=True)
  # replication_completed = False
  # while not replication_completed:
  #   status_xml_str = client_dst.client.GET(test_replicate_get_xml).read()
  #   status_xml_obj = lxml.etree.fromstring(status_xml_str)
  #
  #   for work_item in status_xml_obj.xpath('/replication_queue/replication_item'):
  #     if  work_item.xpath('pid')[0].text == pid and \
  #         work_item.xpath('source_node')[0].text == src_ref and \
  #         work_item.xpath('status')[0].text == 'completed':
  #       replication_completed = True
  #       break
  #
  #   if not replication_completed:
  #     time.sleep(1)
  #
  # # Get checksum of the object on the destination server and compare it to
  # # the checksum retrieved from the source server.
  # dst_checksum_obj = client_dst.checksum(pid)
  # dst_checksum = dst_checksum_obj.value()
  # src_checksum_obj = client_src.checksum(pid)
  # src_checksum = src_checksum_obj.value()
  # if src_checksum != dst_checksum:
  #   raise Exception('Replication failed: Source and destination checksums do not match')


def main():
  log_setup()

  # Command line options.
  parser = optparse.OptionParser(
    'usage: %prog [options] <dst_gmn_ref> <src_gmn_ref> <pid>'
  )
  # General
  parser.add_option(
    '--d1-root',
    dest='d1_root',
    action='store',
    type='string',
    default='http://0.0.0.0:8000/cn/'
  ) # default=d1_common.const.URL_DATAONE_ROOT
  parser.add_option(
    '--verbose',
    dest='verbose',
    action='store_true',
    default=False,
    help='display more information'
  )
  (opts, args) = parser.parse_args()

  if not opts.verbose:
    logging.getLogger('').setLevel(logging.ERROR)

  if len(args) != 3:
    parser.print_help()
    exit()

  multipart_doc = replicate(opts, args)
#   # Add replication task to the destination GMN work queue.
#  client_t = d1_client.client.DataOneClient('http://127.0.0.1:8000')
#  replicate_url = urlparse.urljoin(client_t.client.target, '/replicate')
#  client_t.client.POST(replicate_url, multipart_doc, {})

if __name__ == '__main__':
  main()
