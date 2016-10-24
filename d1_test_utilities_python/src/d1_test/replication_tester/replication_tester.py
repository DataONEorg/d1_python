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

'''
:mod:`replication_tester`
=========================

:Synopsis:
  This script tests replication request handling in source and destination MNs.

:Author:
  DataONE (Dahl)

:Created:
  2014-02-10

:Operation:
  RepTest is documented in the Utilities section of the dataone.test_utilities
  package on PyPI.
'''

# The DataONE terms for the two MNs involved in a given replication is origin
# and target nodes. In this code, source/src and destionation/dst is used
# instead.

# Stdlib.
import cgi
import datetime
import hashlib
import logging
import os
import optparse
import random
import re
import socket
import string
#import sys
import threading
import time
import urllib
import urlparse

import SimpleHTTPServer
import SocketServer
import Queue

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
#import d1_common
import d1_common.const
#import d1_client.data_package
import d1_client.mnclient

# App.
from d1_test.instance_generator import random_data, systemmetadata

# Defaults. These can be modified on the command line.

# BaseURL for the Member Node to be tested. If the script is run on the same
# server as the Member Node, this can be localhost.
SRC_BASE_URL = 'https://localhost'
DST_BASE_URL = 'https://localhost'

# The formatId to use for the Science Object. It should be the ID of an Object
# Format that is registered in the DataONE Object Format Vocabulary. A list of
# valid IDs can be retrieved from https://cn.dataone.org/cn/v1/formats.
FORMAT_ID = 'application/octet-stream'

# The rights holder subject to use in generated system metadata.
SYSMETA_RIGHTSHOLDER = 'random_rights_holder'

# The number of bytes in each science object.
N_SCI_OBJ_BYTES = 1024

# The Base URL to RepTest. The MNs being tested call back to this location. If
# RepTest runs on the same machine as the MN being tested, this can be set to
# localhost. If so, make sure that the port is set to a different port than the
# one used by the MN. Only HTTP is currently supported.
REPTEST_BASE_URL = 'http://localhost:8181'

# Time to wait for MN calls, in seconds.
TIMEOUT = 10

# Internal settings. It should not be necessary to modify these.

def generate_random_ascii_pid(prefix):
  return '[{0}_{1}]'.format(prefix,
    ''.join(random.choice(string.ascii_uppercase +
    string.ascii_lowercase + string.digits) for x in range(10)))


# A PID that is not known on the node receiving the call.
PID_UNKNOWN = generate_random_ascii_pid('replication_tester_pid_unknown')

# A PID that will cause RepTest.getReplica() to return a NotAuthorized exception.
PID_NOT_AUTHORIZED = generate_random_ascii_pid('replication_tester_pid_not_authorized')

# A PID that will cause RepTest.getReplica() to return a valid OctetStream.
PID_KNOWN_AND_AUTHORIZED = generate_random_ascii_pid('replication_tester_pid_known_and_authorized')


## A PID that will cause RepTest to return a valid OctetStream.
#PID_EXISTS = generate_random_ascii_pid('replication_tester_pid_exists')

TEST_CN_NODE_ID = 'urn:node:TestCN'
TEST_MN_NODE_ID = 'urn:node:TestMN'


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)
  logger = logging.getLogger('main')

  parser = optparse.OptionParser()

  # Source and destination Base URLs.

  parser.add_option('--src-base-url', dest='src_base_url', action='store',
                    type='string', default=SRC_BASE_URL,
                    help='Base URL of the source MN to test')

  parser.add_option('--dst-base-url', dest='dst_base_url', action='store',
                    type='string', default=DST_BASE_URL,
                    help='Base URL of the destination MN to test')

  # Source and destination certificates.

  parser.add_option('--cert-get-replica', dest='cert_get_replica',
                    action='store', type='string',
                    help='Certificate to use when calling MNRead.getReplica()')

  parser.add_option('--cert-get-replica-key', dest='cert_get_replica_key',
                    action='store', type='string',
                    help='Certificate key to use when calling MNRead.getReplica()')

  parser.add_option('--cert-replicate', dest='cert_replicate',
                    action='store', type='string',
                    help='Certificate to use when calling MNReplication.replicate()')

  parser.add_option('--cert-replicate-key', dest='cert_replicate_key',
                    action='store', type='string',
                    help='Certificate key to use when calling MNReplication.replicate()')

  # System Metadata.

  parser.add_option('--rights-holder', dest='rights_holder', action='store',
                    type='string', default=SYSMETA_RIGHTSHOLDER,
                    help='The rights holder subject to use in generated system metadata')

  # Adjust RepTest behavior.

  parser.add_option('--timeout', dest='timeout', action='store',
                    type='float', default=TIMEOUT,
                    help='Amount of time to wait for expected calls from MNs, in seconds')

  parser.add_option('--only-src', action='store_true', default=False, dest='only_src',
                    help='Test only the source MN')

  parser.add_option('--only-dst', action='store_true', default=False, dest='only_dst',
                    help='Test only the destination MN')

  parser.add_option('--server-mode', action='store_true', default=False, dest='server_mode',
                    help='Do not run any tests. Just serve the supported CN and MN APIs.')


  parser.add_option('--reptest-base-url', dest='reptest_base_url', action='store',
                    type='string', default=REPTEST_BASE_URL,
                    help='Set the Base URL for the Replication Tester.')

  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  # Known identifiers.

  if len(args) != 3:
    print 'Required arguments: <src_existing_pid_reject> <src_existing_pid_approve> <dst_existing_pid>'
    parser.print_help()
    exit()

  if options.only_src and options.only_dst:
    print '--only-src and --only-dst are mutually exclusive'
    parser.print_help()
    exit()

  options.src_existing_pid_reject = args[0]
  options.src_existing_pid_approve = args[1]
  options.dst_existing_pid = args[2]

  if options.verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)

  # Since each step depends on the previous step in the DataONE replication
  # process, RepTest aborts on the first error.
  try:
    with ReplicationTester(options) as tester:
      if options.server_mode:
        logging.info('Server mode')
        while True:
          time.sleep(.1)
      #if not options.only_dst:
      #  tester.test_src_mn()
      if not options.only_src:
        tester.test_dst_mn()
  except ReplicationTesterError as e:
    logger.error('Replication testing failed: {0}'.format(e))
  else:
    logging.info('All replication tests passed')


class ReplicationTester():
  def __init__(self, options):
    self._options = options
    self._validate_cert_paths()
    self._queue = Queue.Queue()
    self._http_server = TestHTTPServer(self._options, self._queue)
    self._logger = logging.getLogger(self.__class__.__name__)


  def __enter__(self):
    self._http_server.start()
    time.sleep(2)
    return self


  def __exit__(self, type, value, traceback):
    self._http_server.stop()


  def test_src_mn(self):
    self._log_debug_header('Source MNRead.getReplica(PID_UNKNOWN)')
    self._test_getReplica_with_unknown_pid()
    self._log_debug_header('Source MNRead.getReplica(PID_EXISTING_REJECT)')
    self._test_getReplica_with_rejected_pid()
    self._log_debug_header('Source MNRead.getReplica(PID_EXISTING_APPROVE)')
    self._test_getReplica_with_approved_pid()


  def test_dst_mn(self):
    #self._log_debug_header('Destination MNReplication.replicate(PID_EXISTING)')
    #self._test_MNReplication_replicate_with_existing_pid()
    #self._log_debug_header('Destination MNReplication.replicate(PID_NOT_AUTHORIZED)')
    #self._test_MNReplication_replicate_with_unauthorized_pid()
    self._log_debug_header('Destination MNReplication.replicate(PID_KNOWN_AND_AUTHORIZED)')
    self._test_MNReplication_replicate_with_authorized_pid()

  #
  # Source MN tests
  #

  def _test_getReplica_with_unknown_pid(self):
    '''Test that the Source MN responds correctly to MNRead.getReplica()
    in which the identifier is unknown.
    '''
    try:
      self._call_src_get_replica(PID_UNKNOWN)
    except d1_common.types.exceptions.NotFound:
      pass
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'Source MNRead.getReplica(unknown PID): '
        'Expected NotFound exception. Received: {0}'.format(e))
    else:
      raise ReplicationTesterError(
        'Source MNRead.getReplica(unknown PID): '
        'Failed to raise exception')


  def _test_getReplica_with_rejected_pid(self):
    '''Test that the Source MN responds correctly on MNRead.getReplica()
    in which the identifier is valid but replication is rejected by the CN.
    '''
    try:
      self._call_src_get_replica(self._options.src_existing_pid_reject)
    except d1_common.types.exceptions.NotAuthorized:
      pass
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'Source MNRead.getReplica(valid PID with replication rejected): '
        'Expected NotAuthorized exception. Received: {0}'.format(e))
    else:
      raise ReplicationTesterError(
        'Source MNRead.getReplica(valid PID with replication rejected): '
        'Failed to raise exception')
    self._assert_correct_mn_call_instant('isNodeAuthorized_rejected',
      self._options.src_existing_pid_reject, 'public')


  def _test_getReplica_with_approved_pid(self):
    '''Test that the Source MN responds correctly on MNRead.getReplica()
    in which the identifier is valid and replication is approved by the CN.
    '''
    try:
      self._call_src_get_replica(self._options.src_existing_pid_approve)
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'Source MNRead.getReplica(valid PID with replication approved): '
        'Expected OctetStream. Received exception: {0}'.format(e))
    self._assert_correct_mn_call_instant('isNodeAuthorized_approved',
      self._options.src_existing_pid_approve, 'public')


  def _call_src_get_replica(self, pid):
    mn_client = self._create_mn_client_for_get_replica()
    try:
      return mn_client.getReplica(pid).read()
    except socket.error:
      raise ReplicationTesterError('Unable to connect to Source MN')


  def _create_mn_client_for_get_replica(self):
    return d1_client.mnclient.MemberNodeClient(
      self._options.src_base_url,
      cert_path=self._options.cert_get_replica,
      key_path=self._options.cert_get_replica_key)

  #
  # Destination MN tests
  #

  def _test_MNReplication_replicate_with_existing_pid(self):
    '''Test that the destination MN correctly rejects a replication request
    in which the identifier already exists on the MN.
    '''
    try:
      self._call_dst_replicate(self._options.dst_existing_pid)
    except d1_common.types.exceptions.IdentifierNotUnique:
      pass
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'MNReplication.replicate()(existing PID): '
        'Expected exception IdentifierNotUnique. Received: {0}'.format(e))
    else:
      raise ReplicationTesterError(
        'MNReplication.replicate()(existing PID): '
        'Failed to raise exception')


  def _test_MNReplication_replicate_with_unauthorized_pid(self):
    '''Test that the destination MN responds correctly on
    MNReplication.replicate() with an object that is valid for replication but
    for which the CN denies replication.
    '''
    try:
      self._call_dst_replicate(PID_NOT_AUTHORIZED)
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'MNReplication.replicate()(PID_NOT_AUTHORIZED): '
        'Expected MN to accept replication request. Instead, received exception: {0}'.format(e))
    self._assert_correct_mn_call_with_wait(
      'getReplica_NotAuthorized', PID_NOT_AUTHORIZED)
    self._assert_correct_mn_call_with_wait(
      'setReplicationStatus', PID_NOT_AUTHORIZED, 'failed')


  def _test_MNReplication_replicate_with_authorized_pid(self):
    '''Test that the destination MN responds correctly on
    MNReplication.replicate() with an object that is both valid for replication
    and approved for replication by the CN.
    '''
    try:
      self._call_dst_replicate(PID_KNOWN_AND_AUTHORIZED)
    except d1_common.types.exceptions.DataONEException as e:
      raise ReplicationTesterError(
        'MNReplication.replicate()(PID_KNOWN_AND_AUTHORIZED): '
        'Expected MN to accept replication request. Instead, received exception: {0}'.format(e))
    self._assert_correct_mn_call_with_wait(
      'getReplica_NotAuthorized', PID_KNOWN_AND_AUTHORIZED)
    self._assert_correct_mn_call_with_wait(
      'setReplicationStatus', PID_KNOWN_AND_AUTHORIZED, 'failed')


  def _call_dst_replicate(self, pid):
    mn_client = self._create_mn_client_for_replicate()
    object_generator = TestObjectGenerator()
    sys_meta = object_generator.create_science_object_with_sysmeta(pid,
      self._options.rights_holder)[0]
    try:
      mn_client.replicate(sys_meta, TEST_MN_NODE_ID)
    except socket.error:
      raise ReplicationTesterError('Unable to connect to Destination MN')


  def _create_mn_client_for_replicate(self):
    return d1_client.mnclient.MemberNodeClient(
      self._options.dst_base_url,
      cert_path=self._options.cert_replicate,
      key_path=self._options.cert_replicate_key)

  #
  # Shared
  #


  def _log_debug_header(self, msg):
    self._logger.debug('-' * 50)
    self._logger.info('Testing: {0}'.format(msg))


  def _assert_correct_mn_call_with_wait(self, *expected_call):
    return self._assert_correct_mn_call(True, expected_call)


  def _assert_correct_mn_call_instant(self, *expected_call):
    return self._assert_correct_mn_call(False, expected_call)


  def _assert_correct_mn_call(self, block, expected_call):
    if block:
      self._logger.debug('Waiting for call from MN: {0}'.format(expected_call))
    try:
      call = self._queue.get(block, self._options.timeout)
    except Queue.Empty:
      raise ReplicationTesterError('MN did not make expected call: {0}'
                                   .format(expected_call))
    else:
      if call != expected_call:
        raise ReplicationTesterError('MN made an unexpected call: {0}.\nExpected: {1}'
                                     .format(call, expected_call))


  def _validate_cert_paths(self):
    self._assert_if_invalid(self._options.cert_get_replica)
    self._assert_if_invalid(self._options.cert_get_replica_key)
    self._assert_if_invalid(self._options.cert_replicate)
    self._assert_if_invalid(self._options.cert_replicate_key)


  def _assert_if_invalid(self, path):
    if path is not None and not os.path.isfile(path):
      raise ReplicationTesterError('No certificate or key at path: {0}'.format(path))


class TestHTTPServer(threading.Thread):
  def __init__(self, options, queue):
    threading.Thread.__init__(self)
    # Daemon mode causes the Python app to exit when the main thread exits.
    # This lets the app be stopped with Ctrl-C without having to send signals
    # to the threads.
    self.daemon = True
    self._logger = logging.getLogger(self.__class__.__name__)
    self._options = options
    self._queue = queue


  def run(self):
    # Some magic to prevent the socket from hanging for a minute after the
    # script exits.
    SocketServer.TCPServer.allow_reuse_address = True
    #
    SocketServer.TCPServer._queue = self._queue
    SocketServer.TCPServer._options = self._options
    host, port = self._get_host_and_port(self._options.reptest_base_url)
    self._logger.info('Starting HTTP Server. Host={0} Port={1}'.format(host, port))
    self.httpd = SocketServer.TCPServer((host, port), Handler)
    self.httpd.serve_forever()


  def stop(self):
    self._logger.info('Stopping HTTP Server')
    self.httpd.shutdown()


  def _get_host_and_port(self, url, default_port=80):
    url_components = urlparse.urlparse(self._options.reptest_base_url)
    return (url_components.netloc.split(':')[0],
      default_port if url_components.port is None else url_components.port)


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    self._logger = logging.getLogger(self.__class__.__name__)
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)


  def do_GET(self):
    self._logger.debug('Received HTTP GET: {0}'.format(self.path))
    url = urlparse.urlparse(urllib.unquote(self.path))
    if self._handle_isNodeAuthorized(url):
      return
    elif self._handle_getReplica(url):
      return
    elif self._handle_listNodes(url):
      return
    elif self._handle_getSystemMetadata(url):
      return
    else:
      raise ReplicationTesterError('Unknown REST URL: {0}'.format(self.path))


  def do_PUT(self):
    self._logger.debug('Received HTTP PUT: {0}'.format(self.path))
    url = urlparse.urlparse(urllib.unquote(self.path))
    if self._handle_setReplicationStatus(url):
      return
    else:
      raise ReplicationTesterError('Unknown REST URL: {0}'.format(self.path))

  # Request handlers.

  def _handle_isNodeAuthorized(self, url):
    '''CNReplication.isNodeAuthorized(session, targetNodeSubject, pid) → boolean
    GET /replicaAuthorizations/{pid}?targetNodeSubject={targetNodeSubject}
    '''
    m = re.match(r'/v1/replicaAuthorizations/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    query = urlparse.parse_qs(url.query)
    target_node_subject = query['targetNodeSubject'][0]
    self._logger.debug('Handling call: isNodeAuthorized(pid={0}, dst_node={1})'
                       .format(pid, target_node_subject))
    if pid == self.server._options.src_existing_pid_approve:
      self._generate_response_success()
      self._record_mn_call('isNodeAuthorized_approved', pid, target_node_subject)
    elif pid == self.server._options.src_existing_pid_reject:
      self._generate_response_NotAuthorized()
      self._record_mn_call('isNodeAuthorized_rejected', pid, target_node_subject)
    else:
      raise ReplicationTesterError('Invalid Test PID: {0}'.format(pid))
    return True


  def _handle_getReplica(self, url):
    '''MNRead.getReplica(session, pid) → OctetStream
    GET /replica/{pid}

    For the purposes of testing, a call to MNRead.getReplica() can either be for
    an existing or unknown object and the certificate can either be accepted or
    rejected. Thus, there are 4 possible combinations. However, if the
    certificate is rejected, the client receives the same NotAuthorized
    exception regardless of if the object exists or not, which leaves 3
    combinations to be tested.
    '''
    m = re.match(r'/v1/replica/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    self._logger.debug('Handling call: getReplica(pid={0})'.format(pid))
    if pid == PID_NOT_AUTHORIZED:
      self._generate_response_NotAuthorized()
      self._record_mn_call('getReplica_NotAuthorized', pid)
    elif pid == PID_UNKNOWN:
      self._generate_response_NotFound()
      self._record_mn_call('getReplica_NotFound', pid)
    else:
      self._generate_response_OctetStream(pid)
      self._record_mn_call('getReplica_OctetStream', pid)
    return True


  def _handle_listNodes(self, url):
    # CNCore.listNodes() → NodeList
    # GET /node
    m = re.match(r'/v1/node$', url.path)
    if not m:
      return False
    self._generate_response_NodeList()
    return True


  def _handle_getSystemMetadata(self, url):
    '''MNRead.getSystemMetadata(session, pid) → SystemMetadata
    GET /meta/{pid}
    A MN may either save the System Metadata from the original MNReplication.replicate()
    call or pull it from the CN again when processing the request, to ensure
    that the latest version of the System Metadata is used.
    '''
    m = re.match(r'/v1/meta/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    self._logger.debug('Handling call: getSystemMetadata(pid={0})'.format(pid))
    self._generate_response_SystemMetadata(pid)
    return True


  def _handle_setReplicationStatus(self, url):
    '''CNReplication.setReplicationStatus(session, pid, nodeRef, status, failure) → boolean
    PUT /replicaNotifications/{pid}
    '''
    m = re.match(r'/v1/replicaNotifications/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    param_dict = cgi.parse_header(self.headers.getheader('Content-Type'))[1]
    multipart_fields = cgi.parse_multipart(self.rfile, param_dict)
    status = multipart_fields.get('status')[0]
    self._logger.debug('Handling call: setReplicationStatus(pid={0}, status={1})'.format(pid, status))
    self._generate_response_success()
    self._record_mn_call('setReplicationStatus', pid, status)
    return True

  # Response generators.

  def _generate_response_success(self):
    self._logger.debug('Responding with: 200 OK')
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write('ReplicationTester: Testing MN\'s response to 200 OK')


  def _generate_response_NotAuthorized(self):
    self._logger.debug('Responding with: NotAuthorized')
    exception = d1_common.types.exceptions.NotAuthorized(0)
    self.send_response(exception.errorCode)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(exception.serialize())


  def _generate_response_NotFound(self):
    self._logger.debug('Responding with: NotFound')
    exception = d1_common.types.exceptions.NotFound(0)
    self.send_response(exception.errorCode)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(exception.serialize())


  def _generate_response_OctetStream(self, pid):
    self._logger.debug('Responding with: science object bytes')
    self.send_response(200)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_OCTETSTREAM)
    self.end_headers()
    object_generator = TestObjectGenerator()
    object_bytes = object_generator.create_science_object_with_sysmeta(pid,
      self.server._options.rights_holder)[1]
    self.wfile.write(object_bytes)


  def _generate_response_SystemMetadata(self, pid):
    self._logger.debug('Responding with: System Metadata')
    self.send_response(200)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    object_generator = TestObjectGenerator()
    object_bytes = object_generator.create_science_object_with_sysmeta(pid,
      self.server._options.rights_holder)[0].toxml()
    self.wfile.write(object_bytes)


  def _generate_response_ServiceFailure(self, msg):
    self._logger.debug('Responding with: ServiceFailure')
    exception = d1_common.types.exceptions.ServiceFailure(0, msg)
    self.send_response(exception.errorCode)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(exception.serialize())


  def _generate_response_NodeList(self):
    # When debugging this function, remember that GMN caches the response.
    self._logger.debug('Responding with custom NodeList')
    #exception = d1_common.types.exceptions.NotAuthorized(0,
    #  'ReplicationTester: Testing MN\'s response to NotAuthorized')
    self.send_response(200)
    node_list = dataoneTypes.nodeList()
    node_list.append(self._create_cn_node_obj())
    node_list.append(self._create_mn_node_obj())
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(node_list.toxml())


  def _record_mn_call(self, *params):
    self._logger.debug('Recorded call: {0}'.format(', '.join(params)))
    self.server._queue.put(params)


  def _create_cn_node_obj(self):
    return self._create_node_obj(
      node_type='cn',
      node_id=TEST_CN_NODE_ID,
      name='test_cn',
      description='Simulated CN for replication testing',
      subject='public', # this becomes a trusted CN subject.
      service_name='CNCore'
    )


  def _create_mn_node_obj(self):
    return self._create_node_obj(
      node_type='mn',
      node_id=TEST_MN_NODE_ID,
      name='test_mn',
      description='Simulated MN for replication testing',
      subject='public_mn',
      service_name='MNCore'
    )


  def _create_node_obj(self, node_type, node_id, name, description, subject,
                       service_name):
    node_list = dataoneTypes.node()
    node_list.identifier = node_id
    node_list.name = name
    node_list.description = description
    node_list.baseURL = self.server._options.reptest_base_url
    node_list.contactSubject.append('ReplicationTesterContactSubject')
    node_list.replicate = True
    node_list.services = self._create_services_obj(service_name)
    node_list.subject.append(subject)
    node_list.synchronize = False
    node_list.type = node_type
    node_list.state = 'up'
    return node_list


  def _create_services_obj(self, service_name):
    services = dataoneTypes.services()
    service = dataoneTypes.service()
    service.name = service_name
    service.version = 'v1'
    service.available = True
    services.append(service)
    return services


class TestObjectGenerator():
  def __init__(self):
    pass


  def create_science_object_with_sysmeta(self, pid, rights_holder):
    # Seeding the prng with the pid causes the same object and system metadata
    # (checksum) to be returned for multiple calls with the same pid.
    random.seed(pid)
    sci_obj = self._create_science_object_bytes()
    sys_meta = self._generate_system_metadata_for_science_object(pid,
      FORMAT_ID, sci_obj, rights_holder)
    return sys_meta, sci_obj


  def _create_science_object_bytes(self):
    return random_data.random_bytes(N_SCI_OBJ_BYTES)


  def _generate_system_metadata_for_science_object(self, pid, format_id,
      science_object, rights_holder):
    size = len(science_object)
    md5 = hashlib.md5(science_object).hexdigest()
    now = datetime.datetime.now()
    sys_meta = self._generate_sys_meta(pid, format_id, size, md5, now,
                                       rights_holder)
    return sys_meta


  def _generate_sys_meta(self, pid, format_id, size, md5, now,
                         rights_holder):
    sys_meta = dataoneTypes.systemMetadata()
    sys_meta.identifier = pid
    sys_meta.formatId = format_id
    sys_meta.size = size
    sys_meta.rightsHolder = dataoneTypes.subject(rights_holder)
    sys_meta.checksum = dataoneTypes.checksum(md5)
    sys_meta.checksum.algorithm = 'MD5'
    sys_meta.dateUploaded = now
    sys_meta.dateSysMetadataModified = now
    sys_meta.accessPolicy = self._generate_public_access_policy()
    return sys_meta


  def _generate_public_access_policy(self):
    accessPolicy = dataoneTypes.accessPolicy()
    accessRule = dataoneTypes.AccessRule()
    accessRule.subject.append(d1_common.const.SUBJECT_PUBLIC)
    permission = dataoneTypes.Permission('read')
    accessRule.permission.append(permission)
    accessPolicy.append(accessRule)
    return accessPolicy


class ReplicationTesterError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)


if __name__ == '__main__':
  main()
