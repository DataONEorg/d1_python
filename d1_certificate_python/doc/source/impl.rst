Implementation
==============

The library is implemented in C, as Python extensions. The extensions are
thin wrappers of the OpenSSL library.

.. graphviz::

  digraph G {
    size = "6,20";
    ratio = "compress";
    "OpenSSL C library" -> "x509v3 Extractor"
    "OpenSSL C library" -> "x509v3 Generator"
    "Python Dev" -> "x509v3 Extractor"
    "Python Dev" -> "x509v3 Generator"

    "DataONE Common" -> "Test suite"
  }
