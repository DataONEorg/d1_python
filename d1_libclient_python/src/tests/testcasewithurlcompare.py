import unittest
import urlparse


class TestCaseWithURLCompare(unittest.TestCase):
  '''Utility class that check whether two URLs are equal.  Not really as simple
  as it migh seem at first.
  '''

  def assertUrlEqual(self, a, b):
    '''Given two URLs, test if they are equivalent.  This means decomposing into
    their parts and comparing all the pieces.  See RFC 1738 for details.
    
    :param a: URL #1
    :param b: URL #2
    :raises: AssertionError, accumulation of differences between a and b. 
    '''
    ## Accumulator gathers all errors before reporting.
    accumulator = []
    a_parts = urlparse.urlparse(a)
    b_parts = urlparse.urlparse(b)
    #scheme and net location are case insensitive
    try:
      self.assertEqual(
        a_parts.scheme.lower(), b_parts.scheme.lower(),
        u'Schemes of %s and %s differ' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    try:
      self.assertEqual(
        a_parts.netloc.lower(), b_parts.netloc.lower(),
        u'Network location of %s and %s differ' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    #compare paths
    try:
      self.assertEqual(a_parts.path, b_parts.path, u'Paths of %s and %s differ' % (a, b))
    except AssertionError, e:
      accumulator.append(unicode(e))
    #fragments
    try:
      self.assertEqual(
        a_parts.fragment, b_parts.fragment, u'Fragments differ: %s <> %s' % (
          a_parts.fragment, b_parts.fragment
        )
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    #parameters
    aparams = a_parts.params.split(";")
    bparams = b_parts.params.split(";")
    try:
      self.assertEqual(
        len(aparams), len(bparams),
        u'Number of parameters differs between %s and %s' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))

    for aparam in aparams:
      try:
        self.assertTrue(
          aparam in bparams, u'Parameter %s not present in URL %s' % (aparam, b)
        )
      except AssertionError, e:
        accumulator.append(unicode(e))

    #query portion
    a_qry = urlparse.parse_qs(a_parts.query)
    b_qry = urlparse.parse_qs(b_parts.query)
    try:
      self.assertEqual(
        len(a_qry.keys()), len(b_qry.keys()),
        u'Number of query keys differs between %s and %s' % (a, b)
      )
    except AssertionError, e:
      accumulator.append(unicode(e))
    bkeys = b_qry.keys()
    for ak in a_qry.keys():
      try:
        self.assertTrue(ak in bkeys, u'The query key %s not present in %s' % (ak, b))
        for v in a_qry[ak]:
          try:
            self.assertTrue(
              v in b_qry[ak], u'The value %s of key %s not present in %s' % (v, ak, b)
            )
          except AssertionError, e:
            accumulator.append(unicode(e))

      except AssertionError, e:
        accumulator.append(unicode(e))

    if len(accumulator) > 0:
      raise AssertionError(u"\n".join(accumulator))

  def test_assertUrlEqual(self):
    '''Test the Url comparison tester...
    '''
    #According to RFC  these URLs are equivalent
    a = "HTTP://www.some.host:999/a/b/c/;p1;p2;p3?k1=10&k1=20&k2=abc#frag"
    b = "Http://www.SOME.host:999/a/b/c/;p2;p1;p3?k1=10&k2=abc&k1=20#frag"
    self.assertUrlEqual(a, b)
    #and these are not
    b = "Http://www.SOME.host:999/a/b/c/;p2;p4;p3?k1=10&k2=abc&k1=20#frag"
    self.failUnlessRaises(AssertionError, self.assertUrlEqual, a, b)


if __name__ == "__main__":
  unittest.main()
