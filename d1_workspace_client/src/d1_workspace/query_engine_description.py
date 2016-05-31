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
''':mod:`query_engine_description`
==================================

:Synopsis:
 - Cache and manipulate a queryEngineDescription.
:Author: DataONE (Dahl)
'''

# Stdlib.
import logging
import urllib

# 3rd party.
#import pyxb

# D1.
import d1_common.types.generated.dataoneTypes_1_1 as dataoneTypes

# Set up logger for this module.
log = logging.getLogger(__name__)
# Set specific logging level for this module if specified.
try:
  log.setLevel(logging.getLevelName(logging.ONEDRIVE_MODULES[__name__]))
except (KeyError, AttributeError):
  pass


class QueryEngineDescription(object):
  def __init__(self):
    self.doc = None

  def download(self, query_url):
    i = urllib.urlopen(query_url)
    self.read(i)

  def load(self, xml_path):
    i = open(xml_path, 'rb').read()
    self.read(i)

  def read(self, xml_flo):
    self.doc = dataoneTypes.CreateFromDocument(xml_flo)

  def assert_is_initialized(self):
    assert self.doc is not None

  def get_query_engine_version(self):
    return self.doc.queryEngineVersion

  # TODO:
  #<xs:element name="querySchemaVersion" type="xs:string" minOccurs="0" maxOccurs="1">
  #  <xs:annotation>
  #    <xs:documentation>Version of the schema in use by the query engine, e.g. &quot;1.0.1&quot;</xs:documentation>
  #  </xs:annotation>
  #</xs:element>
  #<xs:element name="name" type="xs:string" minOccurs="1" maxOccurs="1">
  #  <xs:annotation>
  #    <xs:documentation>The full, human readable name of the query engine. For example:
  #      &quot;Apache SOLR&quot;</xs:documentation>
  #  </xs:annotation>
  #</xs:element>
  #<xs:element name="additionalInfo" type="d1:NonEmptyString" minOccurs="0" maxOccurs="unbounded">
  #  <xs:annotation>
  #    <xs:documentation>An optional human readable description of the query engine. This can be
  #      used to describe any special capabilities or intended uses for the query engine. For example,
  #      a query engine may be tuned to suit a particular audience or domain as opposed to providing
  #      a general purpose discovery mechanism.</xs:documentation>
  #    <xs:documentation>This field may also contain links to additional information about the query engine,
  #    such as documentation for the search syntax provided by the query engine implemntors.</xs:documentation>
  #    </xs:annotation>
  #</xs:element>
  #<xs:element name="queryField" type="d1_v1.1:QueryField" minOccurs="0" maxOccurs="unbounded">
  #  <xs:annotation>
  #    <xs:documentation>A list of query fields supported by the query engine.</xs:documentation>
  #  </xs:annotation>
  #</xs:element>
