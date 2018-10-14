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

import cgi
import http.server
import logging
import re
import socketserver
import threading
import urllib.error
import urllib.parse
import urllib.request

from . import replication_error
from . import test_object_generator

import d1_common.const
import d1_common.types.dataoneTypes_v1 as dataoneTypes

TEST_CN_NODE_ID = 'urn:node:RepTestCN'
TEST_MN_NODE_ID = 'urn:node:RepTestMN'


class TestHTTPServer(threading.Thread):
  def __init__(
      self,
      options,
      pid_unknown,
      pid_not_authorized,
      pid_known_and_authorized,
      src_existing_pid_approve,
      src_existing_pid_deny,
      queue,
  ):
    threading.Thread.__init__(self)
    # Daemon mode causes the Python app to exit when the main thread exits.
    # This lets the app be stopped with Ctrl-C without having to send signals
    # to the threads.
    self._logger = logging.getLogger(self.__class__.__name__)
    self._options = options
    self._host, self._port = self._get_host_and_port()
    self.pid_unknown = pid_unknown
    self.pid_not_authorized = pid_not_authorized
    self.pid_known_and_authorized = pid_known_and_authorized
    self.src_existing_pid_approve = src_existing_pid_approve
    self.src_existing_pid_deny = src_existing_pid_deny
    self._queue = queue
    self.daemon = True
    # Some magic to prevent the socket from hanging for a minute after the
    # script exits.
    socketserver.TCPServer.allow_reuse_address = True
    self.httpd = socketserver.TCPServer((self._host, self._port), Handler)

  def run(self):
    socketserver.TCPServer._queue = self._queue
    socketserver.TCPServer._options = self._options
    socketserver.TCPServer.pid_unknown = self.pid_unknown
    socketserver.TCPServer.pid_not_authorized = self.pid_not_authorized
    socketserver.TCPServer.pid_known_and_authorized = self.pid_known_and_authorized
    socketserver.TCPServer.src_existing_pid_approve = self.src_existing_pid_approve
    socketserver.TCPServer.src_existing_pid_deny = self.src_existing_pid_deny

    self._logger.info(
      'Starting HTTP Server. Host={} Port={}'.format(self._host, self._port)
    )
    self.httpd.serve_forever()

  def stop(self):
    self._logger.info('Stopping HTTP Server')
    self.httpd.shutdown()

  def _get_host_and_port(self, default_port=80):
    url_components = urllib.parse.urlparse(self._options.reptest_base_url)
    return (
      url_components.netloc.split(':')[0], default_port
      if url_components.port is None else url_components.port
    )


#===============================================================================


class Handler(http.server.SimpleHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    self._logger = logging.getLogger(self.__class__.__name__)
    http.server.SimpleHTTPRequestHandler.__init__(
      self, request, client_address, server
    )

  def do_GET(self):
    self._logger.debug('Received HTTP GET: {}'.format(self.path))
    url = urllib.parse.urlparse(urllib.parse.unquote(self.path))
    if self._handle_isNodeAuthorized(url):
      return
    elif self._handle_getReplica(url):
      return
    elif self._handle_listNodes(url):
      return
    elif self._handle_getSystemMetadata(url):
      return
    else:
      raise replication_error.ReplicationTesterError(
        'Unknown REST URL: {}'.format(self.path)
      )

  def do_PUT(self):
    self._logger.debug('Received HTTP PUT: {}'.format(self.path))
    url = urllib.parse.urlparse(urllib.parse.unquote(self.path))
    if self._handle_setReplicationStatus(url):
      return
    else:
      raise replication_error.ReplicationTesterError(
        'Unknown REST URL: {}'.format(self.path)
      )

  # Request handlers.

  def _handle_isNodeAuthorized(self, url):
    """CNReplication.isNodeAuthorized(session, targetNodeSubject, pid) → boolean
    GET /replicaAuthorizations/{pid}?targetNodeSubject={targetNodeSubject}
    """
    m = re.match(r'/v1/replicaAuthorizations/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    query = urllib.parse.parse_qs(url.query)
    target_node_subject = query['targetNodeSubject'][0]
    self._logger.debug(
      'Handling call: isNodeAuthorized() pid="{}", dst_node="{}")'
      .format(pid, target_node_subject)
    )
    if pid == self.server.src_existing_pid_approve:
      self._generate_response_success()
      self._record_mn_call(
        'isNodeAuthorized_approved', pid, target_node_subject
      )
    elif pid == self.server.src_existing_pid_deny:
      self._generate_response_NotAuthorized()
      self._record_mn_call(
        'isNodeAuthorized_rejected', pid, target_node_subject
      )
    else:
      raise replication_error.ReplicationTesterError(
        'Invalid Test PID: {}'.format(pid)
      )
    return True

  def _handle_getReplica(self, url):
    """MNRead.getReplica(session, pid) → OctetStream
    GET /replica/{pid}

    For the purposes of testing, a call to MNRead.getReplica() can either be for
    an existing or unknown object and the certificate can either be accepted or
    rejected. Thus, there are 4 possible combinations. However, if the
    certificate is rejected, the client receives the same NotAuthorized
    exception regardless of if the object exists or not, which leaves 3
    combinations to be tested.
    """
    m = re.match(r'/v1/replica/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    self._logger.debug('Handling call: getReplica() pid="{}")'.format(pid))
    if pid == self.server.pid_not_authorized:
      self._generate_response_NotAuthorized()
      self._record_mn_call('getReplica_NotAuthorized', pid)
    elif pid == self.server.pid_unknown:
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
    """MNRead.getSystemMetadata(session, pid) → SystemMetadata
    GET /meta/{pid}
    A MN may either save the System Metadata from the original MNReplication.replicate()
    call or pull it from the CN again when processing the request, to ensure
    that the latest version of the System Metadata is used.
    """
    m = re.match(r'/v1/meta/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    self._logger.debug(
      'Handling call: getSystemMetadata() pid="{}")'.format(pid)
    )
    self._generate_response_SystemMetadata(pid)
    return True

  def _handle_setReplicationStatus(self, url):
    """CNReplication.setReplicationStatus(session, pid, nodeRef, status, failure) → boolean
    PUT /replicaNotifications/{pid}
    """
    m = re.match(r'/v1/replicaNotifications/(.*)', url.path)
    if not m:
      return False
    pid = m.group(1)
    logging.debug(self.headers)
    param_dict = cgi.parse_header(self.headers.getheader('Content-Type'))[1]
    logging.debug(param_dict)
    multipart_fields = cgi.parse_multipart(self.rfile, param_dict)
    logging.debug(multipart_fields)
    status = multipart_fields.get('status')[0]
    self._logger.debug(
      'Handling call: setReplicationStatus() pid="{}", status="{}"'.
      format(pid, status)
    )
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
    self.wfile.write(exception.serialize_to_transport())

  def _generate_response_NotFound(self):
    self._logger.debug('Responding with: NotFound')
    exception = d1_common.types.exceptions.NotFound(0)
    self.send_response(exception.errorCode)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(exception.serialize_to_transport())

  def _generate_response_OctetStream(self, pid):
    self._logger.debug('Responding with: science object bytes')
    self.send_response(200)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_OCTET_STREAM)
    self.end_headers()
    object_bytes = test_object_generator.generate_science_object_with_sysmeta(
      pid
    )[1]
    self.wfile.write(object_bytes)

  def _generate_response_SystemMetadata(self, pid):
    self._logger.debug('Responding with: System Metadata')
    self.send_response(200)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    object_bytes = test_object_generator.generate_science_object_with_sysmeta(
      pid, include_revision_bool=True
    )[0].toxml('utf-8')
    self.wfile.write(object_bytes)

  def _generate_response_ServiceFailure(self, msg):
    self._logger.debug('Responding with: ServiceFailure')
    exception = d1_common.types.exceptions.ServiceFailure(0, msg)
    self.send_response(exception.errorCode)
    self.send_header('Content-type', d1_common.const.CONTENT_TYPE_XML)
    self.end_headers()
    self.wfile.write(exception.serialize_to_transport())

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
    self.wfile.write(node_list.toxml('utf-8'))

  def _record_mn_call(self, *params):
    self._logger.debug('Recorded call: {}'.format(', '.join(params)))
    self.server._queue.put(params)

  def _create_cn_node_obj(self):
    return self._create_node_obj(
      node_type='cn',
      node_id=TEST_CN_NODE_ID,
      name='test_cn',
      description='Simulated CN for replication testing',
      subject='public', # this becomes a trusted CN subject.
      service_name='CNCore',
    )

  def _create_mn_node_obj(self):
    return self._create_node_obj(
      node_type='mn',
      node_id=TEST_MN_NODE_ID,
      name='test_mn',
      description='Simulated MN for replication testing',
      subject='public_mn',
      service_name='MNCore',
    )

  def _create_node_obj(
      self, node_type, node_id, name, description, subject, service_name
  ):
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
