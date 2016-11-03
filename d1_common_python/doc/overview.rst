The `DataONE Common Library for Python`_ provides functionality commonly needed
by projects that interact with the :term:`DataONE` infrastructure via Python.

The main functionality provided by the DataONE Common Library for Python is
serialization, deserialization and validation of the DataONE API XML types. It
also includes a wrapper for RESTful services. The serialization and
deserialization functionality allows developers to handle the DataONE types as
native Python objects, reducing development time. Implicit validation means that
developers can assume that information that was received from a DataONE node is
complete and syntactically correct before attempting to process it. Also,
attempts to submit incomplete or syntactically incorrect information to a
DataONE node cause local errors that are easy to debug, rather than less
specific errors returned from the target node.

.. _`DataONE Common Library for Python`: http://pythonhosted.org/dataone.common/
