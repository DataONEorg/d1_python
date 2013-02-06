
def skipws(next):
    skip = 1
    if not skip:
        return next
    else:
        def foo(*args):
            tok = next(*args)
            if tok.isspace():
                tok = next(*args)
            return tok
        return foo

class ParseError(Exception):
    pass

class MiniLex(object):

    def __init__(self, data,
                 whitespace= " \t",
                 sep="[](){}<>\\/@:;,?=",
                 quotes="\"",
                 eof="\n\r"):
        self.data = data
        self.whitespace=whitespace
        self.separators=sep
        self.quotes=quotes
        self.eof=eof

        self.state = 0
        self.token = []
        self.quoted = ''
        self.pos = 0

    def __iter__(self):
        return self

    @skipws
    def next(self):
        while True:
            if self.pos == len(self.data):
                if self.token:
                    tok= ''.join(self.token)
                    self.token = []
                    return tok
                else:
                    raise StopIteration
            char = self.data[self.pos]
            tok = ''
            if self.quoted and not char in self.quotes:
                self.token.append(char)
                self.pos +=1
            elif char in self.quotes:
                if char == self.quoted:
                    # we're in quoted text
                    if self.data[self.pos-1] == "\\":
                        self.token.append(char)
                        self.pos += 1
                    else:
                        self.token.append(char)
                        tok = ''.join(self.token)
                        self.token = []
                        self.pos += 1
                        self.quoted=0
                        self.state=0
                        return tok
                elif self.quoted:
                    # other quotes
                    self.token.append(char)
                    self.pos += 1                    
                else:
                    # begin quoted text
                    if self.token:
                        tok = ''.join(self.token)
                    self.quoted=char
                    self.token = [char]
                    self.pos += 1
                    self.state = 2
                    if tok:
                        return tok
            elif char in self.whitespace:
                if self.state == 1:
                    self.token.append(char)
                else:
                    if self.token:
                        tok = ''.join(self.token)                
                    self.state = 1
                    self.token = [char]
                self.pos += 1
                if tok:
                    return tok
            elif char in self.separators:
                # can't join seps (currently)
                if self.token:
                    tok = ''.join(self.token)
                else:
                    tok = char
                    self.pos += 1
                self.token = []
                self.state = 0
                return tok
            elif char in self.eof:
                if self.token:
                    return ''.join(self.token)
                else:
                    raise StopIteration            
            else:
                if self.state == 3: 
                    self.token.append(char)
                else:
                    if self.token:
                        tok = ''.join(self.token)
                    self.token = [char]
                    self.state=3
                self.pos += 1
                if tok:
                    return tok

class MimeType(object):
    def __init__(self):
        self.mimetype1 = ""
        self.mimetype2 = ""
        self.params = {}
        self.qval = 1.0

    def __str__(self):
        #l = [('q', self.qval)]
        #l.extend(self.params.items())        
        # Actually, most likely Don't want to serialize the qval
        l = self.params.items()
        if l:            
            return self.mimetype1 + "/" + self.mimetype2 + ";" + ";".join(["%s=%s" % x for x in l])
        else:
            return self.mimetype1 + "/" + self.mimetype2
            
    def __repr__(self):
        return "<MimeType: %s>" % self

    def sort2(self):
        if self.mimetype1 == "*":
            return 0
        elif self.mimetype2 == "*":
            return 1
        elif self.params:
            return 2 + len(self.params)
        else:
            return 2

    def matches(self, other):
        if other.mimetype1 == self.mimetype1 or other.mimetype1 == '*' or self.mimetype1 == '*':
            if other.mimetype2 == self.mimetype2 or other.mimetype2 == '*' or self.mimetype2 == '*':
                if other.params == self.params:
                    return True
        return False
        

class Parser(object):

    def __init__(self, ml):
        self.ml = ml

    def process(self):
        mts = []
        mt = self.top()
        while mt:
            if mt.mimetype1 == "*" and mt.mimetype2 == "*" and mt.qval == 1.0:
                # downgrade anything to the lowest, otherwise behaviour is
                # non deterministic.  See apache conneg rules.
                mt.qval = 0.001                
            mts.append(mt)
            mt = self.top()
        return mts

    def top(self):
        mt = MimeType()
        try:
            tok = self.ml.next() # text
        except StopIteration:
            return None
        mt.mimetype1 = tok
        sl = self.ml.next() # /
        if sl != "/":
            raise ParseError("Expected /, got: " + sl)        
        tok2 = self.ml.next() # html
        mt.mimetype2 = tok2

        while True:
            try:
                tok = self.ml.next()
            except StopIteration:
                return mt
            if tok == ',':
                return mt
            elif tok == ';':
                (key, val) = self.param()
                if key == "q":
                    mt.qval = float(val)
                else:
                    mt.params[key] = val
            else:
                raise ParseError("Expected , or ; got: %r" % tok)

    def param(self):
        key = self.ml.next()
        eq = self.ml.next()
        if eq != "=":
            raise ParseError("Expected =, got: " + sl)
        val = self.ml.next()
        return (key, val)
            

def best(client, server):
    # step through client request against server possibilities
    # and find highest according to qvals in client
    # both client and server are lists of mt objects
    # client should be sorted by qval already
    # assume that server is unsorted

    # AFAICT, if the request has any params, they MUST be honored
    # so if params, and no exact match, discard
    # And hence */*;params means that params must be matched.
    
    for mtc in client:
        # this is most wanted, can we provide?
        for mts in server:
            if mts.matches(mtc):
                return mtc
    return None
        

def parse(data):
    lex = MiniLex(data)
    p = Parser(lex)
    mts = p.process()
    mts.sort(key=lambda x: x.sort2(), reverse=True)
    mts.sort(key=lambda x: x.qval, reverse=True)
    return mts

if __name__ == '__main__':
    ml = MiniLex("text/*;q=0.3, text/html;q=0.7, text/html;level=1, text/html;level=2;q=0.4, */*;q=0.2")
    p = Parser(ml)
    mts = p.process()
    mts.sort(key=lambda x: x.sort2(), reverse=True)
    mts.sort(key=lambda x: x.qval, reverse=True)

    ml2 = MiniLex("text/xhtml+xml, text/xml, application/atom+xml, text/html;level=2")
    p2 = Parser(ml2)
    mts2 = p2.process()

    b = best(mts, mts2)
    print b
