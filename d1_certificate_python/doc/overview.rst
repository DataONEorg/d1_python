The :doc:`/certificate/index` provides Python extensions for
parsing and generating PEM formatted :term:`X.509` v3 certificates as used for
authentication within the DataONE infrastructure.

DataONE uses a custom X.509 v3 certificate extension to pass additional identity
information such as equivalent identities and group memberships. In addition,
DataONE uses a specific serialization format of the certificate :term:`DN` to
represent DataONE identities. The library hides these implementation details,
lowering the implementation effort involved in supporting authentication and
authorization within DataONE.

The library is a high performance C extension based on :term:`OpenSSL`.

