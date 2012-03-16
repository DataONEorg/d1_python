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
'''
:mod:`package`
==============

:Synopsis: Create a data package
:Created: 2011-03-13
:Author: DataONE (Pippin)
'''

# Stdlib.
import sys
import urlparse
import StringIO

# 3rd party
from rdflib import Namespace, URIRef
try:
  import foresite
  import foresite.utils
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write(
    '  available at: https://foresite-toolkit.googlecode.com/svn/foresite-python/trunk\n'
  )
  raise

# DataONE
# common
try:
  import d1_common.util as util
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_common.\n')
  raise
# libclient
try:
  import d1_client.mnclient as mnclient
  import d1_client.cnclient as cnclient
except ImportError as e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Please install d1_libclient.\n')
  raise
# cli
from print_level import *
import dataone
import cli_util
import system_metadata

## -- Constants.

GET_ENDPOINT = 'object'
META_ENDPOINT = 'meta'
RDFXML_FORMATID = 'http://www.w3.org/TR/rdf-syntax-grammar'

#-- Public (static) interface --------------------------------------------------


def create(session, name, pids):
  ''' Do the heavy lifting of creating a package.
  '''
  print_info('Creating package %s:' % name)

  # Find all of the scimeta objects
  package_objects = []
  for pid in pids:
    obj_url = _resolve_scimeta_url(session, pid)
    scidata_list = []
    if obj_url is None:
      print_error('Couldn\'t find any object with pid "%s"' % pid)
      break

    scimeta_url = obj_url.replace('/' + GET_ENDPOINT + '/', '/' + META_ENDPOINT + '/')
    scimeta_obj = _get_scimeta_obj(session, obj_url)
    scidata_dict = {'pid': pid, 'uri': obj_url}
    scidata_list.append(scidata_dict)
    package_objects.append(
      {
        'aggr_id': name,
        'scimeta_pid': pid,
        'scimeta_url': scimeta_url,
        'scimeta_obj': scimeta_obj,
        'scidata_list': scidata_list
      }
    )
  #
  # Add all of the objects
  submit = session.get('sysmeta', 'submitter')
  rights = session.get('sysmeta', 'rights-holder')
  orig_mn = session.get('sysmeta', 'origin-mn')
  auth_mn = session.get('sysmeta', 'authoritative-mn')
  pkg = Package(name, submit, rights, orig_mn, auth_mn)
  for package_object in package_objects:
    pkg.add(package_object)
  return pkg


def save(session, pkg):
  ''' Save the package in DataONE.
  '''
  pkg_xml = pkg.serialize('xml')

  algorithm = session.get('sysmeta', 'algorithm')
  hash_fcn = util.get_checksum_calculator_by_dataone_designator(algorithm)
  hash_fcn.update(pkg_xml)
  checksum = hash_fcn.hexdigest()

  access_policy = session.access_control.to_pyxb()
  replication_policy = session.replication_policy.to_pyxb()
  sysmeta_creator = system_metadata.system_metadata()
  sysmeta = sysmeta_creator.create_pyxb_object(
    session,
    pkg.pid,
    len(
      pkg_xml
    ),
    checksum,
    access_policy,
    replication_policy,
    formatId=RDFXML_FORMATID
  )

  client = PkgMNClient(session)
  flo = StringIO.StringIO(pkg_xml)
  response = client.create(pid=pkg.pid, obj=flo, sysmeta=sysmeta)
  if response is not None:
    return response.getvalue()
  else:
    return None


def get_host(url):
  '''Get the host component without the port number.
  '''
  url_dict = urlparse.urlparse(url)
  if url_dict.netloc is not None:
    host = url_dict.netloc
    ndx = host.find(":")
    if ndx > 0:
      host = host[:ndx]
    return host

#-- Public class ---------------------------------------------------------------


class Package(object):
  def __init__(
    self,
    pid,
    submitter=None,
    rights_holder=None,
    orig_mn=None,
    auth_mn=None,
    scimeta_pid=None
  ):
    ''' Create a package
    '''
    self.resmap = None
    #
    self.pid = pid
    self.submitter = submitter
    self.rights_holder = rights_holder
    self.orig_mn = orig_mn
    self.auth_mn = auth_mn
    if scimeta_pid is not None:
      self.add(scimeta_pid)

  def serialize(self, fmt='xml'):
    assert (
      fmt in (
        'xml', 'pretty-xml', 'n3', 'rdfa', 'json', 'pretty-json', 'turtle', 'nt', 'trix'
      )
    )
    if self.resmap.serializer is not None:
      self.resmap.serializer = None
    serializer = foresite.RdfLibSerializer(fmt)
    self.resmap.register_serialization(serializer)
    doc = self.resmap.get_serialization()
    return doc.data

  def add(self, package_object):
    ''' Add a scimeta object referenced by it's pid.  Throw an exception if
        the specified pid is not a scimeta object, or cannot be found.
    '''
    if self._is_metadata_format(package_object['scimeta_obj'].formatId):
      self._add_package(package_object)
    else:
      self._generate_package(package_object)

  def _add_package(self, scimeta):
    ''' The scimeta defines a package.  Use it to define the package.
    '''
    print_info('+ Using metadata to add an existing package')
    print_error('package._add_package() is not implemented!!!')

  def _generate_package(self, pkgobj):
    ''' The scimeta is part of a package.  Create a package.
    
        An example pkgobj looks like:
                {
                  'aggr_id': name,
                  'scimeta_pid': 'test-object'
                  'scimeta_url': 'https://demo1.test.dataone.org:443/knb/d1/mn/v1/meta/test-object'
                  'scimeta_obj': <d1_common.types.generated.dataoneTypes.SystemMetadata>,
                  'scidata_list':(
                                   {
                                     'pid': 'test-object',
                                     'uri': 'https://demo1.test.dataone.org:443/knb/d1/mn/v1/object/test-object'
                                   },
                                 )
                }
    '''
    print_info(' generating a new package...')

    # Create the aggregation
    foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
    aggr = foresite.Aggregation(pkgobj['aggr_id'])
    aggr._dcterms.title = 'Simple aggregation of science metadata and data.'

    # Create a reference to the science metadata
    uri_scimeta = URIRef(pkgobj['scimeta_url'])
    res_scimeta = foresite.AggregatedResource(uri_scimeta)
    res_scimeta._dcterms.identifier = pkgobj['scimeta_pid']
    res_scimeta._dcterms.description = 'A reference to a science metadata object using a DataONE identifier'

    # Create references to the science data
    for scidata_item in pkgobj['scidata_list']:
      uri_scidata = URIRef(scidata_item['uri'])
      res_scidata = foresite.AggregatedResource(uri_scidata)
      res_scidata._dcterms.identifier = scidata_item['pid']
      res_scidata._dcterms.description = 'A reference to a science data object using a DataONE identifier'
      res_scidata._cito.isDocumentedBy = uri_scimeta
      res_scimeta._cito.documents = uri_scidata
      aggr.add_resource(res_scidata)

    # Add this scimeta to the aggregate.
    aggr.add_resource(res_scimeta)

    # Create the resource map
    resmap_id = "resmap_%s" % pkgobj['aggr_id']
    self.resmap = foresite.ResourceMap("https://cn.dataone.org/object/%s" % resmap_id)
    self.resmap._dcterms.identifier = resmap_id
    self.resmap.set_aggregation(aggr)

  def _is_metadata_format(self, formatId):
    if formatId is None:
      return False
    elif ((len(formatId) >= 4) and (formatId[:4] == "eml:")):
      return True
    elif ((len(formatId) >= 9) and (formatId[:9] == "FGDC-STD-")):
      return True
    else:
      return False

#-- Private methods ------------------------------------------------------------


def _verbose(session):
  ''' Are we verbose?
  '''
  verbosity = session.get('cli', 'verbose')
  if verbosity is not None:
    return verbosity
  else:
    return False


def _resolve_scimeta_url(session, pid):
  ''' Get a URL on a member node of the pid.
  '''
  cnclient = PkgCNClient(session)
  try:
    locations = cnclient.resolve(pid)
    if locations is not None:
      for location in locations.objectLocation:
        return location.url # Just get one.
  except:
    exc_class, exc_msgs, exc_traceback = sys.exc_info()
    if exc_class.__name__ == 'NotFound':
      print_warn(' no such pid: %s' % pid)
    return None


def _get_scimeta_obj(session, obj_url):
  ''' Get the actual science metadata object of the url.
  '''
  mn = session.get('node', 'mn-url')
  mn_dict = urlparse.urlparse(mn)
  obj_dict = urlparse.urlparse(obj_url)
  #
  try:
    base = mn_dict.scheme + '://' + obj_dict.netloc + mn_dict.path
    ndx = obj_dict.path.find(GET_ENDPOINT)
    pid = obj_dict.path[(ndx + len(GET_ENDPOINT) + 1):]
    client = PkgMNClient(session, base)
    return client.getSystemMetadata(pid)
  except:
    cli_util._handle_unexpected_exception()
    return None

  #-- Utility classes ------------------------------------------------------------


class PkgMNClient(dataone.CLIClient, mnclient.MemberNodeClient):
  def __init__(self, session, mn_url=None):
    if mn_url is None:
      mn_url = session.get('node', 'mn-url')
    return super(PkgMNClient, self).__init__(session, base_url=mn_url)


class PkgCNClient(dataone.CLIClient, cnclient.CoordinatingNodeClient):
  def __init__(self, session, cn_url=None):
    if cn_url is None:
      cn_url = session.get('node', 'dataone-url')
    return super(PkgCNClient, self).__init__(session, base_url=cn_url)
