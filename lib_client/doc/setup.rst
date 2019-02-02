Installing DataONE Client Library for Python
============================================

:term:`DataONE Common Library for Python` is distributed via PyPI, the Python Package Index.

Set up server packages:

* The build environment for DataONE Python extensions and lxml
* Commands used in the install

::

  $ sudo apt install --yes build-essential python-dev libssl-dev \
  libxml2-dev libxslt-dev openssl

Install pip (Python package installer)::

  $ sudo apt install --yes python-pip; sudo pip install pip --upgrade;

Install the DataONE Client Library for Python and all its dependencies. This
will also automatically build several Python C extensions::

  $ pip install dataone.libclient


Unit Tests
==========

This library is shipped with unit tests that verify correct operation. It is recommended that these are executed after installation.
