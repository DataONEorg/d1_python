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

# Stdlib.
import csv
import datetime
import glob
import hashlib
import os
import pprint
import re
import stat
import sys
import time
import uuid
import urllib
import urlparse
import httplib

import pickle

# Django.
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import Http404
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.utils.html import escape
from django.db.models import Avg, Max, Min, Count
from django.core.urlresolvers import *

from django.db import models
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, Count

# 3rd party.
try:
  import iso8601
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-setuptools\n')
  sys.stderr.write('     sudo easy_install http://pypi.python.org/packages/2.5/i/iso8601/iso8601-0.1.4-py2.5.egg\n')
  raise

# MN API.
import d1_common.exceptions
import d1_client.systemmetadata
import d1_client.client
import d1_common.types.objectlocationlist_serialization
import d1_common.types.pid_serialization
import d1_common.types.nodelist_serialization

# App.
import mn.models
import mn.util
import cn.models
import settings
import cn.util

class ObjectLocationList(d1_common.types.objectlocationlist_serialization.ObjectLocationList):
  def deserialize_db(self, obj):
    cfg = lambda key: mn.models.Node.objects.get(key=key).val

    objectLocation = d1_common.types.generated.dataoneTypes.ObjectLocation()

    objectLocation.nodepid = cfg('pid')
    objectLocation.baseURL = cfg('base_url')
    objectLocation.url = '{0}/object/{1}'.format(cfg('base_url'), obj.pid)

    self.object_location_list.objectLocation.append(objectLocation)
  
    self.object_location_list.pid = obj.pid
    
class NodeList(d1_common.types.nodelist_serialization.NodeList):
  def deserialize_db(self):
    '''
    :param:
    :return:
    '''
    cfg = lambda key: mn.models.Node.objects.get(key=key).val
    
    # Node
     
    # El.
    node = d1_common.types.generated.dataoneTypes.Node()
    node.pid = cfg('pid')
    node.name = cfg('version')
    node.description = cfg('description')
    node.baseURL = cfg('base_url')
    # Attr
    node.replicate = cfg('replicate')
    node.synchronize = cfg('synchronize')
    node.type = cfg('node_type')

    # Services
    
    services = d1_common.types.generated.dataoneTypes.Services()

    svc = d1_common.types.generated.dataoneTypes.Service()
    svc.name = cfg('service_name')
    svc.version = cfg('service_version')
    svc.available = cfg('service_available')
    
    # Methods
    
    methods = []
    
    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'session'
    method.rest = 'session/'
    method.implemented = 'true'
    methods.append(method)

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'object_collection'
    method.rest = 'object'
    method.implemented = 'true'
    methods.append(method)

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'get_object'
    method.rest = 'object/'
    method.implemented = 'true'
    methods.append(method)

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'get_meta'
    method.rest = 'meta/'
    method.implemented = 'true'
    methods.append(method)

    # Log

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'log_collection'
    method.rest = 'log'
    method.implemented = 'true'
    methods.append(method)

    # Health
    
    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'health_ping'
    method.rest = 'health/ping'
    method.implemented = 'true'
    methods.append(method)

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'health_status'
    method.rest = 'health/status'
    method.implemented = 'true'
    methods.append(method)

    # Monitor
    
    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'monitor_object'
    method.rest = 'monitor/object'
    method.implemented = 'true'
    methods.append(method)

    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'monitor_event'
    method.rest = 'monitor/event'
    method.implemented = 'true'
    methods.append(method)

    # Node
    
    method = d1_common.types.generated.dataoneTypes.ServiceMethod()
    method.name = 'node'
    method.rest = 'node'
    method.implemented = 'true'
    methods.append(method)
  
    # Diagnostics, debugging and testing.
    # inject_log
    # get_ip

    # Admin.
    # admin/doc
    # admin 

    svc.method = methods
    
    services.append(svc)

    node.services = services

    self.node_list.append(node)

def resolve(request, pid):
  if request.method == 'GET':
    return resolve_get(request, pid, head=False)
  
  if request.method == 'HEAD':
    return object_collection_get(request, pid, head=True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def resolve_get(request, pid, head):
  try:
    obj = mn.models.Object.objects.get(pid=pid)
  except: # mn.models.DoesNotExist
    raise d1_common.exceptions.NotFound(0, 'Non-existing object was requested', pid)
  
  object_location_list = ObjectLocationList()
  object_location_list.deserialize_db(obj)

  response = HttpResponse(object_location_list.serialize_xml(pretty=True))
  response['Content-Type'] = 'text/xml'
  
  return response

def node(request):
  if request.method == 'GET':
    return node_get(request)

  # Only GET accepted.
  return HttpResponseNotAllowed(['GET'])

def node_get(request):
#  node = NodeList()
#  node.deserialize_db()
#  response = HttpResponse(node.serialize_xml(pretty=True))
  try:
    node_registry = open(os.path.join(settings.STATIC_STORE_PATH, 'nodeRegistry.xml'))
  except EnvironmentError:
    raise d1_common.exceptions.ServiceFailure(0, 'Missing static node registry file')
  response = HttpResponse(node_registry)
  response['Content-Type'] = 'text/xml'
  
  return response

#
# Replication.
#

# CN_data_replication.setReplicationStatus(token, pid, status) → boolean
def set_replication_status(request, status, node_ref, pid):
  if request.method == 'GET':
    return set_replication_status_get(request, status, node_ref, pid)

  return HttpResponseNotAllowed(['GET'])

def set_replication_status_get(request, status, node_ref, pid):
  cn.util.set_replication_status(status, node_ref, pid)
  
  # Return the pid.
  pid = d1_common.types.pid_serialization.Identifier(pid)
  
  if 'HTTP_ACCEPT' in request.META:
    accept = request.META['HTTP_ACCEPT']
  else:
    accept = 'application/xml'

  doc, content_type = pid.serialize(accept)
  return HttpResponse(doc, mimetype=content_type)

#
# Testing.
#

def test_replicate(request, pid, src_node_ref, dst_node_ref):
  res = cn.util.test_replicate(pid, src_node_ref, dst_node_ref)
  return HttpResponse(res)

def test_set_replication_status_put(request, status, node_ref, pid):
  if settings.GMN_DEBUG != True:
    sys_log.info('client({0}): Attempted to access test_set_replication_status_put while not in DEBUG mode'.format(util.request_to_string(request)))
    raise d1_common.exceptions.InvalidRequest(0, 'Unsupported')

  return set_replication_status_put(request, status, node_ref, pid)

def test_get_sysmeta(request, pid):
  return HttpResponse(mn.util.pretty_xml(cn.util.get_sysmeta(pid)[1].toxml()), 'application/xml')

def test_get_replication_status(request, pid):
  if pid == '':
    pid = None

  status_list = cn.util.get_replication_status_list(pid)

  return render_to_response('test_get_replication_status.html',
                            {'status_list': status_list })

def test_get_replication_status_xml(request, pid):
  if pid == '':
    pid = None

  status_list = cn.util.get_replication_status_list(pid)

  return render_to_response('test_get_replication_status.xml',
                            {'status_list': status_list },
                            mimetype='application/xml')

def test_clear_replication_status(request, node_ref, pid):
  if node_ref == '':
    node_ref = None
  if pid == '':
    pid = None
  
  removed_count = cn.util.clear_replication_status(node_ref, pid)
  
  return HttpResponse('{0}'.format(removed_count), mimetype='text/plain')

