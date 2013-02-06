
from ore import *
from utils import namespaces
from rdflib import URIRef, plugin, store

# Store raw triples into a TripleStore somewhere

class TripleStore(object):

    def __init__(self, configuration, db, create):
        self.configuration = configuration
        self.create = create
        self.db = db
        if db:
            self.store = plugin.get(self.storeType,store.Store)(db)
        else:
            self.store = plugin.get(self.storeType,store.Store)()
        self.store.open(configuration, create)

    def close(self):
        self.store.close()

    def store_aggregation(self, aggr):
        # Non memory graph
        g = Graph(self.store, aggr.uri)

        # Don't want to serialise resource map info?

        [g.add(t) for t in aggr._graph_]
        for at in aggr._triples_:
            [g.add(t) for t in at._graph_]
        for c in aggr._agents_:
            [g.add(t) for t in c._graph_]

        for (res, proxy) in aggr._resources_:
            [g.add(t) for t in res._graph_]
            if proxy:
                [g.add(t) for t in proxy._graph_]
            for at in res._triples_:
                [g.add(t) for t in at._graph_]
            for c in res._agents_:
                [g.add(t) for t in c._graph_]
            if isinstance(res, Aggregation):
                # don't recurse, remove aggregates                
                for a in res._ore.aggregates:
                    g.remove((res._uri_, namespaces['ore']['aggregates'], a))
                # but keep all other triples
        g.commit()
        return g

    def set_fields(self, what, graph):
        for (pred, obj) in graph.predicate_objects(what.uri):
            # assert to what's graph
            what.graph.add((what.uri, pred, obj))

    def load_aggregation(self, identifier):
        if not isinstance(identifier, URIRef):
            identifier = URIRef(identifier)
        graph = Graph(self.store, identifier)
        if not len(graph):
            aggr = None
        else:
            uri_a = identifier

            aggr = Aggregation(uri_a)
            self.set_fields(aggr, graph)
            things = {uri_a : aggr}

            res2 = graph.query("PREFIX ore: <http://www.openarchives.org/ore/terms/> SELECT ?b WHERE {<%s> ore:aggregates ?b .}" % uri_a )
            for uri_ar in res2:
                uri_ar = uri_ar[0]
                res = AggregatedResource(uri_ar)
                things[uri_ar] = res
                proxy = list(graph.query("PREFIX ore: <http://www.openarchives.org/ore/terms/> SELECT ?a WHERE {?a ore:proxyFor <%s> .}" % uri_ar ))
                try:
                    uri_p = proxy[0][0]
                    p = Proxy(uri_p)
                    p.set_forIn(res, aggr)
                    things[uri_p] = p
                    aggr.add_resource(res, p)
                    self.set_fields(res, graph)
                    self.set_fields(p, graph)
                except IndexError:
                    aggr.add_resource(res, None)
                    self.set_fields(res, graph)

            allThings = things.copy()

            agents = list(graph.query("PREFIX foaf: <%s> PREFIX dcterms: <%s> SELECT ?a WHERE { { ?a foaf:name ?b } UNION { ?a foaf:mbox ?b } UNION { ?b dcterms:creator ?a } UNION { ?b dcterms:contributor ?a } }" % (namespaces['foaf'], namespaces['dcterms'])))
            for a_uri in agents:
                a_uri = a_uri[0]
                a = Agent(a_uri)
                allThings[a_uri] = a
                self.set_fields(a, graph)
                for (subj, pred) in graph.subject_predicates(URIRef(a_uri)):
                    if things.has_key(subj):
                        # direct manipulation, as will have already added predicate in set_fields
                        things[subj]._agents_.append(a)

            for at in aggr.triples:
                allThings[at.uri] = at            

            for subj in graph.subjects():
                if not allThings.has_key(subj):
                    # triple needed
                    ar = ArbitraryResource(subj)
                    allThings[subj] = ar
                    # find our graph
                    for (pred, obj) in graph.predicate_objects(subj):
                        ar.graph.add((subj, pred, obj))

                    # find shortest distance to main object to link to main graph
                    # Breadth First Search
                    found = 0
                    checked = {}
                    tocheck = list(graph.subject_predicates(subj))
                    while tocheck:
                        subsubj = tocheck.pop(0)[0]
                        if things.has_key(subsubj):
                            things[subsubj]._triples_.append(ar)
                            found = 1
                            break
                        else:
                            tocheck.extend(graph.subject_predicates(subsubj))
                    if not found:
                        # Input graph is not connected!
                        aggr._triples_.append(ar)

        return aggr
        

# types:  Sleepycat, MySQL, SQLite. Others: ZODB, Redland

class SQLiteTripleStore(TripleStore):

    def __init__(self, configuration='', db="rdfstore.sql", create=False):
        """ configuration = path to create store in """
        self.storeType = 'SQLite'
        TripleStore.__init__(self,configuration,db,create)


class MySQLTripleStore(TripleStore):
    def __init__(self, configuration='', db="rdfstore", create=False):
        """ configuration = dbapi2 config:
                 host=SQL-HOST,password=PASSWORD,user=USER,db=DB"
        """
        #"
        self.storeType = 'MySQL'
        TripleStore.__init__(self,configuration,db,create)


class BdbTripleStore(TripleStore):
    def __init__(self, configuration='', db='', create=False):
        """ configuration = path to create files in """
        #"
        self.storeType = 'Sleepycat'
        TripleStore.__init__(self, configuration, db, create)
