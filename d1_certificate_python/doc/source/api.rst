API
===

A single API method is exposed::

  x509_extract_session.extract(
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

  import x509_extract_session

  subject, subject_info_xml = self._extract_session_from_x509_v3_certificate()
  if subject_info_xml == '':
    return subject, None
  else:
    return subject, subject_info_xml
