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
"""Read and write DataONE OAI-ORE Resource Maps.

Includes convenience functions to perform the most common parsing and generating
tasks for Resource Maps.

For more information about how Resource Maps are used in DataONE, see:

https://releases.dataone.org/online/api-documentation-v2.0.1/design/DataPackage.html

<objectFormat>
  <formatId>http://www.openarchives.org/ore/terms</formatId>
  <formatName>Object Reuse and Exchange Vocabulary</formatName>
  <formatType>RESOURCE</formatType>
  <mediaType name="application/rdf+xml"/>
  <extension>rdf</extension>
</objectFormat>
"""

import logging

import rdflib
import rdflib.tools.rdf2dot

import d1_common.const
import d1_common.type_conversions
import d1_common.url
import d1_common.util

# RDFLib wrappers around the namespaces. Others are defined by RDFLib
DCTERMS = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT['dcterms'])
CITO = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT['cito'])
ORE = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT['ore'])


def createSimpleResourceMap(ore_pid, scimeta_pid, sciobj_pid_list):
  """Create a simple resource map with one science metadata document and any
  number of science data objects.
  """
  ore = ResourceMap()
  ore.oreInitialize(ore_pid)
  ore.addMetadataDocument(scimeta_pid)
  ore.addDataDocuments(sciobj_pid_list, scimeta_pid)
  return ore


def createResourceMapFromStream(
    in_stream, base_url=d1_common.const.URL_DATAONE_ROOT
):
  """Create a simple resource map from a stream that contains a list of
  identifiers.

  The first non-blank line is the PID of the resource map itself. Second line
  is the science metadata PID and remaining lines are science data PIDs.

  Example stream:

  PID_ORE_value
  sci_meta_pid_value
  data_pid_1
  data_pid_2
  data_pid_3
  """
  pids = []
  for line in in_stream:
    pid = line.strip()
    if pid == '#' or pid.startswith('# '):
      continue

  if len(pids) < 2:
    raise ValueError('Insufficient identifiers provided.')

  logging.info('Read {} identifiers'.format(len(pids)))
  ore = ResourceMap(base_url=base_url)
  logging.info('ORE PID = {}'.format(pids[0]))
  ore.oreInitialize(pids[0])
  logging.info('Metadata PID = {}'.format(pids[1]))
  ore.addMetadataDocument(pids[1])
  ore.addDataDocuments(pids[2:], pids[1])

  return ore


# ===============================================================================


class ResourceMap(rdflib.ConjunctiveGraph):
  """Subclasses ConjunctiveGraph to provide OAI-ORE functionality for
  DataONE."""

  def __init__(
      self, ore_pid=None, scimeta_pid=None, scidata_pid_list=None,
      base_url=d1_common.const.URL_DATAONE_ROOT, api_major=2, debug=True,
      ore_software_id=d1_common.const.ORE_SOFTWARE_ID, *args, **kwargs
  ):
    """Initialize the Graph instance."""
    super().__init__(*args, **kwargs)
    self._base_url = base_url
    self._version_tag = d1_common.type_conversions.get_version_tag(api_major)
    self._ore_initialized = False
    if ore_pid:
      self.oreInitialize(ore_pid, ore_software_id)
    if scimeta_pid:
      self.addMetadataDocument(scimeta_pid)
      if scidata_pid_list:
        self.addDataDocuments(scidata_pid_list, scimeta_pid)

  def oreInitialize(self, pid, ore_software_id=d1_common.const.ORE_SOFTWARE_ID):
    """Creates the basic ORE document structure."""
    # Set nice prefixes for the namespaces
    for k in list(d1_common.const.ORE_NAMESPACE_DICT.keys()):
      self.bind(k, d1_common.const.ORE_NAMESPACE_DICT[k])
    # Create the ORE entity
    oid = self._pid_to_id(pid)
    ore = rdflib.URIRef(oid)
    self.add((ore, rdflib.RDF.type, ORE.ResourceMap))
    self.add((ore, DCTERMS.identifier, rdflib.term.Literal(pid)))
    self.add((ore, DCTERMS.creator, rdflib.term.Literal(ore_software_id)))
    # Add an empty aggregation
    ag = rdflib.URIRef(d1_common.url.joinPathElements(oid, 'aggregation'))
    self.add((ore, ORE.describes, ag))
    self.add((ag, rdflib.RDF.type, ORE.Aggregation))
    self.add((ORE.Aggregation, rdflib.RDFS.isDefinedBy, ORE.term('')))
    self.add(
      (ORE.Aggregation, rdflib.RDFS.label, rdflib.term.Literal('Aggregation'))
    )
    self._ore_initialized = True

  def serialize_to_transport(self, doc_format='xml', *args, **kwargs):
    """Serialize to ResouceMap UTF-8 encoded bytes
    doc_format can be:
      'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig' and 'nquads'
    """
    return super(
      ResourceMap, self
    ).serialize(format=doc_format, encoding='utf-8', *args, **kwargs)

  def serialize_to_display(self, doc_format='pretty-xml', *args, **kwargs):
    """Serialize to Resouce Map document.
    doc_format can be:
      'xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig' and 'nquads'
    """
    return super(ResourceMap, self
                 ).serialize(format=doc_format, encoding=None, *args, **kwargs
                             ).decode('utf-8')

  def deserialize(self, *args, **kwargs):
    """Deserialize a Resource Map document

    The source is specified using one of source, location, file or
    data.

    :Parameters:

    - `source`: An InputSource, file-like object, or string. In the case of a
    string the string is the location of the source.
    - `location`: A string indicating the relative or absolute URL of the
    source. Graph's absolutize method is used if a relative location is
    specified.
    - `file`: A file-like object.
    - `data`: A string containing the data to be parsed.
    - `format`: Used if format can not be determined from source. Defaults to
    rdf/xml. Format support can be extended with plugins, but 'xml', 'n3', 'nt',
    'trix', 'rdfa' are built in.
    - `publicID`: the logical URI to use as the document base. If None specified
    the document location is used (at least in the case where there is a
    document location).

    Raises xml.sax.SAXException based exception on parse error.
    """
    self.parse(*args, **kwargs)
    self._ore_initialized = True

  def getAggregation(self):
    """Return the URIRef of the Aggregation entity."""
    self._check_initialized()
    return [
      o
      for o in self.subjects(predicate=rdflib.RDF.type, object=ORE.Aggregation)
    ][0]

  def getObjectByPid(self, pid):
    """Returns the URIRef of the entry identified by pid."""
    self._check_initialized()
    opid = rdflib.term.Literal(pid)
    res = [o for o in self.subjects(predicate=DCTERMS.identifier, object=opid)]
    return res[0]

  def addResource(self, pid):
    """Add a resource to the resource map."""
    self._check_initialized()
    try:
      # is entry already in place?
      self.getObjectByPid(pid)
      return
    except IndexError:
      pass
    # Entry not present, add it to the graph
    oid = self._pid_to_id(pid)
    obj = rdflib.URIRef(oid)
    ag = self.getAggregation()
    self.add((ag, ORE.aggregates, obj))
    self.add((obj, ORE.isAggregatedBy, ag))
    self.add((obj, DCTERMS.identifier, rdflib.term.Literal(pid)))

  def setDocuments(self, pid_a, pid_b):
    """Sets the assertion that pid_a cito:documents pid_b.

    pid_a and pid_b must be present.
    """
    self._check_initialized()
    id_a = self.getObjectByPid(pid_a)
    id_b = self.getObjectByPid(pid_b)
    self.add((id_a, CITO.documents, id_b))

  def setDocumentedBy(self, pid_a, pid_b):
    """Sets the assertion that pid_a cito:isDocumentedBy pid_b.

    pid_a and pid_b must be present.
    """
    self._check_initialized()
    id_a = self.getObjectByPid(pid_a)
    id_b = self.getObjectByPid(pid_b)
    self.add((id_a, CITO.isDocumentedBy, id_b))

  def addMetadataDocument(self, pid):
    """Add the specified metadata document to the resource map."""
    self.addResource(pid)

  def addDataDocuments(self, scidata_pid_list, scimeta_pid=None):
    """Add data documents to the resource map and cross reference with
    metadata.
    """
    mpids = self.getAggregatedScienceMetadataPids()
    if scimeta_pid is None:
      if len(mpids) > 1:
        raise ValueError(
          'No metadata PID specified and more than one choice available.'
        )
      scimeta_pid = mpids[0]
    else:
      # Add the metadata object
      if scimeta_pid not in mpids:
        self.addMetadataDocument(scimeta_pid)

    for dpid in scidata_pid_list:
      self.addResource(dpid)
      self.setDocumentedBy(dpid, scimeta_pid)
      self.setDocuments(scimeta_pid, dpid)

  def getResourceMapPid(self):
    """Return the PID of the resource map."""
    ore = [
      o
      for o in self.subjects(predicate=rdflib.RDF.type, object=ORE.ResourceMap)
    ][0]
    pid = [
      str(o) for o in self.objects(predicate=DCTERMS.identifier, subject=ore)
    ][0]
    return pid

  def getAllTriples(self):
    """Return tuples that represent triples in this ORE document."""
    return [(str(s), str(p), str(o)) for s, p, o in self]

  def getAllPredicates(self):
    """Return a list of all unique predicates in the OAI-ORE document.

    Equivalent SPARQL:

      SELECT DISTINCT ?p
      WHERE {
        ?s ?p ?o .
      }

    Returns:

      list of strings
    """
    return sorted(set([str(o) for o in self.predicates()]))

  def getSubjectObjectsByPredicate(self, predicate):
    """Return all subject/objects in the OAI-ORE document with a given
    predicate.

    Equivalent SPARQL:

      PREFIX dc: <http://purl.org/dc/elements/1.1/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns# >
      PREFIX rdfs1: <http://www.w3.org/2001/01/rdf-schema# >
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?s ?o
      WHERE {{
        ?s {0} ?o .
      }}

    Returns:
      list of (subject, object) strings
    """
    return sorted(
      set([(str(s), str(o))
           for s, o in self.subject_objects(rdflib.term.URIRef(predicate))])
    )

  def getAggregatedPids(self):
    q = '''
    PREFIX ore: <http://www.openarchives.org/ore/terms/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT ?pid
    WHERE {
      ?s ore:aggregates ?o .
      ?o dcterms:identifier ?pid .
    }
    '''
    return [str(o[0]) for o in self.query(q)]

  def getAggregatedScienceMetadataPids(self):
    """Return PIDs of all science metadata documents in ORE document."""
    q = '''
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:documents ?o2 .
        ?o dcterms:identifier ?pid .
      }
    '''
    return [str(o[0]) for o in self.query(q)]
    # return [str(o[0]) for o in self.objects(ORE.aggregates, CITO.documents)]

  def getAggregatedScienceDataPids(self):
    """Return PIDs of all the data documents in the ORE document."""
    q = '''
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:isDocumentedBy ?o2 .
        ?o dcterms:identifier ?pid .
      }
    '''
    return [str(o[0]) for o in self.query(q)]
    # return [str(o[0]) for o in self.objects(ORE.aggregates, CITO.isDocumentedBy)]

  def asGraphvizDot(self, stream):
    """Serialize the graph in .dot format for ingest to graphviz.

    Args:

      stream (file): A file like object open for writing that will receive the
         resulting document.
    """
    rdflib.tools.rdf2dot.rdf2dot(self, stream)

  # Private

  def _parse(self, rdf_xml_doc, doc_format):
    """Parse a unicode containing a OAI-ORE document."""
    self.parse(data=rdf_xml_doc, format=doc_format)
    self._ore_initialized = True
    return self

  def _pid_to_id(self, pid):
    """Converts a pid to a URI that can be used as an OAI-ORE identifier."""
    return d1_common.url.joinPathElements(
      self._base_url, self._version_tag, 'resolve',
      d1_common.url.encodePathElement(pid)
    )

  def _check_initialized(self):
    if not self._ore_initialized:
      raise ValueError('ResourceMap is not initialized.')
