'''Low level interaction with the DataONE echoCredentials service.

purl.dataone.org/architecture-dev/apis/CN_APIs.html#CNDiagnostic.echoCredentials

You can use https://github.com/DataONEorg/d1Login to obtain credentials.

'''

import argparse
import logging
import xml.dom.minidom
from d1_common import restclient

default_target = 'https://cn.dataone.org/cn/v2/diag/subject'


def echoCredentials(credentials, target=default_target):
  '''Call the echoCredentials method on a Coordinating Node 
  
  Args:
  
    target (string): URL of the echoCredentials endpoint
    credentials (string): Path to a file that contains the private and public 
      credential parts.
  '''
  cli = restclient.RESTClient(cert_path=credentials)
  res = cli.GET(target)
  doc = xml.dom.minidom.parseString(res.content)
  print(doc.toprettyxml(indent='  '))

#-- Main Section --

parser = argparse.ArgumentParser(description="DataONE Diagnostic: Echo Credentials")

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
  help="echoCredentials endpoint ({0})".format(default_target)
)

parser.add_argument(
  '-E',
  '--certificate',
  required=True,
  help="Path to certificate file for authentication."
)

args = parser.parse_args()

#Setup logging verbosity
levels = [logging.WARNING, logging.INFO, logging.DEBUG]
level = levels[min(len(levels) - 1, args.verbose)]
logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

echoCredentials(args.certificate, target=args.baseurl)
