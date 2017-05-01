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
""":mod:`test_solr_client`
==========================

:Synopsis:
 - Test the SolrClient class.
:Author: DataONE (Dahl)
"""

# Stdlib
import logging
import sys
import unittest

# D1
import d1_client_onedrive.impl.clients.onedrive_solr_client as onedrive_solr_client

options = {}


class O():
  pass


# Example results

# GET /cn/v1/query/solr/?q=%2A%3A%2A
# rows=3
# indent=on
# facet=true
# facet.limit=3
# facet.mincount=1
# facet.sort=false
# facet.count=sort
# wt=python
# facet.field=origin
# facet.field=noBoundingBox
# facet.field=family
# facet.field=text
# facet.field=abstract
# facet.field=rightsHolder
# facet.field=LTERSite
# facet.field=site
# facet.field=namedLocation
# facet.field=topic
# facet.field=edition
# facet.field=geoform
# facet.field=phylum
# facet.field=gcmdKeyword
# facet.field=keywords
# facet.field=titlestr
# facet.field=id
# facet.field=decade
# facet.field=size
# facet.field=sku
# facet.field=isSpatial
# facet.field=documents
# facet.field=changePermission
# facet.field=authorLastName
# facet.field=author
# facet.field=species
# facet.field=source
# facet.field=formatId
# facet.field=obsoletes
# facet.field=fileID
# facet.field=obsoletedBy
# facet.field=parameter
# facet.field=kingdom
# facet.field=southBoundCoord
# facet.field=westBoundCoord
# facet.field=identifier
# facet.field=northBoundCoord
# facet.field=isPublic
# facet.field=formatType
# facet.field=resourceMap
# facet.field=readPermission
# facet.field=originator
# facet.field=keyConcept
# facet.field=writePermission
# facet.field=class
# facet.field=term
# facet.field=genus
# facet.field=eastBoundCoord
# facet.field=investigator
# facet.field=sensor
# facet.field=contactOrganization
# facet.field=title
# facet.field=project
# facet.field=presentationCat
# facet.field=scientificName
# facet.field=datasource
# facet.field=placeKey
# facet.field=submitter
# facet.field=isDocumentedBy
# facet.field=relatedOrganizations
# facet.field=order
# facet.field=purpose
# wt=python

example_query_result_1 = {
  'facet_counts': {
    'facet_dates': {},
    'facet_fields': {
      'LTERSite': [],
      'abstract': [u'\x010', 20, u'\x01000', 20, u'\x0110', 20],
      'author': ['Margaret McManus', 20],
      'authorLastName': ['McManus', 20],
      'changePermission':
        ['CN=Andy Pippin T6339,O=Google,C=US,DC=cilogon,DC=org', 2],
      'class': [],
      'contactOrganization': [
        'Partnership for Interdisciplinary Studies of Coastal Oceans (PISCO)',
        20
      ],
      'datasource': [
        'bogusAuthoritativeNode', 4, 'urn:node:mnDemo5', 5, 'urn:node:mnDevGMN',
        1350
      ],
      'decade': [],
      'documents': [],
      'eastBoundCoord': ['-122.08045', 20],
      'edition': [],
      'family': [],
      'fileID': [
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'FunctionalTest%3AsmdChange%3Aurn%3Anode%3AmnDevGMN', 1,
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'MNodeTierTests.gmn-dev.2012103144439129', 1,
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'MNodeTierTests.gmn-dev.201210315540483', 1
      ],
      'formatId':
        ['CF-1.4', 1, 'eml://ecoinformatics.org/eml-2.0.1', 20, 'text/csv', 3],
      'formatType': ['DATA', 1339, 'METADATA', 20],
      'gcmdKeyword': [],
      'genus': [],
      'geoform': [],
      'id': [
        'FunctionalTest:smdChange:urn:node:mnDevGMN', 1,
        'MNodeTierTests.20129415411786', 1,
        'MNodeTierTests.gmn-dev.2012103144439129', 1
      ],
      'identifier': ['001', 1, '002', 1, '01', 1],
      'investigator': ['McManus', 20],
      'isDocumentedBy': [],
      'isPublic': ['true', 1359],
      'isSpatial': [],
      'keyConcept': [],
      'keywords': [
        'California', 20,
        'EARTH SCIENCE : Oceans : Ocean Temperature : Water Temperature', 20,
        'IOOS', 20
      ],
      'kingdom': [],
      'namedLocation': [],
      'noBoundingBox': [],
      'northBoundCoord': ['36.94342', 20],
      'obsoletedBy': [],
      'obsoletes': [],
      'order': [],
      'origin': [
        'Margaret McManus', 20,
        'Partnership for Interdisciplinary Studies of Coastal Oceans (PISCO)',
        20
      ],
      'originator': [],
      'parameter': [],
      'phylum': [],
      'placeKey': [],
      'presentationCat': [],
      'project': [
        'Partnership for Interdisciplinary Studies of Coastal Oceans (PISCO)',
        20
      ],
      'purpose': [],
      'readPermission': ['public', 1359],
      'relatedOrganizations': [],
      'resourceMap': [],
      'rightsHolder': [
        'CN=Andy Pippin T6339,O=Google,C=US,DC=cilogon,DC=org', 3,
        'CN=Yaxing Wei A1647,O=Google,C=US,DC=cilogon,DC=org', 1,
        'CN=testPerson,DC=dataone,DC=org', 40
      ],
      'scientificName': [],
      'sensor': [],
      'site': [],
      'size': ['33', 2, '58', 1, '73', 2],
      'sku': ['001', 1, '002', 1, '01', 1],
      'source': [],
      'southBoundCoord': ['36.94342', 20],
      'species': [],
      'submitter': [
        'CN=Andy Pippin T6339,O=Google,C=US,DC=cilogon,DC=org', 3,
        'CN=Yaxing Wei A1647,O=Google,C=US,DC=cilogon,DC=org', 1,
        'CN=testPerson,DC=dataone,DC=org', 40
      ],
      'term': [],
      'text': [u'\x010', 20, u'\x0100', 20, u'\x01000', 20],
      'title': [u'\x01100tpt', 20, u'\x01ainrofilac', 20, u'\x01asu', 20],
      'titlestr': [
        'PISCO: Physical Oceanography: moored temperature data: '
        'Terrace Point, California, USA (TPT001)', 20
      ],
      'topic': [],
      'westBoundCoord': ['-122.08045', 20],
      'writePermission': []
    },
    'facet_queries': {},
    'facet_ranges': {}
  },
  'response': {
    'docs': [{
      'authoritativeMN':
        'urn:node:mnDevGMN',
      'checksum':
        '4504b4dd97f2d7a4766dfaaa3f968ec2',
      'checksumAlgorithm':
        'MD5',
      'dataUrl':
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'testMNodeTier3%3A201211113474372_common-unicode-ascii-safe-'
        '%3A%40%24-_.%21*%28%29%27%2C%7E',
      'datasource':
        'urn:node:mnDevGMN',
      'dateModified':
        '2012-08-14T22:29:33.779Z',
      'dateUploaded':
        '2012-04-20T20:47:03.48Z',
      'formatId':
        'text/plain',
      'formatType':
        'DATA',
      'id':
        "testMNodeTier3:201211113474372_common-unicode-ascii-safe-:@$-_.!*()',~",
      'identifier':
        "testMNodeTier3:201211113474372_common-unicode-ascii-safe-:@$-_.!*()',~",
      'isPublic':
        True,
      'readPermission': ['public'],
      'replicaMN': ['urn:node:mnDevGMN'],
      'replicaVerifiedDate': ['2012-08-14T00:00:00Z'],
      'replicationAllowed':
        False,
      'rightsHolder':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'size':
        684336,
      'sku':
        "testMNodeTier3:201211113474372_common-unicode-ascii-safe-:@$-_.!*()',~",
      'submitter':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'updateDate':
        '2012-04-20T20:47:03.48Z'
    }, {
      'authoritativeMN':
        'urn:node:mnDevGMN',
      'checksum':
        '4504b4dd97f2d7a4766dfaaa3f968ec2',
      'checksumAlgorithm':
        'MD5',
      'dataUrl':
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'testMNodeTier3%3A2012115174435840_path-ascii-doc-example-10.1000%2F182',
      'datasource':
        'urn:node:mnDevGMN',
      'dateModified':
        '2012-08-14T22:34:06.029Z',
      'dateUploaded':
        '2012-04-25T00:44:34.993Z',
      'formatId':
        'text/plain',
      'formatType':
        'DATA',
      'id':
        'testMNodeTier3:2012115174435840_path-ascii-doc-example-10.1000/182',
      'identifier':
        'testMNodeTier3:2012115174435840_path-ascii-doc-example-10.1000/182',
      'isPublic':
        True,
      'readPermission': ['public'],
      'replicaMN': ['urn:node:mnDevGMN'],
      'replicaVerifiedDate': ['2012-08-14T00:00:00Z'],
      'replicationAllowed':
        False,
      'rightsHolder':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'size':
        684336,
      'sku':
        'testMNodeTier3:2012115174435840_path-ascii-doc-example-10.1000/182',
      'submitter':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'updateDate':
        '2012-04-25T00:44:34.993Z'
    }, {
      'authoritativeMN':
        'urn:node:mnDevGMN',
      'checksum':
        '4504b4dd97f2d7a4766dfaaa3f968ec2',
      'checksumAlgorithm':
        'MD5',
      'dataUrl':
        'https://cn-dev-ucsb-1.test.dataone.org/cn/v1/resolve/'
        'testMNodeTier3%3A2012111135753253_path-ascii-doc-example-'
        '10.1000%2F182',
      'datasource':
        'urn:node:mnDevGMN',
      'dateModified':
        '2012-08-14T22:30:09.482Z',
      'dateUploaded':
        '2012-04-20T20:57:52.369Z',
      'formatId':
        'text/plain',
      'formatType':
        'DATA',
      'id':
        'testMNodeTier3:2012111135753253_path-ascii-doc-example-10.1000/182',
      'identifier':
        'testMNodeTier3:2012111135753253_path-ascii-doc-example-10.1000/182',
      'isPublic':
        True,
      'readPermission': ['public'],
      'replicaMN': ['urn:node:mnDevGMN'],
      'replicaVerifiedDate': ['2012-08-14T00:00:00Z'],
      'replicationAllowed':
        False,
      'rightsHolder':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'size':
        684336,
      'sku':
        'testMNodeTier3:2012111135753253_path-ascii-doc-example-10.1000/182',
      'submitter':
        'CN=testRightsHolder,DC=dataone,DC=org',
      'updateDate':
        '2012-04-20T20:57:52.369Z'
    }],
    'numFound':
      1359,
    'start':
      0
  },
  'responseHeader': {
    'QTime': 264,
    'params': {
      'facet':
        'true',
      'facet.count':
        'sort',
      'facet.field': [
        'origin', 'noBoundingBox', 'family', 'text', 'abstract', 'rightsHolder',
        'LTERSite', 'site', 'namedLocation', 'topic', 'edition', 'geoform',
        'phylum', 'gcmdKeyword', 'keywords', 'titlestr', 'id', 'decade', 'size',
        'sku', 'isSpatial', 'documents', 'changePermission', 'authorLastName',
        'author', 'species', 'source', 'formatId', 'obsoletes', 'fileID',
        'obsoletedBy', 'parameter', 'kingdom', 'southBoundCoord',
        'westBoundCoord', 'identifier', 'northBoundCoord', 'isPublic',
        'formatType', 'resourceMap', 'readPermission', 'originator',
        'keyConcept', 'writePermission', 'class', 'term', 'genus',
        'eastBoundCoord', 'investigator', 'sensor', 'contactOrganization',
        'title', 'project', 'presentationCat', 'scientificName', 'datasource',
        'placeKey', 'submitter', 'isDocumentedBy', 'relatedOrganizations',
        'order', 'purpose'
      ],
      'facet.limit':
        '3',
      'facet.mincount':
        '1',
      'facet.sort':
        'false',
      'indent':
        'on',
      'q':
        '*:*',
      'rows':
        '3',
      'wt': ['python', 'python']
    },
    'status': 0
  }
}


class TestSolrClient(unittest.TestCase):
  def setUp(self):
    options = O()
    options.base_url = 'https://localhost/'
    options.solr_query_path = ''
    options.solr_query_timeout_sec = 30
    options.max_objects_for_query = 10
    self.c = onedrive_solr_client.SolrClient(options)

  def test_0010(self):
    """instantiate: """
    pass

  #  r = self.c.parse_result_dict(example_query_result_1)

  #def _test_300_parse_result(self):
  #  r = self.c.parse_result_dict(example_query_result_1)

  ##qes = query_engine_description.QueryEngineDescription()
  #qes.load('test_index/query_engine_description.xml')
  #self.s = solr_query.SolrQuery(qes)
  #self.facet_path_parser = facet_path_parser.FacetPathParser()

  #def test_100_query(self):
  #  print self.s.query('/')
  #
  #
  #def _test_100_query(self):
  #  dir_items = self.s.query('/')
  #  self._assert_is_facet_name_list(dir_items)
  #  dir_items = self.s.query('/@origin/#test/')
  #  self._assert_is_facet_name_list(dir_items)
  #
  #
  #def test_200_create_facet_query_string(self):
  #  str = self.s.create_facet_query_string('/test')
  #  self.assertTrue(str.startswith('facet.field=origin&facet.field=noBoundingBox&facet.field=endDate'))
  #  str = self.s.create_facet_query_string('/@origin/#a/@noBoundingBox/#b')
  #  self.assertTrue(str.startswith('facet.field=projectText&facet.field=endDate&facet.field=family'))
  #
  #
  #def _assert_is_facet_name_list(self, dir_items):
  #  for dir_item in dir_items:
  #    self.assertTrue(self.facet_path_parser.is_facet_name(dir_item))

  #===============================================================================


def log_setup():
  formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
  )
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


def main():
  import optparse

  log_setup()

  # Command line opts.
  parser = optparse.OptionParser()
  parser.add_option('--debug', action='store_true', default=False, dest='debug')
  parser.add_option(
    '--test', action='store', default='', dest='test', help='run a single test'
  )

  (options, arguments) = parser.parse_args()

  if options.debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.ERROR)

  s = TestSolrClient
  s.options = options

  if options.test != '':
    suite = unittest.TestSuite(map(s, [options.test]))
  else:
    suite = unittest.TestLoader().loadTestsFromTestCase(s)

  unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  main()
