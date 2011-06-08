Updating the library
====================

How to update your copy of the library.

Update your copy of the code with Subversion (modify the path if the library was
not installed in the suggested location)::

  $ cd /var/local/dataone/d1_common_python
  $ svn update


The python code under ``d1_common/types/generated`` contains PyXB binding
classes. It is generated from the DataONE `schemas`_ using :term:`PyXB`.
Currently, the latest version of the binding classes is included with the
library, so generating them after a Subversion update should not be necessary.
However, if the library is modified locally, they can be generated with::

  $ cd /var/local/dataone/d1_common_python
  $ ./pyxbgen_all.py

.. _schemas: https://repository.dataone.org/software/cicore/trunk/schemas/
