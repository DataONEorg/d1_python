Authentication within the DataONE infrastructure is based on x509 certificates.

This module provides a Python extension for extracting DataONE Session
information from PEM formatted X.509 v3 certificates. It supports extracting the
DataONE SubjectInfo x509v3 extension, in which equivalent identities and group
memberships are passed. It also extract the Subject DN and serializes it to a
DataONE compliant subject string.

.. graphviz::

  digraph G {
    size = "6,20";
    ratio = "compress";
    "OpenSSL C library" -> "x509v3 Extractor"
    "Python Dev" -> "x509v3 Extractor"

    "DataONE Common" -> "x509v3 Extractor (tests)"
  }
