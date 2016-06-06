'''Call the echoSystemMetadata method of the DataONE diagnostic APIs.


purl.dataone.org/architecture-dev/apis/CN_APIs.html#CNDiagnostic.echoSystemMetadata

'''
import argparse
import logging
import codecs
import xml.dom.minidom
from d1_common import restclient
from d1_common.types import dataoneTypes

default_target = 'https://cn.dataone.org/cn/v2/diag/sysmeta'


def echoSystemMetadata(sysmeta, target=default_target):
  '''Call the echoSystemMetadata method on a Coordinating Node 
  
  Args:
  
    target (string): URL of the echoSystemMetadata endpoint
    sysmeta (string): Path to a file that contains the system metadata xml.
  '''
  cli = restclient.RESTClient()
  files = [
    (
      'sysmeta', #field name
      (
        sysmeta, #file name
        codecs.open(
          sysmeta, 'r', encoding='utf-8'
        ), #file stream 
        'text/xml'
      ) #file type
    )
  ]

  files = [('sysmeta', (sysmeta, codecs.open(sysmeta, 'r', encoding='utf-8').read()))]

  res = cli.POST(target, files=files)
  #Show the raw response
  print("Raw response: ")
  print(res.content)

  print("----\nXML formatted response: ")
  doc = xml.dom.minidom.parseString(res.content)
  #Show the response body as formatted xml
  print(doc.toprettyxml(indent='  '))
  if res.status == 200:
    #Try loading the response as a DataONE Type
    print("----\nValues extracted from parsed response: ")
    sysm_parsed = dataoneTypes.CreateFromDocument(res.content)
    #Identifier is not a simple type, so use .value() to get the value
    print u"  Identifier: {0}".format(sysm_parsed.identifier.value())

    #formatID is a simple value, get it's value directly
    print u"  Format ID: {0}".format(sysm_parsed.formatId)

    #submitter is not a simple type, so use .value() to get the value
    print u"  Submitter: {0}".format(sysm_parsed.submitter.value())

    #-- Main Section --


parser = argparse.ArgumentParser(description="DataONE Diagnostic: Echo System Metadata")

parser.add_argument(
  '-v',
  '--verbose',
  action='count',
  default=0,
  help='Set logging level, multiples for more verbose.'
)

parser.add_argument(
  '-b',
  '--baseurl',
  default=default_target,
  help="echoSystemMetadata endpoint ({0})".format(default_target)
)

parser.add_argument(
  '-E',
  '--certificate',
  help="Optional path to certificate file for authentication."
)

parser.add_argument(
  '-s',
  '--sysmeta',
  required=True,
  help="Path to certificate file for authentication."
)

args = parser.parse_args()

#Setup logging verbosity
levels = [logging.WARNING, logging.INFO, logging.DEBUG]
level = levels[min(len(levels) - 1, args.verbose)]
logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

echoSystemMetadata(args.sysmeta, target=args.baseurl)
