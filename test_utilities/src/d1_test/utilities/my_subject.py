# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Given a certificate, show the subject in DataONE format and optionally
display included subject information such as mapped identities and group
memberships.
"""

import logging
import optparse
import sys

#from lxml import etree
from OpenSSL import crypto
from pyasn1.codec.ber import decoder
from pyasn1.error import PyAsn1Error

# flake8: noqa: F403


def getSubjectFromName(xName):
  """Given a DN, returns a DataONE subject
  TODO: This assumes that RDNs are in reverse order...

  @param
  """
  parts = xName.get_components()
  res = []
  for part in parts:
    res.append("%s=%s" % (part[0].upper(), part[1]))
  res.reverse()
  return ",".join(res)


def dumpExtensions(x509):
  decoder.decode.defaultErrorState = decoder.stDumpRawValue
  nExt = x509.get_extension_count()
  logging.debug("There are %d extensions in this certificate" % nExt)
  for i in range(0, nExt):
    ext = x509.get_extension(i)
    logging.debug("Extension %d:" % i)
    logging.debug("  Name: %s" % ext.get_short_name())
    try:
      v = decoder.decode(ext.get_data())
      logging.debug("  Value: %s" % str(v))
    except PyAsn1Error as err:
      logging.warning(err)
      logging.debug("  Value: %s" % str(ext.get_data()))


def getSubjectInfoFromCert(x509):
  """Retrieve the SubjectInfo xml from the certificate, if present
  """
  #This is a huge hack - iterate through the extensions looking for a UTF8
  #object that contains the string "subjectInfo". The extension has no name, and
  #the OpenSSL lib currently has no way to retrieve the extension by OID
  #which is 1.3.6.1.4.1.34998.2.1 for the DataONE SubjectInfo extension
  decoder.decode.defaultErrorState = decoder.stDumpRawValue
  nExt = x509.get_extension_count()
  for i in range(0, nExt):
    ext = x509.get_extension(i)
    sv = decoder.decode(ext.get_data())
    if str(sv).find("subjectInfo") >= 0:
      return sv[0]
  return None


def getSubjectFromCertFile(certFileName):
  status = 1
  certf = file(certFileName, "rb")
  x509 = crypto.load_certificate(crypto.FILETYPE_PEM, certf.read())
  certf.close()
  dumpExtensions(x509)

  if x509.has_expired():
    logging.warning("Certificate has expired!")
    status = 0
  else:
    logging.info("Certificate OK")
    status = 1
  logging.debug("Issuer: %s" % getSubjectFromName(x509.get_issuer()))
  logging.debug("Not before: %s" % x509.get_notBefore())
  logging.debug("Not after: %s" % x509.get_notAfter())
  return {
    'subject': getSubjectFromName(x509.get_subject()),
    'subjectInfo': getSubjectInfoFromCert(x509),
  }, status


if __name__ == "__main__":
  usage = "usage: %prog [options] cert_file_name"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option(
    '-l', '--loglevel', dest='llevel', default=20, type='int',
    help='Reporting level: 10=debug, 20=Info, 30=Warning, '
    '40=Error, 50=Fatal [default: %default]'
  )
  parser.add_option(
    '-i', '--info', action='store_true',
    help='Show subject info in certificate [default: %default]'
  )
  parser.add_option(
    '-f', '--format', action='store_true',
    help='Format output for people [default: %default]'
  )

  (options, args) = parser.parse_args(sys.argv)
  if options.llevel not in [10, 20, 30, 40, 50]:
    options.llevel = 20
  logging.basicConfig(level=int(options.llevel))
  if len(args) < 2:
    parser.print_help()
    sys.exit()

  fname = args[1]
  subject, status = getSubjectFromCertFile(fname)
  print(subject['subject'])
  if options.info:
    if subject['subjectInfo'] is not None:
      if options.format:
        root = etree.fromstring(str(subject['subjectInfo']))
        print("SubjectInfo:")
        print((
          etree.tostring(
            root, pretty_print=True, encoding='utf-8', xml_declaration=True
          )
        ))
      else:
        print(str(subject['subjectInfo']))
  if status == 0:
    sys.exit(2)
  sys.exit(0)
