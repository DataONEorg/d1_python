#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`test_replication`
=======================

:Synopsis:
  Test replication between two GMN instances.

  This test will only work until security is added to the DataONE
  infrastructure as the test works in part by simulating a CN. 
    
.. moduleauthor:: Roger Dahl
"""

import logging
import sys
import optparse
import urlparse
import urllib
import StringIO
import time

# MN API.
try:
  #import d1_common.mime_multipart
  import d1_common.types.exceptions
  import d1_common.types.checksum_serialization
  import d1_common.types.objectlist_serialization
  import d1_common.util
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/api-common-python/src/d1_common\n'
  )
  raise
try:
  import d1_client
  import d1_client.client
  import d1_client.systemmetadata
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    'Try: svn co https://repository.dataone.org/software/cicore/trunk/itk/d1-python/src/d1_client\n'
  )
  raise


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
  baseurl_by_noderef_url = urlparse.urljoin(opts.d1_root,
                                        'test_baseurl_by_noderef/{0}'\
                                        .format(urllib.quote(node_ref, '')))

  client_root = d1_client.client.DataOneClient(opts.d1_root)
  response = client_root.client.GET(baseurl_by_noderef_url)
  return response.read()


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

  # Create connections to src and dst.
  dst_base = baseurl_by_noderef(opts, dst_ref)
  client_dst = d1_client.client.DataOneClient(dst_base)
  src_base = baseurl_by_noderef(opts, src_ref)
  client_src = d1_client.client.DataOneClient(src_base)

  # For easy testing, delete the object on the destination node if it exists
  # there, so that we can test on the same object each time.
  try:
    pid_deleted = client_dst.delete(pid)
    assert (pid == pid_deleted.value())
  except d1_common.types.exceptions.NotFound:
    pass

  # Check that the object does not already exist on dst.
  #   We check for SyntaxError raised by the XML deserializer when it attempts
  #   to deserialize a DataONEException. The exception is caused by the body
  #   being empty since describe() uses a HEAD request.
  try:
    client_dst.describe(pid)
  except SyntaxError:
    pass
  else:
    logging.error('pid({0}): Object already exists on destination'.format(pid))
    exit()

  # Download the SysMeta doc from the source.
  sysmeta_obj = client_src.getSystemMetadata(pid)
  sysmeta_doc = sysmeta_obj.toxml()

  # Add replication task to the destination GMN work queue.
  #   Create the MMP document that is submitted to dst to request a replication.
  files = []
  files.append(('sysmeta', 'sysmeta', sysmeta_doc))
  fields = []
  fields.append(('sourceNode', src_ref))
  multipart = d1_common.mime_multipart.multipart(fields, files)
  #   Post the MMP doc to /replicate on GMN.
  replicate_url = urlparse.urljoin(client_dst.client.target, '/replicate')
  multipart.post(replicate_url)

  # Poll for completed replication.
  test_replicate_get_xml = urlparse.urljoin(
    client_dst.client.target, '/test_replicate_get_xml'
  )
  replication_completed = False
  while not replication_completed:
    status_xml_str = client_dst.client.GET(test_replicate_get_xml).read()
    status_xml_obj = lxml.etree.fromstring(status_xml_str)

    for work_item in status_xml_obj.xpath('/replication_queue/replication_item'):
      if  work_item.xpath('pid')[0].text == pid and \
          work_item.xpath('source_node')[0].text == src_ref and \
          work_item.xpath('status')[0].text == 'completed':
        replication_completed = True
        break

    if not replication_completed:
      time.sleep(1)

  # Get checksum of the object on the destination server and compare it to
  # the checksum retrieved from the source server.
  dst_checksum_obj = client_dst.checksum(pid)
  dst_checksum = dst_checksum_obj.value()
  src_checksum_obj = client_src.checksum(pid)
  src_checksum = src_checksum_obj.value()
  if src_checksum != dst_checksum:
    raise Exception('Replication failed: Source and destination checksums do not match')


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
