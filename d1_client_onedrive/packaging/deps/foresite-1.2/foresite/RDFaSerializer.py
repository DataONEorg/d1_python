from __future__ import generators

from rdflib.syntax.serializers import Serializer

from rdflib.URIRef import URIRef
from rdflib.Literal import Literal
from rdflib.BNode import BNode

from rdflib.util import uniq
from rdflib.exceptions import Error
from rdflib.syntax.xml_names import split_uri

from xml.sax.saxutils import quoteattr, escape


class RDFaSerializer(Serializer):

    def __init__(self, store):
        super(RDFaSerializer, self).__init__(store)

    def __bindings(self):
        store = self.store
        nm = store.namespace_manager
        bindings = {}
        for predicate in uniq(store.predicates()):
            prefix, namespace, name = nm.compute_qname(predicate)
            bindings[prefix] = URIRef(namespace)
        RDFNS = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        if "rdf" in bindings:
            assert bindings["rdf"]==RDFNS
        else:
            bindings["rdf"] = RDFNS
        for prefix, namespace in bindings.iteritems():
            yield prefix, namespace


    def serialize(self, stream, base=None, encoding=None, **args):
        self.base = base
        self.__stream = stream
        self.__serialized = {}
        encoding = self.encoding
        self.write = lambda uni: stream.write(uni.encode(encoding, 'replace'))

        # Basic invisible RDFa
        # <div about="subject">
        #   <a rel="predicate" href="object"></a>
        #   <span property="predicate" content="literal"></span>

        xmlns = []        
        for b in self.__bindings():
            xmlns.append('xmlns:%s=\"%s\"' % b)        

        self.write('<div id="ore:ResourceMap" %s>\n' % ' '.join(xmlns))
        for subject in self.store.subjects():
            self.subject(subject, 1)
        self.write('</div>')
        del self.__serialized


    def subject(self, subject, depth=1):
        if not subject in self.__serialized:
            self.__serialized[subject] = 1
            indent = "  " * depth
            if isinstance(subject, URIRef): 
                uri = quoteattr(self.relativize(subject))
            else:
                # Blank Node
                uri = '"[%s]"' % subject.n3()                
            self.write('%s<div about=%s>\n' % (indent, uri))
            for predicate, object in self.store.predicate_objects(subject):
                self.predicate(predicate, object, depth+1)
            self.write("%s</div>\n" % (indent))


    def predicate(self, predicate, object, depth=1):
        indent = "  " * depth
        qname = self.store.namespace_manager.qname(predicate)
        if isinstance(object, Literal):
            attributes = ""
            if object.language:
                attributes += ' xml:lang="%s"'%object.language
            #if object.datatype:
            #    attributes += ' rdf:datatype="%s"'%object.datatype
            self.write('%s<span property="%s" content="%s"%s></span>\n' %
                       (indent, qname, escape(object, {'"':'&quot;'}), attributes))

        else:
            if isinstance(object, URIRef):
                href = quoteattr(self.relativize(object))
            else:
                # BNode
                href= '"[%s]"' % object.n3()                
            self.write('%s<a rel="%s" href=%s></a>\n' % (indent, qname, href))
