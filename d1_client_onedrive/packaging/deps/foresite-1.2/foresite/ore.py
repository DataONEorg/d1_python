
import os
import urllib, urllib2
from rdflib import ConjunctiveGraph, URIRef, BNode, Literal
from utils import *
from StringIO import StringIO
from utils import unconnectedAction
from foresite import libraryName, libraryUri, libraryEmail
from foresite import conneg

# --- Object Class Definitions ---

class Graph(ConjunctiveGraph):
    def __init__(self, store=None, id=None):
        # id *should* be aggregation URI
        if store != None and id != None:
            ConjunctiveGraph.__init__(self, store, id)
        else:
            ConjunctiveGraph.__init__(self)
        for (key,val) in namespaces.iteritems():
            self.bind(key, val)

    def find_namespace(self, name):
        # find best namespace
        for k in namespaceSearchOrder:
            v = elements[k]
            if name in v:
                return namespaces[k]
        return ''

    def split_uri(self, uri):
        # given namespaced uri, find base property name
        slsplit = uri.split('/')
        hsplit = slsplit[-1].split('#')
        return (uri[:0-len(hsplit[-1])], hsplit[-1])
        

class OREResource(object):
    graph = None
    uri = ""
    currNs = ""
    agents = {}
    triples = {}
    aggregations = []

    def __init__(self, uri):
        graph = Graph()
        self._graph_ = graph
        if isinstance(uri, URIRef) or isinstance(uri, BNode):
            self._uri_ = uri
        else:
            self._uri_ = URIRef(uri)
        self._currNs_ = ''
        self._agents_ = {}
        self._triples_ = {}
        self._aggregations_ = []

    def __str__(self):
        return str(self.uri)

    def __getattr__(self, name):
        # fetch value from graph
        cns = self.currNs
        if name[0] == "_" and name[-1] == "_":
            return getattr(self, name[1:-1])
        elif name[0] == "_" and namespaces.has_key(name[1:]):
            # we're looking for self.namespace.property
            self._currNs_ = name[1:]
            return self
        elif cns:
            val = self.get_value(name, cns)
            self._currNs_ = ''
        else:
            val = self.get_value(name)
        return val

    def __setattr__(self, name, value):
        
        if name[0] == "_" and name[-1] == "_":            
            return object.__setattr__(self, name[1:-1], value)
        elif name[0] == "_" and namespaces.has_key(name[1:]):
            # we're looking for self.namespace.property
            object.__setattr__(self, 'currNs', name[1:])
            return self
        elif self.currNs:
            val = self.set_value(name, value, self.currNs)        
        else:
            val = self.set_value(name, value)
        object.__setattr__(self, 'currNs', '')
        return val

    def set_value(self, name, value, ns=None):
        if ns:
            nsobj = namespaces[ns]
        else:
            nsobj = self.graph.find_namespace(name)

        if value == []:
            for val in self.graph.objects(self.uri, nsobj[name]):
                self.graph.remove((self.uri, nsobj[name], val))
        else:
            if not isinstance(value, URIRef) and not isinstance(value, BNode):
                value = Literal(value)
            self.graph.add((self.uri, nsobj[name], value))
        return 1

    def get_value(self, name, ns=None):        
        if ns:
            nsobj = namespaces[ns]
        else:
            nsobj = self.graph.find_namespace(name)
        l = []
        for obj in self.graph.objects(self.uri, nsobj[name]):
            l.append(obj)
        return l

    def add_triple(self, trip):
        self._triples_[trip._uri_] = trip

    def remove_triple(self, trip):
        del self._triples_[trip._uri_]

    def predicates(self):
        return list(self.graph.predicates())

    def add_agent(self, who, type):
        self._agents_[who._uri_] = who
        setattr(self, type, who._uri_)

    def remove_agent(self, who, type):
        del self._agents_[who._uri_]
        ns = self.graph.find_namespace(type)
        self._graph_.remove((self._uri_, ns[type], who._uri_))

    def on_add(self, aggr, proxy):
        self._aggregations_.append((aggr, proxy))

    def on_remove(self, aggr, proxy):
        self._aggregations_.remove((aggr, proxy))

    def get_proxy(self, aggr=None):
        if aggr:
            for (a,p) in self._aggregations_:
                if a == aggr:
                    return p
            return None
        elif self._aggregations_:
            return self._aggregations_[0][1]
        else:
            return None


class ResourceMap(OREResource):
    aggregation = None
    serializer = None

    def __init__(self, uri):
        OREResource.__init__(self, uri)
        self._aggregation_ = None
        self._serializer_ = None
        self.type = namespaces['ore']['ResourceMap']
        self.add_triple(rem_type)

    def register_serializer(self, serializer):
        # Deprecated
        self.register_serialization(serializer)

    def register_serialization(self, serializer):
        if self.serializer:
            raise OreException("ResourceMap already has serializer")
        if not serializer.mimeType in self._dc.format:
            self.format = serializer.mimeType
        self._serializer_ = serializer
    
    def get_serialization(self, page=-1):
        return self._serializer_.serialize(self)

    def set_aggregation(self, agg):
        if self.aggregation:
            raise OreException("ResourceMap already has an aggregation set")
        self._aggregation_ = agg
        self.describes = agg.uri
        agg.on_describe(self)


class Aggregation(OREResource):
    resourceMaps = []
    resources = []
    fullGraph = None

    def __init__(self, uri):
        OREResource.__init__(self, uri)
        self._resources_ = []
        self._resourceMaps_ = []
        self._fullGraph_ = None
        self._generateProxies_ = False
        self.type = namespaces['ore']['Aggregation']
        self.add_triple(aggr_type)

    def __iter__(self):
        l = [x[0] for x in self._resources_]
        return l.__iter__()

    def __len__(self):
        return len(self._resources_)

    def __contains__(self, what):
        for x in self._resources_:
            if what in x or what == str(x[0].uri) or what == str(x[1].uri):
                return True
        return False

    def __getitem__(self, x):
        if isinstance(x, int):
            return self.resources[x][0]
        if isinstance(x, str):
            x = URIRef(x)
        for r in self.resources:
            if x == r[0].uri:
                return r[0]
        raise KeyError(x)

    def on_describe(self, rem):
        self._resourceMaps_.append(rem)
        
    def add_resource(self, res, proxy=None):
        for x in self._resources_:
            if x[0] == res:
                raise KeyError('Aggregation %s already aggregates %s' % (self.uri, res.uri))
        self.aggregates = res.uri
        if proxy or self.generateProxies:
            if not proxy:
                uri = gen_proxy_uri(res, self)
                proxy = Proxy(uri)
                proxy.set_forIn(res, self)
        else:
            proxy = None
        self._resources_.append((res, proxy))
        res.on_add(self, proxy)
        return proxy

    # List API
    def append(self, res):
        self.add_resource(res)

    # Set API
    def add(self, res):
        self.add_resource(res)

    def remove_resource(self, res):
        tup = None
        for x in self._resources_:
            if x[0] == res:
                tup = x
                break
        if tup:
            self._resources_.remove(tup)
            res.on_remove(self, tup[1])
            del tup[1]

    # List, Set API
    def remove(self, res):
        self.remove_resource(res)

    # Set API
    def discard(self, res):
        self.remove_resource(res)

    def get_authoritative(self):
        rems = []
        for rem in self.resourceMaps:
            if self.uri in rem._orex.isAuthoritativeFor:
                rems.append(rem)
        return rems

    def _merge_all_graphs(self, public=1, top=1):
        # Only used for sparql query across everything, not serialization
        g = Graph()
        for rem in self.resourceMaps:
            g += rem._graph_
            for at in rem._triples_.values():
                g += at._graph_
            for c in rem._agents_.values():
                g += c._graph_
            if not rem.created:
                g.add((rem._uri_, namespaces['dcterms']['created'], Literal(now())))
            g.add((rem._uri_, namespaces['dcterms']['modified'], Literal(now())))

        aggr = self
        g += aggr._graph_
        for at in aggr._triples_.values():
            g += at._graph_
        for c in aggr._agents_.values():
            g += c._graph_
        for (res, proxy) in aggr._resources_:
            g += res._graph_
            if proxy:
                g += proxy._graph_
            for at in res._triples_.values():
                g += at._graph_
            for c in res._agents_.values():
                g += c._graph_
            if isinstance(res, Aggregation):
                # include nestings recursively
                g += res._merge_all_graphs(public, top=0)

        if not g.connected() and unconnectedAction != 'ignore':
            raise OreException("Must have connected graph")

        if public:
            # Remove internal methods
            for p in internalPredicates:
                for (s,o) in g.subject_objects(p):
                    g.remove((s,p,o))
        if top and not g.objects((aggr._uri_, namespaces['ore']['aggregates'])):
            raise OreException("Aggregation must aggregate something")
        return g

    def do_sparql(self, sparql):
        # first merge graphs
        g = self._merge_all_graphs()
        # now do sparql query on merged graph
        return g.query(sparql, initNs=namespaces)

    def register_serialization(self, serializer, uri='', **kw):
        # Create ReM etc.
        if not uri:
            if self.uri.find('#') > -1:
                uri = self.uri + "_ResourceMap"
            else:
                uri = self.uri + "#ResourceMap"
        rem = ResourceMap(uri)
        rem.set_aggregation(self)
        rem.register_serializer(serializer)
        for (k,v) in kw.iteritems():
            if isinstance(v, Agent):
                rem.add_agent(v, k)
            elif isinstance(v, ArbitraryResource):
                setattr(rem, k, v.uri)
                rem.add_triple(v)
            else:
                setattr(rem, k, v)
        return rem

    def get_serialization(self, uri='', page=-1):
        if not uri:
            rem = self.resourceMaps[0]
        else:
            rem = None
            for r in self.resourceMaps:
                if str(r.uri) == uri:
                    rem = r
                    break
            if not rem:
                raise OreException("Unknown Resource Map: %s" % uri)
        return rem.get_serialization()


class Proxy(OREResource):
    resource = None
    aggregation = None

    def __init__(self, uri):
        OREResource.__init__(self, uri)
        self.type = namespaces['ore']['Proxy']
        self._resource_ = None
        self._aggregation_ = None
    
    def set_forIn(self, res, aggr):
        self.proxyFor = res.uri
        self._resource_ = res
        self.proxyIn = aggr.uri
        self._aggregation_ = aggr

class Agent(OREResource):

    def __init__(self, uri=''):
        if not uri:
            if assignAgentUri:
                uri = "urn:uuid:%s" % gen_uuid()
            else:
                uri = BNode()
        OREResource.__init__(self, uri)


class AggregatedResource(OREResource):
    # Convenience class for OREResource
    pass

class ArbitraryResource(OREResource):
    # To allow for arbitrary triples that aren't one of the major
    # ORE classes

    def __init__(self, uri=None):
        if uri == None:
            OREResource.__init__(self, BNode())
        else:
            OREResource.__init__(self, uri)


class ReMDocument(StringIO):    
    # Serialisation of objects
    uri = ""
    mimeType = ""
    data = ""
    format = ""   # rdflib name for format

    def __init__(self, uri, data='', filename='', mimeType='', format ='', accept=''):
        self.uri = uri
        if data:
            self.data = data
        elif filename:
            if os.path.exists(filename):
                fh = file(filename)
                self.data = fh.read()
                fh.close()
        else:
            # try to fetch uri
            try:
                req = urllib2.Request(uri)
                if accept:
                    # add custom accept header
                    req.add_header('Accept', accept)
                else:
                    # otherwise add default
                    req.add_header('Accept', accept_header)
                fh = urllib2.urlopen(req)
                self.data = fh.read()
                self.info = fh.info()
                mimeType = self.info.dict.get('content-type', mimeType)
                self.uri = fh.geturl()
                fh.close()
            except:
                raise OreException('ReMDocument must either have data or filename')

            if not format:
                try:
                    mt = conneg.parse(mimeType)
                    if mt:
                        mimeType = mt[0].mimetype1 + '/' + mt[0].mimetype2
                except:
                    pass
                mimeHash = {'application/atom+xml' : 'atom', 
                        'application/xhtml+xml' : 'rdfa',
                        'application/rdf+xml' : 'xml',
                        'text/plain' : 'nt',  # yes, really
                        'text/rdf+n3' : 'n3',
                        'application/x-turtle' : 'turtle',
                        'application/rdf+nt' : 'nt'}
                format = mimeHash.get(mimeType, '')

        self.mimeType = mimeType
        self.format = format
        StringIO.__init__(self, self.data)

rem_type = ArbitraryResource(namespaces['ore']['ResourceMap'])
rem_type.label = "ResourceMap"
rem_type.isDefinedBy = namespaces['ore']

aggr_type = ArbitraryResource(namespaces['ore']['Aggregation'])
aggr_type.label = "Aggregation"
aggr_type.isDefinedBy = namespaces['ore']

foresiteAgent = Agent(libraryUri)
foresiteAgent._foaf.name = libraryName
foresiteAgent._foaf.mbox = libraryEmail
