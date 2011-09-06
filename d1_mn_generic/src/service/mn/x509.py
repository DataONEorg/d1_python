#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:x509`
==========

:platform: Linux
:Synopsis:
  Manipulate X.509 certificates.

.. moduleauthor:: Roger Dahl

http://stackoverflow.com/questions/5519958/how-do-i-parse-subjectaltname-extension-data-using-pyasn1
'''

# Stdlib.
import logging

# 3rd party.
try:
  from OpenSSL import crypto
except ImportError:
  print 'Try: sudo easy_install pyopenssl'
  raise
try:
  #from pyasn1.type import univ, constraint, char, namedtype  
  #from pyasn1.codec.der.decoder import decode
  #from pyasn1.type import tag
  import pyasn1.codec.ber.decoder
except ImportError:
  print 'Try: sudo easy_install pyasn1'
  raise

# Django.
from django.http import HttpResponse

# D1.
import d1_common.types.generated.dataoneTypes as dataoneTypes

# Get an instance of a logger.
logger = logging.getLogger(__name__)

#MAX = 64
#
#class DirectoryString(univ.Choice):
#  componentType = namedtype.NamedTypes(
#    namedtype.NamedType(
#      'teletexString', char.TeletexString().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    namedtype.NamedType(
#      'printableString', char.PrintableString().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    namedtype.NamedType(
#      'universalString', char.UniversalString().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    namedtype.NamedType(
#      'utf8String', char.UTF8String().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    namedtype.NamedType(
#      'bmpString', char.BMPString().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    namedtype.NamedType(
#      'ia5String', char.IA5String().subtype(
#        subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
#    )
#
#
#class AttributeValue(DirectoryString):
#  pass
#
#
#class AttributeType(univ.ObjectIdentifier):
#  pass
#
#
#class AttributeTypeAndValue(univ.Sequence):
#  componentType = namedtype.NamedTypes(
#    namedtype.NamedType('type', AttributeType()),
#    namedtype.NamedType('value', AttributeValue()),
#    )
#
#
#class RelativeDistinguishedName(univ.SetOf):
#  componentType = AttributeTypeAndValue()
#
#class RDNSequence(univ.SequenceOf):
#  componentType = RelativeDistinguishedName()
#
#
#class Name(univ.Choice):
#  componentType = namedtype.NamedTypes(
#    namedtype.NamedType('', RDNSequence()),
#    )
#
#
#class Extension(univ.Sequence):
#  componentType = namedtype.NamedTypes(
#    namedtype.NamedType('extnID', univ.ObjectIdentifier()),
#    namedtype.DefaultedNamedType('critical', univ.Boolean('False')),
#    namedtype.NamedType('extnValue', univ.OctetString()),
#    )
#
#
#class Extensions(univ.SequenceOf):
#  componentType = Extension()
#  sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)
#
#
#class GeneralName(univ.Choice):
#  componentType = namedtype.NamedTypes(
#    # namedtype.NamedType('otherName', AnotherName()),
#
#    namedtype.NamedType('rfc822Name', char.IA5String().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
#
#    namedtype.NamedType('dNSName', char.IA5String().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
#      
#    # namedtype.NamedType('x400Address', ORAddress()),
#
#    namedtype.NamedType('directoryName', Name().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))),
#
#    # namedtype.NamedType('ediPartyName', EDIPartyName()),
#
#    namedtype.NamedType('uniformResourceIdentifier', char.IA5String().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))),
#
#    namedtype.NamedType('iPAddress', univ.OctetString().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))),
#
#    namedtype.NamedType('registeredID', univ.ObjectIdentifier().subtype(
#      implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))),
#    )
#
#
#class GeneralNames(univ.SequenceOf):
#  componentType = GeneralName()
#  sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)
#
#
#class SubjectAltName(GeneralNames):
#  pass

##session_str = decode(session_asn1_str, asn1Spec=GeneralNames())
#
#  
#
#session_str = (GeneralNames().setComponentByPosition(
#  0, GeneralName().setComponentByPosition(1, char.IA5String('example.com'))), '')
##session_str = decode(session_asn1_str, asn1Spec=GeneralNames())
#
#return HttpResponse(session_str, 'text/plain')


def get_session(cert_pem):
  '''Extract session from certificate.
  
  :param cert: PEM client side certificate.
  :type cert: str
  :returns: Session.
  :return type: PyXB Session
  '''
  cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
  if cert.get_extension_count() != 1:
    raise d1_common.types.exceptions.NotAuthorized(0, 'Missing session')
  session_asn1_str = cert.get_extension(0).get_data()
  session_str = pyasn1.codec.ber.decoder.decode(
    session_asn1_str, asn1Spec=char.IA5String()
  )[0]
  try:
    session = dataoneTypes.CreateFromDocument(session_str)
  except:
    raise d1_common.types.exceptions.NotAuthorized(0, 'Invalid session')
