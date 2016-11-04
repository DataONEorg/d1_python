DataONE Common Library for Python
=================================

See :doc:`/index` for an overview of the DataONE libraries and other products
implemented in Python.

.. include:: overview.rst

The provided serialization, deserialization and validation of DataONE API XML
types allows developers to handle the DataONE types as native Python objects,
reducing development time. Implicit validation means that developers can assume
that information that was received from a DataONE node is complete and
syntactically correct before attempting to process it. Also, attempts to submit
incomplete or syntactically incorrect information to a DataONE node cause local
errors that are easy to debug, rather than less specific errors returned from
the target node to which the incorrect types were sent.

The certificate related functionality provides easy extraction of DataONE
subjects from PEM (base64) encoded X.509 v3 certificates as used in DataONE. If
DataONE's custom SubjectInfo extension is present in the certificate, related
subjects for which the primary subject should also be authenticated are
automatically included.

Index
-----

.. toctree::
  :numbered:
  :maxdepth: 2

  setup


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
