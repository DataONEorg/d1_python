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
import d1_common.types.identifier_serialization

# App.
import mn.models
import cn.models
import settings

class ObjectLocationList(d1_common.types.objectlocationlist_serialization.ObjectLocationList):
  def deserialize_db(self, obj):
    cfg = lambda key: mn.models.Node.objects.get(key=key).val

    objectLocation = d1_common.types.generated.dataoneTypes.ObjectLocation()

    objectLocation.nodeIdentifier = cfg('identifier')
    objectLocation.baseURL = cfg('base_url')
    objectLocation.url = '{0}/object/{1}'.format(cfg('base_url'), obj.guid)

    self.object_location_list.objectLocation.append(objectLocation)
  
    self.object_location_list.identifier = obj.guid
    
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
    node.identifier = cfg('identifier')
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

def resolve(request, guid):
  if request.method == 'GET':
    return resolve_get(request, guid, head=False)
  
  if request.method == 'HEAD':
    return object_collection_get(request, guid, head=True)

  # Only GET and HEAD accepted.
  return HttpResponseNotAllowed(['GET', 'HEAD'])

def resolve_get(request, guid, head):
  try:
    obj = mn.models.Object.objects.get(guid=guid)
  except: # mn.models.DoesNotExist
    raise d1_common.exceptions.NotFound(0, 'Non-existing object was requested', guid)
  
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
  node = NodeList()
  node.deserialize_db()

  response = HttpResponse(node.serialize_xml(pretty=True))
  response['Content-Type'] = 'text/xml'
  
  return response

# CN_data_replication.setReplicationStatus(token, guid, status) → boolean
def set_replication_status(request, guid):
  if request.method == 'PUT':
    return set_replication_status_put(request, guid)

  # Only PUT accepted.
  return HttpResponseNotAllowed(['PUT'])

def set_replication_status_put(request, guid):
  object_replication_status = cn.models.Object_replication_status()
  object_replication_status.guid = guid
  object_replication_status.status = request.GET['status']
  object_replication_status.save()

  # Return the identifier.
  identifier = d1_common.types.identifier_serialization.Identifier(guid)
  
  if 'HTTP_ACCEPT' in request.META:
    accept = request.META['HTTP_ACCEPT']
  else:
    accept = 'application/xml'

  return HttpResponse(identifier.serialize(accept))
  