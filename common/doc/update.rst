Updating the library
====================

To update your copy of the library to the latest version available on PyPI, run ``pip install`` with the ``--upgrade`` option:

::

  $ sudo pip install --upgrade dataone.common


The python code under ``d1_common/types/generated`` contains PyXB binding classes. It is generated from the DataONE `schemas`_ using :term:`PyXB`. Currently, the latest version of the binding classes is included with the library, so generating them after a Subversion update should not be necessary. However, if the library is modified locally, they can be generated with::

  $ cd /var/local/dataone/d1_common_python
  $ ./pyxbgen_all.py

.. _schemas: https://repository.dataone.org/software/cicore/trunk/schemas/
