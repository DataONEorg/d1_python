
import urllib
import time
import re
from rdflib import Namespace

### Configuration Options
### Assign a UUID URI or Blank Node for autogenerating agent URIs
### if not present in data
assignAgentUri = False
#assignAgentUri = True

### Use UUID or oreproxy.org for autogenerating proxy URIs if
### not present in data
proxyType = 'proxy'
# proxyType = 'UUID'

### What to do when encountering an unconnected graph:

unconnectedAction = 'ignore'  # produce unconnected graph
#unconnectedAction = 'drop'  # drop any unconnected triples silently
#unconnectedAction = 'warn' # print a warning
#unconnectedAction = 'raise' # raise an Exception

# Number of resources per page to serialise
pageSize = 10

# XSLT server to create alternate representation from Atom Entry
atomXsltUri = ""
# atomXsltUri = "http://www.oreproxy.org/alt?what=%s"

build_html_atom_content = False
accept_header = 'application/rdf+xml;q=1.0, application/atom+xml;q=0.9, text/rdf+n3;q=0.8'

protocolUriRe = re.compile("^([s]?http[s]?://|[t]?ftp:/|z39.50r:|gopher:|imap://|news:|nfs:|nntp:|rtsp:)")

def gen_proxy_uuid(res, aggr):
    u = gen_uuid()
    return "urn:uuid:%s" % u

def gen_proxy_oreproxy(res, aggr):
    a = urllib.quote(str(aggr.uri))
    ar = urllib.quote(str(res.uri))
    return "http://oreproxy.org/r?what=%s&where=%s" % (ar,a)

# Hash must come after function definitions
# Define your own function, set proxyType, and add to hash
proxyTypeHash = {'UUID' : gen_proxy_uuid,
                 'proxy' : gen_proxy_oreproxy
                 }

### Namespace Definitions
### If you need a new namespace you MUST add it into this hash

namespaces = {'ore' : Namespace('http://www.openarchives.org/ore/terms/'),
              'orex' : Namespace('http://foresite.cheshire3.org/orex/terms/'),
              'dc' : Namespace('http://purl.org/dc/elements/1.1/'),
              'mesur' : Namespace('http://www.mesur.org/schemas/2007-01/mesur#'),
              'dcterms' : Namespace('http://purl.org/dc/terms/'),
              'swap' : Namespace('http://purl.org/eprint/type/'),
              'rdf' : Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
              'foaf' : Namespace('http://xmlns.com/foaf/0.1/'),
              'rdfs' : Namespace('http://www.w3.org/2001/01/rdf-schema#'),
              'dcmitype' : Namespace('http://purl.org/dc/dcmitype/'),
              'atom' : Namespace('http://www.w3.org/2005/Atom'),
              'owl' : Namespace('http://www.w3.org/2002/07/owl#'),
              'xsd' : Namespace('http://www.w3.org/2001/XMLSchema'),
              'xhtml' : Namespace('http://www.w3.org/1999/xhtml'),
              'grddl' : Namespace('http://www.w3.org/2003/g/data-view#'),
              'swetodblp' : Namespace('http://lsdis.cs.uga.edu/projects/semdis/opus#'),
              'skos' : Namespace('http://www.w3.org/2004/02/skos/core#'),
              'eurepo' : Namespace('info:eu-repo/semantics/'),
              'at' : Namespace('http://purl.org/syndication/atomtriples/1/'),
              'iana' : Namespace('http://www.iana.org/assignments/relation/'),
              'bibo' : Namespace('http://purl.org/ontology/bibo/'),
              'prism' : Namespace('http://prismstandard.org/namespaces/1.2/basic/'),
              'vcard' : Namespace('http://nwalsh.com/rdf/vCard#'),
              'zotero' : Namespace('http://www.zotero.org/namespaces/exprt#')              
              }

### Elements commonly used in ORE
### If an element is in this list, you can do object.predicate,
### rather than object._namespace.predicate
# (Not complete for most namespaces, just common terms)
elements = {
    'ore' : ['describes', 'isDescribedBy', 'aggregates', 'isAggregatedBy', 'similarTo', 'proxyFor', 'proxyIn', 'lineage'],
    'orex' : ['isAuthoritativeFor', 'AnonymousAgent', 'page', 'follows', 'firstPage', 'lastPage'],
    'dc' : ['coverage', 'date', 'description', 'format', 'identifier', 'language', 'publisher', 'relation', 'rights', 'source', 'subject', 'title'],  # no creator, contributor
    'dcterms': ['abstract', 'accessRights', 'accrualMethod', 'accrualPeriodicity', 'accrualPolicy', 'alternative', 'audience', 'available', 'bibliographicCitation', 'conformsTo', 'contributor', 'created', 'creator', 'dateAccepted', 'dateCopyrighted', 'dateSubmitted', 'educationLevel', 'extent', 'hasFormat', 'hasPart', 'hasVersion', 'instructionalMethod', 'isFormatOf', 'isPartOf', 'isReferencedBy', 'isReplacedBy', 'isRequiredBy', 'issued', 'isVersionOf', 'license', 'mediator', 'medium', 'modified', 'provenance', 'references', 'replaces', 'requires', 'rights', 'rightsHolder', 'spatial', 'tableOfContents', 'temporal', 'valid'],  # also rights
    'foaf' : ['accountName', 'aimChatID', 'birthday', 'depiction', 'depicts', 'family_name', 'firstName', 'gender', 'givenname', 'homepage', 'icqChatID', 'img', 'interest', 'jabberID', 'knows', 'logo', 'made', 'maker', 'mbox', 'member', 'msnChatID', 'name', 'nick', 'openid', 'page', 'phone', 'surname', 'thumbnail', 'weblog', 'yahooChatID'],
    'owl' : ['sameAs'],
    'rdf' : ['type'],
    'rdfs' : ['seeAlso', 'label', 'isDefinedBy'],
    'mesur' : ['hasAccess', 'hasAffiliation', 'hasIssue', 'hasVolume', 'used', 'usedBy'],
    'skos' : ['prefLabel', 'inScheme', 'broader', 'narrower', 'related', 'Concept', 'ConceptScheme', 'changeNote', 'editorialNote'],
    'iana' : ['alternate', 'current' ,'enclosure', 'edit', 'edit-media', 'first', 'last',  'next', 'next-archive', 'previous', 'payment', 'prev-archive', 'related', 'replies', 'service', 'via'],  # -self, -license
    'bibo' : ['Article', 'Issue', 'Journal', 'pageStart', 'pageEnd', 'volume']
    }

### The order in which to search the above hash
namespaceSearchOrder = ['ore', 'dc', 'dcterms', 'foaf', 'rdf', 'rdfs', 'orex', 'owl', 'mesur', 'skos', 'iana']
internalPredicates = [namespaces['orex']['isAuthoritativeFor'],
                      namespaces['orex']['page'],
                      ]

namespaceElemRe = re.compile('^\{(.+)\}(.+)$')

# UUID generator
try:
    # only in Python 2.5+
    import uuid
    def gen_uuid():
        return str(uuid.uuid4())
except:
    # Try 4Suite if installed
    try:
        from Ft.Lib.Uuid import GenerateUuid, UuidAsString
        def gen_uuid():
            return UuidAsString(GenerateUuid())
    except:
        # No luck, try to generate using unix command
        import commands
        def gen_uuid():
            return commands.getoutput('uuidgen')

        uuidre = re.compile("[0-9a-fA-F-]{36}")
        uuid = gen_uuid()

        if not uuidre.match(uuid):
            # probably sh: command not found or other similar
            # weakest version: just build random token
            import random
            chrs = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
            def gen_uuid():
                uuidl = []
                for y in [8,4,4,4,12]:
                    for x in range(y):
                        uuidl.append(random.choice(chrs))
                    uuidl.append('-')
                uuidl.pop(-1)  # strip trailing -
                return ''.join(uuidl)

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")

def gen_proxy_uri(res, aggr):
    # Allow for easier expansion via adding fn to proxyTypeHash
    if proxyTypeHash.has_key(proxyType):
        return proxyTypeHash[proxyType](res, aggr)
    else:
        raise KeyError("Unknown proxyType setting: %s" % proxyType)

class OreException(Exception):
    pass

