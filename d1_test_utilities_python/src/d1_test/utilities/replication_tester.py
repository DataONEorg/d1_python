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
  The Replication Tester is documented in the Utilities section of the
  dataone.test_utilities package on PyPI.
'''

## Stdlib.
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
import urllib2
import urlparse

import SimpleHTTPServer
import SocketServer
import Queue
#import StringIO

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
#import d1_common
#import d1_common.const
#import d1_client.data_package
import d1_client.mnclient

# App.
from d1_test.instance_generator import random_data, systemmetadata

# Defaults

# BaseURL for the Member Node. If the script is run on the same server as the
# Member Node, this can be localhost.
SRC_BASE_URL = 'http://localhost:8000'
DST_BASE_URL = 'http://localhost:8000'

# Paths to the certificates and keys to use when testing. If the certificate has
# the key embedded, the _KEY setting should be set to None.
#
# If the --anonymous option is used, these paths need not be valid.
#
# The certificate used when calling MNRead.getReplica() on the source MN. The
# source MN must trust this certificate as a valid destination MN.
CERTIFICATE_FOR_GET_REPLICA = './certificates/cert_get_replica.crt'
CERTIFICATE_FOR_GET_REPLICA_KEY = './certificates/cert_get_replica.key'
#
# The certificate used when calling MNReplication.replicate() on the destination
# MN. The destination MN must trust this certificate and allow the same level
# of access as it would a CN.
CERTIFICATE_FOR_REPLICATE = './certificates/cert_replicate.crt'
CERTIFICATE_FOR_REPLICATE_KEY = './certificates/cert_replicate.key'

# A known identifier (PID) to use when calling get MNRead.getReplica() on the
# source MN.
SRC_VALID_PID = 'dataone_test_object_pid'

# The formatId to use for the Science Object. It should be the ID of an Object
# Format that is registered in the DataONE Object Format Vocabulary. A list of
# valid IDs can be retrieved from https://cn.dataone.org/cn/v1/formats.
SYSMETA_FORMATID = 'application/octet-stream'


# The number of bytes in each science object.
N_SCI_OBJ_BYTES = 1024

# Port on which to listen for the MN calls.
HTTP_SERVER_PORT = 8080

# Network interface on which to listen for the MN calls.
HTTP_INTERFACE = '0.0.0.0' # 0.0.0.0 = INADDR_ANY, listen on all interfaces.

# Time to wait for MN calls, in seconds.
TIMEOUT = 10


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)

  parser = optparse.OptionParser()
  parser.add_option('--src-base-url', dest='src_base_url', action='store',
                    type='string', default=SRC_BASE_URL,
                    help='Base URL of the source MN to test')
  parser.add_option('--dst-base-url', dest='dst_base_url', action='store',
                    type='string', default=DST_BASE_URL,
                    help='Base URL of the destination MN to test')

  parser.add_option('--anonymous', action='store_true', default=False,
                    dest='anonymous',
                    help='Create connections without using certificates')

  parser.add_option('--cert-get-replica', dest='cert_get_replica', action='store',
                    type='string', default=CERTIFICATE_FOR_GET_REPLICA,
                    help='Certificate to use when calling MNRead.getReplica()')
  parser.add_option('--cert-get-replica-key', dest='cert_get_replica_key', action='store',
                    type='string', default=CERTIFICATE_FOR_GET_REPLICA_KEY,
                    help='Certificate key to use when calling MNRead.getReplica()')

  parser.add_option('--cert-replicate', dest='cert_replicate', action='store',
                    type='string', default=CERTIFICATE_FOR_REPLICATE,
                    help='Certificate to use when calling MNReplication.replicate()')
  parser.add_option('--cert-replicate-key', dest='cert_replicate_key', action='store',
                    type='string', default=CERTIFICATE_FOR_REPLICATE_KEY,
                    help='Certificate key to use when calling MNReplication.replicate()')

  parser.add_option('--src-valid-pid', dest='src_valid_pid', action='store',
                    type='string', default=SRC_VALID_PID,
                    help='A valid PID on the source MN to use when testing MNRead.getReplica()')

  parser.add_option('--timeout', dest='timeout', action='store',
                    type='int', default=TIMEOUT,
                    help='Amount of time to wait for expected calls from MNs, in seconds')

  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  if len(args) != 0:
    print 'This command does not take any arguments'
    parser.print_help()
    exit()

  if options.verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  try:
    with ReplicationTester(options) as tester:
      #time.sleep(10)
      tester.test_src_mn()
      #tester.test_dst_mn()
  except ReplicationTesterError as e:
    print 'Replication Tester failed: {0}'.format(e)


class ReplicationTester():
  def __init__(self, options):
    self._options = options
    if self._options.anonymous:
      self._clear_cert_paths()
    else:
      self._validate_cert_paths()
    self._queue = Queue.Queue()
    self._web_server = TestHTTPServer(self._queue)


  def __enter__(self):
    self._web_server.start()
    return self


  def __exit__(self, type, value, traceback):
    self._web_server.stop()


  def test_src_mn(self):
    self._test_src_invalid_pid_for_get_replica()
    self._test_src_valid_pid_for_get_replica()
    call = self._wait_for_mn_call()
    pid = self._generate_random_ascii_pid()


  def test_dst_mn(self):
    pass


  def _test_src_invalid_pid_for_get_replica(self):
    mn_client = self._create_mn_client_for_get_replica()
    try:
      mn_client.getReplica('invalid_pid_etgrvujhnicm').read()
      raise ReplicationTesterError('Source MN accepted MNRead.getReplica() with invalid PID')
    except socket.error:
      raise ReplicationTesterError('Unable to connect to Source MN')
    except d1_common.types.exceptions.DataONEException:
      # This call should return a DataONEException.
      pass


  def _test_src_valid_pid_for_get_replica(self):
    mn_client = self._create_mn_client_for_get_replica()
    try:
      mn_client.getReplica(self._options.src_valid_pid)
    except socket.error:
      raise ReplicationTesterError('Unable to connect to Source MN')
    except d1_common.types.exceptions.DataONEException:
      logging.debug('Source MN MNRead.getReplica() failed with valid PID')
      raise


  def _create_mn_client_for_get_replica(self):
    return d1_client.mnclient.MemberNodeClient(
        self._options.src_base_url,
        cert_path=self._options.cert_get_replica,
        key_path=self._options.cert_get_replica_key)


  def _test_dst_invalid_pid_for_replicate(self):
    self._mn_client = d1_client.mnclient.MemberNodeClient(
      self._options.dst_base_url,
      cert_path=self._options.cert_replicate,
      key_path=self._options.cert_replicate_key)


  #To test a source MN, the Replication Tester cals MNRead.getReplica() first
  #for an object known not to exist on the MN. The Tester expects the MN to
  #return an exception for this call.
  #
  #The tester then calls MNRead.getReplica() with an object that is valid on the
  #source MN and waits for the MN to call CNReplication.isNodeAuthorized(). The
  #tester returns "not authorized" for this call and then verifies that the MN
  #returns a NotAuthorized exception on the MNRead.getReplica() call.
  #
  #The tester then repeats the test, this time returning "authorized" for the
  #CNReplication.isNodeAuthorized() call and checks for a valid object return
  #from MNRead.getReplica().


  #- A CN determines that a new replica is needed for an object.
  #- The CN checks replication policies and creates a list of MNs that can hold the
  #  replica, called destination MNs below.
  #- The CN calls ``MNReplication.replicate()`` on the first destination MN in
  #t.send_replication_request(pid)
  #  the list.
  #
  #- The destination MN examines the request, which contains information about the
  #  object and the source MN, and returns a message, either accepting or rejecting
  #  the request. If the request i rejected, the CN tries the next destination MN
  #  in its list.
  #
  #- After accepting the request, the destination MN queues the request for
  #  asynchronous processing, so that requests can be processed serially while the
  #  MN is still immediately ready to accept another request.
  #
  #- The destination MN calls MNRead.getReplica() on the source MN, providing
  #  the object identifier and its node identifier (as part of the client side
  #  certificate).
  #
  #- The source MN calls CNReplication.isNodeAuthorized() with the object
  #  identifier and the name of the destination MN.
  #
  #- If the CN denies the replication, the source MN returns an exception to the
  #  destination MN. If the CN approves the connection, the source MN returns the
  #  object bytes to the destination MN.
  #
  #- The destination MN calls CNReplication.setReplicationStatus() on the CN
  #  to inform the about the success or failure of the replication.


  def _wait_for_mn_call(self):
    return self._queue.get(True, TIMEOUT)


  def _generate_random_ascii_pid(self):
    return ''.join(random.choice(string.ascii_uppercase +
      string.ascii_lowercase + string.digits) for x in range(10))


  def _create_science_object(self):
    return random_data.random_bytes_flo(N_SCI_OBJ_BYTES)


  def _clear_cert_paths(self):
    self._options.cert_get_replica = None
    self._options.cert_get_replica_key = None
    self._options.cert_replicate = None
    self._options.cert_replicate_key = None


  def _validate_cert_paths(self):
    self._assert_if_invalid(self._options.cert_get_replica)
    self._assert_if_invalid(self._options.cert_get_replica_key)
    self._assert_if_invalid(self._options.cert_replicate)
    self._assert_if_invalid(self._options.cert_replicate_key)


  def _assert_if_invalid(self, path):
    if not os.path.isfile(path):
      raise ReplicationTesterError('No certificate or key at path: {0}'.format(path))


  def _generate_system_metadata_for_science_object(pid, format_id, science_object):
    size = len(science_object)
    md5 = hashlib.md5(science_object).hexdigest()
    now = datetime.datetime.now()
    sys_meta = self._generate_sys_meta(pid, format_id, size, md5, now)
    return sys_meta


  def _generate_sys_meta(self, pid, format_id, size, md5, now):
    sys_meta = dataoneTypes.systemMetadata()
    sys_meta.identifier = pid
    sys_meta.formatId = format_id
    sys_meta.size = size
    sys_meta.rightsHolder = SYSMETA_RIGHTSHOLDER
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


class TestHTTPServer(threading.Thread):
  def __init__(self, queue):
    threading.Thread.__init__(self)
    self._queue = queue


  def run(self):
    logging.info('Starting HTTP Server')
    # Some magic to prevent the socket from hanging for a minute after the
    # script exits.
    SocketServer.TCPServer.allow_reuse_address = True
    SocketServer.TCPServer.queue = self._queue
    self.httpd = SocketServer.TCPServer(('', HTTP_SERVER_PORT), Handler)
    logging.info('Listening on port: {0}'.format(HTTP_SERVER_PORT))
    self.httpd.serve_forever()


  def stop(self):
    logging.info('Stopping HTTP Server')
    self.httpd.shutdown()


class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
    allow_reuse_address = True


  def do_GET(self):
    logging.debug('GET path: {0}'.format(self.path))
    url = urlparse.urlparse(self.path)
    # CNReplication.isNodeAuthorized(session, targetNodeSubject, pid) → boolean
    # GET /replicaAuthorizations/{pid}?targetNodeSubject={targetNodeSubject}
    if self._handle_replica_authorizations(url):
      return
    raise ReplicationTesterError('Unknown REST URL: {0}'.format(self.path))


  def _handle_replica_authorizations(self, url):
    m = re.match(r'/v1/replicaAuthorizations/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    query = urlparse.parse_qs(url.query)
    target_node_subject = query['targetNodeSubject'][0]
    logging.debug('PID: {0}'.format(pid))
    logging.debug('targetNodeSubject: {0}'.format(target_node_subject))
    self.server.queue.put(('replicaAuthorizations', pid, target_node_subject))
    self._generate_boolean_success()
    return True


  def _generate_boolean_success(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write('OK')


class ReplicationTesterError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)


if __name__ == '__main__':
  main()
