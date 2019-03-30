#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2019 DataONE
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

"""Generate an OAI-ORE document from stdin.

This script will take a list of identifiers, one per line and create a simple,
single metadata OAI-ORE document and output the result on stdout.

The first non-blank line will contain the identifier for the resource map
document.

The second non-blank line will contain the identifier for the metadata document.

Remaining rows are read until the stream is consumed, and these rows contain
identifiers for data objects described by the metadata document.

example:

$ cat pids.txt
a
b
c

$ cat pids.txt | pids2ore

<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:cito="http://purl.org/spar/cito/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:ore="http://www.openarchives.org/ore/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
  <rdf:Description rdf:about="http://www.openarchives.org/ore/terms/Aggregation">
    <rdfs:isDefinedBy rdf:resource="http://www.openarchives.org/ore/terms/"/>
    <rdfs:label>Aggregation</rdfs:label>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/c">
    <dcterms:identifier>c</dcterms:identifier>
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/a#aggregation"/>
    <cito:isDocumentedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/c"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/a">
    <ore:describes rdf:resource="https://cn.dataone.org/cn/v2/resolve/a#aggregation"/>
    <rdf:type rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/>
    <dcterms:identifier>a</dcterms:identifier>
    <dcterms:creator>d1_pyore DataONE Python library</dcterms:creator>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/a#aggregation">
    <rdf:type rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/>
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/b"/>
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/c"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/b">
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/a#aggregation"/>
    <dcterms:identifier>b</dcterms:identifier>
    <cito:documents rdf:resource="https://cn.dataone.org/cn/v2/resolve/c"/>
  </rdf:Description>
</rdf:RDF>

Different serializations are supported with the -f or --format parameter. e.g.:

$ cat pids.txt | pids2ore --format n3

@prefix cito: <http://purl.org/spar/cito/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix ore: <http://www.openarchives.org/ore/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://cn.dataone.org/cn/v2/resolve/a> a ore:ResourceMap ;
    dcterms:creator "d1_pyore DataONE Python library" ;
    dcterms:identifier "a" ;
    ore:describes <https://cn.dataone.org/cn/v2/resolve/a#aggregation> .

ore:Aggregation rdfs:label "Aggregation" ;
    rdfs:isDefinedBy ore: .

<https://cn.dataone.org/cn/v2/resolve/b> dcterms:identifier "b" ;
    cito:documents <https://cn.dataone.org/cn/v2/resolve/c> ;
    ore:isAggregatedBy <https://cn.dataone.org/cn/v2/resolve/a#aggregation> .

<https://cn.dataone.org/cn/v2/resolve/a#aggregation> a ore:Aggregation ;
    ore:aggregates <https://cn.dataone.org/cn/v2/resolve/b>,
        <https://cn.dataone.org/cn/v2/resolve/c> .

<https://cn.dataone.org/cn/v2/resolve/c> dcterms:identifier "c" ;
    cito:isDocumentedBy <https://cn.dataone.org/cn/v2/resolve/c> ;
    ore:isAggregatedBy <https://cn.dataone.org/cn/v2/resolve/a#aggregation> .

"""

import argparse
import logging
import sys

import d1_pyore

parser = argparse.ArgumentParser(description="stdin to OAI-ORE")

parser.add_argument(
    "-l",
    "--log",
    default=logging.WARN,
    type=int,
    help="Set the logging level (debug=10, error=40)",
)

parser.add_argument(
    "-f", "--format", default="xml", help="Specify the serialization format (xml)"
)

parser.add_argument(
    "-b",
    "--base_url",
    default=u"https://cn.dataone.org/cn",
    help="Specify the base URL for the resource map entity identifiers",
)

args = parser.parse_args()

if args.log not in (10, 20, 30, 40, 50):
    logging.basicConfig(level=logging.INFO)
    logging.warning("Invalid value %s for log level. Using 20 (INFO).", args.log)
else:
    logging.basicConfig(level=args.log)

print(d1_pyore.pids2ore(sys.stdin, fmt=args.format, base_url=args.base_url))
