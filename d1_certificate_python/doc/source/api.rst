API
===

A single API method is exposed::

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
~~~~~~~

Note that if the SubjectInfo is not present in the certificate, an empty string
is returned.

Call the API from Python::

  import d1_x509v3_certificate_extractor

  with open('mycert.pem') as f:
    mycert = f.read()
  subject, subject_info_xml = d1_x509v3_certificate_extractor.extract(mycert)
  if subject_info_xml == '':
    return subject, None
  else:
    return subject, subject_info_xml
