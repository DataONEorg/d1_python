#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Create set of test certificates signed by the DataONE Test CA
"""

import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import OpenSSL

import d1_common.types.dataoneTypes_v1 as dataoneTypes_v1

# Get an instance of a logger.
logger = logging.getLogger()

# Config
ca_cert_key_path = './ca_intermediate.key'
ca_cert_pem_path = './ca_intermediate.crt'
#ca_cert_key_path = './ca.key'
#ca_cert_pem_path = './ca.crt'

cert_dir = './test_subject_certs/'

# Test subjects.
subjects = [
  'santa=purposefully=3775',
  '4782@rigorously@seekers',
  '5227@manuscript@objectively',
  '6011~recoiled~apologist',
  'stalled/squawk/5912',
  'blocking_687',
  '3934~senators',
  '8335_flick_cogitate',
  'sparingly~renault~9208',
  '8920_skye_fondled',
  'folding_5087',
  '9810_paranormal',
  'authenticators-733',
  'artfully/3822',
  'singing.3369',
  '7408@outskirts@absorbency',
  'profiteers=7446',
  'melanie~1855',
  '975@shadily',
  'slugs@6367',
  '5790=customizations',
  'dressed_sublist_1687',
  'equilibrate_8593',
  'stoles=propane=9017',
  '357~western',
  '7491~mystery',
  '1316.ploys',
  'reentered~2695',
  '9376.freon.purporter',
  '7009~observance~roving',
  '4664~tapestries',
  'render.stewardess.5267',
  '789@netherlands@paraboloid',
  'conferred=lurches=5154',
  'selectric~2975',
  '6705.touch.avignon',
  '4320@missionaries@mutability',
  'wronged-7700',
  '9615@breach@magill',
  'deplorable=5891',
  '6592~unicorns',
  '2775~leona~preempt',
  '7309/optical',
  '3724~responsive~ministries',
  '275_martians_aquarius',
  '3974.treetops',
  'exchanging-reinforcements-7818',
  'awarder~7223',
  'tiber~justifying~1796',
  '8067_diffuse',
  '1871-indomitable-straggle',
  '6212.malay.platforms',
  'reworked~8676',
  '433-fission-malta',
  'vegetated/1650',
  '851@combines',
  '7484@zeroed@rehearsal',
  'clenches-2049',
  '8145@punished@alleviation',
  'eros=6864',
  '8841-moment-disarms',
  '1594-flatness',
  '9397~paroling',
  'gaped/9228',
  '1825_redouble',
  '8255~detective',
  'matrimonial~beachhead~3578',
  'instructor.radially.2226',
  '9395@scares@shulman',
  '5819~operate',
  '5161-hebe',
  'descends=knolls=8054',
  'unfamiliarly@citizen@4703',
  '5495-disgusts-ledger',
  'zaire.5691',
  'solvents=zeroing=8956',
  'whitewater/sours/4623',
  'bivouac-seers-2425',
  '9491=comparably',
  'all~babe~9779',
  'pedagogic.salesian.1738',
  'cellular_stouffer_4330',
  '6191.perfectionist',
  '7365.esoteric',
  '1845-inbreed-depths',
  'lays-9905',
  '8416-oxidized',
  'enmity-5176',
  'plurality.design.4874',
  '6390/subspace',
  'observant=reconstruction=6040',
  'vanishingly~fixing~3170',
  'cohesively@1058',
  '607/chided/chesterfield',
  '5685@abolishers',
  'propagated=hoard=3091',
  '846=dostoevsky',
  'evensen.9937',
  'mailmen-6496',
  '2215_sunned',
]


def create_key_pair(key_type, n_bits):
  """Create a public/private key pair.

  :param key_type: Key type (RSA or DSA).
  :type key_type: crypto.TYPE_RSA or crypto.TYPE_DSA
  :param n_bits: Number of bits to use in the key.
  :type n_bits: int
  :returns: Public/private key pair.
  :return type: PKey
  """
  pkey = OpenSSL.crypto.PKey()
  pkey.generate_key(key_type, n_bits)
  return pkey


def create_cert_request(pkey, digest="md5", **name):
  """Create a certificate request.

  :param pkey: Key to associate with the request.
  :type pkey: PKey
  :param digest: Message-Digest algorithm to use for signing.
  :type digest: str
  :param **name: Name of the subject of the request.
  :type **name: keyword arguments
  :returns: Certificate request.
  :return type: X509Req

  Possible keyword arguments (**name):
    C  - Country name
    ST - State or province name
    L  - Locality name
    O  - Organization name
    OU - Organizational unit name
    CN - Common name
    emailAddress - E-mail address
  """
  req = OpenSSL.crypto.X509Req()
  subj = req.get_subject()

  for (key, value) in list(name.items()):
    setattr(subj, key, value)

  req.set_pubkey(pkey)
  req.sign(pkey, digest)
  return req


def create_session_extension(subject, persons, groups):
  """Create the custom X.509 extension object in which DataONE passes session
  information.

  :param subjects: Subjects to store in session.
  :type subjects: list
  :returns: X.509 v3 certificate extension.
  :return type: X509Extension
  """

  subject_list = dataoneTypes_v1.SubjectList()
  for person in persons:
    person_pyxb = dataoneTypes_v1.Person()
    person_pyxb.subject = person
    person_pyxb.givenName = ['given']
    person_pyxb.familyName = 'family'
    person_pyxb.email = ['email@email.com']
    subject_list.person.append(person_pyxb)
  for group in groups:
    group_pyxb = dataoneTypes_v1.Group()
    group_pyxb.subject = group
    group_pyxb.groupName = 'groupname'
  session = dataoneTypes_v1.Session()
  session.subject = subject
  session.subjectList = subject_list

  # Each extension has its own id, expressed as Object identifier, a set of
  # values and either critical or non-critical indication. A certificate-using
  # system MUST reject the certificate if it encounters a critical extension it
  # does not recognize or a critical extension that contains information that it
  # cannot process. A non-critical extension MAY be ignored if it is not
  # recognized, but MUST be processed if it is recognized.

  #Create a NID for the extension
  #nid = OBJ_create([OID for your extension], [short name for your extension],
  # [long name for your extension]);

  # adding the alias
  #X509V3_EXT_add_alias(nid, NID_netscape_comment);

  #  /* Try to get a NID for the name */
  #if ((ext_nid = OBJ_sn2nid(type_name)) == NID_undef)
  #{
  #    PyErr_SetString(PyExc_ValueError, "Unknown extension name");
  #    return NULL;
  #}
  ext = OpenSSL.crypto.X509Extension('nsComment', False, session.toxml('utf-8'))

  return ext


def create_certificate(
    req, xxx_todo_changeme, serial, xxx_todo_changeme1, digest="md5"
):
  """Generate a certificate given a certificate request.

  :param req: Certificate reqeust.
  :type req: X509Req
  :param issuer_cert: Certificate of the issuer.
  :type issuer_cert:
  :param issuer_key: Private key of the issuer.
  :type issuer_key:
  :param serial: Serial number for certificate.
  :type serial: str
  :param not_before: Timestamp (relative to now) for when the certificate starts
    being valid.
  :type not_before: int
  :param not_after: Timestamp (relative to now) for when the certificate stops
    being valid.
  :type not_after: int
  :param digest: Digest method to use for signing.
  :type digest: str
  :returns: The signed certificate.
  :return type: X509
  """
  (issuer_cert, issuer_key) = xxx_todo_changeme
  (not_before, not_after) = xxx_todo_changeme1
  cert = OpenSSL.crypto.X509()
  cert.set_serial_number(serial)
  cert.gmtime_adj_notBefore(not_before)
  cert.gmtime_adj_notAfter(not_after)
  cert.set_issuer(issuer_cert.get_subject())
  cert.set_subject(req.get_subject())
  cert.set_pubkey(req.get_pubkey())
  # Add DataONE session.
  ext = create_session_extension(
    str(req.get_subject()), ['p1', 'p2'], ['g1', 'g2']
  )
  cert.add_extensions([ext])
  # Sign the certificate.
  cert.sign(issuer_key, digest)

  return cert


def main():
  logging.basicConfig(level=logging.DEBUG)

  test_ca_pw = input(
    'Dataone Test CA private key pass phrase (in SystemPW.txt): '
  )

  # Create the destination folder.
  try:
    dst_path = os.path.join(os.path.dirname(__file__), cert_dir)
    os.mkdir(dst_path)
  except EnvironmentError:
    pass

    # Load the DataONE Test CA private key.
  try:
    ca_key_file = open(ca_cert_key_path, 'r').read()
  except IOError:
    logger.error('Must set path to CA key in config section')
    raise
  ca_key = OpenSSL.crypto.load_privatekey(
    OpenSSL.crypto.FILETYPE_PEM, ca_key_file, test_ca_pw
  )

  # Load the DataONE Test CA cert.
  try:
    ca_cert_file = open(ca_cert_pem_path, 'r').read()
  except IOError:
    logger.error('Must set path to CA key in config section')
    raise
  ca_cert = OpenSSL.crypto.load_certificate(
    OpenSSL.crypto.FILETYPE_PEM, ca_cert_file
  )

  # Generate test certs.
  for subject in subjects:
    logger.info(subject)

    # Create private key.
    # crypto.TYPE_DSA does not work with digest='SHA1'
    pkey = create_key_pair(OpenSSL.crypto.TYPE_RSA, 4096)

    # Create CSR for subject.
    req = create_cert_request(pkey, CN=subject, digest='SHA1')

    # Create certificate by signing the CSR.
    cert = create_certificate(
      req,
      (ca_cert, ca_key),
      1,
      (0, 60 * 60 * 24 * 365 * 10), # 10 years
      digest='SHA1'
    )

    # Write the private key to disk.
    out_cert_key_path = os.path.join(
      cert_dir, '{}.key'.format(urllib.parse.quote(subject, ''))
    )
    out_key_file = open(out_cert_key_path, 'w')
    out_key_file.write(
      OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pkey)
    )

    # Write the cert to disk.
    out_cert_pem_path = os.path.join(
      cert_dir, '{}.crt'.format(urllib.parse.quote(subject, ''))
    )
    out_cert_file = open(out_cert_pem_path, 'w')
    out_cert_file.write(
      OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    )


if __name__ == '__main__':
  #import pyxb
  #pyxb.RequireValidWhenGenerating(False)
  sys.exit(main())
