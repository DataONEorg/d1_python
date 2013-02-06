
import re
from ore import *
from ore import foresiteAgent
from foresite import libraryName, libraryUri, libraryVersion
from utils import namespaces, OreException, unconnectedAction, pageSize
from utils import gen_uuid, build_html_atom_content
from rdflib import URIRef, BNode, Literal, plugin, syntax, RDF
from rdflib.util import uniq
from lxml import etree
from lxml.etree import Element, SubElement

plugin.register('rdfa', syntax.serializers.Serializer, 'foresite.RDFaSerializer', 'RDFaSerializer')
plugin.register('json', syntax.serializers.Serializer, 'foresite.JsonSerializer', 'JsonSerializer')
plugin.register('pretty-json', syntax.serializers.Serializer, 'foresite.JsonSerializer', 'PrettyJsonSerializer')


class ORESerializer(object):
    # Take objects and produce data
    mimeType = ""
    format = ""
    public = 1

    def __init__(self, format, public=1):
        mimetypes = {'atom' : 'application/atom+xml', 
                     'rdfa' : 'application/xhtml+xml',
                     'xml' : 'application/rdf+xml',
                     'nt' : 'text/plain',
                     'n3' : 'text/rdf+n3',
                     'turtle' : 'application/x-turtle',
                     'pretty-xml' : 'application/rdf+xml'
                     }
        self.extensions = {'atom': 'atom',
                           'rdfa' : 'xhtml',
                           'xml' : 'xml',
                           'nt' : 'nt',
                           'n3' : 'n3',
                           'turtle' : 'ttl',
                           'pretty-xml' : 'pretty.xml'
                           }        
        self.format = format
        self.public = public
        self.mimeType = mimetypes.get(format, '')

    def merge_graphs(self, rem, page=-1):
        g = Graph()
        # Put in some sort of recognition of library?

        n = now()
        if not rem.created:
            rem._dcterms.created = n
        rem._dcterms.modified = n
        if not rem._dcterms.creator:
            rem.add_agent(foresiteAgent, 'creator')

        aggr = rem.aggregation
        stack = [rem, aggr]

        if page != -1:
            # first is 1, 2, 3 ...
            start = (page-1) * pageSize
            tosrlz = aggr._resources_[start:start+pageSize]
        else:
            tosrlz = aggr._resources_

        remove = []
        for (r, p) in tosrlz:
            if isinstance(r, Aggregation):
                for a in r._ore.aggregates:
                    remove.append((r._uri_, namespaces['ore']['aggregates'], a))                
            stack.extend([r, p])

        done = []
        while stack:
            what = stack.pop(0)
            if what == None or what in done:
                continue
            done.append(what)            
            g += what._graph_
            for at in what._triples_.values():
                stack.append(at)
            for who in what._agents_.values():
                stack.append(who)
                
        if self.public:
            # Remove internal methods
            for p in internalPredicates:
                for (s,o) in g.subject_objects(p):
                    g.remove((s,p,o))
        for trip in remove:
            g.remove(trip)
            
        if not aggr._resources_:
            raise OreException("Aggregation must aggregate something")
        g = self.connected_graph(g, aggr._uri_)
        return g

    def connected_graph(self, graph, uri):
        if unconnectedAction == 'ignore':
            return graph
        g = Graph()
        all_nodes = list(graph.all_nodes())
        all_nodes = filter(lambda y: not isinstance(y, Literal), all_nodes)
        discovered = {}
        visiting = [uri]
        while visiting:
            x = visiting.pop()
            if not discovered.has_key(x):
                discovered[x] = 1
            for (p, new_x) in graph.predicate_objects(subject=x):
                g.add((x,p,new_x))
                if (isinstance(new_x, URIRef) or isinstance(new_x, BNode)) and not discovered.has_key(new_x) and not new_x in visiting:
                    visiting.append(new_x)
            for (new_x, p) in graph.subject_predicates(object=x):
                g.add((new_x,p,x))
                if (isinstance(new_x, URIRef) or isinstance(new_x, BNode)) and not discovered.has_key(new_x) and not new_x in visiting:
                    visiting.append(new_x)
        if len(discovered) != len(all_nodes):
            if unconnectedAction == 'warn':
                print "Warning: Graph is unconnected, some nodes being dropped"
            elif unconnectedAction == 'raise':
                raise OreException('Graph to be serialized is unconnected')
            elif unconnectedAction != 'drop':
                raise ValueError('Unknown unconnectedAction setting: %s' % unconnectedAction)
        return g


class RdfLibSerializer(ORESerializer):

    def serialize(self, rem, page=-1):
        g = self.merge_graphs(rem, page)
        data = g.serialize(format=self.format)
        uri = str(rem._uri_)
        rd = ReMDocument(uri, data, format=self.format, mimeType=self.mimeType)
        return rd

class AtomSerializer(ORESerializer):

    def __init__(self, format="atom", public=1):
        ORESerializer.__init__(self, format)
        self.spacesub = re.compile('(?<=>)[ ]+(?=<)')
        self.done_triples = []


    def generate_rdf(self, parent, sg):
        # remove already done, then serialize to rdf/xml
        for t in self.done_triples:
            sg.remove(t)
        data = sg.serialize(format='xml')
        root = etree.fromstring(data)
        for child in root:
            parent.append(child)

    def make_agent(self, parent, agent):
        n = SubElement(parent, '{%s}name' % namespaces['atom'])
        try:
            name = agent._foaf.name[0]
            n.text = str(name)
            self.done_triples.append((agent._uri_, namespaces['foaf']['name'], name))
        except:
            pass
        if agent._foaf.mbox:
            n = SubElement(parent, '{%s}email' % namespaces['atom'])
            mb = agent._foaf.mbox[0]
            self.done_triples.append((agent._uri_, namespaces['foaf']['mbox'], mb))
            mb = str(mb)
            if mb[:7] == "mailto:":
                mb = mb[7:]
            n.text = mb            

        # There's currently nowhere for URI to go!
        #if not isinstance(agent._uri_, BNode):
        #    n = SubElement(parent, 'uri')
        #    n.text = str(agent._uri_)
            
        # Silly, but it's what the spec says...
        if agent._foaf.page:
            n = SubElement(parent, '{%s}uri' % namespaces['atom'])
            fp = agent._foaf.page[0]
            self.done_triples.append((agent._uri_, namespaces['foaf']['page'], fp))
            n.text = fp


    def make_link(self, parent, rel, t, g):

        iana = str(namespaces['iana'])
        if rel.startswith(iana):
            rel = rel[len(iana):]
        e = SubElement(parent, '{%s}link' % namespaces['atom'], rel=rel, href=str(t))
        fmts = list(g.objects(t, namespaces['dc']['format']))
        if fmts:
            f = fmts[0]
            e.set('type', str(f))
            self.done_triples.append((t, namespaces['dc']['format'], f))
        langs = list(g.objects(t, namespaces['dc']['language']))
        if langs:
            l = langs[0]
            e.set('hreflang', str(langs[0]))        
            self.done_triples.append((t, namespaces['dc']['language'], l))
            
        exts = list(g.objects(t, namespaces['dc']['extent']))
        if exts:
            l = exts[0]
            e.set('length', str(l))
            self.done_triples.append((t, namespaces['dc']['extent'], l))
            
        titls = list(g.objects(t, namespaces['dc']['title']))
        if titls:
            l = titls[0]
            e.set('title', str(l))
            self.done_triples.append((t, namespaces['dc']['title'], l))


    def serialize(self, rem, page=-1):
        aggr = rem._aggregation_
        g = self.merge_graphs(rem)

        # make nsmap better
        nm = g.namespace_manager
        nsmap = {'atom' : str(namespaces['atom'])}
        poss = uniq(g.predicates()) + uniq(g.objects(None, RDF.type))        
        for pred in poss:
            pf,ns,l = nm.compute_qname(pred)
            nsmap[pf] = ns
        
        root = Element("{%s}entry" % namespaces['atom'], nsmap=nsmap)

        # entry/id == tag for entry == ReM dc:identifier
        # if not exist, generate Yet Another uuid
        e = SubElement(root, '{%s}id' % namespaces['atom'])
        if rem._dc.identifier:
            dcid = rem._dc.identifier[0]
            e.text = str(dcid)
            self.done_triples.append((rem._uri_, namespaces['dc']['identifier'], dcid))
        else:
            e.text = "urn:uuid:%s" % gen_uuid()

        # entry/title == Aggr's dc:title 
        title = aggr._dc.title
        tns = 'dc'
        if not title:
            title = aggr._dcterms.title
            tns = 'dcterms'
        if not title:
            raise OreException("Atom Serialisation requires title on aggregation")
        else:
            e = SubElement(root, '{%s}title' % namespaces['atom'])
            dctit = title[0]
            e.text = str(dctit)
            self.done_triples.append((aggr._uri_, namespaces[tns]['title'], dctit))

        # entry/author == Aggr's dcterms:creator
        for who in aggr._dcterms.creator:
            e = SubElement(root, '{%s}author' % namespaces['atom'])
            agent = aggr._agents_[who]
            self.make_agent(e, agent)
            self.done_triples.append((aggr._uri_, namespaces['dcterms']['creator'], agent._uri_))

        # entry/contributor == Aggr's dcterms:contributor
        for bn in aggr._dcterms.contributor:
            e = SubElement(root, '{%s}contributor' % namespaces['atom'])
            agent = aggr._agents_[who]
            self.make_agent(e, agent)
            self.done_triples.append((aggr._uri_, namespaces['dcterms']['contributor'], agent._uri_))

        # entry/category[@scheme="(magic)"][@term="(datetime)"]        
        for t in aggr._dcterms.created:
            t = t.strip()
            e = SubElement(root, '{%s}category' % namespaces['atom'], term=str(t),
                           scheme="http://www.openarchives.org/ore/terms/datetime/created")   
        for t in aggr._dcterms.modified:
            t = t.strip()
            e = SubElement(root, '{%s}category' % namespaces['atom'], term=str(t),
                           scheme="http://www.openarchives.org/ore/terms/datetime/modified")
        
        # entry/category == Aggr's rdf:type
        for t in aggr._rdf.type:
            e = SubElement(root, '{%s}category' % namespaces['atom'], term=str(t))
            try:
                scheme = list(g.objects(t, namespaces['rdfs']['isDefinedBy']))[0]
                e.set('scheme', str(scheme))
                self.done_triples.append((t, namespaces['rdfs']['isDefinedBy'], scheme))
            except:
                pass
            try:
                label = list(g.objects(t, namespaces['rdfs']['label']))[0]
                e.set('label', str(label))
                self.done_triples.append((t, namespaces['rdfs']['label'], label))
            except:
                pass
            self.done_triples.append((aggr._uri_, namespaces['rdf']['type'], t))

        # entry/summary
        if aggr._dc.description:
            e = SubElement(root, '{%s}summary' % namespaces['atom'])
            desc = aggr._dc.description[0]
            e.text = str(desc)
            self.done_triples.append((aggr._uri_, namespaces['dc']['description'], desc))

        # All aggr links:
        done = [namespaces['rdf']['type'],
                namespaces['ore']['aggregates'],
                namespaces['dcterms']['creator'],
                namespaces['dcterms']['contributor'],
                namespaces['dc']['title'],
                namespaces['dc']['description']
                ]
        for (p, o) in g.predicate_objects(aggr.uri):
            if not p in done:
                if isinstance(o, URIRef):
                    self.make_link(root, p, o, g)
                    self.done_triples.append((aggr._uri_, p, o))
        
        # entry/content   //  link[@rel="alternate"]
        # Do we have a splash page?
        altDone = 0
        atypes = aggr._rdf._type
        possAlts = []
        for (r, p) in aggr.resources:
            mytypes = r._rdf.type
            if namespaces['eurepo']['humanStartPage'] in mytypes:
                altDone = 1
                self.make_link(root, 'alternate', r.uri, g)
                break
            # check if share non Aggregation type
            # eg aggr == article and aggres == article, likely
            # to be good alternate
            for m in mytypes:
                if m != namespaces['ore']['Aggregation'] and \
                   m in atypes:
                    possAlt.append(r.uri)

        if not altDone and possAlts:
            # XXX more intelligent algorithm here
            self.make_link(root, '{%s}alternate' % namespaces['atom'], possAlts[0], g)
            altDone = 1

        if not altDone and build_html_atom_content:
            e = SubElement(root, '{%s}content' % namespaces['atom'])
            e.set('type', 'html')
            # make some representative html
            # this can get VERY LONG so default to not doing this
            html = ['<ul>']
            for (r, p) in aggr.resources:
                html.append('<li><a href="%s">%s</a></li>' % (r.uri, r.title[0]))
            html.append('</ul>')
            e.text = '\n'.join(html)
        else:
            e = SubElement(root, '{%s}content' % namespaces['atom'])
            e.set('type', 'html')
            e.text = "No Content"

        # entry/link[@rel='self'] == URI-R
        self.make_link(root, 'self', rem._uri_, g)
        # entry/link[@rel='ore:describes'] == URI-A
        self.make_link(root, namespaces['ore']['describes'], aggr._uri_, g)

        
        ### These are generated automatically in merge_graphs
        
        # entry/published == ReM's dcterms:created
        if rem._dcterms.created:
            e = SubElement(root, '{%s}published' % namespaces['atom'])
            c = rem._dcterms.created[0]
            md = str(c)
            if md.find('Z') == -1:
                # append Z
                md += "Z"
            e.text = md
            self.done_triples.append((rem._uri_, namespaces['dcterms']['created'], c))

        # entry/updated == ReM's dcterms:modified
        e = SubElement(root, '{%s}updated' % namespaces['atom'])
        if rem._dcterms.modified:
            c = rem._dcterms.modified[0]
            md = str(c)
            if md.find('Z') == -1:
                # append Z
                md += "Z"
            e.text = str(md)
            
            self.done_triples.append((rem._uri_, namespaces['dcterms']['modified'], c))
        else:
            e.text = now()

        # entry/rights == ReM's dc:rights
        if rem._dc.rights:
            e = SubElement(root, '{%s}rights' % namespaces['atom'])
            r = rem._dc.rights[0]
            e.text = str(r)
            self.done_triples.append((rem._uri_, namespaces['dc']['rights'], r))


        # entry/source/author == ReM's dcterms:creator
        if rem._dcterms.creator:
            # Should at least be our generator! (right?)
            src = SubElement(root, '{%s}source' % namespaces['atom'])
            for who in rem._dcterms.creator:
                e = SubElement(src, '{%s}author' % namespaces['atom'])
                agent = rem._agents_[who]
                self.make_agent(e, agent)
                self.done_triples.append((rem._uri_, namespaces['dcterms']['creator'], agent._uri_))
            for who in rem._dcterms.contributor:
                e = SubElement(src, '{%s}contributor' % namespaces['atom'])
                agent = rem._agents_[who]
                self.make_agent(e, agent)
                self.done_triples.append((rem._uri_, namespaces['dcterms']['contributor'], agent._uri_))
            e = SubElement(src, '{%s}generator' % namespaces['atom'], uri=str(libraryUri), version=str(libraryVersion))
            e.text = str(libraryName)


        # Remove aggregation, resource map props already done
        # All of agg res needs to be done

        for (r, p) in aggr.resources:
            self.make_link(root, namespaces['ore']['aggregates'], r.uri, g)
            self.done_triples.append((aggr._uri_, namespaces['ore']['aggregates'], r._uri_))

        # Now create ore:triples
        # and populate with rdf/xml

        trips = SubElement(root, '{%s}triples' % namespaces['ore'])
        self.generate_rdf(trips, g)

        data = etree.tostring(root, pretty_print=True)
        #data = data.replace('\n', '')
        #data = self.spacesub.sub('', data)
        uri = str(rem._uri_)

        self.done_triples = []

        return ReMDocument(uri, data, format='atom', mimeType=self.mimeType)




class OldAtomSerializer(ORESerializer):

    def __init__(self, format="atom0.9", public=1):
        ORESerializer.__init__(self, format)
        self.spacesub = re.compile('(?<=>)[ ]+(?=<)')
        self.done_triples = []

    def remove_link_attrs(self, sg, a):
        # only remove first from each list
        for ns in (namespaces['dc']['format'], namespaces['dc']['title'], namespaces['dc']['language'], namespaces['dc']['extent']):
            objs = list(sg.objects(a, ns))
            if objs:
                sg.remove((a, ns, objs[0]))
        
    def generate_rdf(self, parent, what):
        # extract not processed parts of graph
        # serialise with rdflib
        # parse with lxml and add to parent element

        sg = Graph()
        sg += what.graph
        for at in what.triples.values():
            sg += at.graph
        for a in what.agents.values():
            sg += a.graph

        for a in what.type:                
            for b in sg.objects(a, namespaces['rdfs']['isDefinedBy']):
                sg.remove((a, namespaces['rdfs']['isDefinedBy'], b))
            for b in sg.objects(a, namespaces['rdfs']['label']):
                sg.remove((a, namespaces['rdfs']['label'], b))
            sg.remove((what.uri, namespaces['rdf']['type'], a))

        for t in self.done_triples:
            sg.remove(t)

        if isinstance(what, Aggregation) or isinstance(what, AggregatedResource):
            # remove atom srlzd bits
            self.remove_link_attrs(sg, what.uri)
            try:
                sg.remove((what.uri, namespaces['dc']['description'], what.description[0]))
            except:
                pass
            for a in what.creator:
                sg.remove((what.uri, namespaces['dcterms']['creator'], a))
                                
            for a in what.contributor:
                sg.remove((what.uri, namespaces['dcterms']['contributor'], a))

            for a in what._ore.similarTo:
                self.remove_link_attrs(sg, a)
                sg.remove((what.uri, namespaces['ore']['similarTo'], a))
            for a in what._ore.aggregates:
                sg.remove((what.uri, namespaces['ore']['aggregates'], a))
            try:
                # aggregation uses dcterms rights, as it's a URI
                for a in what._dcterms.rights:
                    self.remove_link_attrs(sg, a)
                    sg.remove((what.uri, namespaces['dcterms']['rights'], a))
            except:
                pass
            try:
                sg.remove((what.uri, namespaces['foaf']['logo'], what._foaf.logo))
            except:
                pass
            if isinstance(what, Aggregation):
                for a in sg.objects(what.uri, namespaces['ore']['isDescribedBy']):
                    self.remove_link_attrs(sg, a)
                    sg.remove((what.uri, namespaces['ore']['isDescribedBy'], a))
                self.done_triples.extend(list(sg))
            else:
                # remove isAggregatedBy == rel=related
                for a in what._ore.isAggregatedBy:
                    sg.remove((what.uri, namespaces['ore']['isAggregatedBy'], a))
                self.done_triples = []
                # and add in proxy info
                proxy = what._currProxy_
                if proxy:
                    sg += proxy.graph
                    for a in proxy._agents_.values():
                        sg += a.graph
                    # remove proxyFor, proxyIn
                    for a in proxy._ore.proxyFor:
                        sg.remove((proxy.uri, namespaces['ore']['proxyFor'], a))
                    for a in proxy._ore.proxyIn:
                        sg.remove((proxy.uri, namespaces['ore']['proxyIn'], a))
                    for a in proxy.type:                
                        for b in sg.objects(a, namespaces['rdfs']['isDefinedBy']):
                            sg.remove((a, namespaces['rdfs']['isDefinedBy'], b))
                        for b in sg.objects(a, namespaces['rdfs']['label']):
                            sg.remove((a, namespaces['rdfs']['label'], b))
                        sg.remove((proxy.uri, namespaces['rdf']['type'], a))

        elif isinstance(what, ResourceMap):

            self.remove_link_attrs(sg, what.uri)
            for a in what.describes:
                sg.remove((what.uri, namespaces['ore']['describes'], a))
            for a in what.creator:
                sg.remove((what.uri, namespaces['dcterms']['creator'], a))
            try:
                # ReM uses dc rights, as it's a string
                sg.remove((what.uri, namespaces['dc']['rights'], what._dc.rights[0]))
            except:
                pass
            try:
                sg.remove((what.uri, namespaces['dcterms']['modified'], what._dcterms.modified[0]))
            except:
                pass
            try:
                sg.remove((what.uri, namespaces['foaf']['logo'], what._foaf.logo[0]))
            except:
                pass
            try:
                sg.remove((what.uri, namespaces['ore']['describes'], what._ore.describes[0]))
            except:
                pass
            self.done_triples = []

        data = sg.serialize(format='xml')
        root = etree.fromstring(data)
        for child in root:
            parent.append(child)


    def make_agent(self, parent, agent):
        n = SubElement(parent, 'name')
        try:
            name = agent._foaf.name[0]
            n.text = str(name)
            self.done_triples.append((agent._uri_, namespaces['foaf']['name'], name))
        except:
            # allow blank names where unknown
            pass

        if agent._foaf.mbox:
            n = SubElement(parent, 'email')
            mb = agent._foaf.mbox[0]
            self.done_triples.append((agent._uri_, namespaces['foaf']['mbox'], mb))
            mb = str(mb)
            # Strip mailto: (eg not a URI any more)
            if mb[:7] == "mailto:":
                mb = mb[7:]
            n.text = mb            
        if not isinstance(agent._uri_, BNode):
            n = SubElement(parent, 'uri')
            n.text = str(agent._uri_)


    def make_link(self, parent, rel, t, g):
        e = SubElement(parent, 'link', rel=rel, href=str(t))
        # look for format, language, extent  of t
        fmts = list(g.objects(t, namespaces['dc']['format']))
        if fmts:
            e.set('type', str(fmts[0]))
        langs = list(g.objects(t, namespaces['dc']['language']))
        if langs:
            e.set('hreflang', str(langs[0]))        
        exts = list(g.objects(t, namespaces['dc']['extent']))
        if exts:
            e.set('length', str(exts[0]))
        titls = list(g.objects(t, namespaces['dc']['title']))
        if titls:
            e.set('title', str(titls[0]))

    def serialize(self, rem, page=-1):
        aggr = rem._aggregation_
        # Check entire graph is connected
        g = self.merge_graphs(rem)
        
        if namespaces.has_key(''):
            del namespaces[u'']
        root = Element("feed", nsmap=namespaces)
        #namespaces[''] = myNamespace

        ## Aggregation Info
        e = SubElement(root, 'id')
        e.text = str(aggr.uri)
        if not aggr._dc.title:
            raise OreException("Atom Serialisation requires title on aggregation")
        else:
            e = SubElement(root, 'title')
            e.text = str(aggr._dc.title[0])
        if aggr._dc.description:
            e = SubElement(root, 'subtitle')
            e.text = str(aggr._dc.description[0])

        for who in aggr._dcterms.creator:
            e = SubElement(root, 'author')            
            agent = aggr._agents_[who]
            self.make_agent(e, agent)

        for bn in aggr._dcterms.contributor:
            e = SubElement(root, 'contributor')
            agent = aggr._agents_[bn]
            self.make_agent(e, agent)
            
        for t in aggr._ore.similarTo:
            self.make_link(root, 'related', t, g)

        for t in aggr._dcterms.rights:
            self.make_link(root, 'license', t, g)

        for t in aggr._rdf.type:
            e = SubElement(root, 'category', term=str(t))
            try:
                scheme = list(g.objects(t, namespaces['rdfs']['isDefinedBy']))[0]
                e.set('scheme', str(scheme))
            except:
                pass
            try:
                label = list(g.objects(t, namespaces['rdfs']['label']))[0]
                e.set('label', str(label))
            except:
                pass

        orms = []
        for orm in aggr._resourceMaps_:
            if orm != rem:
                self.make_link(root, 'alternate', orm.uri, g)
                orms.append(orm.uri)
        for t in aggr._ore.isDescribedBy:
            # check not in orms
            if not t in orms:
                self.make_link(root, 'alternate', t, g)

        self.generate_rdf(root, aggr)

        ## ReM Info
        self.make_link(root, 'self', rem.uri, g)

        e = SubElement(root, 'updated')
        e.text = now()

        # ReM Author
        if rem._dcterms.creator:
            uri = rem._dcterms.creator[0]
            e = SubElement(root, 'generator', uri=str(uri))
            agent = rem._agents_[uri]
            n = agent._foaf.name[0]
            e.text = str(n)
            self.done_triples.append((uri, namespaces['foaf']['name'], n))

        # if no logo, put in nice ORE icon
        e = SubElement(root, 'icon')
        if aggr._foaf.logo:
            e.text = str(aggr._foaf.logo[0])
        elif rem._foaf.logo:
            e.text = str(rem._foaf.logo[0])
        else:
            e.text = "http://www.openarchives.org/ore/logos/ore_icon.png"
        
        if rem._dc.rights:
            e = SubElement(root, 'rights')
            e.text = rem._dc.rights[0]

        self.generate_rdf(root, rem)

        ## Process Entries
        for (res, proxy) in aggr._resources_:
            entry = SubElement(root, 'entry')
            
            e = SubElement(entry, 'id')
            if proxy:
                e.text = str(proxy.uri)
            else:
                e.text = "urn:uuid:%s" % gen_uuid()
            e = SubElement(entry, 'link', rel="alternate", href=str(res.uri))
            # type = dc:format
            fmt = list(g.objects(res.uri, namespaces['dc']['format']))
            if fmt:
                e.set('type', str(fmt[0]))
            
            if not res._dc.title:
                raise ValueError("All entries must have a title for ATOM serialisation")
            else:
                e = SubElement(entry, 'title')
                e.text = str(res._dc.title[0])
            for t in res._rdf.type:
                e = SubElement(entry, 'category', term=str(t))
                try:
                    scheme = list(g.objects(t, namespaces['rdfs']['isDefinedBy']))[0]
                    e.set('scheme', str(scheme))
                except:
                    pass
                try:
                    label = list(g.objects(t, namespaces['rdfs']['label']))[0]
                    e.set('label', str(label))
                except:
                    pass
            for a in res._dcterms.creator:
                e = SubElement(entry, 'author')
                agent = res._agents_[a]
                self.make_agent(e, agent)
            for a in res._dcterms.contributor:
                e = SubElement(entry, 'contributor')
                agent = res._agents_[a]
                self.make_agent(e, agent)
            if res._dcterms.abstract:
                e = SubElement(entry, 'summary')
                e.text = str(res._dcterms.abstract[0])

            # Not sure about this at object level?
            for oa in res._ore.isAggregatedBy:
                if oa != aggr._uri_:
                    e = SubElement(entry, 'link', rel="related", href=str(oa))

            e = SubElement(entry, 'updated')
            e.text = now()

            if proxy and proxy._ore.lineage:
                e = SubElement(entry, 'link', rel="via", href=str(proxy._ore.lineage[0]))
            res._currProxy_ = proxy
            self.generate_rdf(entry, res)
            res._currProxy_ = None

        data = etree.tostring(root)
        data = data.replace('\n', '')
        data = self.spacesub.sub('', data)
        uri = str(rem._uri_)

        self.done_triples = []

        return ReMDocument(uri, data)
