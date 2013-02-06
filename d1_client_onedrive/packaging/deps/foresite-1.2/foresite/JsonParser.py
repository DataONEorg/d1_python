
try:
    import json
except ImportError:
    import simplejson as json

from rdflib.syntax.parsers import Parser
from rdflib import URIRef, BNode, Literal

class JsonParser(Parser):
    
    def __init__(self):
        pass

    def parse(self, source, sink, **args):

        data = source.getByteStream().read()
        objs = json.loads(data)

        # check if pretty-json
        keys = objs.keys()
        pretty = 0
        bindings = {}

        for k in keys:
            if k.startswith('xmlns$') or k.startswith('xmlns:'):
                pretty = 1
                bindings[k[6:]] = objs[k]

        for k in keys:
            if not k.startswith('xmlns$') and not k.startswith('xmlns:'):
                if k[0] == "_" and k[1] in [':', '$']:
                    # bnode
                    s = BNode(k[2:])
                else:
                    # uri
                    s = URIRef(k)
                # predicates
                preds = objs[k]
                for (p, v) in preds.items():
                    if pretty:
                        dpidx = p.find('$')
                        if dpidx == -1:                            
                            dpidx = p.find(':')
                        if dpidx > -1:
                            pfx = p[:dpidx]
                            dmn = bindings.get(pfx, '')
                            if dmn:
                                pred = URIRef(dmn + p)
                            else:
                                raise ValueError("Unassigned Prefix: %s" % pfx)
                        else:
                            pred = URIRef(p)
                    else:
                        pred = URIRef(p)
                        
                    for vh in v:
                        value = vh['value']
                        vt = vh['type']
                        if vt == 'literal':
                            args = {}
                            lang = vh.get('lang', '')
                            if lang:
                                args['lang'] = lang                            
                            datatype = vh.get('datatype', '')
                            if datatype:
                                args['datatype'] = datatype
                            val = Literal(value, **args)
                        elif vt == 'uri':
                            val = URIRef(value)
                        elif vt == 'bnode':
                            val = BNode(val[2:])
                        sink.add((s, pred, val))
        

            


        # returns None
