Foresite
========

Usage
-----

Import everything

    >>> from foresite import *
    >>> from rdflib import URIRef

Create an aggregation

    >>> a = Aggregation('my-aggregation-uri')

Set properties on the aggregation.
The first defaults to dc:title, the second explicitly sets it as 
dcterms:created.

    >>> a.title = "My Aggregation"
    >>> a._dcterms.created = "2008-07-10T12:00:00"

And retrieve properties:

    >>> a._dc.title
    [rdflib.Literal('My Aggregation', ...
    >>> a.created
    [rdflib.Literal('2008-07-10T12:00:00', ...

Note that they become lists as any property can be added multiple times.

Create and Aggregate two resources

    >>> res = AggregatedResource('my-photo-1-uri')
    >>> res.title = "My first photo"
    >>> res2 = AggregatedResource('my-photo-2-uri')
    >>> res2.title = "My second photo"
    >>> a.add_resource(res)
    >>> a.add_resource(res2)


Create and associate an agent (without a URI) with the aggregation

    >>> me = Agent()
    >>> me.name = "Rob Sanderson"
    >>> a.add_agent(me, 'creator')

If no URI assigned, then it will be a blank node:

    >>> me.uri
    rdflib.BNode(...

Create an agent with a URI:

    >>> you = Agent('uri-someone-else')

Register an Atom serializer with the aggregation.
The registration creates a new ResourceMap, which needs a URI.

    >>> serializer = AtomSerializer()
    >>> rem = a.register_serialization(serializer, 'my-atom-rem-uri')

And fetch the serialisation.

    >>> remdoc = a.get_serialization()
    >>> print remdoc.data
    <entry ...

Or, equivalently:

    >>> remdoc = rem.get_serialization()
    >>> print remdoc.data
    <entry ...

Resource Maps can be created by hand:

    >>> rem2 = ResourceMap('my-rdfa-rem-uri')
    >>> rem2.set_aggregation(a)

And have their own serializers:

    >>> rdfa = RdfLibSerializer('rdfa')
    >>> rem2.register_serialization(rdfa)
    >>> remdoc2 = rem2.get_serialization()
    >>> print remdoc2.data
    <div id="ore:ResourceMap" xmlns...

Possible values for RdfLibSerializer:  rdf (rdf/xml), pretty-xml (pretty rdf/xml), nt (n triples), turtle, n3, rdfa (Invisible RDFa XHTML snippet)


Parsing existing Resource Maps.
The argument to ReMDocument can be a filename or a URL.

    >>> remdoc = ReMDocument("http://www.openarchives.org/ore/1.0/atom-examples/atom_arXiv_maxi.atom")
    >>> ap = AtomParser()
    >>> rem = ap.parse(remdoc)
    >>> aggr = rem.aggregation

Or an RDF Parser, which requires format to be set on the rem document:

    >>> rdfp = RdfLibParser()
    >>> remdoc2.format = 'rdfa'     # done by the serializer by default
    >>> rdfp.parse(remdoc2)
    <foresite.ore.ResourceMap object ...

Possible values for format:  xml, trix, n3, nt, rdfa

And then re-serialise in a different form:

    >>> rdfxml = RdfLibSerializer('xml')
    >>> rem2 = aggr.register_serialization(rdfxml, 'my-rdf-rem-uri')
    >>> remdoc3 = rem2.get_serialization()

Creating arbitrary triples:

    >>> something = ArbitraryResource('uri-random')
    >>> a.add_triple(something)

And then treat them like any object

    >>> something.title = "Random Title"
    >>> something._rdf.type = URIRef('http://somewhere.org/class/something')

