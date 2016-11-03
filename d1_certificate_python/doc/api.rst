API
===


DataONE X.509 v3 Certificate Extractor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The certificate extractor enables easy access to the contents of DataONE
compliant X.509 v3 certificates from Python.

::

  d1_x509v3_certificate_extractor.extract(
    pem_certificate
  )

:param pem_certificate: PEM formatted DataONE certificate.
:type pem_certificate: string

:returns:
  * Subject DN (DataONE compliant serialization)
  * SubjectInfo XML document
:return type:
  list of two strings


Example
-------

Note that if the SubjectInfo is not present in the certificate, an empty string
is returned.

Call the API from Python::

  import d1_x509v3_certificate_extractor

  with open('mycert.pem', 'rb') as f:
    mycert = f.read()
  subject, subject_info_xml = d1_x509v3_certificate_extractor.extract(mycert)
  if subject_info_xml == '':
    subject_info_xml = None
  print subject
  print subject_info_xml


DataONE X.509 v3 Certificate Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The certificate generator enables easy generation of DataONE compliant
X.509 certificates for testing. Before using this function, a :term:`CA` must
be available. See :ref:`local_ca` for instructions.

::

  generate_x509v3_certificate.generate(
    cert_out_path,
    ca_cert_path,
    ca_key_path
    ca_key_pw,
    public_key_path,
    subject_info,
    subject_alt_name,
    rdns,
    long_term
  )

:param cert_out_path: Output path for the newly generated certificate.
:type cert_out_path: string

:param ca_cert_path: Input path for PEM formatted CA certificate to use for
  signing new certificate.
:type ca_cert_path: string

:param ca_key_path: Input path for PEM formatted private key for CA certificate.
:type ca_key_path: string

:param ca_key_pw: Input password for private key for CA certificate.
:type ca_key_pw: string

:param public_key_path: Input path to PEM formatted public key for new
  certificate.
:type public_key_path:

:param subject_info: Input string for complete SubjectInfo XML document.
:type subject_info: string

:param subject_alt_name: Input string for the standard subjectAltName v3 extension.
:type subject_alt_name: string

:param rdns: List containing the RDNs for the Subject DN.
:type rdns: list

:param long_term: 0 = Generated certificate expires after 1 day. 1 = Generated certificate expires after 10 years.
:type long_term: int


Example
-------

Generation of the private and public keys on which the new certificate will be
based has been kept as a manual step. This is because it is convenient to use
the same keys for a large set of test certificates.

Use OpenSSL to generate the private and public keys on which the generated
certificate will be based::

  $ openssl genrsa -out privkey.pem 2048
  $ openssl rsa -in privkey.pem -pubout -out pubkey.pem


Then call the API from Python::

  import d1_x509v3_certificate_generator

  cert_out_path = './newcert.pem'

  ca_path = './ca.crt'
  ca_key_path = './ca.key'
  ca_key_pw = "my_ca_password"

  public_key_path = './pubkey.pem'
  private_key_path = './privkey.pem'

  subject_alt_name = 'DNS:dataone.org'

  dn = (
    ('CN', 'Test User Name'),
    ('O', 'Provider'),
    ('C', 'US'),
    ('DC', 'test-domain'),
    ('DC', 'com'),
  )

  long_term = 0

  subject_info = '''<?xml version="1.0" encoding="UTF-8"?>
  <d1:subjectInfo xmlns:d1="http://ns.dataone.org/service/types/v1">
    <person>
      <subject>Test User Name,O=Provider,C=US,DC=test-domain,DC=com</subject>
      <givenName>Test</givenName>
      <familyName>User Name</familyName>
      <email>test@test-domain.com</email>
      <equivalentIdentity>CN=Second User Name,C=US,DC=another-test-domain,dc=com</equivalentIdentity>
      <verified>true</verified>
    </person>
  </d1:subjectInfo>
  '''

  d1_x509v3_certificate_generator.generate(cert_out_path, ca_path, ca_key_path,
                                       ca_key_pw, public_key_path, subject_info,
                                       subject_alt_name, dn, long_term)
