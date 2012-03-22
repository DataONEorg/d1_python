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
:Created: 2012-03-13
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

# cli
from print_level import * #@UnusedWildImport
import cli_util
import cli_client
import system_metadata

## -- Constants.

GET_ENDPOINT = 'object'
META_ENDPOINT = 'meta'
RDFXML_FORMATID = 'http://www.w3.org/TR/rdf-syntax-grammar'

#-- Public (static) interface --------------------------------------------------


def create(session, name, pids):
  ''' Do the heavy lifting of creating a package.
  '''
  # Create the resource map.
  submit = session.get('sysmeta', 'submitter')
  rights = session.get('sysmeta', 'rights-holder')
  orig_mn = session.get('sysmeta', 'origin-mn')
  auth_mn = session.get('sysmeta', 'authoritative-mn')
  pkg = Package(name, submit, rights, orig_mn, auth_mn)

  # Find all of the scimeta objects
  package_objects = []
  for pid in pids:
    get_scimeta_url = _resolve_scimeta_url(session, pid)
    if get_scimeta_url is None:
      print_error('Couldn\'t find any object with pid "%s"' % pid)
      return None
    else:
      scimeta_url = get_scimeta_url.replace(
        '/' + GET_ENDPOINT + '/', '/' + META_ENDPOINT + '/'
      )
      scimeta_obj = _get_scimeta_obj(session, get_scimeta_url)
      package_objects.append(
        {
          'scimeta_obj': scimeta_obj,
          'scimeta_url': scimeta_url,
          'scidata_pid': pid,
          'scidata_url': get_scimeta_url
        }
      )

  pkg.finalize(package_objects)
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

  client = cli_client.CLIMNClient(session)
  flo = StringIO.StringIO(pkg_xml)
  response = client.create(pid=pkg.pid, obj=flo, sysmeta=sysmeta)
  if response is not None:
    return response.value()
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

  def finalize(self, package_objects):
    ''' Create the resource map.
    '''
    for package_object in package_objects:
      sysmeta_obj = package_object['scimeta_obj']
      if self._is_metadata_format(sysmeta_obj.formatId):
        self._add_inner_package_objects(package_objects, sysmeta_obj)

    return self._generate_resmap(package_objects)

  def _add_inner_package_objects(self, package_objects, sysmeta_obj):
    ''' The given sysmeta object actually defines a data package.  Process the
        package and add all of the thingsd specified to the package_object_list.
    '''
    print_info('+ Using metadata to add to an existing package')
    print_error('package._add_inner_package_objects() is not implemented!!!')

  def _generate_resmap(self, package_object_list):
    ''' The scimeta is part of a package.  Create a package.
    
        An example package_object item looks like:
                {
                  'scimeta_obj': <d1_common.types.generated.dataoneTypes.SystemMetadata>,
                  'scimeta_url': 'https://demo1.test.dataone.org:443/knb/d1/mn/v1/meta/test-object'
                  'scidata_pid':pid,
                  'scidata_url':get_scimeta_url
                }
    '''
    # Create the aggregation
    foresite.utils.namespaces['cito'] = Namespace("http://purl.org/spar/cito/")
    aggr = foresite.Aggregation(self.pid)
    aggr._dcterms.title = 'Simple aggregation of science metadata and data.'

    # Create references to the science data
    for item in package_object_list:
      # Create a reference to the science metadata
      scimeta_obj = item['scimeta_obj']
      scimeta_pid = scimeta_obj.identifier.value()
      uri_scimeta = URIRef(item['scimeta_url'])
      res_scimeta = foresite.AggregatedResource(uri_scimeta)
      res_scimeta._dcterms.identifier = scimeta_pid
      res_scimeta._dcterms.description = 'A reference to a science metadata object using a DataONE identifier'

      uri_scidata = URIRef(item['scidata_url'])
      res_scidata = foresite.AggregatedResource(uri_scidata)
      res_scidata._dcterms.identifier = item['scidata_pid']
      res_scidata._dcterms.description = 'A reference to a science data object using a DataONE identifier'
      res_scidata._cito.isDocumentedBy = uri_scimeta
      res_scimeta._cito.documents = uri_scidata

      aggr.add_resource(res_scimeta)
      aggr.add_resource(res_scidata)

    # Create the resource map
    resmap_id = "resmap_%s" % self.pid
    self.resmap = foresite.ResourceMap("https://cn.dataone.org/object/%s" % resmap_id)
    self.resmap._dcterms.identifier = resmap_id
    self.resmap.set_aggregation(aggr)
    return self.resmap

  def _is_metadata_format(self, formatId):
    ''' Check to see if this formatId specifies a resource map.
    '''
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
  cnclient = cli_client.CLICNClient(session)
  try:
    locations = cnclient.resolve(pid)
    if locations is not None:
      for location in locations.objectLocation:
        return location.url # Just get one.
  except:
    exc_class, exc_msgs, exc_traceback = sys.exc_info()
    if exc_class.__name__ == 'NotFound':
      print_warn(' no such pid: %s' % pid)
    cli_util._handle_unexpected_exception()
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
    client = cli_client.CLIMNClient(session, base)
    return client.getSystemMetadata(pid)
  except:
    cli_util._handle_unexpected_exception()
    return None
