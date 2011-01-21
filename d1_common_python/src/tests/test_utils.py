'''
Created on Jan 21, 2011

@author: vieglais
'''

import unittest
import codecs
import d1_common.util


class TestRESTClient(unittest.TestCase):
  def testEncodePathElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('path'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodePathElement(v))

  def testEncodeQueryElement(self):
    ftest = 'd1_testdocs/encodingTestSet/testUnicodeStrings.utf8.txt'
    testfile = codecs.open(ftest, encoding='utf-8', mode='r')
    testrows = testfile.readlines()
    for row in testrows:
      parts = row.split('\t')
      if len(parts) > 1:
        v = parts[0]
        if v.startswith('common') or v.startswith('query'):
          e = parts[1].strip()
          self.assertEqual(e, d1_common.util.encodeQueryElement(v))

  def testEncodeURL(self):
    data = [
      ('a', '"#<>[]^`{}|'), ('b', '-&=&='), ('c', 'http://example.com/data/mydata?row=24')
    ]
    expected = 'a=%22%23%3C%3E%5B%5D%5E%60%7B%7D%7C&b=-%26%3D%26%3D&c=http://example.com/data/mydata?row%3D24'
    test = d1_common.util.urlencode(data)
    self.assertEqual(test, expected)


if __name__ == "__main__":
  unittest.main()
