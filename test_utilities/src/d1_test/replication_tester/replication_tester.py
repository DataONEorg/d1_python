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
Test replication request handling in source and destination MNs.

RepTest is documented in the Utilities section of the dataone.test_utilities
package on PyPI.
"""

# The DataONE terms for the two MNs involved in creating a replica is origin
# and target nodes. In this code, source/src and destination/dst is used
# instead.

import io
import logging
import optparse
import os
import queue
import socket
import sys
import time

import d1_common.const
import d1_common.types.exceptions
import d1_common.url

import d1_test.replication_tester.replication_error as replication_error
import d1_test.replication_tester.replication_server as replication_server
import d1_test.replication_tester.test_object_generator as test_object_generator
from d1_test.replication_tester.test_object_generator import \
  generate_random_ascii

import d1_client.mnclient

# Defaults. These can be modified on the command line.

# BaseURL for the Member Node to be tested. If the script is run on the same
# server as the Member Node, this can be localhost.
SRC_BASE_URL = 'http://localhost'
DST_BASE_URL = 'http://localhost'

# The Base URL to RepTest. The MNs being tested call back to this location. If
# RepTest runs on the same machine as the MN being tested, this can be set to
# localhost. If so, make sure that the port is set to a different port than the
# one used by the MN. Only HTTP is currently supported.
REPTEST_BASE_URL = 'http://localhost:8181'

# Time to wait for MN calls, in seconds.
TIMEOUT = 60

TEST_CN_NODE_ID = 'urn:node:RepTestCN'
TEST_MN_NODE_ID = 'urn:node:RepTestMN'


def main():
  logging.basicConfig(level=logging.DEBUG)
  logger = logging.getLogger('main')

  parser = optparse.OptionParser()

  # Base URLs

  parser.add_option(
    '--reptest-base-url', action='store', type='string',
    default=REPTEST_BASE_URL, help='Set the Base URL for the Replication Tester'
  )

  parser.add_option(
    '--src-base-url', action='store', type='string', default=SRC_BASE_URL,
    help='Base URL of the source MN to test'
  )

  parser.add_option(
    '--dst-base-url', action='store', type='string', default=DST_BASE_URL,
    help='Base URL of the destination MN to test'
  )

  # Source and destination certificates

  parser.add_option(
    '--cert-get-replica', action='store', type='string',
    help='Certificate to use when calling MNRead.getReplica()'
  )

  parser.add_option(
    '--cert-get-replica-key', action='store', type='string',
    help='Certificate key to use when calling MNRead.getReplica()'
  )

  parser.add_option(
    '--cert-replicate', action='store', type='string',
    help='Certificate to use when calling MNReplication.replicate()'
  )

  parser.add_option(
    '--cert-replicate-key', action='store', type='string',
    help='Certificate key to use when calling MNReplication.replicate()'
  )

  # Adjust RepTest behavior.

  parser.add_option(
    '--timeout', dest='timeout_sec', action='store', type='float',
    default=TIMEOUT,
    help='Amount of time to wait for expected calls from MNs, in seconds'
  )

  parser.add_option(
    '--only-src', action='store_true', help='Test only the source MN'
  )

  parser.add_option(
    '--only-dst', action='store_true', help='Test only the destination MN'
  )

  parser.add_option(
    '--server-mode', action='store_true',
    help='Do not run any tests. Just serve the supported CN and MN APIs'
  )

  parser.add_option('--debug', action='store_true')

  (options, args) = parser.parse_args()

  # Known identifiers.

  if options.only_src and options.only_dst:
    logging.error('--only-src and --only-dst are mutually exclusive')
    parser.print_help()
    sys.exit()

  logging.getLogger('').setLevel(
    logging.DEBUG if options.debug else logging.INFO
  )

  # A PID that is not known on the node receiving the call.
  pid_unknown = generate_random_ascii('replication_tester_pid_unknown')

  # A PID that will cause RepTest.getReplica() to return a NotAuthorized exception.
  pid_not_authorized = generate_random_ascii(
    'replication_tester_pid_not_authorized'
  )

  # A PID that will cause RepTest.getReplica() to return a valid OctetStream.
  pid_known_and_authorized = generate_random_ascii(
    'replication_tester_pid_known_and_authorized'
  )

  src_existing_pid_approve = generate_random_ascii('src_existing_pid_approve')
  src_existing_pid_deny = generate_random_ascii('src_existing_pid_deny')

  dst_existing_pid = generate_random_ascii('dst_existing_pid')

  # Run tests
  try:
    with ReplicationTester(
        options,
        pid_unknown,
        pid_not_authorized,
        pid_known_and_authorized,
        src_existing_pid_approve,
        src_existing_pid_deny,
        dst_existing_pid,
    ) as tester:
      if options.server_mode:
        logging.info('Server mode')
        while True:
          time.sleep(.1)
      else:
        # assert requests.get(
        #   d1_common.url.joinPathElements(
        #     options.src_base_url, 'diag', 'clear_replication_queue'
        #   )
        # ).ok
        # An existing PID that returns approved on isNodeAuthorized()
        create_test_object_on_mn(options.src_base_url, src_existing_pid_approve)
        # An existing PID that returns denied on isNodeAuthorized()
        create_test_object_on_mn(options.src_base_url, src_existing_pid_deny)
        # DST: Existing
        create_test_object_on_mn(options.dst_base_url, dst_existing_pid)

      if not options.only_dst:
        tester.test_src_mn()
      if not options.only_src:
        tester.test_dst_mn()
  except replication_error.ReplicationTesterError as e:
    logger.error('Replication testing failed: {}'.format(e))
  else:
    logging.info('All replication tests passed')


def create_test_object_on_mn(base_url, pid):
  sys_meta, sci_obj = test_object_generator.generate_science_object_with_sysmeta(
    pid
  )
  mn_client = d1_client.mnclient.MemberNodeClient(base_url, retries=1)
  # , cert_pem_path=self._options.cert_get_replica, cert_key_path=self._options.cert_get_replica_key
  mn_client.create(pid, io.StringIO(sci_obj), sys_meta)


#===============================================================================


class ReplicationTester(object):
  def __init__(
      self,
      options,
      pid_unknown,
      pid_not_authorized,
      pid_known_and_authorized,
      src_existing_pid_approve,
      src_existing_pid_deny,
      dst_existing_pid,
  ):
    self._options = options
    self._pid_unknown = pid_unknown
    self._pid_not_authorized = pid_not_authorized
    self._pid_known_and_authorized = pid_known_and_authorized
    self._src_existing_pid_approve = src_existing_pid_approve
    self._src_existing_pid_deny = src_existing_pid_deny
    self._dst_existing_pid = dst_existing_pid
    self._validate_cert_paths()
    self._queue = queue.Queue()
    self._http_server = replication_server.TestHTTPServer(
      self._options,
      pid_unknown,
      pid_not_authorized,
      pid_known_and_authorized,
      src_existing_pid_approve,
      src_existing_pid_deny,
      self._queue,
    )
    self._logger = logging.getLogger(self.__class__.__name__)

  def __enter__(self):
    self._http_server.start()
    time.sleep(2)
    return self

  # noinspection PyShadowingBuiltins
  def __exit__(self, type, value, traceback):
    self._http_server.stop()

  def test_src_mn(self):
    self._log_debug_header('Source MNRead.getReplica(PID_UNKNOWN)')
    self._test_getReplica_with_unknown_pid()
    self._log_debug_header('Source MNRead.getReplica(PID_EXISTING_REJECT)')
    self._test_getReplica_with_rejected_pid()
    self._log_debug_header('Source MNRead.getReplica(PID_EXISTING_APPROVE)')
    self._test_getReplica_with_approved_pid()
    pass

  def test_dst_mn(self):
    self._log_debug_header('Destination MNReplication.replicate(PID_EXISTING)')
    self._test_MNReplication_replicate_with_existing_pid()
    self._log_debug_header(
      'Destination MNReplication.replicate(PID_NOT_AUTHORIZED)'
    )
    self._test_MNReplication_replicate_with_unauthorized_pid()
    self._log_debug_header(
      'Destination MNReplication.replicate(PID_KNOWN_AND_AUTHORIZED)'
    )
    self._test_MNReplication_replicate_with_authorized_pid()
    pass

  #
  # Source MN tests
  #

  def _test_getReplica_with_unknown_pid(self):
    """Source MN responds correctly to MNRead.getReplica() in which the
    identifier is unknown.
    """
    try:
      self._call_src_get_replica(self._pid_unknown)
    except d1_common.types.exceptions.NotFound:
      pass
    except (
        d1_common.types.exceptions.DataONEException,
        replication_error.ReplicationTesterError,
    ) as e:
      raise replication_error.ReplicationTesterError(
        'Source MNRead.getReplica(unknown PID): '
        'Expected NotFound exception. Received: {}'.format(str(e))
      )

  def _test_getReplica_with_rejected_pid(self):
    """Source MN responds correctly on MNRead.getReplica()
    in which the identifier is valid but replication is rejected by the CN.
    """
    try:
      self._call_src_get_replica(self._src_existing_pid_deny)
    except d1_common.types.exceptions.NotAuthorized:
      pass
    except (
        d1_common.types.exceptions.DataONEException,
        replication_error.ReplicationTesterError,
    ) as e:
      raise replication_error.ReplicationTesterError(
        'Source MNRead.getReplica(valid PID with replication rejected): '
        'Expected NotAuthorized exception. Received: {}'.format(e)
      )
    self._assert_correct_mn_call_instant(
      'isNodeAuthorized_rejected', self._src_existing_pid_deny, 'public'
    )

  # def generate_science_object_with_sysmeta(self, pid, rights_holder):
  #   # Seeding the prng with the pid causes the same object and system metadata
  #   # (checksum) to be returned for multiple calls with the same pid.
  #   random.seed(pid)
  #   sci_obj = self._create_science_object_bytes()
  #   sys_meta = self._generate_system_metadata_for_science_object(
  #     pid, FORMAT_ID, sci_obj, rights_holder
  #   )
  #   return sys_meta, sci_obj
  #
  #

  def _test_getReplica_with_approved_pid(self):
    """Source MN responds correctly on MNRead.getReplica()
    in which the identifier is valid and replication is approved by the CN.
    """
    try:
      self._call_src_get_replica(self._src_existing_pid_approve)
    except d1_common.types.exceptions.DataONEException as e:
      raise replication_error.ReplicationTesterError(
        'Source MNRead.getReplica(valid PID with replication approved): '
        'Expected OctetStream. Received exception: {}'.format(e)
      )
    self._assert_correct_mn_call_instant(
      'isNodeAuthorized_approved', self._src_existing_pid_approve, 'public'
    )

  def _call_src_get_replica(self, pid):
    mn_client = self._create_mn_client_for_get_replica()
    try:
      return mn_client.getReplica(pid).content
    except socket.error:
      raise replication_error.ReplicationTesterError(
        'Unable to connect to Source MN'
      )

  def _create_mn_client_for_get_replica(self):
    return d1_client.mnclient.MemberNodeClient(
      self._options.src_base_url, cert_pem_path=self._options.cert_get_replica,
      cert_key_path=self._options.cert_get_replica_key, retries=1
    )

  #
  # Destination MN tests
  #

  def _test_MNReplication_replicate_with_existing_pid(self):
    """The destination MN correctly rejects a replication request in which the
    identifier already exists on the MN.
    """
    try:
      self._call_dst_replicate(self._dst_existing_pid)
    except d1_common.types.exceptions.IdentifierNotUnique:
      pass
    except d1_common.types.exceptions.DataONEException as e:
      raise replication_error.ReplicationTesterError(
        'MNReplication.replicate()(existing PID): '
        'Expected exception IdentifierNotUnique. Received: {}'.format(e)
      )
    else:
      raise replication_error.ReplicationTesterError(
        'MNReplication.replicate()(existing PID): '
        'Failed to raise exception'
      )

  def _test_MNReplication_replicate_with_unauthorized_pid(self):
    """The destination MN responds correctly on MNReplication.replicate() with
    an object that is valid for replication but for which the CN denies
    replication.
    """
    try:
      self._call_dst_replicate(self._pid_not_authorized)
    except d1_common.types.exceptions.DataONEException as e:
      raise replication_error.ReplicationTesterError(
        'MNReplication.replicate(PID_NOT_AUTHORIZED): '
        'Expected MN to accept replication request. Instead, received exception: {}'.
        format(e)
      )
    self._assert_correct_mn_call_with_wait(
      'getReplica_NotAuthorized', self._pid_not_authorized
    )
    self._assert_correct_mn_call_with_wait(
      'setReplicationStatus', self._pid_not_authorized, 'failed'
    )

  def _test_MNReplication_replicate_with_authorized_pid(self):
    """Test that the destination MN responds correctly on
    MNReplication.replicate() with an object that is both valid for replication
    and approved for replication by the CN.
    """
    try:
      self._call_dst_replicate(self._pid_known_and_authorized)
    except d1_common.types.exceptions.DataONEException as e:
      raise replication_error.ReplicationTesterError(
        'MNReplication.replicate()(PID_KNOWN_AND_AUTHORIZED): '
        'Expected MN to accept replication request. Instead, received exception: {}'.
        format(e)
      )
    self._assert_correct_mn_call_with_wait(
      'getReplica_OctetStream', self._pid_known_and_authorized
    )
    self._assert_correct_mn_call_with_wait(
      'setReplicationStatus', self._pid_known_and_authorized, 'completed'
    )

  def _call_dst_replicate(self, pid):
    mn_client = self._create_mn_client_for_replicate()
    sys_meta = test_object_generator.generate_science_object_with_sysmeta(pid)[0]
    try:
      mn_client.replicate(sys_meta, TEST_MN_NODE_ID)
    except socket.error:
      raise replication_error.ReplicationTesterError(
        'Unable to connect to Destination MN'
      )

  def _create_mn_client_for_replicate(self):
    return d1_client.mnclient.MemberNodeClient(
      self._options.dst_base_url, cert_pem_path=self._options.cert_replicate,
      cert_key_path=self._options.cert_replicate_key, retries=1
    )

  #
  # Shared
  #

  def _log_debug_header(self, msg):
    self._logger.debug('-' * 100)
    self._logger.info('Testing: {}'.format(msg))

  def _assert_correct_mn_call_with_wait(self, *expected_call):
    return self._assert_correct_mn_call(True, expected_call)

  def _assert_correct_mn_call_instant(self, *expected_call):
    return self._assert_correct_mn_call(False, expected_call)

  def _assert_correct_mn_call(self, block, expected_call):
    if block:
      self._logger.debug('Waiting for call from MN: {}'.format(expected_call))
    try:
      call = self._queue.get(block, self._options.timeout_sec)
    except queue.Empty:
      raise replication_error.ReplicationTesterError(
        'MN did not make expected call: {}'.format(expected_call)
      )
    else:
      if call != expected_call:
        raise replication_error.ReplicationTesterError(
          'MN made an unexpected call: {}.\nExpected: {}'
          .format(call, expected_call)
        )

  def _validate_cert_paths(self):
    self._assert_if_invalid(self._options.cert_get_replica)
    self._assert_if_invalid(self._options.cert_get_replica_key)
    self._assert_if_invalid(self._options.cert_replicate)
    self._assert_if_invalid(self._options.cert_replicate_key)

  def _assert_if_invalid(self, path):
    if path is not None and not os.path.isfile(path):
      raise replication_error.ReplicationTesterError(
        'No certificate or key at path: {}'.format(path)
      )


#===============================================================================

if __name__ == '__main__':
  sys.exit(main())
