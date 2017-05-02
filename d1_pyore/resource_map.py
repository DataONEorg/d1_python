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

import logging
import rdflib
from rdflib import URIRef, RDF, RDFS

try:
  from d1_common.url import encodePathElement
except:
  #Approximate the URLPath encoder used in DataONE. The urllib version should
  #provide equivalent functionality for the purposes of the ORE documents.
  import urllib
  def encodePathElement(s):
    return urllib.quote(s.encode('utf-8'))

# A tag that will be added to the resource map
SOFTWARE_ID = u"d1_pyore DataONE Python library"


# Namespaces and prefixes used here.
NAMESPACES = {u'cito': u'http://purl.org/spar/cito/',
              u'dc': u'http://purl.org/dc/elements/1.1/',
              u'dcterms': u'http://purl.org/dc/terms/',
              u'ore': u'http://www.openarchives.org/ore/terms/',
              u'foaf': u'http://xmlns.com/foaf/0.1/',
              }

# RDFLib wrappers around the namespaces. Others are defined by RDFLib
DCTERMS = rdflib.Namespace( NAMESPACES[u'dcterms'] )
CITO = rdflib.Namespace( NAMESPACES[u'cito'] )
ORE = rdflib.Namespace( NAMESPACES[u'ore'] )


#===============================================================================

class ResourceMap(rdflib.ConjunctiveGraph):
  '''Subclasses ConjunctiveGraph to provide OAI-ORE functionality for DataONE.
  '''
  
  def __init__(self, 
               base_url=u'https://cn.dataone.org/cn',
               dataone_api_version="2"):
    '''Initialize the Graph instance
    '''
    super(ResourceMap, self).__init__()
    self._L = logging.getLogger(self.__class__.__name__)
    self._dataone_api_version = dataone_api_version
    self._base_url = base_url
    self._ore_initialized = False
    self.aggregate_id = None


  def _parse(self, rdf_xml_doc):
    '''Parse a unicode containing a OAI-ORE document
    '''
    self.parse(data=rdf_xml_doc)
    self._ore_initialized = True
    return self

  
  def _pidToId(self, pid):
    '''Converts a pid to a URI that can be used as an OAI-ORE identifier.
    '''
    return u"{0}/v{1}/resolve/{2}".format( self._base_url, 
                                           self._dataone_api_version, 
                                           encodePathElement(pid) )


  def oreInitialize(self, pid):
    '''Creates the basic ORE document structure. 
    '''
    #Set nice prefixes for the namespaces
    for k in NAMESPACES.keys():
      self.bind(k, NAMESPACES[k])
    
    #Create the ORE entity
    oid = self._pidToId(pid)
    ore = URIRef( oid )
    self.add( (ore, RDF.type, ORE.ResourceMap) )
    self.add( (ore, DCTERMS.identifier, rdflib.term.Literal(pid)) )
    self.add( (ore, DCTERMS.creator, rdflib.term.Literal(SOFTWARE_ID)) )
    
    #Add an empty aggregation
    self.aggregate_id = u"{0}#aggregation".format( oid )
    ag = URIRef( self.aggregate_id )
    self.add( (ore, ORE.describes, ag))
    self.add( (ag, RDF.type, ORE.Aggregation) )
    self.add( (ORE.Aggregation, RDFS.isDefinedBy, ORE.term('')) )
    self.add( (ORE.Aggregation, RDFS.label, rdflib.term.Literal(u'Aggregation')) )
    self._ore_initialized = True
    
  
  def getAggregation(self):
    '''Return the URIRef of the Aggregation entity
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    return [ o for o in self.subjects(predicate=RDF.type, 
                                      object=ORE.Aggregation) ][0]
  
  
  def getObjectByPid(self, pid):
    '''Returns the URIRef of the entry identified by pid
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    opid = rdflib.term.Literal(pid)
    res = [o for o in self.subjects( predicate=DCTERMS.identifier,
                                      object=opid) ]
    self._L.debug(res)
    return res[0]
    

  def addResource(self, pid):
    '''Add a resource to the resource map.    
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    try:
      # is entry already in place?
      self.getObjectByPid(pid)
      return
    except IndexError:
      pass
    #Entry not present, add it to the graph
    oid = self._pidToId(pid)
    obj = URIRef( oid )
    ag = self.getAggregation()
    self.add( (ag, ORE.aggregates, obj) )
    self.add( (obj, ORE.isAggregatedBy, ag) )
    self.add( (obj, DCTERMS.identifier, rdflib.term.Literal(pid)) )
  

  def removeResource(self, oid):
    '''
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    raise NotImplementedError()
    
    
  def setDocuments(self, pid_a, pid_b):
    '''Sets the assertion that pid_a cito:documents pid_b.

    pid_a and pid_b must be present.
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    id_a = self.getObjectByPid( pid_a )
    id_b = self.getObjectByPid( pid_b )
    self.add( (id_a, CITO.documents, id_b) )
    
  
  def setDocumentedBy(self, pid_a, pid_b):
    '''Sets the assertion that pid_a cito:isDocumentedBy pid_b.
  
    pid_a and pid_b must be present.
    '''
    if not self._ore_initialized:
      raise ValueError("Resource map structure is not initialized.")
    id_a = self.getObjectByPid( pid_a )
    id_b = self.getObjectByPid( pid_a )
    self.add( (id_a, CITO.isDocumentedBy, id_b) )
    
    
  def addMetadataDocument(self, pid):
    '''Add the specified metadata document to the resource map
    '''
    self.addResource(pid)


  def addDataDocuments(self, data_pids, metadata_pid=None):
    '''Add data documents to the resource map and cross reference with metadata.
    
    Args
    
      data_pids (list): A list of identifiers for data objects
      metadata_pid (unicode): The metadata document identifier
    '''
    mpids = self.getAggregatedScienceMetadataPids()
    if metadata_pid is None:
      if len(mpids) > 1:
        raise ValueError('No metadata PID specified and more than one choice available.')
      metadata_pid = mpids[0]
    else:
      #Add the metadata object
      if not metadata_pid in mpids:
        self.addMetadataDocument( metadata_pid )
    
    for dpid in data_pids:
      self.addResource(dpid)
      self.setDocumentedBy(dpid, metadata_pid)
      self.setDocuments(metadata_pid, dpid)
    
  
  def getResourceMapPid(self):
    '''Return the PID of the resource map
    '''
    ore = [ o for o in self.subjects( predicate=RDF.type, 
                                      object=ORE.ResourceMap) ][0]
    pid = [ str(o) for o in self.objects( predicate=DCTERMS.identifier,
                                          subject=ore) ][0]
    return pid


  def getAllTriples(self):
    '''Return tuples that represent triples in this ORE document.
    '''
    return [(str(s), str(p), str(o)) for s, p, o in self]


  def getAllPredicates(self):
    '''Return a list of all unique predicates in the OAI-ORE document

    Equivalent SPARQL:
    
      SELECT DISTINCT ?p
      WHERE {
        ?s ?p ?o .
      }
      
    Returns:
    
      list of strings
    '''
    return map(str, [o for o in self.predicates()] )


  def getSubjectObjectsByPredicate(self, predicate):
    '''Return all subject/objects in the OAI-ORE document with a given predicate
    
    Equivalent SPARQL:
    
      PREFIX dc: <http://purl.org/dc/elements/1.1/>
      PREFIX foaf: <http://xmlns.com/foaf/0.1/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX rdfs1: <http://www.w3.org/2001/01/rdf-schema#>
      PREFIX ore: <http://www.openarchives.org/ore/terms/>
      PREFIX dcterms: <http://purl.org/dc/terms/>
      PREFIX cito: <http://purl.org/spar/cito/>
  
      SELECT DISTINCT ?s ?o
      WHERE {{
        ?s {0} ?o .
      }}

    Returns:
      list of (subject, object) strings

    '''
    return [(str(s), str(o)) for s, o in self.subject_objects( predicate )]


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
    return map(str, [o[0] for o in self.query(q)])


  def getAggregatedScienceMetadataPids(self):
    '''Return PIDs of all science metadata documents in ORE document.
    
    '''
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
    return map(str, [o[0] for o in self.query(q)])
    #return map(str, [o[0] for o in self.objects( ORE.aggregates,
    #                                             CITO.documents )])


  def getAggregatedScienceDataPids(self):
    '''Return PIDs of all the data documents in the ORE document.

    '''
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
    return map(str, [o[0] for o in self.query(q)])
    #return map(str, [o[0] for o in self.objects( ORE.aggregates,
    #                                             CITO.isDocumentedBy )])


  def asGraphvizDot(self, stream):
    '''Serialize the graph in .dot format for ingest to graphviz. 
    
    Args:
    
      stream (file): A file like object open for writing that will receive the
         resulting document.
    '''
    import rdflib.tools.rdf2dot
    rdflib.tools.rdf2dot.rdf2dot(self, stream)
    
