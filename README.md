# README for d1_pyore

d1_pyore is a python library and utilities for working with OAI-ORE documents.

## Dependencies:

  * rdflib >= 4.0
  * rdflib-jsonld
  * requests
  
## How to use

### A. Create an OAI-ORE document from a list of PIDs.

Given the text file pids.txt:

<pre>
# Comment line, separate the # from text with a space.
# These are example values for pids2ore
# First row = identifier for resource map object
# Second row = identifier for metadata document
# Subsquent rows = identifiers for data
# Blank rows are ignored
# White space is stripped from start and end of rows.

ore_pid_value
sci_meta_pid_value
data_pid_1
data_pid_2
data_pid_3
</pre>

Generate an OAI-ORE document by:

<pre>
cat pids.txt | pids2ore
</pre>

The rdf-xml ORE document will be sent to stdout. Different formats (e.g. n3, turtle, json-ld) may be specified with the --format parameter. 

RDF-xml output from the above example:

```xml
<rdf:RDF
   xmlns:cito="http://purl.org/spar/cito/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   xmlns:ore="http://www.openarchives.org/ore/terms/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value">
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation"/>
    <dcterms:identifier>sci_meta_pid_value</dcterms:identifier>
    <cito:documents rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/>
    <cito:documents rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
    <cito:documents rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/ore_pid_value">
    <rdf:type rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/>
    <ore:describes rdf:resource="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation"/>
    <dcterms:identifier>ore_pid_value</dcterms:identifier>
    <dcterms:creator>d1_pyore DataONE Python library</dcterms:creator>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_1">
    <dcterms:identifier>data_pid_1</dcterms:identifier>
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation"/>
    <cito:isDocumentedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation">
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_1"/>
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value"/>
    <ore:aggregates rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/>
    <rdf:type rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_3">
    <dcterms:identifier>data_pid_3</dcterms:identifier>
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation"/>
    <cito:isDocumentedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_3"/>
  </rdf:Description>
  <rdf:Description rdf:about="https://cn.dataone.org/cn/v2/resolve/data_pid_2">
    <dcterms:identifier>data_pid_2</dcterms:identifier>
    <ore:isAggregatedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation"/>
    <cito:isDocumentedBy rdf:resource="https://cn.dataone.org/cn/v2/resolve/data_pid_2"/>
  </rdf:Description>
  <rdf:Description rdf:about="http://www.openarchives.org/ore/terms/Aggregation">
    <rdfs:isDefinedBy rdf:resource="http://www.openarchives.org/ore/terms/"/>
    <rdfs:label>Aggregation</rdfs:label>
  </rdf:Description>
</rdf:RDF>
```

### B. Text dump of an OAI-ORE document

Given the rdf-xml OAI-ORE document from above saved as "test.xml", parse and dump out the contents in slightly more intelligable plain text:

<pre>
ore2txt test.xml
</pre>

<pre>
OAI-ORE Description

Resource Map Document PID: ore_pid_value
                       ID: https://cn.dataone.org/cn/v2/resolve/ore_pid_value

Aggregations

1: https://cn.dataone.org/cn/v2/resolve/ore_pid_value#aggregation
   Contents:
    1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
       pid: data_pid_1
    2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
       pid: data_pid_3
    3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
       pid: data_pid_2
    4:  id: https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value
       pid: sci_meta_pid_value

CITO:documents

The document:
1:  id: https://cn.dataone.org/cn/v2/resolve/sci_meta_pid_value   pid: sci_meta_pid_value

   describes:
    1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
       pid: data_pid_1
    2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
       pid: data_pid_2
    3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
       pid: data_pid_3

CITO:isDocumentedBy

The data:
1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
   pid: data_pid_1

   is described by:
    1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_1
       pid: data_pid_1

The data:
2:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
   pid: data_pid_3

   is described by:
    1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_3
       pid: data_pid_3

The data:
3:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
   pid: data_pid_2

   is described by:
    1:  id: https://cn.dataone.org/cn/v2/resolve/data_pid_2
       pid: data_pid_2
</pre>


### C. Create an ORE programmatically in Python

```python
import d1_pyore

pkg = d1_pyore.ResourceMap()
pkg.oreInitialize("pid_for_ore")
pkg.addMetadataDocument("pid_for_metadata")
pkg.addDataDocuments(["data_pid_1", "data_pid_2"], "pid_for_metadata")
print pkg.serialize(format="json-ld", indent=2)

```

```json
[
  {
    "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1",
    "http://purl.org/dc/terms/identifier": [
      {
        "@value": "data_pid_1"
      }
    ],
    "http://purl.org/spar/cito/isDocumentedBy": [
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
      }
    ]
  },
  {
    "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2",
    "http://purl.org/dc/terms/identifier": [
      {
        "@value": "data_pid_2"
      }
    ],
    "http://purl.org/spar/cito/isDocumentedBy": [
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
      }
    ]
  },
  {
    "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_metadata",
    "http://purl.org/dc/terms/identifier": [
      {
        "@value": "pid_for_metadata"
      }
    ],
    "http://purl.org/spar/cito/documents": [
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
      },
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
      }
    ]
  },
  {
    "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore",
    "@type": [
      "http://www.openarchives.org/ore/terms/ResourceMap"
    ],
    "http://purl.org/dc/terms/creator": [
      {
        "@value": "d1_pyore DataONE Python library"
      }
    ],
    "http://purl.org/dc/terms/identifier": [
      {
        "@value": "pid_for_ore"
      }
    ],
    "http://www.openarchives.org/ore/terms/describes": [
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore#aggregation"
      }
    ]
  },
  {
    "@id": "http://www.openarchives.org/ore/terms/Aggregation",
    "http://www.w3.org/2000/01/rdf-schema#isDefinedBy": [
      {
        "@id": "http://www.openarchives.org/ore/terms/"
      }
    ],
    "http://www.w3.org/2000/01/rdf-schema#label": [
      {
        "@value": "Aggregation"
      }
    ]
  },
  {
    "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_ore#aggregation",
    "@type": [
      "http://www.openarchives.org/ore/terms/Aggregation"
    ],
    "http://www.openarchives.org/ore/terms/aggregates": [
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_2"
      },
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/pid_for_metadata"
      },
      {
        "@id": "https://cn.dataone.org/cn/v2/resolve/data_pid_1"
      }
    ]
  }
]
```
