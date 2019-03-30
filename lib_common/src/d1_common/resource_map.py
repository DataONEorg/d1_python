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
"""Read and write DataONE OAI-ORE Resource Maps.

DataONE supports a system that allows relationships between Science Objects to be
described. These relationships are stored in :term:`OAI-ORE Resource Map`\s.

This module provides functionality for the most common use cases when parsing and
generating Resource Maps for use in DataONE.

For more information about how Resource Maps are used in DataONE, see:

https://releases.dataone.org/online/api-documentation-v2.0.1/design/DataPackage.html

Common RDF-XML namespaces:

.. highlight: xml

::

  dc: <http://purl.org/dc/elements/1.1/>
  foaf: <http://xmlns.com/foaf/0.1/>
  rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns# >
  rdfs1: <http://www.w3.org/2001/01/rdf-schema# >
  ore: <http://www.openarchives.org/ore/terms/>
  dcterms: <http://purl.org/dc/terms/>
  cito: <http://purl.org/spar/cito/>

Note:

  In order for Resource Maps to be recognized and indexed by DataONE, they must be created
  with ``formatId`` set to ``http://www.openarchives.org/ore/terms``.

"""

import logging

import rdflib
import rdflib.tools.rdf2dot

import d1_common.const
import d1_common.type_conversions
import d1_common.url

# RDFLib wrappers around the namespaces. Additional ones are defined by RDFLib
DCTERMS = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT["dcterms"])
CITO = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT["cito"])
ORE = rdflib.Namespace(d1_common.const.ORE_NAMESPACE_DICT["ore"])


def createSimpleResourceMap(ore_pid, scimeta_pid, sciobj_pid_list):
    """Create a simple OAI-ORE Resource Map with one Science Metadata document and any
    number of Science Data objects.

    This creates a document that establishes an association between a Science Metadata
    object and any number of Science Data objects. The Science Metadata object contains
    information that is indexed by DataONE, allowing both the Science Metadata and the
    Science Data objects to be discoverable in DataONE Search. In search results, the
    objects will appear together and can be downloaded as a single package.

    Args:
      ore_pid: str
        Persistent Identifier (PID) to use for the new Resource Map

      scimeta_pid: str
        PID for an object that will be listed as the Science Metadata that is
        describing the Science Data objects.

      sciobj_pid_list: list of str
        List of PIDs that will be listed as the Science Data objects that are being
        described by the Science Metadata.

    Returns:
      ResourceMap : OAI-ORE Resource Map

    """
    ore = ResourceMap()
    ore.initialize(ore_pid)
    ore.addMetadataDocument(scimeta_pid)
    ore.addDataDocuments(sciobj_pid_list, scimeta_pid)
    return ore


def createResourceMapFromStream(in_stream, base_url=d1_common.const.URL_DATAONE_ROOT):
    """Create a simple OAI-ORE Resource Map with one Science Metadata document and any
    number of Science Data objects, using a stream of PIDs.

    Args:
      in_stream:
        The first non-blank line is the PID of the resource map itself. Second line is
        the science metadata PID and remaining lines are science data PIDs.

        Example stream contents:

        ::

          PID_ORE_value
          sci_meta_pid_value
          data_pid_1
          data_pid_2
          data_pid_3

      base_url : str
        Root of the DataONE environment in which the Resource Map will be used.

    Returns:
      ResourceMap : OAI-ORE Resource Map

    """
    pids = []
    for line in in_stream:
        pid = line.strip()
        if pid == "#" or pid.startswith("# "):
            continue

    if len(pids) < 2:
        raise ValueError("Insufficient numbers of identifiers provided.")

    logging.info("Read {} identifiers".format(len(pids)))
    ore = ResourceMap(base_url=base_url)
    logging.info("ORE PID = {}".format(pids[0]))
    ore.initialize(pids[0])
    logging.info("Metadata PID = {}".format(pids[1]))
    ore.addMetadataDocument(pids[1])
    ore.addDataDocuments(pids[2:], pids[1])

    return ore


# ===============================================================================


class ResourceMap(rdflib.ConjunctiveGraph):
    """OAI-ORE Resource Map."""

    def __init__(
        self,
        ore_pid=None,
        scimeta_pid=None,
        scidata_pid_list=None,
        base_url=d1_common.const.URL_DATAONE_ROOT,
        api_major=2,
        ore_software_id=d1_common.const.ORE_SOFTWARE_ID,
        *args,
        **kwargs
    ):
        """Create a OAI-ORE Resource Map.

        Args:
          ore_pid: str
            Persistent Identifier (PID) to use for the new Resource Map

          scimeta_pid: str
            PID for an object that will be listed as the Science Metadata that is
            describing the Science Data objects.

          scidata_pid_list: list of str
            List of PIDs that will be listed as the Science Data objects that are being
            described by the Science Metadata.

          base_url: str
            Root of the DataONE environment in which the Resource Map will be used.

          api_major:
            The DataONE API version to use for the the DataONE Resolve API. Clients
            call the Resolve API to get a list of download locations for the objects in
            the Resource Map.

          ore_software_id: str
            Optional string which identifies the software that was used for creating
            the Resource Map. If specified, should be on the form of a UserAgent
            string.

          args and kwargs:
            Optional arguments forwarded to rdflib.ConjunctiveGraph.__init__().

        """
        super().__init__(*args, **kwargs)
        self._base_url = base_url
        self._version_tag = d1_common.type_conversions.get_version_tag(api_major)
        self._ore_initialized = False
        if ore_pid:
            self.initialize(ore_pid, ore_software_id)
        if scimeta_pid:
            self.addMetadataDocument(scimeta_pid)
            if scidata_pid_list:
                self.addDataDocuments(scidata_pid_list, scimeta_pid)

    def initialize(self, pid, ore_software_id=d1_common.const.ORE_SOFTWARE_ID):
        """Create the basic ORE document structure."""
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
        ag = rdflib.URIRef(oid + "#aggregation")
        self.add((ore, ORE.describes, ag))
        self.add((ag, rdflib.RDF.type, ORE.Aggregation))
        self.add((ORE.Aggregation, rdflib.RDFS.isDefinedBy, ORE.term("")))
        self.add(
            (ORE.Aggregation, rdflib.RDFS.label, rdflib.term.Literal("Aggregation"))
        )
        self._ore_initialized = True

    def serialize_to_transport(self, doc_format="xml", *args, **kwargs):
        """Serialize ResourceMap to UTF-8 encoded XML document.

        Args:
          doc_format: str
            One of: ``xml``, ``n3``, ``turtle``, ``nt``, ``pretty-xml``, ``trix``,
            ``trig`` and ``nquads``.

          args and kwargs:
            Optional arguments forwarded to rdflib.ConjunctiveGraph.serialize().

        Returns:
          bytes: UTF-8 encoded XML doc.

        Note:
          Only the default, "xml", is automatically indexed by DataONE.

        """
        return super(ResourceMap, self).serialize(
            format=doc_format, encoding="utf-8", *args, **kwargs
        )

    def serialize_to_display(self, doc_format="pretty-xml", *args, **kwargs):
        """Serialize ResourceMap to an XML doc that is pretty printed for display.

        Args:
          doc_format: str
            One of: ``xml``, ``n3``, ``turtle``, ``nt``, ``pretty-xml``, ``trix``,
            ``trig`` and ``nquads``.

          args and kwargs:
            Optional arguments forwarded to rdflib.ConjunctiveGraph.serialize().

        Returns:
          str: Pretty printed Resource Map XML doc

        Note:
          Only the default, "xml", is automatically indexed by DataONE.

        """
        return (
            super(ResourceMap, self)
            .serialize(format=doc_format, encoding=None, *args, **kwargs)
            .decode("utf-8")
        )

    # noinspection PyIncorrectDocstring
    def deserialize(self, *args, **kwargs):
        """Deserialize Resource Map XML doc.

        The source is specified using one of source, location, file or data.

        Args:
          source: InputSource, file-like object, or string
            In the case of a string the string is the location of the source.

          location: str
            String indicating the relative or absolute URL of the source. Graph``s
            absolutize method is used if a relative location is specified.

          file: file-like object

          data: str
            The document to be parsed.

          format : str
            Used if format can not be determined from source. Defaults to ``rdf/xml``.
            Format support can be extended with plugins.

            Built-in: ``xml``, ``n3``, ``nt``, ``trix``, ``rdfa``

          publicID: str
            Logical URI to use as the document base. If None specified the document
            location is used (at least in the case where there is a document location).

        Raises:
          xml.sax.SAXException based exception: On parse error.

        """
        self.parse(*args, **kwargs)
        self._ore_initialized = True

    def getAggregation(self):
        """Returns:

        str : URIRef of the Aggregation entity

        """
        self._check_initialized()
        return [
            o for o in self.subjects(predicate=rdflib.RDF.type, object=ORE.Aggregation)
        ][0]

    def getObjectByPid(self, pid):
        """
    Args:
      pid : str

    Returns:
      str : URIRef of the entry identified by ``pid``."""
        self._check_initialized()
        opid = rdflib.term.Literal(pid)
        res = [o for o in self.subjects(predicate=DCTERMS.identifier, object=opid)]
        return res[0]

    def addResource(self, pid):
        """Add a resource to the Resource Map.

        Args:
          pid : str

        """
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

    def setDocuments(self, documenting_pid, documented_pid):
        """Add a CiTO, the Citation Typing Ontology, triple asserting that
        ``documenting_pid`` documents ``documented_pid``.

        Adds assertion: ``documenting_pid cito:documents documented_pid``

        Args:
          documenting_pid: str
            PID of a Science Object that documents ``documented_pid``.

          documented_pid: str
            PID of a Science Object that is documented by ``documenting_pid``.

        """
        self._check_initialized()
        documenting_id = self.getObjectByPid(documenting_pid)
        documented_id = self.getObjectByPid(documented_pid)
        self.add((documenting_id, CITO.documents, documented_id))

    def setDocumentedBy(self, documented_pid, documenting_pid):
        """Add a CiTO, the Citation Typing Ontology, triple asserting that
        ``documented_pid`` isDocumentedBy ``documenting_pid``.

        Adds assertion: ``documented_pid cito:isDocumentedBy documenting_pid``

        Args:
          documented_pid: str
            PID of a Science Object that is documented by ``documenting_pid``.

          documenting_pid: str
            PID of a Science Object that documents ``documented_pid``.

        """
        self._check_initialized()
        documented_id = self.getObjectByPid(documented_pid)
        documenting_id = self.getObjectByPid(documenting_pid)
        self.add((documented_id, CITO.isDocumentedBy, documenting_id))

    def addMetadataDocument(self, pid):
        """Add a Science Metadata document.

        Args:
          pid : str
            PID of a Science Metadata object.

        """
        self.addResource(pid)

    def addDataDocuments(self, scidata_pid_list, scimeta_pid=None):
        """Add Science Data object(s)

        Args:
          scidata_pid_list : list of str
            List of one or more PIDs of Science Data objects

          scimeta_pid: str
            PID of a Science Metadata object that documents the Science Data objects.

        """
        mpids = self.getAggregatedScienceMetadataPids()
        if scimeta_pid is None:
            if len(mpids) > 1:
                raise ValueError(
                    "No metadata PID specified and more than one choice available."
                )
            scimeta_pid = mpids[0]
        else:
            if scimeta_pid not in mpids:
                self.addMetadataDocument(scimeta_pid)

        for dpid in scidata_pid_list:
            self.addResource(dpid)
            self.setDocumentedBy(dpid, scimeta_pid)
            self.setDocuments(scimeta_pid, dpid)

    def getResourceMapPid(self):
        """Returns:

        str : PID of the Resource Map itself.

        """
        ore = [
            o for o in self.subjects(predicate=rdflib.RDF.type, object=ORE.ResourceMap)
        ][0]
        pid = [str(o) for o in self.objects(predicate=DCTERMS.identifier, subject=ore)][
            0
        ]
        return pid

    def getAllTriples(self):
        """Returns:

        list of tuples : Each tuple holds a subject, predicate, object triple

        """
        return [(str(s), str(p), str(o)) for s, p, o in self]

    def getAllPredicates(self):
        """Returns: list of str: All unique predicates.

        Notes:

          Equivalent SPARQL:

          .. highlight: sql

          ::

            SELECT DISTINCT ?p
            WHERE {
              ?s ?p ?o .
            }

        """
        return sorted(set([str(o) for o in self.predicates()]))

    def getSubjectObjectsByPredicate(self, predicate):
        """
    Args:
      predicate : str
        Predicate for which to return subject, object tuples.

    Returns:
      list of subject, object tuples: All subject/objects with ``predicate``.

    Notes:

      Equivalent SPARQL:

      .. highlight: sql

      ::

        SELECT DISTINCT ?s ?o
        WHERE {{
          ?s {0} ?o .
        }}
    """
        return sorted(
            set(
                [
                    (str(s), str(o))
                    for s, o in self.subject_objects(rdflib.term.URIRef(predicate))
                ]
            )
        )

    def getAggregatedPids(self):
        """Returns: list of str: All aggregated PIDs.

        Notes:

          Equivalent SPARQL:

          .. highlight: sql

          ::

            SELECT ?pid
            WHERE {
              ?s ore:aggregates ?o .
              ?o dcterms:identifier ?pid .
            }

        """
        q = """
    PREFIX ore: <http://www.openarchives.org/ore/terms/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT ?pid
    WHERE {
      ?s ore:aggregates ?o .
      ?o dcterms:identifier ?pid .
    }
    """
        return [str(o[0]) for o in self.query(q)]

    def getAggregatedScienceMetadataPids(self):
        """Returns: list of str: All Science Metadata PIDs.

        Notes:

          Equivalent SPARQL:

          .. highlight: sql

          ::

            SELECT DISTINCT ?pid
            WHERE {
              ?s ore:aggregates ?o .
              ?o cito:documents ?o2 .
              ?o dcterms:identifier ?pid .
            }

        """
        q = """
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:documents ?o2 .
        ?o dcterms:identifier ?pid .
      }
    """
        return [str(o[0]) for o in self.query(q)]
        # return [str(o[0]) for o in self.objects(ORE.aggregates, CITO.documents)]

    def getAggregatedScienceDataPids(self):
        """Returns: list of str: All Science Data PIDs.

        Notes:

          Equivalent SPARQL:

          .. highlight: sql

          ::

            SELECT DISTINCT ?pid
            WHERE {
              ?s ore:aggregates ?o .
              ?o cito:isDocumentedBy ?o2 .
              ?o dcterms:identifier ?pid .
            }

        """
        q = """
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>

      SELECT DISTINCT ?pid
      WHERE {
        ?s ore:aggregates ?o .
        ?o cito:isDocumentedBy ?o2 .
        ?o dcterms:identifier ?pid .
      }
    """
        return [str(o[0]) for o in self.query(q)]
        # return [str(o[0]) for o in self.objects(ORE.aggregates, CITO.isDocumentedBy)]

    def asGraphvizDot(self, stream):
        """Serialize the graph to .DOT format for ingestion in Graphviz.

        Args:   stream: file-like object open for writing that will receive the
        resulting document.

        """
        rdflib.tools.rdf2dot.rdf2dot(self, stream)

    def parseDoc(self, doc_str, format="xml"):
        """Parse a OAI-ORE Resource Maps document.

        See Also:   ``rdflib.ConjunctiveGraph.parse`` for documentation on arguments.

        """
        self.parse(data=doc_str, format=format)
        self._ore_initialized = True
        return self

    # Private

    def _pid_to_id(self, pid):
        """Converts a pid to a URI that can be used as an OAI-ORE identifier."""
        return d1_common.url.joinPathElements(
            self._base_url,
            self._version_tag,
            "resolve",
            d1_common.url.encodePathElement(pid),
        )

    def _check_initialized(self):
        if not self._ore_initialized:
            raise ValueError("ResourceMap is not initialized.")
