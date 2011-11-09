# Stdlib.
import xml

# 3rd party.
import pyxb

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.generated.dataoneErrors as dataoneErrors


def deserialize_and_check(doc, shouldfail=False):
  try:
    obj = dataoneTypes.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')


def deserialize_exception_and_check(doc, shouldfail=False):
  try:
    obj = dataoneErrors.CreateFromDocument(doc)
  except (pyxb.PyXBException, xml.sax.SAXParseException):
    if shouldfail:
      return
    else:
      raise
  if shouldfail:
    raise Exception('Did not receive expected exception')
